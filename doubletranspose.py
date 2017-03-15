#!/usr/bin/env python

import argparse
import sys
import math

#as described here: http://users.telenet.be/d.rijmenants/en/handciphers.htm

def getColumnOrder(key):
    '''
    Return a list of the order of the key indices
    '''
    skey = sorted(list(key))
    cidx = []
    for ch in key:
        idx = skey.index(ch)
        cidx.append(idx)
        skey[idx] = '0'
    return cidx

def getMessageRows(key,message):
    ncols = len(key)
    nrows = int(math.ceil(len(message)/ncols))
    msgrows = []
    for i in range(0,nrows+1):
        mstart = i*ncols
        mend = min(len(message),mstart+ncols)
        msgrow = message[mstart:mend]
        msgrows.append(msgrow)

    return msgrows

def orderMessageRows(msgrows,skey):
    newmsgrows = []
    for row in msgrows:
        newrow = []
        for i in range(0,len(row)):
            try:
                idx = skey.index(i)
                newrow.append(row[idx])
            except:
                pass
        newmsgrows.append(''.join(newrow))
    return newmsgrows

def transposeMessageRows(msgrows,ncols):
    messagelist = []
    nrows = len(msgrows)
    for j in range(0,ncols):
        for i in range(0,nrows):
            row = msgrows[i]
            if j >= len(row):
                break
            messagelist.append(row[j])
    message = ''.join(messagelist)
    return message

def main(args):
    if args.doEncrypt and args.doDecrypt:
        print 'Cannot do both encryption and decryption.'
        sys.exit(1)
    if args.doEncrypt:
        message = args.message
        message = message.replace(' ','').upper() #get rid of spaces, uppercase
        message = message + ((5-(len(message) % 5)) * 'X') #pad with Xs to ensure message length is multiple of 5

        #now figure out the order of the columns of the first key
        key1 = args.key1
        skey1 = getColumnOrder(key1)
        key2 = args.key2
        skey2 = getColumnOrder(key2)

        msgrows1 = getMessageRows(key1,message)
        msgrows1 = orderMessageRows(msgrows1,skey1)
        crypt1message = transposeMessageRows(msgrows1,len(key1))
        msgrows2 = getMessageRows(key2,crypt1message)
        msgrows2 = orderMessageRows(msgrows2,skey2)
        crypt2message = transposeMessageRows(msgrows2,len(key2))
        print crypt2message
                
        
            
        
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('key1', help='First keyword (no spaces)')
    parser.add_argument('key2', help='Second keyword (no spaces)')
    parser.add_argument('message', help='Message to en/decrypt (in quotes)')
    parser.add_argument('-e','--encrypt', dest='doEncrypt', action='store_true',
                        default=True,help='Perform encryption (default behavior)')
    parser.add_argument('-d','--decrypt', dest='doDecrypt', action='store_true',
                        default=False,help='Perform decryption')

    pargs = parser.parse_args()
    main(pargs)
