__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Multiply import Multiply


def TestMultiply():
    multiply_a = Multiply(642)
    original_inputvalue = 178
    logger.info("original_inputvalue = {0}".format(original_inputvalue))
    original_outputvalue = multiply_a.execute_obverse(original_inputvalue)
    logger.info("original_outputvalue = {0}".format(original_outputvalue))
    equivalent_inputvalue = multiply_a.execute_reverse(original_outputvalue)
    logger.info("equivalent_inputvalue = {0}".format(equivalent_inputvalue))
    equivalent_outputvalue = multiply_a.execute_obverse(equivalent_inputvalue)
    logger.info("equivalent_outputvalue = {0}".format(equivalent_outputvalue))
    if original_outputvalue == equivalent_outputvalue:
        logger.info("PASS: output_value == equivalent_output_value")
    else:
        logger.info("FAIL: output_value != equivalent_output_value")
    pass

TestMultiply()