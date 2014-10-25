#!/usr/bin/env python

from fileio import *
import sys

markers = {'0xe0':'APP0',
           '0xc0':'SOF0',
           '0xc4':'DHT',
           '0xdb':'DQT',
           '0xda':'SOS',
           '0xfe':'COM',
           '0xd9':'EOI'}

imtypes = {1:'greyscale',3:'YcbCr',4:'CMYK'}

def ycbcr2rgb(ycbcr):
    Y = ycbcr[0]
    Cb = ycbcr[1]
    Cr = ycbcr[2]
    R = Y                                 + 1.402  (Cr-128)
    G = Y - 0.34414 (Cb-128) - 0.71414 (Cr-128)
    B = Y    + 1.772 (Cb-128)
    return (R,G,B)

def rgb2ycbcr(rgb):
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    Y = 0.299*R  + 0.587*G  + 0.114*B
    Cb = -0.1687*R - 0.3313*G  + 0.5*B + 128
    Cr = 0.5*R - 0.4187*G - 0.0813*B + 128
    return (Y,Cb,Cr)

def hexify(bytes):
    hexbytes = [hex(b) for b in bytes]
    return hexbytes

def readAPP0(f):
    segment = {}
    segment['id'] = fread(f,5,'string')[0:4]
    vmaj = fread(f,1,'uchar')
    vmin = fread(f,1,'uchar')
    segment['version'] = '%i.%i' % (vmaj,vmin)
    denunits = fread(f,1,'uchar')
    if denunits == 0:
        segment['density_units'] = 'None'
    if denunits == 1:
        segment['density_units'] = 'dpi'
    if denunits == 2:
        segment['density_units'] = 'dpc'
    segment['x_density'] = fread(f,1,'ushort',dendian='big')
    segment['y_density'] = fread(f,1,'ushort',dendian='big')
    nrows = fread(f,1,'ushort')
    ncols = fread(f,1,'ushort')
    segment['thumb_cols'] = nrows
    segment['thumb_rows'] = ncols
    if segment['thumb_cols']:
        segment['thumbnail'] = fread(f,nrows*ncols*3,'uchar')
    return segment

def readSOF0(f):
    segment = {}
    segment['precision'] = fread(f,1,'uchar')
    segment['nrows'] = fread(f,1,'ushort',dendian='big')
    segment['ncols'] = fread(f,1,'ushort',dendian='big')
    ncomps = fread(f,1,'uchar')
    if ncomps == 1:
        segment['ncomps'] = 'greyscale'
    if ncomps == 3:
        segment['ncomps'] = 'YcbCr'
    if ncomps == 4:
        segment['ncomps'] = 'CMYK'
    segment['components'] = []
    for i in range(0,ncomps):
        component = {}
        compid = fread(f,1,'uchar')
        component['component_id'] = compid
        sampfactor = fread(f,1,'uchar')
        vertsamp,horizsamp = splitSampling(sampfactor)
        quantnumber = fread(f,1,'uchar')
        component['vertical_sampling'] = vertsamp
        component['horizontal_sampling'] = vertsamp
        component['quant_number'] = quantnumber
        segment['components'].append(component)
    return segment

def splitSampling(sampling):
    horiz = sampling >> 4
    vert = sampling - (horiz << 4)
    return (vert,horiz)

def readDHT(f):
    segment = {}
    htinfo = fread(f,1,'uchar')
    htype = htinfo >> 4
    numht = htinfo - (htype << 4)
    segment['number_ht'] = numht
    segment['ht_type'] = htype
    segment['number_symbols'] = fread(f,16,'uchar')
    nsymbols = sum(segment['number_symbols'])
    segment['symbols'] = fread(f,nsymbols,'uchar')
    return segment

def readDQT(f):
    segment = {}
    qtinfo = fread(f,1,'uchar')
    qtprec = htinfo >> 4
    numqt = htinfo - (htype << 4)
    if qtprec == 0:
        segment['precision_qt'] = 8
    else:
        segment['precision_qt'] = 16
    segment['number_qt'] = numqt
    nbytes = (segment['precision_qt']+1)*64
    segment['qt_values'] = fread(f,nbytes,'uchar')
    return segment

def readCOM(f,slen):
    segment = {}
    segment['comment'] = fread(f,slen,'string')
    return segment

def readSOS(f):
    segment = {}
    ncomps = fread(f,1,'uchar')
    segment['number_components'] = ncomps
    components = []
    for i in range(0,ncomps):
        comp = {}
        comp['component_id'] = fread(f,1,'uchar')
        hufftables = fread(f,1,'uchar')
        dctable = hufftables >> 4
        actable = hufftables - (dctable << 4)
        comp['huffman_actable'] = actable
        comp['huffman_dctable'] = actable
        components.append(comp)
    segment['components'] = components
    igbytes = fread(f,3,'uchar')
    return segment
    

def readSegment(segtype,f,slen):
    if segtype == 'APP0':
        return readAPP0(f)
    if segtype == 'SOF0':
        return readSOF0(f)
    if segtype == 'DHT':
        return readDHT(f)
    if segtype == 'DQT':
        return readDQT(f)
    if segtype == 'SOS':
        return readSOS(f)
    if segtype == 'COM':
        return readCOM(f,slen)
    

