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
from machine import Pin, SPI, PWM, ADC, mem32, mem8
from utime import localtime, mktime, sleep_ms
from os import listdir
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
button_released = True

def rotary_changed(change):
    global val, button_pressed
    if change == Rotary.ROT_CW:
        val = val + 1
    elif change == Rotary.ROT_CCW:
        val = val - 1
    elif change == Rotary.SW_PRESS:
        button_pressed = True
        button_released = False
    elif change == Rotary.SW_RELEASE:
        button_released = True


def set_time():
    global select, button_pressed, val

    tft4.fill(white)
    time = list(localtime())
    dh = int(time[3] // 10)
    uh = time[3] % 10
    dm = int(time[4] // 10)
    um = time[4] % 10
    pos = (8, 20, 44, 56)
    num = [dh, uh, dm, um]
    for i in range(4):
        tft4.text(str(num[i]), pos[i], 20, black)
    tft4.text(':', 32,20,black)
    tft4.show()
    
    for i in range(4):
        while (not button_released):
            pass
        gc.collect()
        old_val = val = num[i]
        tft4.text(str(val), pos[i], 20, red)
        tft4.show()
        while(not button_pressed):
            sleep_ms(50)
            newval = val
            if (i == 0):
                newval = newval % 3
            elif (i == 1) and (num[0] == 2):
                newval = newval % 4
            elif (i == 1) and (num[0] < 2):
                newval = newval % 10
            elif (i == 2):
                newval = newval % 6
            elif (i == 3):
                newval = newval % 10
            if (newval != old_val):
                tft4.fill_rect(pos[i],20, 8,8, white)
                tft4.text(str(newval), pos[i], 20, red)
                tft4.show()
                old_val = newval
        num[i] = newval
        tft4.fill_rect(pos[i],20, 8,8, white)
        tft4.text(str(num[i]), pos[i], 20, black)
        tft4.show()
        button_pressed = False
    time[3] = num[0] * 10 + num[1]
    time[4] = num[2] * 10 + num[3]
    time[5] = 0
    newtime = mktime(time)
    ctime=localtime(newtime)
    
    # insert data  to RTC register
    
    setup_0 = (ctime[0] << 12) | (ctime[1] << 8) | ctime[2]
    setup_1 =  (ctime[3] << 16) | (ctime[4] << 8) | ctime[5]
    setup_1 =  setup_1 |  (((ctime[6] + 1) % 7) << 24)
    
    # register RTC address
    rtc_base_mem = 0x4005c000
    atomic_bitmask_set = 0x2000
    
    mem32[rtc_base_mem + 4] = setup_0
    mem32[rtc_base_mem + 8] = setup_1
    mem8[rtc_base_mem + atomic_bitmask_set + 0xc] = 0x10


def menu_faces():
    global select, button_pressed, val
    
    tft4.fill(white)
    idx = 0
    for f in font:
        tft4.text(f,8, 10 + idx * 10, black)
        idx += 1
    tft4.text('>', 0, 10 + select * 10, red)
    tft4.show()
    button_pressed = False
    while (not button_released):
        pass
    val = select
    old_val = val
    while (not button_pressed):
        sleep_ms(50)
        if (val != old_val):
            newsel = val % len(font)
            tft4.fill_rect(0, 10 + select * 10, 8, 18 + select * 10, white)
            tft4.text('>', 0, 10 + newsel * 10, red)
            tft4.show()
            select = newsel
            old_val = val
    button_pressed = False

main_menu = ({'item':'Faces', 'func':menu_faces}, {'item':'Set time', 'func':set_time}, {'item':'Quit', 'func':None})

def menu( dictionary):
    global select, button_pressed, val
    
    tft4.fill(white)
    idx = 0
    old_val = val = 0
    for i in main_menu:
        tft4.text(i['item'],8, 10 + idx * 10, black)
        idx += 1
    tft4.text('>', 0, 10, red)
    tft4.show()
    button_pressed = False
    while (not button_released):
        pass
    while (not button_pressed):
        sleep_ms(50)
        if (val != old_val):
            newval = val % len(dictionary)
            tft4.fill_rect(0, 10 + old_val * 10, 8, 18 + old_val * 10, white)
            tft4.text('>', 0, 10 + newval * 10, red)
            tft4.show()
            old_val = val = newval
    button_pressed = False
    if (main_menu[val]['func'] != None):
        main_menu[val]['func']()


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
white = tft1.rgb(255,255,255)
yellow = tft1.rgb(255,255,0)
red = tft1.rgb(255,0,0)
green = tft1.rgb(0, 255,0)
blue = tft1.rgb(0, 0, 255)
black = tft1.rgb(0, 0, 0)


#black = 0
#white = 0xff

root = 'digits' # path to the directory holding the different font of numbers
#font = ('nixie','tiles','rounded','hand','balloon','monsters','stamp') # font of digits
font = listdir(root)
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
            menu(main_menu)
            break
        backlight = int(lum.read_u16()/65535*100)
        if (backlight <= 0):
            backlight = 1
        tft1.backlight(backlight)
        sleep_ms(250)
