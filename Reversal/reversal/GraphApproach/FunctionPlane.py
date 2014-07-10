__author__ = 'dmd'

# from Reversal.reversal.bin.utils import *
import json
import uuid
import collections # Makes it possible to perform: if isinstance(e, collections.Iterable):
from enum import Enum
from Reversal.reversal.GraphApproach.Lib import *
from Reversal.reversal.GraphApproach.Runtime import *
from Reversal.reversal.GraphApproach.DataPlane import *
from Reversal.reversal.GraphApproach.ExecutionPlane import *
from Reversal.reversal.GraphApproach.FunctionPlane import *


class Call(DataObject):

    # TODO: Consider simplifying the implementation by not using dedicated classes for collection,
    # instead, it should be possible to expose get_iterator methods, such as get_inbound_ports_iterator.

    def __init__(self, label=None, logic=None):
        #Base classes initialization
        DataObject.__init__(self, label=label)
        #Initialize pseudo-private members
        self._data_inbound_surface = None
        self._data_private_surface = None
        self._data_outbound_surface = None
        self._logic = None
        #Call set methods to comply with their logic
        self._set_data_inbound_surface(data_inbound_surface=CallDataInboundSurface())
        self._set_data_private_surface(data_private_surface=CallDataPrivateSurface())
        self._set_data_outbound_surface(data_outbound_surface=CallDataOutboundSurface())
        self.set_logic(logic=LogicLibrary.get().get_logic(TypicalLabels.logic_do_nothing))

    def get_data_inbound_surface(self):
        return self._data_inbound_surface

    def _set_data_inbound_surface(self, data_inbound_surface):
        if not (isinstance(data_inbound_surface, CallDataInboundSurface)):
            raise Error(container=None, label=None, level=ErrorLevel.execution_stop, caller_object=self, data_inbound_surface=data_inbound_surface)
        data_inbound_surface._set_container(self)
        self._data_inbound_surface = data_inbound_surface

    def get_data_private_surface(self):
        return self._data_private_surface

    def _set_data_private_surface(self, data_private_surface):
        data_private_surface._set_container(self)
        self._data_private_surface = data_private_surface

    def get_data_outbound_surface(self):
        return self._data_outbound_surface

    def _set_data_outbound_surface(self, data_outbound_surface):
        data_outbound_surface._set_container(self)
        self._data_outbound_surface = data_outbound_surface

    def get_logic(self):
        return self._logic

    def set_logic(self, logic):
        # Clean inbound ports
        self.get_data_inbound_surface().reinitialize()
        # Clean private ports
        self.get_data_private_surface().reinitialize()
        # Clean outbound ports
        self.get_data_outbound_surface().reinitialize()
        # Attach the logic to the call
        self._logic = logic
        # Configure inbound ports
        for label, data_inbound_port in self.get_logic().get_data_inbound_surface().get_ports().items():
            label = data_inbound_port.get_label()
            data_inbound_port = CallDataInboundPort(container=None, label=label)
            self.get_data_inbound_surface().set_port(data_inbound_port)
        # Configure private ports
        for label, data_private_port in self.get_logic().get_data_private_surface().get_ports().items():
            label = data_private_port.get_label()
            data_private_port = CallDataPrivatePort(container=None, label=label)
            self.get_data_private_surface().set_port(data_private_port)
        # Configure outbound ports
        for label, data_outbound_port in self.get_logic().get_data_outbound_surface().get_ports().items():
            label = data_outbound_port.get_label()
            data_outbound_port = CallDataOutboundPort(container=None, label=label)
            self.get_data_outbound_surface().set_port(data_outbound_port)

    def get_logic(self):
        return self._logic


