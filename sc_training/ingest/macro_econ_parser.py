# AUTOGENERATED! DO NOT EDIT! File to edit: 03_macro_econ_parser.ipynb (unless otherwise specified).

__all__ = ['gen_interval_sub_dfs', 'list_attr_interval_values', 'get_player_macro_econ_stats']

# Internal Cell

from pathlib import Path
from pprint import pprint
from dataclasses import dataclass, astuple, field
from datetime import datetime
from typing import *
from fastcore import test as ft

import pandas as pd
import numpy as np

import sc2reader

from .handle_tracker_event import *

# Internal Cell

# The Following are the module's helper functions

def get_pstatse(rpl: sc2reader.resources.Replay,
                current_pid: int) \
                -> list[sc2reader.events.tracker.PlayerStatsEvent]:
    """Extracts a list of all the `PlayerStatsEvent` instances related to
    a player from a replay.

    *Args*
        - rpl (sc2reader.resources.Replay)
            The replay that contains the information.
        - current_pid (int):
            The player id of the player who's events are being extracted.

    *Retruns*
        - lis[PlayerStatsEvent]
            List of all the `PlayerStatsEvent` instances of a player in a
            replay.
    """

    return [event for event in rpl.events
            if isinstance(event, sc2reader.events.tracker.PlayerStatsEvent)
            and event.pid == current_pid]

# Internal Cell

def complete_pstatse_df(rpl: sc2reader.resources.Replay,
                        df: pd.DataFrame) -> pd.DataFrame:
    """Expands the initial DataFrame that can be extracted directly from
    the PlayerStatsEvents with several relevant features.

    This function uses the replay data to compose several features time
    series that can facilitate the extraction of macroeconomic stats later.
    The function adds the following columns to the macroeconomic stats
    DataFrame extracted from the PlayerStatsEvents: real_time (realtime
    indexes that match the replay duration), unspent_rsrc,
    rsrc_collection_rate.

    *Args*
        - rpl (sc2reader.resources.Replay)
            Working replay.
        - df (pd.DataFrame)
            DataFrame containing the data on the main macroeconomic
            indicators recorded in the Replay's the PlayerStatsEvents.

    *Returns*
        - pd.DataFrame
            Expanded DataFrame that includes all relevant data about a
            replay's macroeconomic indicators.

    """
    # Eliminate the record of the loser record if present.
    if (df.iloc[-1] == df.iloc[-2]).all():
        df_no_loss_record = df.drop([len(df)-1])
    else:
        df_no_loss_record = df.copy()

    # Get the last recorded time in the dataframe
    last_time_record = df_no_loss_record.iloc[-1].second

    # Calculate the values for the real time column
    real_time_indexes = [calc_realtime_index(rec_time_ind, rpl)
                         for rec_time_ind in df_no_loss_record.second]

    # Add the real_time indexes column to the data frame
    df_no_loss_record.insert(0,'real_time', real_time_indexes)

    # Add columns for extra features
    df_no_loss_record.insert(4,'unspent_rsrc',
                            (df_no_loss_record.minerals_current
                            + df_no_loss_record.vespene_current))
    df_no_loss_record.insert(7,'army_value',
                            (df_no_loss_record.minerals_used_active_forces
                            +df_no_loss_record.vespene_used_active_forces))
    df_no_loss_record.insert(10,'rsrc_collection_rate',
                            (df_no_loss_record.minerals_collection_rate
                            + df_no_loss_record.vespene_collection_rate))

    supply_capped_column = np.where(df_no_loss_record['food_made'] <=
                                    df_no_loss_record['food_used'],
                                    True, False)

    df_no_loss_record.insert(26, 'supply_capped', supply_capped_column)
    return df_no_loss_record

# Internal Cell
# Functions for specific indicators
def get_subdf_mean(subdf: pd.DataFrame) -> float:
    """Wraper for the pd.DataFrame.mean() function.

    *Args*
        -subdf (pd.DataFrame)
               This is the DatraFrame whos mean will be evaluated.

    *Returns*
        - float
            Mean value of the DataFrame.
    """
    return subdf.mean()

def get_subdf_total(subdf: pd.DataFrame) -> float:
    """Wraper for the pd.DataFrame.mean() function.

    *Args*
        -subdf (pd.DataFrame)
               This is the DatraFrame whos mean will be evaluated.

    *Returns*
        - float
            Total value of a particular attribute up to a certain point of
            the game.
    """
    return subdf.iloc[len(subdf)-1]

