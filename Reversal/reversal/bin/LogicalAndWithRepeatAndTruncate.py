__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class LogicalAndWithRepeatAndTruncate(Function):
    def __init__(self,parameter):
        self.parameter = ConvertAnything2BitArray(parameter)
        super(LogicalAndWithRepeatAndTruncate, self).__init__(self.logicaland_obverse, self.logicaland_reverse)
    def __repr__(self):
        return "{0}(x, t = {1})".format(self.__class__.__name__, self.parameter)
    def logicaland_obverse(self, input_value):
        # A logical AND operation only keeps those bits
        # that are equal to 1 in both parameters.
        # The only difficulty is to determine what to do
        # if the lengths in bits of the two parameters
        # are not equal.
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        output_value = input_cleanvalue & self.get_key_properlysized(len(input_cleanvalue))
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue, self, output_value))
        return output_value
        pass
    def logicaland_reverse(self, input_value):
        # We must find x such that x & key = input_value
        # Because AND only keeps bits that are 1 in both params,
        # we may return 0xffffff or input_value, both will do.
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        output_value = input_cleanvalue.copy()
        logger.debug("x = {0}, {1}ˉ¹ = {2}".format(input_cleanvalue, self, output_value))
        return output_value
        pass
    def get_key_properlysized(self, target_size):
        key_properlysized = self.parameter.copy()
        while(len(key_properlysized) < target_size):
            key_properlysized += self.parameter
        if(len(key_properlysized) > target_size):
            #Key must be truncated to match target
            key_properlysized = key_properlysized[0:target_size]
        return key_properlysized
        pass
