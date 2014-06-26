__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Add import Add
from Reversal.reversal.bin.Composite import Composite
from Reversal.reversal.bin.Multiply import Multiply


def test_composite():
    a_add = Add(32)
    b_multiply = Multiply(346)
    c_add = Add(17)
    d_multiply = Multiply(37)
    composite_a = Composite()
    composite_a.add_step(a_add)
    composite_a.add_step(b_multiply)
    composite_a.add_step(c_add)
    composite_a.add_step(d_multiply)
    original_value = 178
    logger.info("original_value = {0}".format(original_value))
    output_value = composite_a.execute_obverse(original_value)
    logger.info("output_value = {0}".format(output_value))
    equivalent_value = composite_a.execute_reverse(output_value)
    logger.info("equivalent_value = {0}".format(equivalent_value))

test_composite()

