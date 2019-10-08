import services
import sims4.commands
import sims
from functools import wraps
from ui.ui_dialog_picker import UiSimPicker, SimPickerRow
from sims4.localization import LocalizationHelperTuning
from distributor.shared_messages import IconInfoData
from s4mmtlib.game_injector import GameInjector
from s4mmtlib.mod_logger import logger

@logger
def watch_stuff(obs, val, ctrl):
    client_id = services.client_manager().get_first_client_id()
    output = sims4.commands.CheatOutput(client_id)
    output(obs.fnc_name + " called!")

@sims4.commands.Command('you_did_it', command_type=sims4.commands.CommandType.Live)
@logger
def sim_picker_dialog_test(_connection=None):
    client_id = services.client_manager().get_first_client_id()
    output = sims4.commands.CheatOutput(client_id)
    client = services.client_manager().get_first_client()

    injector = GameInjector()
    injector.wrap_function(sims.sim.Sim, 'on_add', observe_key='test_inject')
    injector.after('test_inject', watch_stuff)
