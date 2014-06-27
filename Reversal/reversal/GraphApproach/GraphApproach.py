__author__ = 'dmd'

from Reversal.reversal.bin.utils import *

class Source(object):
    """
    A super base class that inherits from object,
    in such a way as to implement the diamond rule
    in the presence of multiple inheritance
    """
    def __init__(self):
        pass

    def __repr__(self):
        return self.to_json()

    def to_json_content(self):
        """
        Returns the content of the JSON object, i.e. without the brackets {}.
        This is useful when you want to concatenate content from multiple super classes.
        """
        pass

    def to_json(self):
        """
        Returns the complete JSON object, i.e. with the brackets {}.
        """
        return '{{{0}}}'.format(self.to_json_content())

class Contained(Source):
    """
    Containment designate an exclusive relationship of ownership, semantically equivalent to a UML composition.
    """
    def __init__(self, container=None):
        #Base classes initialization
        Source.__init__(self)
        #Initialize pseudo-private members
        self._container = None
        #Call set methods to comply with their logic
        self._set_container(container)

    def __repr__(self):
        # Containment is not represented to avoid cluttering.
        # Parenthesis are used in parent Sources to represent containment.
        return ""

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


class Labelled(Source):
    """
    Makes it possible to label elements for readability purposes.
    """
    def __init__(self, label=None):
        #Base classes initialization
        Source.__init__(self)
        #Initialize pseudo-private members
        self._label = None
        #Call set methods to comply with their logic
        if label == None:
            label = "toto"
        self.set_label(label=label)

    def __repr__(self):
        return "{0}('{1}')".format(self.__class__.__name__, self._label)

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def to_json_content(self):
        return '"label":"{0}"'.format(self.get_label())


class Function(Labelled, Source):

    def __init__(self, label=None, logic=None):
        #Base classes initialization
        Source.__init__(self)
        Labelled.__init__(self, label=label)
        #Initialize pseudo-private members
        self._data_inbound_surface = None
        self._data_outbound_surface = None
        self._execution_inbound_surface = None
        self._execution_outbound_surface = None
        self._logic = None
        #Call set methods to comply with their logic
        self._set_data_inbound_surface(data_inbound_surface=FunctionDataInboundSurface())
        self._set_data_outbound_surface(data_outbound_surface=FunctionDataOutboundSurface())
        self._set_execution_inbound_surface(execution_inbound_surface=FunctionExecutionInboundSurface())
        self._set_execution_outbound_surface(execution_outbound_surface=FunctionExecutionOutboundSurface())
        self.set_logic(logic)

    def get_data_inbound_surface(self):
        return self._data_inbound_surface

    def _set_data_inbound_surface(self, data_inbound_surface):
        data_inbound_surface._set_container(self)
        self._data_inbound_surface = data_inbound_surface

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
        self._logic = logic

    def to_json_content(self):
        #return Labelled.to_json_content(self) + \
        return \
            '"data_inbound_surface":{0}'.format(self._data_inbound_surface.to_json()) + \
            ',"data_outbound_surface":{0}'.format(self._data_inbound_surface.to_json()) + \
            ',"execution_inbound_surface":{0}'.format(self._data_inbound_surface.to_json()) + \
            ',"execution_outbound_surface":{0}'.format(self._data_inbound_surface.to_json()) + \
            ',"logic":{0}'.format(self._data_inbound_surface.to_json())


class Logic(Contained, Labelled, Source):
    """
    A logic component is always able to implement a forward execution
    on its parent function.
    A logic component should be able to find ways to implement a
    backward execution on its parent function.
    """
    def __init__(self, container_function, label):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container_function)
        Labelled.__init__(self, label=label)

    def execute_forward(self):
        pass

    def execute_backward(self):
        pass


class FunctionDataInboundSurface(Contained, Source):

    def __init__(self, container=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container)
        #Initialize pseudo-private members
        self._data_inbound_ports = {}

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._data_inbound_ports)

    def add_port(self, data_inbound_port):
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
            new_port = FunctionDataInboundPort(label=label)
            self.add_port(new_port)
            return new_port

class FunctionDataInboundPort(Contained, Labelled, Source):

    def __init__(self, container_surface=None, label=None, linked_variable=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container_surface)
        Labelled.__init__(self, label=label)
        #Initialize pseudo-private members
        self._linked_variable = None
        #Call set methods to comply with their logic
        self.set_linked_variable(linked_variable=linked_variable)

    def __repr__(self):
        return "{0}({1},LinkedVariable({2}))".format(self.__class__.__name__, super(Labelled, self), self.get_linked_variable().get_label())

    def get_linked_variable(self):
        return self._linked_variable

    def set_linked_variable(self, linked_variable):
        self._linked_variable = linked_variable


class FunctionDataOutboundSurface(Contained, Source):

    def __init__(self, container_function=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container_function)
        #Initialize pseudo-private members
        self._data_outbound_ports = {}

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._data_outbound_ports)

    def add_port(self, data_outbound_port=None):
        #If a pre-configured port is not provided, create one out of the blue.
        if data_outbound_port == None:
            data_outbound_port = FunctionDataOutboundPort()
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
            new_port = FunctionDataOutboundPort(label=label)
            self.add_port(new_port)
            return new_port


class FunctionDataOutboundPort(Contained, Labelled, Source):

    def __init__(self, container_surface=None, label=None, linked_variable=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container_surface)
        Labelled.__init__(self, label=label)
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


class FunctionExecutionInboundSurface(Contained, Source):

    def __init__(self, container=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container)
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
            new_port = FunctionDataInboundPort(container_surface=self, label=label)
            self.add_port(new_port)
            return new_port

class FunctionExecInboundPort(Contained, Labelled, Source):

    def __init__(self, parent_surface, label):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=parent_surface)
        Labelled.__init__(self, label=label)
        #Pseudo-private members
        self._parent_surface = parent_surface
        self._label = label
        #Public members
        self.label = self._label


class FunctionExecutionOutboundSurface(Contained, Source):

    def __init__(self, container=None):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=container)
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
            new_port = FunctionDataInboundPort(container_surface=self, label=label)
            self.add_port(new_port)
            return new_port

class FunctionExecOutboundPort(Contained, Labelled, Source):

    def __init__(self, parent_surface,label):
        #Base classes initialization
        Source.__init__(self)
        Contained.__init__(self, container=parent_surface)
        Labelled.__init__(self, label=label)
        #Pseudo-private members
        self._parent_surface = parent_surface
        self._label = label
        #Public members
        self.label = self._label


class DataVariable(Contained, Source):

    def __init__(self):
        pass


class DataSurface(Contained, Source):

    def __init__(self):
        pass


class FunctionComposite(Source):
    #TODO: Inherit from Function in such a way as to make Algorithms callable
    def __init__(self, start_function, end_function):
        self._start_function = start_function
        self._end_function = end_function

    def start(self):
        self._start_function.execute_forward()


class ExecTrace(Source, ):

    def __init__(self):
        pass


class ExecTraceForward(ExecTrace, Source):

    def __init__(self):
        pass


class ExecTraceBackward(ExecTrace, Source):
    """
    A backward execution trace is distinct from a forward exec trace
    because it informs us on one possible pass amongst multiple
    possible execuction pathes.
    """
    def __init__(self):
        pass