from forbiddenfruit import curse
import types

def bind(func, *bound_args, **bound_kwargs):
    def inner(*args, **kwargs):
        all_args = bound_args + args
        all_kwargs = dict(bound_kwargs.items() + kwargs.items())
        return func(*all_args, **all_kwargs)
    
    return inner

curse(types.FunctionType, 'bind', bind)

