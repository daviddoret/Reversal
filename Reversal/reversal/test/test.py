from Reversal.reversal.bin import Multiply, Add, LRC_ISO1105, LogicalXorWithRepeatAndTruncate, Composite

__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Add import Add
from Reversal.reversal.bin.Multiply import Multiply
from Reversal.reversal.bin.Composite import Composite
from Reversal.reversal.bin.LogicalXorWithRepeatAndTruncate import LogicalXorWithRepeatAndTruncate

def Test1():
    m10 = Multiply(10)
    x = 178
    print(x)
    y = m10.ExecuteObverse(x)
    print(y)
    z = m10.ExecuteReverse(y)
    print(z)



def Test3():
    x = "bonjour"
    print(x)
    print(ConvertASCIIString2BitString(x))
    xor = LogicalXorWithRepeatAndTruncate("salut les amis")
    y = xor.ExecuteObverse(x)
    print(y.bin)
    z = xor.ExecuteReverse(y)
    print(z.bin)
    print(ConvertBitArray2ASCIIString(z))
    pass

def Test4():
    x = "bonjour"
    lrc = LRC_ISO1105()
    pass

#Test1()
#Test2()
Test3()