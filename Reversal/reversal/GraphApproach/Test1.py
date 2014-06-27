__author__ = 'dmd'

from Reversal.reversal.GraphApproach.GraphApproach import *
import json

f = Function(label="f1")
f.get_data_inbound_surface().add_port(FunctionDataInboundPort(label="coucou"))

print(f)
print(repr(f))
print(f.to_json_content())
