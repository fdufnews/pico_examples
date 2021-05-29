#!python
# Convert images from bmp, jpg, png to a raw binary file
# Create a header with: width and height as 2 16 bits words before raw image data
# the image is resized and colors encoded in RGB 3-3-2

from PIL import Image, ImageOps
from argparse import ArgumentParser
import sys
import math
from ctypes import *

#define a parser for the command line
parser = ArgumentParser(description='convert images from bmp, jpg, png to a raw data with a 4 bytes header')
parser.add_argument('inputfile', action="store", help='name of the input file')
parser.add_argument('outputfile', action="store", help='name of the output file')
parser.add_argument('width', action="store", type=int, help='width of the converted image')
parser.add_argument('height', action="store", type=int, help='height of the converted image')

args = parser.parse_args()

im = Image.open(args.inputfile)
# convert to RGB
im = im.convert(mode='RGB')
width = args.width
height = args.height

# compute resize argument in order to fill the screen as much as possible and keep image ratio
coef = max(im.width/width, im.height/height)
width = int(im.width/coef)
height = int(im.height/coef)

# create a thumbnail the right size
newim = im.resize((width, height), Image.ANTIALIAS)

# Write out the output file.
with open(args.outputfile, 'wb') as f:
    # generate header
    print('\n\twidth = {} \n\theight = {}\n'.format(width,height))
    f.write(c_ushort(width))
    f.write(c_ushort(height))
    # scan the image in order to create the data content
    for y in range(0, newim.size[1]):
        for x in range(0, newim.size[0]):
        # concatenate RGB 8-8-8 in RGB 3-3-2
            l = newim.getpixel((x, y))
            pixel = c_ubyte((l[0] & 0xe0) | ((l[1] & 0xe0)>>3) | (l[2] >> 6))
            f.write(pixel)
    f.close()
