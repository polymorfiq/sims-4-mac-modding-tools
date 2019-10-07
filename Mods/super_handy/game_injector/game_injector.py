import types
from functools import wraps

START_LIFECYCLE = 'start'
END_LIFECYCLE = 'end'

class GameInjector:
    def __init__(self):
        self.observed_funcs = {}

    def before(self, observe_key, do_this):
        observed = self.observed(observe_key)
        return observed.start.subscribe(do_this)

    def after(self, observe_key, do_this):
        observed = self.observed(observe_key)
        return observed.end.subscribe(do_this)

    def observed(self, observe_key):
        return self.observed_funcs[observe_key]

    def wrap_function(self, obj, fnc_name, observe_key):
        if observe_key in self.observed_funcs:
            return self.observed_funcs[observe_key]

        target_fnc = getattr(obj, fnc_name)

        observed = ObservedFunc(obj, fnc_name)
        def fnc_replacement(*args, **kwargs):
            observed.start.publish(None)
            ret_value = target_fnc(*args, **kwargs)
            observed.end.publish(ret_value)

            return ret_value

        setattr(obj, fnc_name, inject(target_fnc, fnc_replacement))

        self.observed_funcs[observe_key] = observed

        return observed

class ObservedFunc:
    def __init__(self, obj, fnc_name):
        self.obj = obj
        self.fnc_name = fnc_name
        self.start = Observable(self)
        self.end = Observable(self)

class Observable:
    def __init__(self, observed):
        self.callbacks = []
        self.observed = observed

    def subscribe(self, cb):
        self.callbacks.append(cb)

    def publish(self, data):
        for cb in self.callbacks:
            cb(self.observed, data)

def inject(target_function, new_function):
    @wraps(target_function)
    def _inject(*args, **kwargs):
        return new_function(*args, **kwargs)
    return _inject