class Logic(DataObject):
    """
    A logic component is always able to implement a forward execution
    on its parent call.
    A logic component should be able to find ways to implement a
    backward execution on its parent call.
    A logic component defines a template of inbound, private and outbound ports.
    These ports will be copied to the call component where the logic will be executed.
    """
    def __init__(self, container=None, label=None, execute_forward=None, execute_backward=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self.execute_forward = execute_forward
        self.execute_backward = execute_backward
        self._data_inbound_surface = None
        self._data_private_surface = None
        self._data_outbound_surface = None
        #Call set methods to comply with their logic
        self._set_data_inbound_surface(data_inbound_surface=CallDataInboundSurface())
        self._set_data_private_surface(data_private_surface=CallDataPrivateSurface())
        self._set_data_outbound_surface(data_outbound_surface=CallDataOutboundSurface())

    def execute_forward(self):
        pass

    def execute_backward(self):
        pass

    def get_reverse(self, label=None):
        return Logic(container=self.get_container(), \
                     label=label, \
                     execute_forward=self.execute_backward, \
                     execute_backward=self.execute_forward)

    def get_data_inbound_surface(self):
        return self._data_inbound_surface

    def _set_data_inbound_surface(self, data_inbound_surface):
        data_inbound_surface._set_container(self)
        self._data_inbound_surface = data_inbound_surface

    def get_data_private_surface(self):
        return self._data_private_surface

    def _set_data_private_surface(self, data_private_surface):
        data_private_surface._set_container(self)
        self._data_private_surface = data_private_surface

    def get_data_outbound_surface(self):
        return self._data_outbound_surface

    def _set_data_outbound_surface(self, data_outbound_surface):
        data_outbound_surface._set_container(self)
        self._data_outbound_surface = data_outbound_surface


class LogicLibrary(DataObject):
    """
    """

    _lib = None

    def __init__(self):
        self._library = {}
        do_nothing = Logic(container=None, \
                    label=TypicalLabels.logic_do_nothing, \
                    execute_forward=self._do_nothing, \
                    execute_backward=self._do_nothing)
        self.set_logic(do_nothing)
        add = Logic(container=None, \
                    label=TypicalLabels.logic_add, \
                    execute_forward=self._add, \
                    execute_backward=self._subtract)
        add.get_data_inbound_surface().set_port(CallDataInboundPort(container=None, \
                                                                    label=TypicalLabels.inbound_port_1))
        add.get_data_inbound_surface().set_port(CallDataInboundPort(container=None, \
                                                                    label=TypicalLabels.inbound_port_2))
        add.get_data_outbound_surface().set_port(CallDataOutboundPort(container=None, \
                                                                      label=TypicalLabels.outbound_port_1))
        self.set_logic(add)
        subtract = add.get_reverse(label=TypicalLabels.logic_subtract)
        self.set_logic(subtract)

    @classmethod
    def get(cls):
        if LogicLibrary._lib is None:
            LogicLibrary._lib = LogicLibrary()
        return(LogicLibrary._lib)

    def _do_nothing(self, call):
        pass

    def _add(self, call):
        x = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_1).get_linked_value().get_value()
        y = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_2).get_linked_value().get_value()
        z = x + y
        call.get_data_outbound_surface().get_port(TypicalLabels.outbound_port_1).get_linked_value().set_value(value=z)

    def _subtract(self, call):
        x = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_1).get_linked_value().get_value()
        y = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_2).get_linked_value().get_value()
        z = x - y
        call.get_data_outbound_surface().get_port(TypicalLabels.outbound_port_1).get_linked_value().set_value(value=z)

    def get_logic(self, label=None):
        return self._library[label]

    def set_logic(self, logic):
        # Clean all inbound ports
        # Clean all private ports
        # Clean all outbound ports
        self._library[logic.get_label()] = logic


class TypicalLabels(Enum):
    logic_add = "logic_add"
    logic_do_nothing = "logic_do_nothing"
    logic_subtract = "logic_subtract"
    inbound_port_1 = "a"
    inbound_port_2 = "b"
    inbound_port_3 = "c"
    outbound_port_1 = "x"
    outbound_port_2 = "y"
    outbound_port_3 = "z"


