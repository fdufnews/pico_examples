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
from machine import Pin, SPI, PWM
from utime import localtime, sleep_ms
import framebuf
import uctypes

# defines header format of image file
IMG_HEADER = {
"width": 0 | uctypes.UINT16,
"height": 2 | uctypes.UINT16
}

select = Pin(5, Pin.IN, Pin.PULL_UP)
dc = Pin(3,Pin.OUT)
cs1 = Pin(10, Pin.OUT)
cs2 = Pin(11, Pin.OUT)
cs3 = Pin(12, Pin.OUT)
cs4 = Pin(13, Pin.OUT)
res = Pin(2,Pin.OUT)
blk = Pin(8,Pin.OUT)
blkPWM = PWM(blk)
# as all the reset from the displays are wired to one pin of the Pico
# the reset shall only be done for the first display
tft1 = ST7735B(SPI(0,baudrate=25000000), cs1,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = True)
tft2 = ST7735B(SPI(0,baudrate=25000000), cs2,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
tft3 = ST7735B(SPI(0,baudrate=25000000), cs3,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
tft4 = ST7735B(SPI(0,baudrate=25000000), cs4,dc,res, blk=blkPWM, height=160, width=80, usd = True, reset_tft = False)
 # all the blk line are wired to one GP so only one call is necessary
tft1.backlight(100)

root = 'digits' # path to the directory holding the different families of numbers
family = ('nixie','tiles') # family of digits
digits = ('digit0','digit1','digit2','digit3','digit4','digit5','digit6','digit7','digit8','digit9')
displays = (tft4, tft3, tft2, tft1)

while (True):
    if (select.value()):
        family_name = family[1]
    else:
        family_name = family[0]
    Time = localtime()
    val = Time[3] * 100 + Time[4]
    for tft in displays:
        number = val % 10
        val //=10
        path = root + '//' + family_name + '//' + digits[number] + '.raw'
        with open(path, mode='rb') as f:
            buf = f.read(uctypes.sizeof(IMG_HEADER, uctypes.LITTLE_ENDIAN))
            header = uctypes.struct(uctypes.addressof(buf), IMG_HEADER, uctypes.LITTLE_ENDIAN)
            width = header.width
            height = header.height
            buffer = bytearray(width * height)
            f.readinto(buffer, width * height)
            f.close()
            fb = framebuf.FrameBuffer(buffer,width,height, framebuf.GS8)
            tft.blit(fb, (tft.width-width)//2, (tft.height-height)//2)
            tft.show()
    while (localtime()[5]!=00):
        sleep_ms(250)
