# Drivers directory
 Contains some drivers:
-  **SSD1306** the ubiquitous 128 x 64 monochrome oled display from Peter Hinch  
-  **SH1122** a much better (but more expensive) 256 x 64 oled display with 16 levels of grey. Based on the SSD1306 driver from [Peter Hinch](https://github.com/peterhinch/micropython-nano-gui)
-  **ST7735b** a driver for a TFT screen usin an ST7735 driver  
This driver is using Peter Hinch st7735r.py driver as a base  
This driver is writen for a 0.96" 80 x 160 display (with blue tab) and tested on that display  
The specificities of that display are:  
-  inverted contrast
-  there is a 24 lines offset that is taken into account in the driver

# Setup
The drivers are supposed to be in a drivers directory just under the root
The test scripts expect the drivers are there

Todo : add DMA support
 
