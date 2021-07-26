# AUTOGENERATED! DO NOT EDIT! File to edit: 02_handle_tracker_events.ipynb (unless otherwise specified).

__all__ = ['INTERVALS_BASE', 'calc_realtime_index']

# Internal Cell

#Load Module's dependencies

from pathlib import Path
from pprint import pprint
from typing import *

import fastcore.test as ft

import sc2reader

# Cell
INTERVALS_BASE = 4*60

# Cell

def calc_realtime_index(registered_time: int,
                        rpl: sc2reader.resources.Replay) -> float:
    """Calculate the time index of an event based on the replay recorded
    duration.

    Given that the registered time index on TrackerEvents don not necessarily
    coincide with the replay duration, this function recalculates the time
    index of an event to correct this discrepancy.

    *Args*
        - registered_time (int)
            The time index in seconds recorded in the event. Normally
            accessible through the .second attribute.
        - rpl (sc2reader.resources.Replay)
            Working replay

    *Returns*
        - float
            The time index that would match the replay's duration
    """
    rpl_length = rpl.length.seconds
    rpl_last_rec_time = [e.second for e in rpl.events
                        if isinstance(e,
                        sc2reader.events.tracker.PlayerStatsEvent)][-1]

    return (registered_time/rpl_last_rec_time) * rpl_length