__author__ = 'dmd'

class Function():
    def __init__(self,function_obverse,function_reverse):
        self.function_obverse = function_obverse
        self.function_reverse = function_reverse
        pass
    def execute_obverse(self,inputValue):
        return self.function_obverse(inputValue)
        pass
    def execute_reverse(self,outputValue):
        return self.function_reverse(outputValue)
        pass