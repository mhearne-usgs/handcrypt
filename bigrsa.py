#!/usr/bin/env python

from rsa.bigfile import *
import rsa
import cStringIO
import tempfile

def bigEncrypt(message,public_key,private_key=None):
    instring = cStringIO.StringIO()
    #instring = tempfile.TemporaryFile('w+')
    instring.write(message)
    instring.seek(0)
    if private_key is not None:
        signature = rsa.sign(message,private_key,'SHA-1')
    else:
        signature = ''
    outstring = cStringIO.StringIO()
    #outstring = tempfile.TemporaryFile('w+')
    encrypt_bigfile(instring,outstring,public_key)
    crypto = outstring.getvalue()
    instring.close()
    outstring.close()
    return (crypto,signature)

def bigDecrypt(crypto,private_key,public_key=None,signature=None):
    instring = cStringIO.StringIO()
    instring.write(crypto)
    instring.seek(0)
    outstring = cStringIO.StringIO()
    decrypt_bigfile(instring,outstring,private_key)
    plaintext = outstring.getvalue()
    isVerified = False
    if public_key is not None and signature is not None:
        try:
            rsa.verify(plaintext,signature,public_key)
            isVerified = True
        except:
            pass
        
    instring.close()
    outstring.close()
    return (plaintext,isVerified)

if __name__ == '__main__':
    (pub,pri) = rsa.newkeys(1024)
    message = '''Over a century ago Washington laid the corner stone of the Capitol in what was then little more than a tract of wooded wilderness here beside the Potomac. We now find it necessary to provide by great additional buildings for the business of the government.'''
    print pub
    print 'The message has %i characters' % len(message)
    crypt,sig = bigEncrypt(message,pub,pri)
    print 'The encrypted message has %i characters' % len(crypt)
    plain,isok = bigDecrypt(crypt,pri,pub,sig)
    print plain
    if isok:
        print 'The message has been verified.'
    else:
        print 'Warning: The message cannot be verified!'
    
