#!python
# Convert images from bmp, jpg, png to a Python binary array to be displayed on a 16 grey levels OLED display
# Create a dictionnary with: width, height and image data
# the picture is converted to black and white and resized

from PIL import Image, ImageOps
from argparse import ArgumentParser
import sys
import math

#define a parser for the command line
parser = ArgumentParser(description='convert images from bmp, jpg, png to a Python binary array to be displayed on a 16 grey levels OLED display')
parser.add_argument('inputfile', action="store", help='name of the input file')
parser.add_argument('arrayname', action="store", help='name of the variable handling the data')
parser.add_argument('outputfile', action="store", help='name of the output file')
parser.add_argument('width', action="store", type=int, help='width of the converted image')
parser.add_argument('height', action="store", type=int, help='height of the converted image')

args = parser.parse_args()

if args.width % 2:
    print("image width must be even!", file=sys.stderr)
    sys.exit(1)

im = Image.open(args.inputfile)
# convert to grayscale
im = im.convert(mode='L')
width = args.width
height = args.height

# create a thumbnail the right size
im.thumbnail((width, height), Image.ANTIALIAS)

# Write out the output file.
with open(args.outputfile, 'w') as f:
    # generate entries of the dictionnary
    f.write('{} = {}"imwidth": {},\\\n "imheight": {},\\\n "data": bytearray(b"'.format(args.arrayname,'{', width, height))
    # scan the image in order to create the data content of the dictionnary
    for y in range(0, im.size[1]):
        byte = 0
        done = True
        for x in range(0, im.size[0]):
        # concatenate 2 pixels in a byte
            l = im.getpixel((x, y))
            if x % 2 == 0:
                byte = l & 0xF0
                done = False;
            else:
                byte |= l >> 4
                f.write("\\x{:02X}".format(byte))
                done = True
        if not done:
            f.write("\\x{:02X}".format(byte))
        f.write("\\\n");
    f.write('")}\n')
