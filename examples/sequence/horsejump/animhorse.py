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


oled = SH1122_SPI(WIDTH, HEIGHT, spi, dc, res, cs)     # Init oled display

# import images
# 2 pixels per byte
from image1 import image1 as image1
from image2 import image2 as image2
from image3 import image3 as image3
from image4 import image4 as image4
from image5 import image5 as image5
from image6 import image6 as image6
from image7 import image7 as image7
from image8 import image8 as image8
from image9 import image9 as image9
from image10 import image10 as image10
from image11 import image11 as image11
from image12 import image12 as image12
from image13 import image13 as image13
from image14 import image14 as image14
from image15 import image15 as image15
from image16 import image16 as image16
from image17 import image17 as image17
from image18 import image18 as image18
from image19 import image19 as image19
from image20 import image20 as image20

imgstack = (image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12, image13, image14, image15, image16, image17, image18, image19, image20)

width = image1['imwidth']
height = image1['imheight']
pos = 0
while button.value():
    for image in imgstack:
        speed = pot.read_u16() >> 12
        # Load the image into the framebuffer
        fb = framebuf.FrameBuffer(image['data'], width, height, framebuf.GS4_HMSB)
        # Clear the oled display in case it has junk on it.
        oled.fill(0xff)
        # Blit the image from the framebuffer to the oled display
        oled.blit(fb, pos, 0)
        # Finally update the oled display so the image is displayed
        oled.show()
        pos = (pos + 1 + ((16- speed) >> 3)) % 256
        print('speed {} \n'.format(speed))
        time.sleep_ms(10 + speed)
oled.fill(0)
oled.show()
