__author__ = 'dmd'

import sys
import bitstring
from bitstring import BitArray, BitStream
from array import array
import logging
import ipaddress

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def ConvertAnything2BitArray(anything):
    if(isinstance(anything, str)):
        #TODO: CHECK ENCODING
        return ConvertAnything2BitArray(bytes(anything, encoding='ascii'))
        pass
    elif(isinstance(anything, int)):
        return BitArray(anything)
        pass
    elif(isinstance(anything, bytes)):
        return BitArray(anything)
        pass
    elif(isinstance(anything, BitArray)):
        return anything
        pass
    elif(isinstance(anything, ipaddress.IPv4Address)):
        return BitArray(int(anything))
        pass
    pass

def ConvertBitArray2ASCIIString(anything):
    return str(ConvertBitArray2Bytes(anything), encoding = 'ascii')

def ConvertASCIIString2BitString(anything):
    return ConvertAnything2BitArray(anything).bin

def ConvertBitArray2Bytes(anything):
    return anything.bytes