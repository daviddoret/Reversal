__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class Multiply(Function):
    def __init__(self, parameter):
        self.parameter = parameter
        super(Multiply, self).__init__(self.multiply_obverse, self.multiply_reverse)
    def __repr__(self):
        return "{0}(x, t = {1})".format(self.__class__.__name__, self.parameter)
    def multiply_obverse(self, input_value):
        output_value = input_value * self.parameter
        logger.debug("x = {0}, {1} = {2}".format(input_value, self, output_value))
        return output_value
        pass
    def multiply_reverse(self, input_value):
        output_value = input_value / self.parameter
        logger.debug("x = {0}, {1}ˉ¹ = {2}".format(input_value, self, output_value))
        return output_value
        pass
