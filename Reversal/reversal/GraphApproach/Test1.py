__author__ = 'dmd'

from Reversal.reversal.GraphApproach.GraphApproach import *
import json

f = Call(label="f1")
f.get_data_inbound_surface().add_port(CallDataInboundPort(label="coucou"))

#print(f)
#print(repr(f))
print(f.to_json())
