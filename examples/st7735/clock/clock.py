# Evaluation before designing a "faux nixie" clock
# The assembly uses 4 small tft displays, each display is a digit of the clock
# a bitmap is used for each number so any shape can be used for the digits
#
#
# Displays are oriented this way so shall use the following parameters in the init
#  width = 80, height = 160 and usd = True
#  _____________
# | _________   |
# | |---/ X  |  |
# | ||       | o|
# | ||       | o|
# | ||       | o|
# | ||/      | o|
# | |Y       | o|
# | |        | o|
# | |        | o|
# | |        | o|
# | |________| o|
# |_____________|
#
# Wiring
#
# Using SPI(0) default the displays are wired this way
#
# | Display | Pico GP    | Pico pin# |
# |---------|------------|-----------|
# |   GND   | GND        | pin 38    | 
# |   VCC   | 3V3        | pin 36    |
# |   SCL   | GP6 SCL    | pin 9     | 
# |   SDA   | SPI TX GP7 | pin 10    | 
# |   RES   | GP2        | pin 4     | 
# |    DC   | GP3        | pin 5     | 
# |   CS1   | GP10       | pin 14    | 
# |   CS2   | GP11       | pin 15    | 
# |   CS3   | GP12       | pin 16    | 
# |   CS4   | GP13       | pin 17    | 
# |   BLK   | GP8        | pin 11    |
#  ----------------------------------
#
#
from drivers.st7735b import ST7735B
from drivers.rotary import Rotary
from machine import Pin, SPI, PWM, ADC
from utime import localtime, sleep_ms
import framebuf
import uctypes
import gc

# defines header format of image file
IMG_HEADER = {
"width": 0 | uctypes.UINT16,
"height": 2 | uctypes.UINT16
}

val = 0
select = 0
button_pressed = False


def rotary_changed(change):
    global val, button_pressed
    if change == Rotary.ROT_CW:
        val = val + 1
    elif change == Rotary.ROT_CCW:
        val = val - 1
    elif change == Rotary.SW_PRESS:
        button_pressed = True
    elif change == Rotary.SW_RELEASE:
        pass

def menu():
    global select, button_pressed, val
    
    white = tft1.rgb(255,255,255)
    yellow = tft1.rgb(255,255,0)
    red = tft1.rgb(255,0,0)
    green = tft1.rgb(0, 255,0)
    blue = tft1.rgb(0, 0, 255)
    black = tft1.rgb(0, 0, 0)
    
    tft4.fill(white)
    idx = 0
    for f in font:
        tft4.text(f,8, 10 + idx * 10, black)
        idx += 1
    tft4.text('>', 0, 10 + select * 10, red)
    tft4.show()
    button_pressed = False
    val = select
    old_val = val
    while (button_pressed == False):
        sleep_ms(50)
        if (val != old_val):
            newsel = val % len(font)
            tft4.fill_rect(0, 10 + select * 10, 8, 18 + select * 10, white)
            tft4.text('>', 0, 10 + newsel * 10, red)
            tft4.show()
            select = newsel
            old_val = val
    button_pressed = False


button = Rotary(14,15,16)
button.add_handler(rotary_changed)
dc = Pin(3,Pin.OUT)
cs1 = Pin(10, Pin.OUT)
cs2 = Pin(11, Pin.OUT)
cs3 = Pin(12, Pin.OUT)
cs4 = Pin(13, Pin.OUT)
res = Pin(2,Pin.OUT)
blk = Pin(8,Pin.OUT)
blkPWM = PWM(blk)
lum = ADC(0)
machine.Pin(26, machine.Pin.IN) #adc0
# as all the reset from the displays are wired to one pin of the Pico
# the reset shall only be done for the first display
tft1 = ST7735B(SPI(0,baudrate=25000000), cs1,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = True)
tft2 = ST7735B(SPI(0,baudrate=25000000), cs2,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
tft3 = ST7735B(SPI(0,baudrate=25000000), cs3,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
tft4 = ST7735B(SPI(0,baudrate=25000000), cs4,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
 # all the blk line are wired to one GP so only one call is necessary
backlight = int(lum.read_u16()/65535*100)
tft1.backlight(backlight)

black = 0
white = 0xff

root = 'digits' # path to the directory holding the different font of numbers
font = ('nixie','tiles','rounded','hand','balloon','monsters','stamp') # font of digits
digits = ('digit0','digit1','digit2','digit3','digit4','digit5','digit6','digit7','digit8','digit9')
displays = (tft4, tft3, tft2, tft1)

while (True):
    font_name = font[select]
    
    Time = localtime()
    val = Time[3] * 100 + Time[4]
    for tft in displays:
        number = val % 10
        val //=10
        path = root + '//' + font_name + '//' + digits[number] + '.raw'
        with open(path, mode='rb') as f:
            buf = f.read(uctypes.sizeof(IMG_HEADER, uctypes.LITTLE_ENDIAN))
            header = uctypes.struct(uctypes.addressof(buf), IMG_HEADER, uctypes.LITTLE_ENDIAN)
            width = header.width
            height = header.height
            buffer = bytearray(width * height)
            f.readinto(buffer, width * height)
            f.close()
            fb = framebuf.FrameBuffer(buffer,width,height, framebuf.GS8)
            colorfb = fb.pixel(0,0)
            tft.fill(colorfb)
            tft.blit(fb, (tft.width-width)//2, (tft.height-height)//2)
            tft.show()
    # wait for the 00 second to end
    while (localtime()[5]==00):
        sleep_ms(250)
    gc.collect()  # we have a huge amount of time to collect garbage here
    # wait for the start of the next minute
    while (localtime()[5]!=00):
        if button_pressed:
            menu()
            break
        backlight = int(lum.read_u16()/65535*100)
        tft1.backlight(backlight)
        sleep_ms(250)
