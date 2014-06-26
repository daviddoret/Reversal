__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class LogicalNot(Function):
    def __init__(self):
        super(LogicalNot, self).__init__(self.logicalnot_obverse, self.logicalbitshitleft_reverse)
        pass
    def __repr__(self):
        return "{0}(x)".format(self.__class__.__name__)
        pass
    def logicalnot_obverse(self, input_value):
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        output_value = ~input_cleanvalue
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue, self, output_value))
        return output_value
        pass
    def logicalbitshitleft_reverse(self, input_value):
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        output_value = ~input_cleanvalue
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue, self, output_value))
        return output_value
        pass

