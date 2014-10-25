#!/usr/bin/env python


from PIL import Image
from PIL.ExifTags import TAGS
import sys

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

if __name__ == '__main__':
    print get_exif(sys.argv[1])
