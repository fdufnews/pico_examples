# Test before designing a "faux nixie" clock
#
# Each display is a digit
# a bitmap is used for each number so any shape can be used
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
# Using SPI(0) default  the displays are wired this way
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
from utime import sleep

def draw_arrows(tft, color):
    # draw an arrow along the x axis
    x = tft.width >> 1
    symbol = 10
    tft.line(0, 0, x, 0, color)
    tft.line(x, 0, x - symbol, symbol, color)
    tft.line(x + (symbol >> 1), 0, x + symbol + (symbol >> 1), symbol, color)
    tft.line(x + symbol + (symbol >> 1), 0, x + (symbol >> 1), symbol, color)

    # draw an arrow along the y axis
    y = tft.height >> 1
    tft.line(0, 0, 0, y, color)
    tft.line(0, y, symbol, y - symbol, color)
    tft.line(0, y + (symbol >> 1), (symbol >> 1), y + symbol, color)
    tft.line(symbol, y + (symbol >> 1), 0, y + symbol + (symbol >> 1), color)


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

yellow = tft1.rgb(255,255,0)
red = tft1.rgb(255,0,0)
green = tft1.rgb(0, 255,0)
blue = tft1.rgb(0, 0, 255)
displays = [tft1, tft2, tft3 ,tft4]
colors   = [yellow, red, green, blue]
while (True):
    for i in range(4):
        draw_arrows(displays[i], colors[i])
        displays[i].show()
    sleep(2)
    col = colors.pop()
    colors.insert(0,col)
