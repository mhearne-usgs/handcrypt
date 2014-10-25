#!/usr/bin/env python
import sys
from optparse import OptionParser

class PiGenerator(object):
    digits = []
    dstring = ''
    def __init__(self,N):
        pigen = self.pi()
        self.digits = []
        for i in range(N):
            p = pigen.next() % 10
            self.digits.append(p)
            self.dstring = self.dstring + str(p)

    def pi(self):
        N = 0
        n, d = 0, 1
        while True:
            xn = (120*N**2 + 151*N + 47)
            xd = (512*N**4 + 1024*N**3 + 712*N**2 + 194*N + 15)
            n = ((16 * n * xd) + (xn * d)) % (d * xd)
            d *= xd
            yield 16 * n // d
            N += 1

if __name__ == "__main__":
    usage = "usage: %prog [options] N (integer number of random digits desired)"
    parser = OptionParser(usage=usage)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    try:
        N = int(args[0])
    except:
        print 'Input must be an integer.'
        parser.print_help()
        sys.exit(1)

    p = PiGenerator(N)
    for i in range(N):
        sys.stdout.write('%i' % p.digits[i])
    print
