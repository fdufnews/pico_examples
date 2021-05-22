# ST7735b

Test the driver for a TFT screen usin an ST7735 driver  
This driver is using Peter Hinch st7735r.py driver as a base  
This driver is writen for a 0.96" 80 x 160 display (with blue tab) and tested on that display  
The specificities of that display are:  
-  inverted contrast
-  there is a 24 lines offset that is taken into account in the driver

# Wiring information

Wiring the TFT to Pico SPI  
Using SPI(0) default  
| Display | Pico |
| :--- | :--- |
| GND | GND (pin 38) | 
| VCC | 3V3 (pin 36) |
| SCL | SCL GP6 (pin 9) | 
| SDA | SPI TX GP7 (pin 10) | 
| RES | GP2 (pin 4) | 
| DC |  GP3 (pin 5) | 
| CS  |  GP5 (pin 7) | 
| BLK |  GP8 (pin 11) |

# Display orientation
'''
 if width > height and usd = False
  _____________________
 |   o o o o o o o o   |
 |  _________________  |
 | | ------/ X       | |
 | | |               | |
 | | |/              | |
 | | Y               | |
 | |_________________| |
 |_____________________|


 if width > height and usd = True
  _____________________
 |  _________________  |
 | | ------/ X       | |
 | | |               | |
 | | |/              | |
 | | Y               | |
 | |_________________| |
 |   o o o o o o o o   |
 |_____________________|


 if width < height and usd = False
  _____________
 |  _________  |
 |  |---/ X  | |
 |o ||       | |
 |o ||       | |
 |o ||       | |
 |o ||/      | |
 |o |Y       | |
 |o |        | |
 |o |        | |
 |o |        | |
 |  |________| |
 |_____________|


 if width < height and usd = True
  _____________
 | _________   |
 | |---/ X  |  |
 | ||       | o|
 | ||       | o|
 | ||       | o|
 | ||/      | o|
 | |Y       | o|
 | |        | o|
 | |        | o|
 | |        | o|
 | |________| o|
 |_____________|

'''
