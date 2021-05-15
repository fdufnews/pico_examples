# Display a short animation on an SPI driven sh1122 OLED display 
# display connections to Pico
#   GND     ----->      GND (pin 38)
#   VCC     ----->      3V3 (pin 36)
#   SCLK    ----->      SCL GP6 (pin 9)
#   SDIN    ----->      SPI TX GP7 (pin 10)
#   RES     ----->      GP3 (pin 5)
#   DC      ----->      GP4 (pin 6)
#   CS      ----->      GP5 (pin 7)
#
#   A pot on GP26 (ADC0), used to change speed of the animation
#   A push-button on GP14, used to halt the script
#

from machine import Pin, SPI, ADC
from sh1122 import SH1122_SPI
import time


import framebuf

WIDTH  = 256                                            # oled display width
HEIGHT = 64                                             # oled display height

pot = ADC(0)
button = Pin(14, Pin.IN, Pin.PULL_UP)

spi = SPI(0)                                            # Init SPI0
dc = Pin(4, Pin.OUT)
dc.value(0)
res = Pin(3, Pin.OUT)
res.value(1)
cs = Pin(5, Pin.OUT)
cs.value(1)


oled = SH1122_SPI(WIDTH, HEIGHT, spi, dc, res, cs)      # Init oled display

# import workers
# 2 pixels per byte
from workers1 import workers1 as image1
from workers2 import workers2 as image2
from workers3 import workers3 as image3
from workers4 import workers4 as image4
from workers5 import workers5 as image5
from workers6 import workers6 as image6
from workers7 import workers7 as image7
from workers8 import workers8 as image8
from workers9 import workers9 as image9
from workers10 import workers10 as image10
from workers11 import workers11 as image11
from workers12 import workers12 as image12

imgstack = (image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12)

width = image1['imwidth']
height = image1['imheight']

while button.value():
    for image in imgstack:
        speed = pot.read_u16() >> 12
        # Load the image into the framebuffer
        fb = framebuf.FrameBuffer(image['data'], width, height, framebuf.GS4_HMSB)
        # Clear the oled display in case it has junk on it.
        oled.fill(0)
        # Blit the image from the framebuffer to the oled display
        oled.blit(fb, 90, 0)
        # Finally update the oled display so the image is displayed
        oled.show()
        print('speed {} \n'.format(speed))
        time.sleep_ms(20 + 10 * (speed + 2))
oled.fill(0)
oled.show()