def listMarkers(jpegfilename):
    f = open(jpegfilename,'rb')
    fpos = f.tell()
    soi = fread(f,2,'uchar')
    print 'SOI: %s (Offset %i)' % (str(hexify(soi)),fpos)
    while True:
        headerbytes = fread(f,2,'uchar')
        ident = hex(headerbytes[1])
        segtype = None
        slen  = fread(f,1,'ushort',dendian='big')-2
        if ident in markers.keys():
            print 'Segment "%s": %i bytes (offset %i)' % (markers[ident],slen,fpos)
            segtype = markers[ident]
            if segtype == 'EOI':
                break
        else:
            print 'Unidentified segment "%s": %i bytes (offset %i)' % (ident,slen,fpos)
        
        if segtype == None:
            f.seek(slen,1)
            continue
        if ident == '0xfe': #comment
            fpos = f.tell()
            comment = fread(f,slen,'string').strip()
            print '\tImage comment: "%s"' % comment
            f.seek(fpos,0)
        if ident == '0xc0':
            fpos = f.tell()
            dprec = fread(f,1,'uchar')
            nrows = fread(f,1,'ushort',dendian='big')
            ncols = fread(f,1,'ushort',dendian='big')
            ncomps = fread(f,1,'uchar')
            imtype = imtypes[ncomps]
            fmt = '\tImage has %i rows, %i columns %i bit data, %s'
            print fmt % (nrows,ncols,dprec,imtype)
            f.seek(fpos,0)
        f.seek(slen,1)
    f.close()

if __name__ == '__main__':
    fname = sys.argv[1]
    listMarkers(fname)

# class ImageDecoder(object):
#     markers = {}
#     SOICheck = ['0xff','0xd8']
#     headers = {'jfif':['0xff','0xe0']}
#     jfif_id = 'JFIF'
#     jext_id = 'JFXX'
#     #jfif_id = ['0x4A','0x46','0x49','0x46','0x00']
#     #jext_id = ['0x4A','0x46','0x58','0x58','0x00']
    
    
#     File = None
#     def __init__(self,fname):
#         self.File = open(fname,'rb')
#         soibytes = fread(self.File,2,'uchar',dendian='big')
#         if not self.checkMarker(soibytes,self.SOICheck):
#             raise Exception,'Not a JPEG Image!'
#         marker = self.readMarker(fname)
#         markers[marker['name']] = marker
#         while marker['name'] != 'EOI':
#             marker = self.readMarker(fname)
#             markers[marker['name']] = marker

#     def checkMarker(self,bytes,bcheck):
#         for i in range(0,len(bytes)):
#             b = bytes[i]
#             c = bcheck[i]
#             if b != c:
#                 return False
#         return True

#     def readJFIF(self):
#         vmaj = fread(self.File,1,'string')
#         vmin = fread(self.File,1,'string')
#         version = '%i.%i' % (vmaj,vmin)
#         dunits = fread(self.File,1,'uchar')
#         xden = fread(self.File,1,'ushort',dendian='big')
#         yden = fread(self.File,1,'ushort',dendian='big')
#         tw = fread(self.File,1,'uchar',dendian='big')
    
#     def readMarker(self):
#         marker = {}
#         markerbytes = [hex(b) for b in fread(self.File,2,'uchar')]
#         for hdrname,bytes in self.headers.iteritems():
#             res = self.checkMarker(markerbytes,bytes)
#             if res:
#                 if hdrname == 'jfif':
#                     ident = fread(self.File,5,'uchar')
#                     ident = [chr(i) for i in ident[0:4]]
#                     ident = ''.join(ident)
#                     if ident == self.jfif_id:
#                         markerbody = self.readJFIF()
#                     elif ident == self.jext_id:
#                         markerbody = self.readJEXT()
#                 elif hdrname == 'dqt':
#                     markerbody = self.readDQT()
                    

# f = open(fname,'rb')
# soi = ['0xff','0xd8']
# soibytes = [hex(b) for b in fread(f,2,'uchar',dendian='big')]
# print soibytes
# if soibytes[0] != soi[0] or soibytes[1] != soi[1]:
#     print 'Incorrect start of image.'
#     sys.exit(0)

# app0 = ['0xff','0xe0']
# app0bytes = [hex(b) for b in fread(f,2,'uchar',dendian='big')]
# print app0bytes
# if app0bytes[0] != app0[0] or app0bytes[1] != app0[1]:
#     print 'Incorrect app0 marker.'
#     sys.exit(0)

# fpos = f.tell()
# app0len = fread(f,1,'ushort',dendian='big')
# print app0len
# app0id = [hex(b) for b in fread(f,5,'uchar',dendian='big')]
# print app0id

# #jump to beginning of next segment
# f.seek(fpos,0)
# f.seek(app0len,1)

# #read beginning of next marker
# marker2 = [hex(b) for b in fread(f,2,'uchar',dendian='big')]
# print marker2
# fpos = f.tell()
# hdrlen = fread(f,1,'ushort',dendian='big')

# #jump to beginning of next segment
# f.seek(fpos,0)
# f.seek(hdrlen,1)

# marker3 = [hex(b) for b in fread(f,2,'uchar',dendian='big')]
# print marker3

# f.close()
