__author__ = 'dmd'

from Reversal.reversal.bin.utils import *
import json
import uuid
import collections # Makes it possible to perform: if isinstance(e, collections.Iterable):
from enum import Enum


class DataObject(object):
    """
    A super base class that inherits from object,
    in such a way as to implement the diamond rule
    in the presence of multiple inheritance
    """

    #class initialization
    _database = {}

    def __init__(self, uid=None, label=None, container=None):
        #Base classes initialization
        object.__init__(self)
        self.uid = uuid.uuid4()
        self._container = None
        self._label = None
        DataObject._database[self.uid] = self
        #Initialize pseudo-private members
        #Call set methods to comply with their logic
        self._set_container(container=container)
        self.set_label(label=label)

    def __repr__(self):
        return self.to_json()

    def __hash__(self):
        return self.uid

    def __eq__(self, other):
        if isinstance(other, DataObject):
            if self.uid == other.uid:
                return True
            else:
                return False
        else:
            return False

    def __ne__(self, other):
        return not(self == other)

    def _set_uid(self, uid):
        """
        The set uid method is pseudo private to avoid messing around with objects.
        Its only use cases are object initialization and deserialization.
        :param uid:
        """
        if self.uid != None:
            # If the object had a uid before, we should implement some magic here to ensure
            # all references are made to the new uid instead. We may decide to keep the old
            # uid as a "redirected" reference.
            DataObject._database.pop(uid)
        self.uid = uid
        DataObject._database[uid] = self

    def _set_uid_auto(self):
        uid = uuid.uuid4()
        self._set_uid(uid)

    def get_uid(self):
        return self.uid

    def get_object(cls, key):
        return DataObject._database[key]

    def get_container(self):
        return self._container

    def _set_container(self, container):
        """
        The set container method is pseudo-private because it is the responsibility
        of the container object only to call it to assign ownership. Hence, it shall
        never be called directly, otherwise the consistency of hierarchical relationships
        may be broken.
        :param container:
        """
        self._container = container

    #def to_json_content(self, depth=0):
    #    """
    #    Returns the content of the JSON object, i.e. without the brackets {}.
    #    This is useful when you want to concatenate content from multiple super classes.
    #    """
    #    pass

    #def to_json(self, depth=0):
    #    """
    #    Returns the complete JSON object, i.e. with the brackets {}.
    #    """
    #    return '\n{0}{{{1}\n{2}}}'.format(' ' * depth, self.to_json_content(depth=depth + 1), ' ' * depth)
    #    #return json.dumps('{{{0}}}'.format(self.to_json_content()), indent=4, sort_keys=True)

    def to_json(self, depth=0, prevent_infinite_loop_list=None):
        return "\n{0}{{{1}\n{0}}}".format(" " * depth, self.to_json_content(depth=depth, prevent_infinite_loop_list=prevent_infinite_loop_list))

    def to_json_content(self, depth=0, prevent_infinite_loop_list={}):
        # QUESTION: Consider using __hash__ instead of get_uid in such a way to cover all objects
        if prevent_infinite_loop_list == None:
            prevent_infinite_loop_list = {}
        prevent_infinite_loop_list.update(self._get_references_direct())
        json = '\n{0}"class":"{1}"'.format(" " * depth, self.__class__.__name__)
        for key in self.__dict__:
            if key not in prevent_infinite_loop_list:
                if isinstance(self.__dict__[key], DataObject):
                    if self.__dict__[key].get_uid() in prevent_infinite_loop_list:
                        # This object was already or will be serialized as part of a parent object,
                        # in conclusion we must only serialize it as a reference.
                        json += '\n{0}"{{reference":{{"class":"{1}","label":"{2}","uid":"{3}"}}'.format(" " * (depth + 1),  self.__dict__[key].__class__.__name__,  self.__dict__[key].get_label(),  self.__dict__[key].get_uid())
                    else:
                        # Otherwise we can perform a deep serialization.
                        json += '\n{0}"{1}":{2}'.format(" " * depth, key, self.__dict__[key].to_json(depth=depth + 1, prevent_infinite_loop_list=prevent_infinite_loop_list))
                else:
                    json += '\n{0}"{1}":"{2}"'.format(" " * depth, key, str(self.__dict__[key]))
        return json

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def _get_references_direct(self):
        references_direct = {}
        for key in self.__dict__:
            if isinstance(self.__dict__[key], DataObject):
                # If a reference
                references_direct[self.__dict__[key].get_uid()] = self.__dict__[key]
            elif isinstance(self.__dict__[key], dict):
                for sub_key in self.__dict__[key]:
                    if isinstance(self.__dict__[key][sub_key], DataObject):
                        # If a reference
                        references_direct[self.__dict__[key][sub_key].get_uid()] = self.__dict__[key][sub_key]
        return references_direct


