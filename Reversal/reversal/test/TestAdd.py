__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Add import Add


def test_add():
    multiply_a = Add(72831)
    original_value = 34912
    logger.info("original_value = {0}".format(original_value))
    output_value = multiply_a.execute_obverse(original_value)
    logger.info("output_value = {0}".format(output_value))
    equivalent_value = multiply_a.execute_reverse(output_value)
    logger.info("equivalent_value = {0}".format(equivalent_value))

test_add()