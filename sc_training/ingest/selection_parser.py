# AUTOGENERATED! DO NOT EDIT! File to edit: 06_selection_parser.ipynb (unless otherwise specified).

__all__ = ['CtrlGroupTracker', 'count_max_active_groups', 'calc_ctrlg_ratio', 'calc_get_ctrl_grp_ratio',
           'calc_select_ratio']

# Internal Cell
# Load Module's dependencies
from pathlib import Path
from pprint import pprint
from typing import *

import json
import pandas as pd
import fastcore.test as ft

# Internal Cell
import sc2reader

from .handle_tracker_event import *
from .macro_econ_parser import *

# Cell
class CtrlGroupTracker(object):
    """Tracks the composition of the Replay's Players Control Groups.

    Using this plug-in, the Replay object will include the `ctrl_grp_trk`
    attribute. This attribute will store a dictionary of the control group
    compositions using the replay's human players' ids (`pid`) as keys.
    i.e.:
	`dict[pid (int):  control_group_compositions (dict)]`

    Each of these dictionaries uses the `second` attribute of a
    `ControlGroupEvent` as an index and organises the control group
    composition as one more dictionary, indexed with the integers 1 to 9,
    which stores a list of units that compose each one of the nine control
    groups of the player. i.e.

    `dict[pid(int): dict[second(int): dict[group(int): list_of_units]]]`
    """
    from sc2reader.engine.plugins import SelectionTracker
    sc2reader.engine.register_plugin(SelectionTracker())
    name = "CtrlGroupTracker"

    def handleInitGame(self, event, replay):
        replay.ctrl_grp_trk = dict()
        for human in replay.humans:
            selection = human.selection
            replay.ctrl_grp_trk[human.pid] = {0:{k: v for k, v
                                                in selection.items()
                                                if 0<k<10}}

    def handleEvent(self, event, replay):

        if isinstance(event, sc2reader.events.game.ControlGroupEvent):
            selection = event.player.selection
            replay.ctrl_grp_trk[event.player.pid][event.second] = {
                                                        k: v for k, v
                                                        in selection.items()
                                                        if 0<k<10}

# Internal Cell
def count_active_groups(ctrl_grps: dict[int, list]) -> int:
    '''Count how many of the control groups have units assign to them.

    *Args*
        - ctrl_grps (dict[int, list])
            Control group compossitions indexed from 1 to 9

    *Returns*
        - (int)
            Number of active control groups
    '''
    count = 0
    for l in ctrl_grps.values():
        if l:
            count += 1

    return count


# Internal Cell
def build_ctrlg_df(events: list,
                   rpl:sc2reader.resources.Replay) -> pd.DataFrame:

    raw_df = pd.DataFrame([e.__dict__ for e in events])[['second',
                                                         'player',
                                                         'name',
                                                         'control_group']]

    raw_df.insert(1, 'pid', [player.pid for player in raw_df.player])
    raw_df.insert(0, 'real_time',
                  [calc_realtime_index(sec, rpl) for sec in raw_df.second])

    return raw_df.drop(['player'], axis=1)

# Cell
def count_max_active_groups(rpl: sc2reader.resources.Replay,
                      pid: int) -> dict[str, float]:
    """Counts the maximum number of active control groups during the
    different stages of the game.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay being analysed.
        - pid (int)
            In-game player ID of the player being considered in the
            analysis.

    *Returns*
        - dict[str, int]
            Maximum number of active control groups at each game stage
            indexed with the keys [stage]_max_act_grps
    """
    column_names = ['whole_max_act_grps', 'early_max_act_grps',
                    'mid_max_act_grps', 'late_max_act_grps']
    ctrl_grp_e = [e for e in rpl.events
                if isinstance(e, sc2reader.events.game.ControlGroupEvent)
                and e.pid == (pid - 1)]

    if not ctrl_grp_e:
        return {name: 0 for name in column_names}

    ctrl_grp_e_df = build_ctrlg_df(ctrl_grp_e, rpl)

    grp_trk = rpl.ctrl_grp_trk
    grp_trk_indexes = [(row[1].pid, row[1].second)
                        for row in ctrl_grp_e_df.iterrows()]
    ctrl_grp_e_df['active_groups'] = [count_active_groups(grp_trk[player][sec])
                                      for player, sec in grp_trk_indexes]



    interv_dfs= gen_interval_sub_dfs(rpl.length.seconds,
                                     ctrl_grp_e_df,
                                     ['active_groups'])

    return {name: (df.agg('max')['active_groups'] if
                   not df.empty else 0)
            for name, df in zip(column_names, interv_dfs)}

# Cell
def calc_ctrlg_ratio(rpl: sc2reader.resources.Replay,
                      pid: int) -> dict[str, float]:

    """Calculates the ratio between `ControlGroupEvents` and the union of
    the `CommandEvents`, `SelectionEvents` and `ControlGroupCommand` sets
    to quantify the players' level of awareness and use of this tactical
    feature.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay being analysed.
        - pid (int)
            In-game player ID of the player being considered in the
            analysis.

    *Returns*
        - (dict[str, float])

    """

    command_secs = {e.second for e in rpl.events
                    if isinstance(e, sc2reader.events.game.CommandEvent)
                    and e.pid == (pid - 1)}

    select_secs = {e.second for e in rpl.events
                    if isinstance(e, sc2reader.events.game.SelectionEvent)
                    and e.pid == (pid - 1)}

    ctrlg_secs = {e.second for e in rpl.events
                    if isinstance(e, sc2reader.events.game.ControlGroupEvent)
                    and e.pid == (pid - 1)}


    total_counted_events = len(command_secs | select_secs | ctrlg_secs)

    if not total_counted_events:
        return {"ctrlg_ratio": 0}

    return {"ctrlg_ratio": len(ctrlg_secs)/total_counted_events}

# Cell
def calc_get_ctrl_grp_ratio(rpl: sc2reader.resources.Replay,
                            pid: int) -> dict[str, float]:
    """Calculates the ratio between `GetControlGroupEvent` to the all
    section events (i.e. the union of `GetControlGroupEvent` and
    `SelectEvent`).
    """

    select_secs = {e.second for e in rpl.events
                   if isinstance(e, sc2reader.events.game.SelectionEvent)
                   and e.pid == (pid - 1)}

    ctrlg_secs = {e.second for e in rpl.events
                  if isinstance(e, sc2reader.events.game.GetControlGroupEvent)
                  and e.pid == (pid - 1)}

    selection_union = len(ctrlg_secs | select_secs)

    if not selection_union:
        return {"get_ctrl_grp_ratio": 0}

    return {'get_ctrl_grp_ratio':len(ctrlg_secs)/selection_union}

# Cell
def calc_select_ratio(rpl: sc2reader.resources.Replay,
                            pid: int) -> dict[str, float]:
    """Calculates the ratio between `SelectEvent` to the all
    section events (i.e. the union of `GetControlGroupEvent` and
    `SelectEvent`).
    """
    select_secs = {e.second for e in rpl.events
                   if isinstance(e, sc2reader.events.game.SelectionEvent)
                   and e.pid == (pid - 1)}

    ctrlg_secs = {e.second for e in rpl.events
                  if isinstance(e, sc2reader.events.game.GetControlGroupEvent)
                  and e.pid == (pid - 1)}

    selection_union = len(ctrlg_secs | select_secs)

    if not selection_union:
        return {"get_ctrl_grp_ratio": 0}

    return {'select_ratio':len(select_secs)/selection_union}