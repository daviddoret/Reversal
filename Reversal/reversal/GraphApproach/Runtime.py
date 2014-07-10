__author__ = 'dmd'


from Reversal.reversal.GraphApproach.Lib import *
from Reversal.reversal.GraphApproach.Runtime import *
from Reversal.reversal.GraphApproach.DataPlane import *
from Reversal.reversal.GraphApproach.ExecutionPlane import *
from Reversal.reversal.GraphApproach.FunctionPlane import *


class Runtime(DataObject):
    """
    A runtime is an environment within which a function graph is executed,
    following an execution graph and with the support of the data plane.
    """
    def __init__(self):
        self._data_plane = DataPlane()
        self._execution_plane = ExecutionPlane()
        self._data_plane = DataPlane()
        pass