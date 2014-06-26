__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.LogicalBitShiftLeft import LogicalBitShiftLeft

def TestLogicalBitShiftLeft():
    a_bitshiftleft = LogicalBitShiftLeft(15)
    original_inputvalue_raw = "Hellow world"
    original_inputvalue = ConvertAnything2BitArray(original_inputvalue_raw)
    logger.info("original_inputvalue = {0}".format(original_inputvalue.bin))
    original_outputvalue = a_bitshiftleft.execute_obverse(original_inputvalue)
    logger.info("original_outputvalue = {0}".format(original_outputvalue.bin))
    equivalent_inputvalue = a_bitshiftleft.execute_reverse(original_outputvalue)
    logger.info("equivalent_inputvalue = {0}".format(equivalent_inputvalue.bin))
    equivalent_outputvalue = a_bitshiftleft.function_obverse(equivalent_inputvalue)
    logger.info("equivalent_outputvalue = {0}".format(equivalent_outputvalue.bin))
    if original_outputvalue == equivalent_outputvalue:
        logger.info("PASS: original_outputvalue == equivalent_outputvalue")
    else:
        logger.info("FAIL: original_outputvalue != equivalent_outputvalue")
    pass

TestLogicalBitShiftLeft()