def get_cappedTime(subdf:pd.DataFrame) -> float:
    lapse_start = 0
    capped_lapses = []

    # Verify row by row if at the time the supply was capped.
    # Add a time lapse to the capped_lapses list every time concludes.
    for _, row in subdf.iterrows():
        if row['supply_capped']:
            if not lapse_start:
                lapse_start = row['real_time']
        else:
            if lapse_start:
                capped_lapses.append(row['real_time'] - lapse_start)
                lapse_start = 0

    # Verify if the interval finished capped. If so, account
    # for the lapse.
    if lapse_start:

        last_event_length = (subdf.iloc[-1]['real_time']
                             - subdf.iloc[-2]['real_time'])
        capped_lapses.append(subdf.iloc[-1]['real_time']
                             - lapse_start + last_event_length)

    return sum(capped_lapses)


def calculate_spending_coeficient(unspent_rsrc: float,
                                  total_rates: float) -> float:
    if unspent_rsrc and total_rates:
        return (35*((0.00137*total_rates) - np.log(unspent_rsrc)) + 240)
    else:
        return None

# Internal Cell

def get_player_macro_econ_df(rpl: sc2reader.resources.Replay,
                             pid: int) -> pd.DataFrame:
    """This function organises the records of a player's major
    macroeconomic performance indicators.

    The function uses a player's PlayerStatsEvents contained in a Replay
    object to compose a DataFrame. In the DataFrame, each column points to
    a particular indicator. Each row points to the records of all
    indicators at a specific moment during the game.

    *Arguments*
        - rpl (sc2reader.resources.Replay)
                Replay object generated with sc2reader containing a match's
                data.
        - pid (int)
                A player's id number distinguishes them from the other
                players in a match. It can be extracted from a Participant
                object through the pid attribute.

    *Returns*
        - pd.DataFrame
            This DataFrame contains all the time series that illustrate the
            changes of each attribute during a match. Each column alludes
            to an attribute, each row to a moment during the match.
    """

    columns_names =[
    'second',
    'minerals_current',
    'vespene_current',
    'minerals_used_active_forces',
    'vespene_used_active_forces',
    'minerals_collection_rate',
    'vespene_collection_rate',
    'workers_active_count',
    'minerals_used_in_progress',
    'vespene_used_in_progress',
    'resources_used_in_progress',
    'minerals_used_current',
    'vespene_used_current',
    'resources_used_current',
    'minerals_lost',
    'vespene_lost',
    'resources_lost',
    'minerals_killed',
    'vespene_killed',
    'resources_killed',
    'food_used',
    'food_made'
    ]

    # Generate a DataFrame with the columns listed above
    pstatse_list = get_pstatse(rpl, pid)
    pstatse_dicts_list = [event.__dict__ for event in pstatse_list]
    pstatse_df = pd.DataFrame(pstatse_dicts_list, columns= columns_names)

    # Complete the DataFrame with the real_time, unspent_rsrc columns and
    # army_value.
    # Also, eliminate possible duplicate last record.
    return complete_pstatse_df(rpl, pstatse_df)

# Cell

