#workers

The **original** directory contains the eadweard-muybridge-animal-locomotion-04.jpg image from which the images for the animation were extracted.  

**imgconvert.py** is used to convert an image from jpg, bmp, png, ... (any format supported by PIL) into an Python dictionnary.  
The dictionnary has the following keys:  
-  __imwidth__: width of the picture
-  __imheight__: height of the picture
-  __data__: a bytearray with the content of the picture formated with 2 pixels per byte

**convbash.sh** is used to iterate through the file in the directory and call imgconvert.py with the right parameters

**animworkers.py** is the script executed on the Pico

The animworkers.py and all the workers*xx*.py files should be copied in the Pico's filesystem 
The pot change the speed of the animation
The push-button is used to clear the screen and halt the script
