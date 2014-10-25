#!/usr/bin/env python

from operator import itemgetter

def unique(inlist, keepstr=True):
  typ = type(inlist)
  if not typ == list:
    inlist = list(inlist)
  i = 0
  while i < len(inlist):
    try:
      del inlist[inlist.index(inlist[i], i + 1)]
    except:
      i += 1
  if not typ in (str, unicode):
    inlist = typ(inlist)
  else:
    if keepstr:
      inlist = ''.join(inlist)
  return inlist



def freqCount(instring,sort=False):
    ustring = unique(instring)
    freqdict = {}
    for ch in ustring:
        num = instring.count(ch)
        freqdict[ch] = num
    return freqdict

def printFreq(freqdict,reverse=False,alphabetical=False):
    keys = freqdict.keys()
    if not alphabetical:
        d2 = sorted(freqdict.iteritems(),key=itemgetter(1),reverse=reverse)
        for d in d2:
            k = d[0]
            v = d[1]
            if '"' in keys:
                print "'%s':%i" % (k,v)
            if "'" in keys:
                print '"%s":%i'% (k,v)
    else:
        keys = sorted(freqdict.keys())
        for k in keys:
            v = freqdict[k]
            if '"' in keys:
                print "'%s':%i" % (k,v)
            if "'" in keys:
                print '"%s":%i'% (k,v)
                