class Call(DataObject):

    def __init__(self, label=None, logic=None):
        #Base classes initialization
        DataObject.__init__(self, label=label)
        #Initialize pseudo-private members
        self._data_inbound_surface = None
        self._data_midbound_surface = None
        self._data_outbound_surface = None
        self._execution_inbound_surface = None
        self._execution_outbound_surface = None
        self._logic = None
        #Call set methods to comply with their logic
        self._set_data_inbound_surface(data_inbound_surface=CallDataInboundSurface())
        self._set_data_midbound_surface(data_midbound_surface=CallDataMidboundSurface())
        self._set_data_outbound_surface(data_outbound_surface=CallDataOutboundSurface())
        self._set_execution_inbound_surface(execution_inbound_surface=CallExecutionInboundSurface())
        self._set_execution_outbound_surface(execution_outbound_surface=CallExecutionOutboundSurface())
        self.set_logic(logic)

    def get_data_inbound_surface(self):
        return self._data_inbound_surface

    def _set_data_inbound_surface(self, data_inbound_surface):
        data_inbound_surface._set_container(self)
        self._data_inbound_surface = data_inbound_surface

    def get_data_midbound_surface(self):
        return self._data_midbound_surface

    def _set_data_midbound_surface(self, data_midbound_surface):
        data_midbound_surface._set_container(self)
        self._data_midbound_surface = data_midbound_surface

    def get_data_outbound_surface(self):
        return self._data_outbound_surface

    def _set_data_outbound_surface(self, data_outbound_surface):
        data_outbound_surface._set_container(self)
        self._data_outbound_surface = data_outbound_surface

    def get_execution_inbound_surface(self):
        return self._execution_inbound_surface

    def _set_execution_inbound_surface(self, execution_inbound_surface):
        execution_inbound_surface._set_container(self)
        self._execution_inbound_surface = execution_inbound_surface

    def get_execution_outbound_surface(self):
        return self._execution_outbound_surface

    def _set_execution_outbound_surface(self, execution_outbound_surface):
        execution_outbound_surface._set_container(self)
        self._execution_outbound_surface = execution_outbound_surface

    def get_logic(self):
        return self._logic

    def set_logic(self, logic):
        # Clean inbound ports
        # Clean midbound ports
        # Clean outbound ports
        self._logic = logic
        # Configure outbound ports
        # Configure midbound ports
        # Configure inbound ports


class Logic(DataObject):
    """
    A logic component is always able to implement a forward execution
    on its parent call.
    A logic component should be able to find ways to implement a
    backward execution on its parent call.
    A logic component defines a template of inbound, midbound and outbound ports.
    These ports will be copied to the call component where the logic will be executed.
    """
    def __init__(self, container=None, label=None, execute_forward=None, execute_backward=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self.execute_forward = execute_forward
        self.execute_backward = execute_backward
        self._data_inbound_surface = None
        self._data_midbound_surface = None
        self._data_outbound_surface = None
        #Call set methods to comply with their logic
        self._set_data_inbound_surface(data_inbound_surface=CallDataInboundSurface())
        self._set_data_midbound_surface(data_midbound_surface=CallDataMidboundSurface())
        self._set_data_outbound_surface(data_outbound_surface=CallDataOutboundSurface())

    def execute_forward(self):
        pass

    def execute_backward(self):
        pass

    def get_reverse(self, label=None):
        return Logic(container=self.get_container(), label=label, execute_forward=self.execute_backward, execute_backward=self.execute_forward)

    def get_data_inbound_surface(self):
        return self._data_inbound_surface

    def _set_data_inbound_surface(self, data_inbound_surface):
        data_inbound_surface._set_container(self)
        self._data_inbound_surface = data_inbound_surface

    def get_data_midbound_surface(self):
        return self._data_midbound_surface

    def _set_data_midbound_surface(self, data_midbound_surface):
        data_midbound_surface._set_container(self)
        self._data_midbound_surface = data_midbound_surface

    def get_data_outbound_surface(self):
        return self._data_outbound_surface

    def _set_data_outbound_surface(self, data_outbound_surface):
        data_outbound_surface._set_container(self)
        self._data_outbound_surface = data_outbound_surface


class LogicLibrary(DataObject):
    """
    """
    def __init__(self):
        self._library = {}
        add = Logic(container=None, label=TypicalLabels.logic_add, execute_forward=self._add, execute_backward=self._subtract)
        add.get_data_inbound_surface().set_port(CallDataInboundPort(container=self, XXX))
        self.set_logic(add)
        subtract = add.get_reverse(label=TypicalLabels.logic_subtract)
        self.set_logic(subtract)

    def _add(self, call):
        x = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_1)
        y = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_2)
        z = x + y
        call.get_data_outbound_surface().set_port(TypicalLabels.outbound_port_1)

    def _subtract(self, call):
        x = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_1)
        y = call.get_data_inbound_surface().get_port(TypicalLabels.inbound_port_2)
        z = x - y
        call.get_data_outbound_surface().set_port(TypicalLabels.outbound_port_1)

    def get_logic(self, label=None):
        return self._library[label]

    def set_logic(self, logic):
        # Clean all inbound ports
        # Clean all midbound ports
        # Clean all outbound ports
        self._library[logic.get_label()] = logic
        #TODO: ADD AUTO GENERATION OF PORTS


