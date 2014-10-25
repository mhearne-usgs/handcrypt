#!/usr/bin/env python

import string
import re
import copy

class Secom(object):
    key = None
    def __init__(self,key):
        key = key.upper()
        key = re.sub('[^A-Z]','',key)
        if len(key) < 20:
            raise ValueError, 'Key must be at least 20 characters in length!'
        self.key = key
        self.defineCheckerboard()

    def defineCheckerboard(self):
        half1 = self.key[0:10]
        half2 = self.key[10:20]
        d1 = self.getDigits(half1)
        d2 = self.getDigits(half2)
        d3 = self.addDigits(d1,d2)
        d4,alldigits = self.addChain(d3)

    def getDigits(self,hstr):
        if isinstance(hstr,str):
            hlist = list(hstr)
        else:
            hlist = copy.copy(hstr)
        hlist.sort()
        digits = [-1]*10
        for i in range(0,len(hlist)):
            ch = hlist[i]
            if isinstance(hstr,str):
                idx = hstr.find(ch)
                if digits[idx] != -1:
                    while digits[idx] != -1:
                        newhstr = hstr[idx+1:]
                        idx = newhstr.find(ch)+idx+1
            else:
                idx = hstr.index(ch)
                if digits[idx] != -1:
                    while digits[idx] != -1:
                        newhstr = hstr[idx+1:]
                        idx = newhstr.index(ch)+idx+1
            if i == len(hlist)-1:
                digits[idx] = 0
            else:
                digits[idx] = i+1

        return digits

    def addDigits(self,d1,d2):
        d3 = []
        for i in range(0,len(d1)):
            sum = (d1[i]+d2[i]) % 10
            d3.append(sum)

        return d3

    def addChain(self,d3):
        d4 = []
        dt = d3
        for i in range(0,5):
            dt2 = []
            for j in range(0,len(dt)-1):
                d1 = dt[j]
                d2 = dt[j+1]
                dt2.append((d1+d2)%10)
            d1 = dt[-1]
            d2 = dt2[0]
            dt2.append((d1+d2)%10)
            d4.append(dt2)
            dt = copy.copy(dt2)
        digits = self.getDigits(d4[-1])
        return (digits,d4)

if __name__ == '__main__':
    s = Secom('MAKE NEW FRIENDS BUT KEEP THE OLD')
        
                          
        
            
            
