__author__ = 'dmd'

class A(object):
    def __init__(self):
        pass

class B(A):
    def __init__(self, **kwargs):
        self.b = kwargs.get("b" ,kwargs)
        pass

class C(A):
    def __init__(self, **kwargs):
        self.c = kwargs.get("c" ,kwargs)
        pass

class D(C, B):
    def __init__(self, **kwargs):
        B.__init__(self,**kwargs)
        C.__init__(self,**kwargs)
        self.d = kwargs.get("d" ,kwargs)
        pass

x = D(b=2, popo=3)

print(x)