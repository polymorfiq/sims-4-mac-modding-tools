from interactions.privacy import PrivacyService
from s4mmtlib.game_injector import GameInjector

def connect_mod():
    injector = GameInjector()

    injector.wrap_function(PrivacyService, 'add_vehicle_to_monitor', observe_key='add_vehicle_override')
    injector.before('add_vehicle_override', disable_vehicle_call)

    injector.wrap_function(PrivacyService, 'remove_vehicle_to_monitor', observe_key='remove_vehicle_override')
    injector.before('remove_vehicle_override', disable_vehicle_call)


def disable_vehicle_call(obs, val, ctrl):
    if len(ctrl.args) > 1 and ("Drone" in str(ctrl.args[1])):
        ctrl.do_skip_call()

connect_mod()
