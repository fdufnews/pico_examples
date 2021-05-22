# pico_examples
Some example code while starting to use Raspberry Pi Pico and Micropython


## Drivers directory
 Contains some drivers:
-  **SSD1306** the ubiquitous 128 x 64 monochrome oled display
-  **SH1122** a much better (but more expensive) 256 x 64 oled display with 16 levels of grey
-  **ST7735b** for a color TFT with ST7735 driver with blue tab
 
## Examples directory
-  **1306oled**, the code to test the SSD1306 driver
-  **1122oled**, the code to test the SH1122 driver
-  **st7735**, code to test the st7735b driver
-  **led_timer_class**, a class to play with LEDs and make them flashing asynchronously using timers
-  **sequence** some code to display short anim on the SH1122. I have seen [Harifun's video on Youtube](https://www.youtube.com/watch?v=cm2Fz9WTL1A) using Eadweard Muybridge pictures of animals in motion and think it will be fun to make the same thing on the SH1122 display.
   -  **horsejump**, a horse travel across the screen jumping over a fence.
   -  **workers**, 2 blacksmiths knocking on an anvil 
  For the 2 anim, there is an orginal directory in wich one can find the original picture, the sub pictures that were extracted with Gimp, a Python script and a bash script used to convert each sub picture into a Pyton dictionnary.
