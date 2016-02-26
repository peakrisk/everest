"""
Decorate methods with monitoring code.


"""
from functools import wraps

def debug(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(fn.__qualname__)
        return fn(*args, **kwargs)

    return wrapper

class X:

    @debug
    def foo(self):

        pass

    @debug
    def bar(self, x, y=None):

        pass

class Y(X):

    @debug
    def foo(self):
        pass
    

x = X()

x.foo()

x.bar(12)

x.bar(12, y=10)

y = Y()

y.foo()

y.bar(12, y=10)
