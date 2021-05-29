# Short script to test the possible orientations of the display
# swapping width and height rotate the screen
# usd mirrors the screen
#
#
# if width > height and usd = False
#  _____________________
# |   o o o o o o o o   |
# |  _________________  |
# | | ------/ X       | |
# | | |               | |
# | | |/              | |
# | | Y               | |
# | |_________________| |
# |_____________________|
#
#
# if width > height and usd = True
#  _____________________
# |  _________________  |
# | | ------/ X       | |
# | | |               | |
# | | |/              | |
# | | Y               | |
# | |_________________| |
# |   o o o o o o o o   |
# |_____________________|
#
#
# if width < height and usd = False
#  _____________
# |  _________  |
# |  |---/ X  | |
# |o ||       | |
# |o ||       | |
# |o ||       | |
# |o ||/      | |
# |o |Y       | |
# |o |        | |
# |o |        | |
# |o |        | |
# |  |________| |
# |_____________|
#
#
# if width < height and usd = True
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
#
from drivers.st7735b import ST7735B
from machine import Pin, SPI, PWM

dc = Pin(3,Pin.OUT)
cs1 = Pin(5, Pin.OUT)
cs2 = Pin(9, Pin.OUT)
res = Pin(2,Pin.OUT)
blk = Pin(8,Pin.OUT)
blkPWM = PWM(blk)
#blkPWM.duty_u16(65534)
tft1 = ST7735B(SPI(0,baudrate=25000000), cs1,dc,res, blk=blkPWM, height=80, width=160, usd = False)
tft2 = ST7735B(SPI(0,baudrate=25000000), cs2,dc,res, blk=blkPWM, height=80, width=160, usd = False, reset_tft = False)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res, blk=blkPWM, height=80, width=160, usd = True)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res, blk=blkPWM, height=160, width=80, usd = False)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res, blk=blkPWM, height=160, width=80, usd = True)
tft1.backlight(100)
tft2.backlight(100)
yellow = tft1.rgb(255,255,0)
red = tft1.rgb(255,0,0)
x = tft1.width >> 1
symbol = 10
tft1.line(0, 0, x, 0, yellow)
tft1.line(x, 0, x - symbol, symbol, yellow)
tft1.line(x + (symbol >> 1), 0, x + symbol + (symbol >> 1), symbol, yellow)
tft1.line(x + symbol + (symbol >> 1), 0, x + (symbol >> 1), symbol, yellow)

y = tft1.height >> 1
tft1.line(0, 0, 0, y, yellow)
tft1.line(0, y, symbol, y - symbol, yellow)
tft1.line(0, y + (symbol >> 1), (symbol >> 1), y + symbol, yellow)
tft1.line(symbol, y + (symbol >> 1), 0, y + symbol + (symbol >> 1), yellow)

tft2.line(0, 0, x, 0, red)
tft2.line(x, 0, x - symbol, symbol, red)
tft2.line(x + (symbol >> 1), 0, x + symbol + (symbol >> 1), symbol, red)
tft2.line(x + symbol + (symbol >> 1), 0, x + (symbol >> 1), symbol, red)

tft2.line(0, 0, 0, y, red)
tft2.line(0, y, symbol, y - symbol, red)
tft2.line(0, y + (symbol >> 1), (symbol >> 1), y + symbol, red)
tft2.line(symbol, y + (symbol >> 1), 0, y + symbol + (symbol >> 1), red)

tft1.show()
tft2.show()
