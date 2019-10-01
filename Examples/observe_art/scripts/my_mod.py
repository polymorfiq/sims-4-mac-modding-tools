import services
import sims4.commands
import types
from protocolbuffers import Consts_pb2

@sims4.commands.Command('getpopulation', command_type=sims4.commands.CommandType.Live)
def getpop(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Your town\'s population is {}'.format(len(services.sim_info_manager().get_all())))


def _fire_allowed_override(self, transform, routing_surface, run_placement_tests=True):
    return True


@sims4.commands.Command('apples', command_type=(sims4.commands.CommandType.Live))
def apples(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Loading fire mod...')

    tgt_client = services.client_manager().get(_connection)
    my_sim = tgt_client.active_sim

    output('Active Sim Loaded...')

    fire_service = services.get_fire_service()
    sim_info_manager = services.sim_info_manager()
    for sim in sim_info_manager.instanced_sims_gen():
        current_zone = services.current_zone()
        sim_obj = current_zone.find_object(sim.id)

        if sim_obj is not None:
            output('Sim Obj Loaded...')
            orig_allowed = fire_service.is_fire_allowed
            output('Orig is_fire_allowed stored...')

            fire_service.is_fire_allowed = types.MethodType(_fire_allowed_override, fire_service)

            try:
                output('Orig is_fire_allowed overrided...')

                fire_object = fire_service._spawn_fire(sim_obj.transform, sim_obj.routing_surface)
                output('Fire spawned...')
            except Exception as ex:
                output('HMM...')
                output(str(ex))

            fire_service.is_fire_allowed = orig_allowed
            output('Orig is_fire_allowed returned...')
