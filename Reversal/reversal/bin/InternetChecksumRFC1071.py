__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
from Reversal.reversal.bin.Function import Function

class InternetChecksumRFC1071(Function):
    def __init__(self):
        """
        References:
        - http://www.faqs.org/rfcs/rfc1071.html
        - http://codewiki.wikispaces.com/ip_checksum.py

        :param parameter: the distance in bits for the shift, typically an int
        """
        super(InternetChecksumRFC1071, self).__init__(self.internetchecksumrfc1071_obverse, self.internetchecksumrfc1071_reverse)
        pass
    def __repr__(self):
        return "{0}(x, t = {1})".format(self.__class__.__name__, self.parameter)
        pass
    def internetchecksumrfc1071_obverse(self, input_value):
        input_cleanvalue = ConvertAnything2BitArray(input_value)
        input_bytesvalue = input_cleanvalue.bytes
        pos = len(input_bytesvalue)
        if (pos & 1):  # If odd...
            pos -= 1
            sum = ord(input_bytesvalue[pos])  # Prime the sum with the odd end byte
        else:
            sum = 0
        #Main code: loop to calculate the checksum
        while pos > 0:
            pos -= 2
            sum += (ord(input_bytesvalue[pos + 1]) << 8) + ord(input_bytesvalue[pos])
        sum = (sum >> 16) + (sum & 0xffff)
        sum += (sum >> 16)
        output_bytesvalue = (~ sum) & 0xffff #Keep lower 16 bits
        output_bytesvalue = output_bytesvalue >> 8 | ((output_bytesvalue & 0xff) << 8)  # Swap bytes
        output_cleanvalue = BitArray(output_bytesvalue)
        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue.bin, self, output_cleanvalue.bin))
        return output_cleanvalue
        pass
    def internetchecksumrfc1071_reverse(self, input_value):
        """
        :param input_value:
        :return:
        """
        input_cleanvalue = ConvertAnything2BitArray(input_value)


        logger.debug("x = {0}, {1} = {2}".format(input_cleanvalue.bin, self, output_value.bin))
        return output_value
        pass



"""
def ip_checksum(data):  # Form the standard IP-suite checksum
  pos = len(data)
  if (pos & 1):  # If odd...
    pos -= 1
    sum = ord(data[pos])  # Prime the sum with the odd end byte
  else:
    sum = 0

  #Main code: loop to calculate the checksum
  while pos > 0:
    pos -= 2
    sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

  sum = (sum >> 16) + (sum & 0xffff)
  sum += (sum >> 16)

  result = (~ sum) & 0xffff #Keep lower 16 bits
  result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
  return result

References:
http://www.faqs.org/rfcs/rfc1071.html
http://codewiki.wikispaces.com/ip_checksum.py
"""