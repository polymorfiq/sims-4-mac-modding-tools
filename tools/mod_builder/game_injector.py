import types
from rx import create
from functools import wraps

START_LIFECYCLE = 'start'
END_LIFECYCLE = 'end'

class GameInjector:
    def __init__(self):
        self.observed_funcs = {}

    def before(self, observe_key, do_this):
        observed = self.observed(observe_key)
        source = observed.observable

        def on_call(lifecycle_data):
            lifecycle = lifecycle_data[0]
            data = lifecycle_data[1]

            if lifecycle == START_LIFECYCLE:
                do_this(observed, data)

        return source.subscribe(on_next=on_call)

    def after(self, observe_key, do_this):
        observed = self.observed(observe_key)
        source = observed.observable

        def on_call(lifecycle_data):
            lifecycle = lifecycle_data[0]
            data = lifecycle_data[1]

            if lifecycle == END_LIFECYCLE:
                do_this(observed, data)

        return source.subscribe(on_next=on_call)

    def observed(self, observe_key):
        return self.observed_funcs[observe_key]

    def wrap_function(self, obj, fnc_name, observe_key):
        if observe_key in self.observed_funcs:
            return self.observed_funcs[observe_key]

        def func_observer(observer, schedule):
            target_fnc = getattr(obj, fnc_name)

            def fnc_replacement(*args, **kwargs):
                observer.on_next((START_LIFECYCLE, None))
                ret_value = target_fnc(*args, **kwargs)
                observer.on_next((END_LIFECYCLE, ret_value))

                return ret_value

            setattr(obj, fnc_name, inject(target_fnc, fnc_replacement))

        source = create(func_observer)
        self.observed_funcs[observe_key] = ObservedFunc(obj, fnc_name, source)

        return source

class ObservedFunc:
    def __init__(self, obj, fnc_name, observer):
        self.obj = obj
        self.fnc_name = fnc_name
        self.observable = observer

def inject(target_function, new_function):
    @wraps(target_function)
    def _inject(*args, **kwargs):
        return new_function(*args, **kwargs)
    return _inject
