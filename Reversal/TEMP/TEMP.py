__author__ = 'dmd'

import bitstring
from bitstring import BitArray, BitStream
from array import array

#x = "bonjour"
#print(x)
#print(bytes(x,encoding='ascii'))

import ipaddress

a = ipaddress.ip_address('192.168.53.12')
print(a)

b = int(a)
print(b)

c = bitstring.BitArray(uint=b,length=32)
print(c.bin)

d = ~c
print(d.bin)

