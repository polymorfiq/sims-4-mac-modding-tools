# The Sims 4
# Copyright 2014 Electronic Arts Inc. All rights reserved.
"""
Example script mod.

This adds a game command that fills all commodities of all Sims
on the current lot.  By default, it fills only "core" commodities,
which are the motives initially added to all Sims.  Calling

|maslow true

will fill all commodities, including special ones.
"""

import sims4.commands
import services

@sims4.commands.Command('maslow', command_type=sims4.commands.CommandType.Live)
def fill_commodities(core_only:bool=True , _connection=None):
    """
    Fill all commodities of all Sims on the current lot.
    
    core_only: fill only the core (initial) commodities.
    """
    output = sims4.commands.CheatOutput(_connection)
    output("Ascending Maslow's hierarchy of needs!")
    
    for sim_info in services.sim_info_manager().objects:
        sim_info.commodity_tracker.set_all_commodities_to_max(core_only=core_only)


