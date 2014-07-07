__author__ = 'dmd'

from Reversal.reversal.GraphApproach.GraphApproach import *
import json

f = Call(label="f1")
f.set_logic(logic=LogicLibrary.get().get_logic(label=TypicalLabels.logic_add))
#f.get_data_inbound_surface().get_port(label=TypicalLabels.inbound_port_1).
print(f)
#print(repr(f))
#print(f.to_json_content())

