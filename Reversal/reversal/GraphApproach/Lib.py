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


#TODO Implement execution logic, we need:
#A call or environment variables bag, etc.


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

    #def to_json(self, depth=0, prevent_infinite_loop_list=None):
    #    return "\n{0}{{{1}\n{0}}}".format(" " * depth, self.to_json_content(depth=depth + 1, prevent_infinite_loop_list=prevent_infinite_loop_list))

    def to_json(self, depth=0):
        # QUESTION: Consider using __hash__ instead of get_uid in such a way to cover all objects
        # TODO: Manage dictionaries and lists (all iterable) in sub-loops?
        json = '\n{0}{{'.format(" " * depth)
        json += '\n{0}"class":"{1}"'.format(" " * depth, self.__class__.__name__)
        for key in self.__dict__:
            item = self.__dict__[key]
            if isinstance(item, DataObject):
                if item.get_container() is None or item.get_container().get_uid() != self.get_uid():
                    json += '\n{0},"{1}":{{reference:{{{2}}}}}'.format(" " * depth, key, item.to_json_reference())
                else:
                    json += '\n{0},"{1}":{2}'.format(" " * depth,  key, item.to_json(depth=depth + 1))
            elif type(item) is dict:
                json += '\n{0},"{1}":'.format(" " * depth, key)
                json += '\n{0}['.format(" " * (depth + 1))
                is_first_sub_item = True
                for sub_key, sub_item in item.items():
                    if isinstance(sub_item, DataObject):
                        if sub_item.get_container() is None or sub_item.get_container().get_uid() != self.get_uid():
                            json += '\n{0}{{reference:{{{1}}}}}'.format(" " * (depth + 1), sub_item.to_json_reference())
                        else:
                            json += sub_item.to_json(depth=(depth + 2))
                    else:
                        json += '\n{0}""{1}""'.format(" " * (depth + 1), str(sub_item))
                json += '\n{0}]'.format(" " * (depth + 1))
            else:
                json += '\n{0},"{1}":"{2}"'.format(" " * depth, key, str(item))
        json += '\n{0}}}'.format(" " * depth)
        return json

    def to_json_reference(self):
        return '{{"reference":{{"class":"{0}","label":"{1}","uid":"{2}"}}'.format(self.__class__.__name__,  self.get_label(),  self.get_uid())

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
                    if isinstance(self.__dict__[key], DataObject):
                        # If a reference
                        references_direct[self.__dict__[key][sub_key].get_uid()] = self.__dict__[key][sub_key]
        return references_direct


class Error(Exception, DataObject):
    def __init__(self, container=None, label=None, level=None, **kwargs):
        #Base classes initialization
        DataObject.__init__(self, container=None, label=label)
        #Initialize pseudo-private members
        self._level = level
        self._information_items = kwargs


class ErrorLevel(Enum):
    system_stop = 1
    system_warning = 2
    system_info = 3
    execution_stop = 4
    execution_warning = 5
    execution_info = 6