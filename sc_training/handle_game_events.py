# AUTOGENERATED! DO NOT EDIT! File to edit: 05_handle_game_events.ipynb (unless otherwise specified).

__all__ = ['data_path']

# Internal Cell

# Load Module's dependencies

from pathlib import Path
from pprint import pprint
from typing import *

import json
import fastcore.test as ft

import sc2reader

# Cell
data_path = (Path(Path.cwd()/'data')
             if Path('data').exists() else Path('../data'))

with open(data_path/'ability_list.json') as af:
    ab_lists = json.load(af)