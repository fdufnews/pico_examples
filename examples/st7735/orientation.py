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
cs = Pin(5, Pin.OUT)
res = Pin(2,Pin.OUT)
blk = Pin(8,Pin.OUT)
#blk.on()
blkPWM = PWM(blk)
blkPWM.duty_u16(65534)
tft = ST7735B(SPI(0,baudrate=25000000), cs,dc,res,height=80, width=160, usd = False)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res,height=80, width=160, usd = True)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res,height=160, width=80, usd = False)
#tft = ST7735B(SPI(0,baudrate=20000000), cs,dc,res,height=160, width=80, usd = True)
white = tft.rgb(255,255,0)
x = tft.width >> 1
symbol = 10
tft.line(0, 0, x, 0, white)
tft.line(x, 0, x - symbol, symbol, white)
tft.line(x + (symbol >> 1), 0, x + symbol + (symbol >> 1), symbol, white)
tft.line(x + symbol + (symbol >> 1), 0, x + (symbol >> 1), symbol, white)

y = tft.height >> 1
tft.line(0, 0, 0, y, white)
tft.line(0, y, symbol, y - symbol, white)
tft.line(0, y + (symbol >> 1), (symbol >> 1), y + symbol, white)
tft.line(symbol, y + (symbol >> 1), 0, y + symbol + (symbol >> 1), white)

tft.show()

