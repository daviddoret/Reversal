__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class LRC_ISO1105():
    def __init__(self,keyObverse):
        self.keyObverse = ConvertAnything2BitArray(keyObverse)
        super(LRC_ISO1105, self).__init__(self.lrc_obverse, self.lrc_reverse)
    def lrc_obverse(self,inputValue):
        #Pseudocode:
        #Set LRC = 0
        #For each byte b in the buffer
        #do
        #   Set LRC = (LRC + b) AND 0xFF
        #end do
        #Set LRC = (((LRC XOR 0xFF) + 1) AND 0xFF)
        #Reference: http://en.wikipedia.org/wiki/Longitudinal_redundancy_check
        lrc = 0
        for byte in inputValue.bytes:
            lrc = (lrc + byte) & 0xff
        lrc = (((lrc ^ 0xff) + 1) & 0xff)
        return lrc
        pass
    def lrc_reverse(self,outputValue):
        # Resolve it to a single byte b
        # For a single byte, the obverse function would be:
        # ((b & 0xff) ^ 0xff) + 1 & 0xff
        # Hence the reverse would be:


        pass
