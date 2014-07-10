__author__ = 'dmd'


from Reversal.reversal.GraphApproach.Lib import *
from Reversal.reversal.GraphApproach.Runtime import *
from Reversal.reversal.GraphApproach.DataPlane import *
from Reversal.reversal.GraphApproach.ExecutionPlane import *
from Reversal.reversal.GraphApproach.FunctionPlane import *


class DataPlane(DataObject):
    """

    """
    def __init__(self, container=None, label=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Initialize pseudo-private members
        self._all_variables = {}
        self._inbound_variables = {}
        self._private_variables = {}
        self._outbound_variables = {}

    def get_variable(self):
        pass

    def set_variable(self):
        pass


class DataVariable(DataObject):
    """

    """
    def __init__(self, container=None, label=None, value=None):
        #Base classes initialization
        DataObject.__init__(self, container=container, label=label)
        #Pseudo-private members
        self._value = None
        #Public members
        #Initialization methods
        self.set_value(value=value)

    def get_value(self):
        return self._value

    def set_value(self,value):
        self._value = value


class DataVariableScope(Enum):
    """

    """
    inbound = 1
    private = 2
    outbound = 3