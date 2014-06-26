__author__ = 'dmd'

import bitstring

class Function():
    def __init__(self,functionObverse,functionReverse):
        self.functionObverse = functionObverse
        self.functionReverse = functionReverse
        pass
    def ExecuteObverse(self,inputValue):
        return self.functionObverse(inputValue)
        pass
    def ExecuteReverse(self,outputValue):
        return self.functionReverse(outputValue)
        pass

class Multiply(Function):
    def __init__(self,factor):
        self.factor = factor
        super(Multiply, self).__init__(self.MultiplyObverse,self.MultiplyReverse)
    def MultiplyObverse(self,inputValue):
        return inputValue * self.factor
        pass
    def MultiplyReverse(self,outputValue):
        return outputValue / self.factor
        pass

class Add(Function):
    def __init__(self,factor):
        self.factor = factor
        super(Add, self).__init__(self.AddObverse,self.AddReverse)
    def AddObverse(self,inputValue):
        return inputValue + self.factor
        pass
    def AddReverse(self,outputValue):
        return outputValue - self.factor
        pass

class Composite(Function):
    def __init__(self):
        self.steps = []
        super(Composite, self).__init__(self.CompositeObverse,self.CompositeReverse)
        pass
    def CompositeObverse(self,inputValue):
        for step in self.steps:
            inputValue = step.execute_obverse(inputValue)
        return inputValue
        pass
    def CompositeReverse(self,outputValue):
        for step in reversed(self.steps):
            outputValue = step.execute_reverse(outputValue)
        return outputValue
        pass
    def AddStep(self,step):
        self.steps.append(step)
        pass

