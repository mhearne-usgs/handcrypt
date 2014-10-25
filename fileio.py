#!/usr/bin/env python

import struct

FORMATS = {'char':('b',1),'uchar':('B',1),
           'short':('h',2),'ushort':('H',2),
           'int':('i',4),'uint':('I',4),
           'long':(8,'l'),'ulong':('L',8),
           'float':('f',4),'double':('d',8),
           'string':('b',1)}

ENDIANS = {'little':'<','big':'>','native':'@'}

def fwrite(f,data,dtype,dendian='native'):
    endian = ENDIANS[dendian]
    fmt = FORMATS[dtype][0]
    typesize = FORMATS[dtype][1]
    dsize = len(data)
    structfmt = '%s%i%s' % (endian,dsize,fmt)
    rawdata = struct.pack(structfmt,*data)
    f.write(rawdata)
    return len(rawdata)

def fread(f,dsize,dtype,dendian='native'):
    endian = ENDIANS[dendian]
    fmt = FORMATS[dtype][0]
    typesize = FORMATS[dtype][1]
    nbytes = dsize*typesize
    rawdata = f.read(nbytes)
    structfmt = '%s%i%s' % (endian,dsize,fmt)
    data = struct.unpack(structfmt,rawdata)
    if dsize == 1:
        data = data[0]
    if dtype == 'string':
        data = ''.join([chr(d) for d in data])
    return data

if __name__ == '__main__':
    indata = [4,5,6] 
    fname = 'foo.dat'
    f = open(fname,'wb')
    fwrite(f,indata,'ushort')
    f.close()
    f = open(fname,'rb')
    outdata = fread(f,3,'ushort')
    f.close()
    print indata,outdata

    indata = [4.1,5.2,6.3]
    f = open(fname,'wb')
    fwrite(f,indata,'float')
    f.close()
    f = open(fname,'rb')
    outdata = fread(f,3,'float')
    f.close()
    print indata,outdata
    