class CallDataInboundSurface(DataObject):

    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        self._data_inbound_ports = {}

    #def __repr__(self):
    #    return "{0}({1})".format(self.__class__.__name__, self._data_inbound_ports)

    def reinitialize(self):
        #Initialize pseudo-private members
        self._data_inbound_ports = {}

    def set_port(self, data_inbound_port):
        #Assign the proper container object
        data_inbound_port._set_container(self)
        if data_inbound_port.get_label() in self._data_inbound_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._data_inbound_ports.pop(key=data_inbound_port.get_label())
        self._data_inbound_ports[data_inbound_port.get_label()] = data_inbound_port

    def get_port(self, label):
        if label in self._data_inbound_ports:
            return self._data_inbound_ports(label)
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataInboundPort(label=label)
            self.set_port(new_port)
            return new_port

    def get_ports(self):
        return self._data_inbound_ports


class CallDataPrivateSurface(DataObject):

    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._data_private_ports = {}

    #def __repr__(self):
    #    return "{0}({1})".format(self.__class__.__name__, self._data_private_ports)

    def reinitialize(self):
        #Initialize pseudo-private members
        self._data_private_ports = {}

    def set_port(self, data_private_port):
        #Assign the proper container object
        data_private_port._set_container(self)
        if data_private_port.get_label() in self._data_private_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._data_private_ports.pop(key=data_private_port.get_label())
        self._data_private_ports[data_private_port.get_label()] = data_private_port

    def get_port(self, label):
        if label in self._data_private_ports:
            return self._data_private_ports(label)
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataPrivatePort(label=label)
            self.set_port(new_port)
            return new_port

    def get_ports(self):
        return self._data_private_ports


class CallDataPrivatePort(DataObject):

    def __init__(self, container=None, label=None, linked_variable=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._linked_variable = None
        #Call set methods to comply with their logic
        self.set_linked_variable(linked_variable=linked_variable)

    def get_linked_variable(self):
        return self._linked_variable

    def set_linked_variable(self, linked_variable):
        self._linked_variable = linked_variable


class CallDataInboundPort(DataObject):

    def __init__(self, container=None, label=None, linked_variable=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._linked_variable = None
        #Call set methods to comply with their logic
        if linked_variable is None:
            linked_variable = DataVariable(container=self)
        self.set_linked_variable(linked_variable=linked_variable)

    def get_linked_variable(self):
        return self._linked_variable

    def set_linked_variable(self, linked_variable):
        self._linked_variable = linked_variable


class CallDataOutboundSurface(DataObject):

    def __init__(self, container=None):
        #Base classes initialization
        DataObject.__init__(self, container=container)
        #Initialize pseudo-private members
        self._data_outbound_ports = {}

    def reinitialize(self):
        #Initialize pseudo-private members
        self._data_outbound_ports = {}

    def set_port(self, data_outbound_port=None):
        #If a pre-configured port is not provided, create one out of the blue.
        if data_outbound_port == None:
            data_outbound_port = CallDataOutboundPort()
        #Assign the proper container object
        data_outbound_port._set_container(container=self)
        if data_outbound_port.get_label() in self._data_outbound_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._data_outbound_ports.pop(key=data_outbound_port.get_label())
        self._data_outbound_ports[data_outbound_port.get_label()] = data_outbound_port

    def get_port(self, label=None):
        if label in self._data_outbound_ports:
            return self._data_outbound_ports[label]
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataOutboundPort(label=label)
            self.set_port(new_port)
            return new_port

    def get_ports(self):
        return self._data_outbound_ports


class CallDataOutboundPort(DataObject):

    def __init__(self, container=None, label=None, linked_variable=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._linked_variable = None
        #Call set methods to comply with their logic
        if linked_variable is None:
            linked_variable = DataVariable(container=self)
        self.set_linked_variable(linked_variable=linked_variable)

    #def __repr__(self):
    #    return "{0}({1},LinkedVariable({2}))".format(self.__class__.__name__, super(Labelled, self), self._linked_variable.get_label())

    def get_linked_variable(self):
        return self._linked_variable

    def set_linked_variable(self, linked_variable):
        # TODO: Check point: variable must not be contained by port, it must be rather owned by the bigger parent environment
        self._linked_variable = linked_variable


