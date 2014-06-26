__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class LogicalBitShiftLeft(Function):
    def __init__(self, parameter):
        """
        In a logical shift, zeros are shifted in to replace the discarded bits.
        References:
        - http://en.wikipedia.org/wiki/Bitwise_operation

        :param parameter: the distance in bits for the shift, typically an int
        """
        self.parameter = parameter
        super(LogicalBitShiftLeft, self).__init__(self.logicalbitshiftleft_obverse, self.logicalbitshitleft_reverse)
        pass
    def __repr__(self):
        return "{0}(x, t = {1})".format(self.__class__.__name__, self.parameter)
        pass
    def logicalbitshiftleft_obverse(self, input_value):
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        # Rotates bits to the left and pad right with 0s
        pad = BitArray(length=self.parameter)
        slice = input_cleanvalue[self.parameter: len(input_cleanvalue):1]
        output_value = slice + pad
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue.bin, self, output_value.bin))
        return output_value
        pass
    def logicalbitshitleft_reverse(self, input_value):
        """
        In order to revert a bit left shit, x << y = z,
        we must perform a bit right shit x' = z >> y,
        and fill in the left margin bit with any values, such as 0s.
        :param input_value:
        :return:
        """
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        # Rotates bits to the right and pad left with 0s
        pad = BitArray(length=self.parameter)
        slice = input_cleanvalue[0: len(input_cleanvalue) - self.parameter:1]
        output_value = pad + slice
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue.bin, self, output_value.bin))
        return output_value
        pass

