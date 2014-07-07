__author__ = 'dmd'

from Reversal.reversal.GraphApproach.GraphApproach import *
import json

f = Call(label="f1")
f.get_data_inbound_surface().set_port(CallDataInboundPort(label="coucou"))



lib = LogicLibrary()

f.set_logic(lib.get_logic(TypicalLabels.logic_add))
#f.get_data_inbound_surface().set_port("a", 2)
#f.get_data_inbound_surface().set_port("b", 4)
# f.ex

print(f.to_json())