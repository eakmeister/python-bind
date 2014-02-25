from forbiddenfruit import curse
from functools import wraps
import types
import inspect

def bind(func, *bound_args, **bound_kwargs):

    def inner(*args, **kwargs):
        all_args = bound_args + args
        all_kwargs = dict(bound_kwargs.items() + kwargs.items())
        return func(*all_args, **all_kwargs)
    
    # Fetch the original argspec, remove the curried arguments, and create a
    # new argspec
    argspec_orig = inspect.getargspec(func)

    args = argspec_orig.args[len(bound_args):]
    for arg_name in bound_kwargs:
        args.remove(arg_name)
    
    argspec_new = inspect.ArgSpec(args = args,
                                  varargs = argspec_orig.varargs,
                                  keywords = argspec_orig.keywords,
                                  defaults = argspec_orig.defaults)

    # Create a lambda to wrap the inner function with the correct argspec. We
    # use eval for this because it's the only way I know of to create a
    # function with an arbitrary argspec.
    formatted_args = inspect.formatargspec(*argspec_new)
    params = formatted_args.lstrip('(').rstrip(')')
    lambda_str = 'lambda %s: inner%s' % (params, formatted_args)
    eval_func = eval(lambda_str, {'inner' : inner})

    return wraps(func)(eval_func)

curse(types.FunctionType, 'bind', bind)

