import services
import sims4.commands
import sims
from functools import wraps
from ui.ui_dialog_picker import UiSimPicker, SimPickerRow
from sims4.localization import LocalizationHelperTuning
from distributor.shared_messages import IconInfoData
from game_injector import GameInjector
from mod_logger import logger

@logger
def watch_stuff(obs, val):
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

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was closed/cancelled")
            return
        output("Dialog was accepted")
        for sim_id in dialog.get_result_tags():
            output("id={}".format(sim_id))

    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Sim Picker Dialog Test")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Select up to five sims and press OK or close dialog....")
    max_selectable_immutable = sims4.collections.make_immutable_slots_class(set(['multi_select', 'number_selectable', 'max_type']))
    max_selectable = max_selectable_immutable({'multi_select':False, 'number_selectable':5, 'max_type':1})
    dialog = UiSimPicker.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, max_selectable=max_selectable, min_selectable=1, should_show_names=True, hide_row_description=False)
    for sim_info in services.sim_info_manager().get_all():
        # Set second arg below to True to have that sim preselected/highlighted....
        dialog.add_row(SimPickerRow(sim_info.sim_id, False, tag=sim_info.sim_id))

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(obj_instance=(sim_info)))
