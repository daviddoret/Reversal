__author__ = 'dmd'

from Reversal.reversal.GraphApproach.GraphApproach import *
import json

f1 = Call(label="Add 10")
f1.set_logic(logic=LogicLibrary.get().get_logic(label=TypicalLabels.logic_add))
#f.get_data_inbound_surface().get_port(label=TypicalLabels.inbound_port_1).
print(f1)

f2 = Call(label="Subtract 5")
f2.set_logic(logic=LogicLibrary.get().get_logic(label=TypicalLabels.logic_subtract))
print(f2)

#print(repr(f))
#print(f.to_json_content())

