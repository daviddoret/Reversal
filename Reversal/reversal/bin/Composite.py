__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class Composite(Function):
    def __init__(self):
        self.steps = []
        super(Composite, self).__init__(self.composite_obverse, self.composite_reverse)
        pass
    def __repr__(self):
        return "{0}(x, f1°f2°fn... = {1})".format(self.__class__.__name__, self.steps)
    def composite_obverse(self, input_value):
        output_value = input_value
        for step in self.steps:
            output_value = step.execute_obverse(output_value)
        logger.debug("x = {0}, {1} = {2}".format(input_value, self, output_value))
        return output_value
        pass
    def composite_reverse(self, input_value):
        output_value = input_value
        for step in reversed(self.steps):
            output_value = step.execute_reverse(output_value)
        logger.debug("x = {0}, {1} = {2}".format(input_value, self, output_value))
        return output_value
        pass
    def add_step(self, step):
        self.steps.append(step)
        pass