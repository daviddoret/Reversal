__author__ = 'dmd'


from Reversal.reversal.GraphApproach.Lib import *
from Reversal.reversal.GraphApproach.DataPlane import *
from Reversal.reversal.GraphApproach.ExecutionPlane import *
from Reversal.reversal.GraphApproach.FunctionPlane import *
from Reversal.reversal.GraphApproach.Runtime import *


class ExecutionGraph(DataObject):
    """
    ...
    """
    def __init__(self, container=None, label=None, logic=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        # INBOUND PORTS
        # OUTBOUND PORTS
        self._start = None
        self._end = None
        self._execution_inbound_surface = None
        self._execution_outbound_surface = None
        #Call set methods to comply with their logic
        self._set_execution_inbound_surface(execution_inbound_surface=CallExecutionInboundSurface())
        self._set_execution_outbound_surface(execution_outbound_surface=CallExecutionOutboundSurface())

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


class Task(DataObject):
    """
    ...
    """
    def __init__(self):
        pass


class ExecuteFunction(Task):
    """
    ...
    """
    def __init__(self):
        pass


class Condition(Task):
    """
    ...
    """
    def __init__(self):
        pass


class Start(Task):
    """
    ...
    """
    def __init__(self):
        pass


class End(Task):
    """
    ...
    """
    def __init__(self):
        pass


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
            new_port = CallDataOutboundPort(container_surface=self, label=label)
            self.add_port(new_port)
            return new_port


class CallExecutionOutboundPort(DataObject):

    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Pseudo-private members
        #Public members


class CallComposite(Call):
    """
    A composite call is a call that contains a collection of calls
    and that maps them together with an execution graph.
    This inheritance makes it easy to set inbound ports and retrieve
    outbound ports after execution.
    """
    def __init__(self):
        self._calls = {}
        self._start_call = None
        self._end_call = None

    def start(self):
        self._start_call.execute_forward()

    def add_call(self, call=None):
        label = call.get_label()
        call._set_container(container=self)
        self._calls[label] = call

    def set_start_call(self, call=None):
        ######
        # TODO: Complete implementation from here
        self._start_call = call

    def set_end_call(self, call=None):
        self._end_call = call


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

