__author__ = 'dmd'

class ComplexValue():
    def __init__(self):
        self.items = {}
        pass
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.items)
