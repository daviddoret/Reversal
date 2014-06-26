__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.LogicalXorWithRepeatAndTruncate import LogicalXorWithRepeatAndTruncate

def TestLogicalXorWithRepeatAndTruncate():
    xor_a = LogicalXorWithRepeatAndTruncate("some key")
    original_inputvalue_raw = "the original text"
    original_inputvalue = ConvertAnything2BitArray(original_inputvalue_raw)
    logger.info("original_inputvalue = {0} ({1})".format(original_inputvalue,ConvertBitArray2ASCIIString(original_inputvalue)))
    original_outputvalue = xor_a.execute_obverse(original_inputvalue)
    logger.info("original_outputvalue = {0} ({1})".format(original_outputvalue,ConvertBitArray2ASCIIString(original_outputvalue)))
    equivalent_inputvalue = xor_a.execute_reverse(original_outputvalue)
    logger.info("equivalent_inputvalue = {0} ({1})".format(equivalent_inputvalue,ConvertBitArray2ASCIIString(equivalent_inputvalue)))
    equivalent_outputvalue = xor_a.function_obverse(equivalent_inputvalue)
    logger.info("equivalent_outputvalue = {0} ({1})".format(equivalent_outputvalue,ConvertBitArray2ASCIIString(equivalent_outputvalue)))
    if original_outputvalue == equivalent_outputvalue:
        logger.info("PASS: original_outputvalue == equivalent_outputvalue")
    else:
        logger.info("FAIL: original_outputvalue != equivalent_outputvalue")
    pass

TestLogicalXorWithRepeatAndTruncate()