class TypicalLabels(Enum):
    logic_add = "logic_add"
    logic_subtract = "logic_subtract"
    inbound_port_1 = "a"
    inbound_port_2 = "b"
    inbound_port_3 = "c"
    outbound_port_1 = "x"


class CallDataInboundSurface(DataObject):

    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._data_inbound_ports = {}

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._data_inbound_ports)

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


class CallDataMidboundSurface(DataObject):

    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._data_midbound_ports = {}

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._data_midbound_ports)

    def set_port(self, data_midbound_port):
        #Assign the proper container object
        data_midbound_port._set_container(self)
        if data_midbound_port.get_label() in self._data_midbound_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._data_midbound_ports.pop(key=data_midbound_port.get_label())
        self._data_midbound_ports[data_midbound_port.get_label()] = data_midbound_port

    def get_port(self, label):
        if label in self._data_midbound_ports:
            return self._data_midbound_ports(label)
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataMidboundPort(label=label)
            self.set_port(new_port)
            return new_port


class CallDataMidboundPort(DataObject):

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
        self._data_outbound_ports[data_outbound_port.label] = data_outbound_port

    def get_port(self, label=None):
        if label in self._data_outbound_ports:
            return self._data_outbound_ports[label]
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataOutboundPort(label=label)
            self.set_port(new_port)
            return new_port


class CallDataOutboundPort(DataObject):

    def __init__(self, container=None, label=None, linked_variable=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._linked_variable = None
        #Call set methods to comply with their logic
        self.set__linked_variable(linked_variable=linked_variable)

    def __repr__(self):
        return "{0}({1},LinkedVariable({2}))".format(self.__class__.__name__, super(Labelled, self), self._linked_variable.get_label())

    def get_linked_variable(self):
        return self._linked_variable

    def set_linked_variable(self, linked_variable):
        self._linked_variable = linked_variable


class CallExecutionInboundSurface(DataObject):

    def __init__(self, container=None):
        #Base classes initialization
        DataObject.__init__(self, container=container)
        #Initialize pseudo-private members
        self._exec_inbound_ports = {}

    def add_port(self, exec_inbound_port):
        #Assign the proper container object
        exec_inbound_port._set_container(self)
        if exec_inbound_port.get_label() in self._exec_inbound_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._exec_inbound_ports.pop(key=exec_inbound_port.get_label())
        self._exec_inbound_ports[exec_inbound_port.label] = exec_inbound_port

    def get_port(self, label):
        if label in self._exec_inbound_ports:
            return self._exec_inbound_ports(label)
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataInboundPort(container_surface=self, label=label)
            self.add_port(new_port)
            return new_port

class CallExecutionInboundPort(DataObject):

    def __init__(self, container, label):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Pseudo-private members
        #Public members


class CallExecutionOutboundSurface(DataObject):

    def __init__(self, container=None):
        #Base classes initialization
        DataObject.__init__(self, container=container)
        #Initialize pseudo-private members
        self._exec_outbound_ports = {}

    def add_port(self, exec_outbound_port):
        #Assign the proper container object
        exec_outbound_port._set_container(self)
        if exec_outbound_port.get_label() in self._exec_outbound_ports:
            # A port with this label exists already,
            # remove it automatically.
            self._exec_outbound_ports.pop(key=exec_outbound_port.get_label())
        self._exec_outbound_ports[exec_outbound_port.label] = exec_outbound_port

    def get_port(self, label):
        if label in self._exec_outbound_ports:
            return self._exec_outbound_ports(label)
        else:
            # Instead of throwing exceptions, dynamically create a new unlinked port
            new_port = CallDataInboundPort(container_surface=self, label=label)
            self.add_port(new_port)
            return new_port

class CallExecOutboundPort(DataObject):

    def __init__(self, container,label):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Pseudo-private members
        #Public members


class DataVariable(DataObject):

    def __init__(self):
        pass


class DataSurface(DataObject):

    def __init__(self):
        pass


class CallComposite(DataObject):
    #TODO: Inherit from Call in such a way as to make Algorithms callable
    def __init__(self, start_call, end_call):
        self._start_call = start_call
        self._end_call = end_call

    def start(self):
        self._start_call.execute_forward()


class CallExecutionTrace(DataObject):

    def __init__(self):
        pass


class CallExecutionTraceForward(CallExecutionTrace):

    def __init__(self):
        pass


class CallExecutionTraceBackward(CallExecutionTrace):
    """
    A backward execution trace is distinct from a forward exec trace
    because it informs us on one possible pass amongst multiple
    possible execuction pathes.
    """
    def __init__(self):
        pass

class Runtime(DataObject):

    def __init__(self):
        #Base classes initialization
        DataObject.__init__(self, container=None, label="Runtime")
        #Pseudo-private members
        #Public members
