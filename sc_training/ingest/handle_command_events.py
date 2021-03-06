# AUTOGENERATED! DO NOT EDIT! File to edit: 05_handle_command_events.ipynb (unless otherwise specified).

__all__ = ['calc_apms', 'calc_spe_abil_ratios', 'get_prefered_spec_abil', 'calc_attack_ratio']

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
from sc2reader.engine.plugins import SelectionTracker, APMTracker
sc2reader.engine.register_plugin(SelectionTracker())
sc2reader.engine.register_plugin(APMTracker())

from .handle_tracker_event import *
from .macro_econ_parser import *

# Internal Cell
#
# Internal constants
if __name__ == "__main__":
    data_path = Path(Path.cwd()/'data')

else:
    data_path = (Path(Path(__file__)/'data')
            if Path(Path(__file__)/'data').exists()
            else Path(Path(__file__)/'../../../data'))

with open(data_path/'ability_list.json') as af:
    ABILITIES = json.load(af)

COMMON_ABILITIES = ['Attack',
                    'Stop',
                    'HoldPosition',
                    'Patrol',
                    'RightClick']

MOVE_COMMAND = ['RightClick']

# Internal Cell

# Helper functions for calc_apms
def reindex(rpl: sc2reader.resources.Replay, apm_dict:dict) -> dict:
    """Uses a dictionary that contains the player's minute-to-minute average
    APM of the player to compose a dictionary that uses the correct time
    index for this values based on the match's extension"""
    out_dict = {}
    for m in apm_dict.keys():
        real_t = calc_realtime_index(m, rpl)
        out_dict[real_t] = apm_dict[m]

    return out_dict

def average(lst: list[float]) -> float:
    """Calculates the average of a list of floats."""
    if len(lst) != 0:
        return sum(lst)/len(lst)
    else:
        return 0


# Cell
def calc_apms(rpl: sc2reader.resources.Replay,
             pid: int) -> dict[str, float]:
    """Extracts the average APM of a specific player during the whole game
    and the early, mid and late stages of the game.

    The function uses sc2reader APMTracker plugin to extract the
    minute-to-minute APM measurement of the player. Based on this it
    calculates the average values for the whole, early, mid and late game
    stages.

    *Args*
        - rpl (sc2reader.resources.Replay)
            Replay being analysed
        - pid (int)
            Player id of the player being considered by the function

    *Returns*
        - dict[str, float]
            Dictionary with the game stage names as key and the Average
            APMs measurements of each stage as values"""
    if not rpl.player[pid].is_human:
        return {'whole_APM':0,'early_APM':0,'mid_APM':0,'late_APM':0,}

    apms_dict = reindex(rpl, rpl.player[pid].apm)

    apms_lists = [[apm for m, apm in apms_dict.items() if m < 4],
                  [apm for m, apm in apms_dict.items() if 4 <= m < 8],
                  [apm for m, apm in apms_dict.items() if 8 <= m]]

    dict_keys = ['early_APM', 'mid_APM', 'late_APM']

    avg_apms = {k: average(vals) for k, vals in zip(dict_keys, apms_lists)}

    avg_apms['whole_APM'] = rpl.player[pid].avg_apm

    return avg_apms



# Internal Cell
# Herlper fucntion that supports all exportable functions below.
def build_commands_df(rpl: sc2reader.resources.Replay,
                events: list[sc2reader.events.game.GameEvent]) -> pd.DataFrame:
    df_columns =  ['real_time', 'second', 'ability_name']

    commands_df = pd.DataFrame([[calc_realtime_index(com_e.second, rpl),
                            com_e.second,
                            com_e.ability_name]
                        for com_e in events], columns= df_columns)

    return commands_df

# Cell

def calc_spe_abil_ratios(rpl: sc2reader.resources.Replay,
                         pid: int) -> dict[str, float]:
    '''
    Extracts a ratio from 0 to 1 that quantifies the use use of special
    abilities.

    The special abilities ratio (sar) indicates the proportion of special
    abilities to general commands executed by the player.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay being analysed.
        - pid (int)
            In-game player ID of the player being considered in the
            analysis.

    *Returns*
        - dict[float]
            A dictionary containing the special abilities ratio (sar)
            values for the whole, early, mid and late game.

    '''

    replay_lenght = rpl.length.seconds
    player_race = rpl.player[pid].play_race

    commands_list = [com_e for com_e in rpl.events
                if isinstance(com_e, sc2reader.events.game.CommandEvent)
                and com_e.player.pid == pid]

    abil_comm_list = [com_e for com_e in rpl.events
                    if isinstance(com_e, sc2reader.events.game.CommandEvent)
                    and com_e.player.pid == pid
                    and com_e.ability_name in ABILITIES[player_race]
                    and com_e.ability_name not in COMMON_ABILITIES]

    commands = build_commands_df(rpl, commands_list)
    abilities_commands = build_commands_df(rpl, abil_comm_list)

    commands_dfs = gen_interval_sub_dfs(replay_lenght, commands,
                                       ['real_time', 'ability_name'])
    abilities_dfs = gen_interval_sub_dfs(replay_lenght, abilities_commands,
                                        ['real_time', 'ability_name'])

    ratios = [total_abilities / total_commands if total_commands != 0 else 0
              for total_abilities, total_commands
              in zip(map(len, abilities_dfs), map(len, commands_dfs))]
    ratios_names = ['whole_sar', 'early_sar', 'mid_sar', 'late_sar']

    return {nam: rat for nam, rat in zip(ratios_names, ratios)}