def gen_interval_sub_dfs(rpl_length: float,
                        df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Extract a set of DataFrames containing the records for a particular
    field of the PlayerStatsEvent.

    The function extracts the information of a particular column of the df
    DataFrame. It returns a list of four DataFrames for the whole, early,
    mid and late game intervals.

    *Args*
        - df (pd.DataFrame)
            DataFrame containing all PlayerStatsEvent instances of a
            replay. The DataFrame must have a 'real_time' column that
            indexes the events in the data frame in time in a manner that
            consistent with the replays length.
        - rpl_length (float)
            Length of a match in seconds.
        - column (str)
            Name of the column that should be extracted in the DataFrames

    *Returns*
        - list[DataFrame]
            List of the DataFrames, containing the column information for
            the whole, early, mid and late games in that order.
    """
    process_df = df.copy()
    early_mark = INTERVALS_BASE
    mid_mark = early_mark * 2


    if rpl_length > mid_mark:
        time_intervals = [(0, rpl_length), (0, early_mark),
                         (early_mark, mid_mark), (mid_mark, rpl_length)]

    elif early_mark < rpl_length <= mid_mark:
        time_intervals = [(0, rpl_length), (0, early_mark),
                         (early_mark, rpl_length), None]

    elif 0 < rpl_length <= early_mark:
        time_intervals = [(0, rpl_length), (0, rpl_length), None, None]


    sub_dfs = [process_df[column].loc[process_df.real_time.between(*interval)]
               if interval != None else pd.DataFrame()
               for interval in time_intervals]

    return sub_dfs

# Cell

def list_attr_interval_values(df: pd.DataFrame,
                            func: Callable[[pd.DataFrame], Any],
                            df_attribute: str, rpl_length: float) -> list[Any]:
    """Lists the result of a function it receives applied to the values of
    various listed DataFrames.

    This function receives a DataFrame, splits it into sub-DataFrames based
    on various game intervals, and then applies a function to those
    intervals listing the results.

    *Args*
        - df (pandas.DataFrame)
            A DataFrame of various attributes of a replay, including those
            that must be processed.
        - func (callable)
            A function that will be applied to each interval
        - df_attribute (str)
            Name of the DataFrame's attribute (i.e. column) to which the
            function must be applied.
        - rpl_length (float)
            The duration of the Replay from which the DataFrame is
            constructed in seconds.

    *Returns*
        -  List of the return values of the function func applied to the
        various game intervals.

    """
    return [func(subdf) if not subdf.empty else None
            for subdf in gen_interval_sub_dfs(rpl_length, df, df_attribute)]

# Cell

def get_player_macro_econ_stats(rpl: sc2reader.resources.Replay,
                                pid: int)-> dict:
    """This function organises a player's major macroeconomic performance
    indicatorsinto a dictionary.

    The function uses a player's PlayerStatsEvents in a Replay object to
    calculate the player's major economic performance indicators. These
    indicators are calculated for the whole game, as well as for the early
    (first 4 minutes), mid (between minutes 4 and 8) and
    late games (paste minute 8).

    *Arguments*
        - rpl (sc2reader.resources.Replay)
                Replay object generated with sc2reader containing a match's
                data.
        - pid (int)
                A player's id number distinguishes them from the other
                players in a match. It can be extracted from a Participant
                object through the pid attribute.

    *Returns*
        - dict
            This dictionary contains the values for a player's major
            macroeconomic performance indicators. Each indicator is
            calculated for the entire game and the early, mid and late
            game intervals.
    """

    replay_info = {'replay_name': rpl.filename,
                'player_username': rpl.player[pid].name,
                'player_id': pid}

    rpl_length = rpl.length.seconds
    pstatse_complete_df = get_player_macro_econ_df(rpl, pid)

    # I use the following list of tuples to direct the generation of the
    # macroeconomic indicators based on the comluns of the replay's df.
    # Each tuple has three values:
    #   - The name used as a key to store the value in the macroeconomic
    #     stats dictionary returned by this function
    #   - The name of the indicator's column in the replay's DataFrame
    #   - The function that must be used to transform the values of the
    #     latter column in the DataFrame into a single value stored with
    #     the former key in the dictionary.

    main_indicators_params = [
                    ('unspent_minerals_avg', 'minerals_current',
                     get_subdf_mean),
                    ('unspent_vespene_avg', 'vespene_current',
                     get_subdf_mean),
                    ('unspent_resources_avg', 'unspent_rsrc',
                     get_subdf_mean),
                    ('active_workers_avg', 'workers_active_count',
                     get_subdf_mean),
                    ('mineral_collection_rate_avg',
                     'minerals_collection_rate',
                      get_subdf_mean),
                    ('vespene_collection_rate_avg',
                     'vespene_collection_rate',
                     get_subdf_mean),
                    ('resource_collection_rate_avg',
                     'rsrc_collection_rate',
                     get_subdf_mean),
                    ('army_value_avg', 'army_value', get_subdf_mean),
                    ('lost_minerals_totals', 'minerals_lost',
                     get_subdf_total),
                    ('lost_vespene_totals', 'vespene_lost',
                     get_subdf_total),
                    ('time_supply_capped', ['real_time', 'supply_capped'],
                     get_cappedTime)
                    ]

    # Run the functions to build dict
    indicator_groups = {k: list_attr_interval_values(pstatse_complete_df,
                                                     func, attr,
                                                     rpl_length)
                        for (k, attr, func)
                        in main_indicators_params}



    # Add a column for the spending qs value. This is compute separately,
    # because its values do not depend on the DataFrame, but in the
    # indicators dictionaries.
    indicator_groups['spending_qs'] = [
                    calculate_spending_coeficient(unspent, col_rate)
                    for unspent, col_rate
                    in zip(indicator_groups['unspent_resources_avg'],
                           indicator_groups['resource_collection_rate_avg'])
                    ]

    game_intervals = ['whole', 'early', 'mid', 'late']

    attr_full_list = {f'{k}_{interval}':v[game_intervals.index(interval)]
                      for k, v in indicator_groups.items()
                      for interval in game_intervals}

    replay_info.update(attr_full_list)

    return replay_info