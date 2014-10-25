#!/usr/bin/env python

import random
import sys

def gcd(a,b):
    """Euclid's Algorithm"""
    while b:
        a, b = b, a % b
    return a 

def totient(n):
    """
    Compute the number of positives < n that are
    relatively prime to n -- good solution!
    """
    tot, pos = 0, n-1
    while pos>0:
        if gcd(pos,n)==1: tot += 1
        pos -= 1
    return tot



def primes(n,low=3): 
	if n==2: return [2]
	elif n<2: return []
	s=range(3,n+1,2)
	mroot = n ** 0.5
	half=(n+1)/2-1
	i=0
	m=3
	while m <= mroot:
		if s[i]:
			j=(m*m-3)/2
			s[j]=0
			while j<half:
				s[j]=0
				j+=m
		i=i+1
		m=2*i+3
	return [2]+[x for x in s if x]

def keygen():
    plist = primes(3000,low=1000)
    if len(plist) < 2:
        print 'List of primes is too short!'
        sys.exit(1)
        
    ip = random.randint(0,len(plist))
    iq = random.randint(0,len(plist))
    while iq == ip:
        iq = random.randint(0,len(plist))
    p = plist[ip]
    q = plist[iq]
    n = p*q
    totient = (p-1)*(q-1)
    
