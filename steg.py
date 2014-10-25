#!/usr/bin/env python

from PIL import Image
import os.path
import math
import sys
import datetime
from optparse import OptionParser

EOM = 'EOM'

def bitset(number,value,pos):
    """Set a bit at a specified position.
    Set the bit value at position pos in number.
    """
    if value:
        return number | pow(2,(7-pos))
    else:
        if not bitget(number,pos):
            return number
        else:
            return number ^ pow(2,(7-pos))

def bitget(number,pos):
    #pos is ordered from the most significant bit to least (left to right, 0 to 7)
    return (number & pow(2,(7-pos))) >> (7-pos)

def ind2sub(offset,sz):
    nrows = sz[0]
    ncols = sz[1]
    row = offset/ncols
    col = offset % ncols
    return (row,col)

def steghide(message,imagefile,outfile):
    if not os.path.isfile(imagefile):
        raise Exception,"Could not find file %s" % imagefile
    path,filename = os.path.split(imagefile)
    basename,ext = os.path.splitext(filename)
    try:
        im = Image.open(imagefile)
        if im.format == 'JPEG':
            raise Exception,"This module does not support the JPEG format" % imagefile
    except Exception,msg:
        raise Exception,'Opening this image file failed: "%s"' % msg
    message = message + EOM
    pix = im.load()
    #Only use the first band for now...
    offset = 0
    nchanged = 0
    for character in message:
        #print character,bin(ord(character))
        for i in range(0,8):
            row,col = ind2sub(offset,im.size)
            pixel = pix[row,col]
            bit = bitget(ord(character),i)
            newpixel = bitset(pixel[0],bit,7)
            if newpixel != pixel[0]:
                nchanged += 1
            #print pixel[0],bit,newpixel
            pix[row,col] = (newpixel,pixel[1],pixel[2])
            offset += 1
    im.save(outfile)
    return nchanged

def stegread(imagefile):
    if not os.path.isfile(imagefile):
        raise Exception,"Could not find file %s" % imagefile
    try:
        im = Image.open(imagefile)
        if im.format == 'JPEG':
            raise Exception,"This module does not support not find file %s" % imagefile
    except Exception,msg:
        raise Exception,'Opening this image file failed: "%s"' % msg
    message = ''
    pix = im.load()
    nrows,ncols = im.size
    npixels = nrows*ncols
    offset = 0
    noMessage = False
    while not message.endswith(EOM):
        value = 0
        for i in range(0,8):
            if offset > npixels:
                noMessage = True
                break
            row,col = ind2sub(offset,im.size)
            try:
                pixel = pix[row,col]
            except:
                pass
            bit = bitget(pixel[0],7)
            value = bitset(value,bit,i)
            offset += 1
        message = message + chr(value)
    if noMessage:
        return ''
    return message[0:message.find(EOM)]

if __name__ == '__main__':
    usage = "usage: %prog [options] infile [outfile]"
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--message", dest="message",
                      help="The message to hide/encrypt (in quotes)")
    parser.add_option("-f", "--messagefile", dest="messageFile",
                      help="The text file containing the message to hide/encrypt (in quotes)")
    

    (options, args) = parser.parse_args()

    if not options.message and not options.messageFile and len(args) > 1:
        print 'You must specify the message using the -m or -f options when hiding.'
        parser.print_usage()
        sys.exit(1)

    if (options.message or options.messageFile) and len(args) < 2:
        print 'When unhiding, specifying a message is unnecessary, as the message should be hidden in the image file.'
        parser.print_usage()
        sys.exit(1)

    doHide = False
    if len(args) == 2:
        doHide = True

    if doHide:
        if options.message:
            message = options.message.replace('"','')
        else:
            f = open(options.messageFile,'rt')
            message = f.read()
            f.close()
        
        nchanged = steghide(message,args[0],args[1])
        print '%i pixels in input image were changed' % nchanged
        sys.exit(0)
    else:
        hidden = stegread(args[0])
        print 'Your secret message is: "%s"' % hidden
        sys.exit(0)
