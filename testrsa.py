#!/usr/bin/env python

import rsa

public,private = rsa.newkeys(512)
pempubkey = public.save_pkcs1(format='PEM')
pemprikey = private.save_pkcs1(format='PEM')
pubfile = 'mypublickey.pem'
prifile = 'myprivatekey.pem'
f = open(pubfile,'wt')
f.write(pempubkey)
f.close()
f = open(prifile,'wt')
f.write(pemprikey)
f.close()
print 'Your public key has been saved in %s' % pubfile
print 'Your private key has been saved in %s' % prifile

f = open(pubfile,'rt')
pubcontents = f.read()
f.close()
newpublicstr = rsa.pem.load_pem(pubcontents,'RSA PUBLIC KEY')

newpublic = rsa.PublicKey.load_pkcs1(pubcontents,format='PEM')
print newpublic
# newprivate = rsa.PrivateKey.load_pkcs1(prifile,format='PEM')