# Internal Cell

def get_top_abilities(abilities: pd.DataFrame) -> dict[str, tuple[str,str]]:
    prefered = None
    second = None
    if not abilities.empty:
        ability_count = (abilities
                        .groupby('ability_name')
                        .size())

        ability_count.sort_values(ascending=False, inplace=True)

        if len(ability_count) > 0:
            prefered = ability_count.index[0]

        if len(ability_count) >= 2:
            second = ability_count.index[1]

    return (prefered, second)



# Cell
def get_prefered_spec_abil(rpl: sc2reader.resources.Replay,
                           pid: int) -> dict[str, tuple[str, int]]:

    '''Extracts the names of the two special abilities a player uses the
    most during the whole, early, mid and late games.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay being analysed.
        - pid (int)
            In-game player ID of the player being considered in the
            analysis.

    *Returns*
        - dict[str, tuple[str, int]]
            The keys of the dictionary separate the preferences according
            to the game stages. The dictionary values contain a tuple with
            the first and second abilities the player uses the most in
            that order.
    '''
    replay_lenght = rpl.length.seconds
    player_race = rpl.player[pid].play_race


    abil_comm_list = [com_e for com_e in rpl.events
                    if isinstance(com_e, sc2reader.events.game.CommandEvent)
                    and com_e.player.pid == pid
                    and com_e.ability_name in ABILITIES[player_race]
                    and com_e.ability_name not in COMMON_ABILITIES]

    abilities_commands = build_commands_df(rpl, abil_comm_list)

    abilities_dfs = gen_interval_sub_dfs(replay_lenght, abilities_commands,
                                        ['real_time', 'ability_name'])

    stage_names = ['whole_pref_sab', 'early_pref_sab',
                   'mid_pref_sab', 'late_pref_sab']
    preferences = [get_top_abilities(df) for df in abilities_dfs]

    return {nam: pref for nam, pref in zip(stage_names, preferences)}

# Cell
def calc_attack_ratio(rpl: sc2reader.resources.Replay,
                      pid: int) -> dict[str, float]:
    '''Calculates the ratio between a player's attack orders and their
    common commands.

    Offers a ratio between attacks and other common commands such as move,
    follow, stop, and hold position as a measurement of a player's tactical
    aggresiveness.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay being analysed.
        - pid (int)
            In-game player ID of the player being considered in the
            analysis.

    *Returns*
        - dict[str, float]
            A dictionary that separates a player's attack ratios for the
            different stages of a match.
    '''
    replay_lenght = rpl.length.seconds

    common_comms = [com_e for com_e in rpl.events
                if isinstance(com_e, sc2reader.events.game.CommandEvent)
                and com_e.player.pid == pid
                and not com_e.ability.is_build
                and com_e.ability.name in COMMON_ABILITIES
                and com_e.ability_name in COMMON_ABILITIES]

    attack_comms = [att for att in common_comms
                if att.ability.name == 'Attack']

    common_comms_dfs = build_commands_df(rpl, common_comms)
    attack_comms_dfs = build_commands_df(rpl, attack_comms)

    cc_subdf_list = gen_interval_sub_dfs(replay_lenght, common_comms_dfs,
                                        ['real_time', 'ability_name'])

    ca_subdf_list = gen_interval_sub_dfs(replay_lenght, attack_comms_dfs,
                                        ['real_time', 'ability_name'])


    ratios_names = ['whole_att_ratio', 'early_att_ratio',
                   'mid_att_ratio', 'late_att_ratio']
    att_ratios = [round(len(att) / len(comm), ndigits=3)
                  if len(comm) != 0 else 0
                  for att, comm in zip(ca_subdf_list, cc_subdf_list)]

    return {nam: rat for nam, rat in zip(ratios_names, att_ratios)}