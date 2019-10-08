import services
import sims4.commands
from weakref import WeakSet
from s4mmtlib.game_injector import GameInjector
from s4mmtlib.mod_logger import logger
from routing.object_routing.object_routing_component import ObjectRoutingComponent
from interactions.privacy import PrivacyService, Privacy
from objects.components.privacy_component import PrivacyComponent
from objects.components.idle_component import IdleComponent
from objects.game_object import GameObject
from turbolib2.events.privacy import _TurboPrivacyUtil
from turbolib2.events.utils.events_handler import TurboEventsHandler
from turbolib2.wrappers.line_of_sight import _SuperTurboLineOfSight

@sims4.commands.Command('uncensor_drones', command_type=sims4.commands.CommandType.Live)
@logger
def uncensor_drones(_connection=None):
    client_id = services.client_manager().get_first_client_id()
    output = sims4.commands.CheatOutput(client_id)

    connect_mod()
    output("Mod Injected!")

@logger
def connect_mod(_connection=None):
    injector = GameInjector()

    injector.wrap_function(PrivacyService, 'add_vehicle_to_monitor', observe_key='add_vehicle_override')
    injector.before('add_vehicle_override', disable_vehicle_call)

    injector.wrap_function(PrivacyService, 'remove_vehicle_to_monitor', observe_key='remove_vehicle_override')
    injector.before('remove_vehicle_override', disable_vehicle_call)


@logger
def disable_vehicle_call(obs, val, ctrl):
    if len(ctrl.args) > 1 and ("Drone" in str(ctrl.args[1])):
        ctrl.do_skip_call()


@logger
def watch_call(obs, val, ctrl):
    client_id = services.client_manager().get_first_client_id()
    output = sims4.commands.CheatOutput(client_id)
    output(obs.fnc_name + " called! - " + str(ctrl.args))
