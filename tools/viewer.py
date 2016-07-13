from __future__ import print_function

#
# viewer
# Simple hex viewer
# (c) 2016 Luke Donovan
#
# Usage: "python viewer.py file"
# "file" can be any file
#

import binascii
import sys

yellow = '\033[1;33m'
reset = '\033[0m'

with open(sys.argv[1], 'rb') as f:
    data = f.read()
data = binascii.hexlify(data)
data = [data[i:i+2] for i in range(0, len(data), 2)]

try:
    w = int(sys.argv[2])
    n = int(sys.argv[3])
except:
    w = 3 # width
    n = 5 # number of columns

c = 1
for i in range(0, len(data)):
    if (c == w * n + 1):
        uni = ''.join([unichr(int(c, 16)) for c in data[i-(w*n):i]]).replace('\n', yellow+u'\u2424'+reset)
        print('| '+uni)
        c = 1
    elif (i == len(data) - 1):
        spaces = (n * w * 2 + n) - (2 * c) - (c / w)
        uni = ''.join([unichr(int(c, 16)) for c in data[i-c+1:]]).replace('\n', yellow+u'\u2424'+reset)
        print(data[i] + ' '*spaces + '| ' + uni)
        break
    print(data[i], end='')
    if (c % w == 0): print(end=' ')
    c += 1
