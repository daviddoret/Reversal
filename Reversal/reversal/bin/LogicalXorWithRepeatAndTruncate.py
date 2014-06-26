__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class LogicalXorWithRepeatAndTruncate(Function):
    def __init__(self,parameter):
        self.parameter = ConvertAnything2BitArray(parameter)
        super(LogicalXorWithRepeatAndTruncate, self).__init__(self.xor_obverse,self.xor_reverse)
    def __repr__(self):
        return "{0}(x, t = {1})".format(self.__class__.__name__, self.parameter)
    def xor_obverse(self,input_value):
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        output_value = input_cleanvalue ^ self.get_key_properlysized(len(input_cleanvalue))
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue, self, output_value))
        return output_value
        pass
    def xor_reverse(self,input_value):
        # We must find x such that x^key = outputValue
        # --> x = outputValue ^ key
        input_valueclean = ConvertAnything2BitArray(input_value)
        output_value = input_valueclean ^ self.get_key_properlysized(len(input_valueclean))
        logger.debug("x = {0}, {1}ˉ¹ = {2}".format(input_valueclean, self, output_value))
        return output_value
        pass
    def get_key_properlysized(self, target_size):
        keyProperlySized = self.parameter.copy()
        while(len(keyProperlySized) < target_size):
            keyProperlySized += self.parameter
        if(len(keyProperlySized) > target_size):
            #Key must be truncated to match target
            keyProperlySized = keyProperlySized[0:target_size]
        return keyProperlySized
        pass
