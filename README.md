# sc_training
> : This library is a prototype meant to facilitate the exploration of the technical feasibility, requirements, possibilities and limitations of developing an in-game recommender system for StarCraft II, i.e. SC2 Training Grounds.


```python
%load_ext autoreload
%autoreload 2
```

{% include note.html content='this prototype is mainly a tool for the reflective practice of development. This reflection is part of my PhD research project, "Encouraging Play Experience Expansion Through Machine-Learning-Based Recommendations: User-Experience Design considerations in the use of Machine-Learning-Based Recommendation System for Videogames".' %}
## Introduction

`sc_training` is a python library developed to document, organise and communicate the basic technical posibilities, specifications and design that support SC2 Training Grounds.

As such, I develop this library using literate and iterative programming. This means that I try to build the library while simultaneously providing a narrative explanation and documentation for this development, i.e. literate programming. In other words, "the program is its own documentation" (Knuth, 1984; Ramsey, 1994; Literate Programming, 2014; Kery et al., 2018). This approach also helps me keep a journal of the development process, which is especially useful as this library is developed as part of my creative practice PhD project. Furthermore, this methodology allows me to rapidly test and explore many features and ideas while integrating the finalised elements into the library's source code and structure (Howard, 2019).

In this case, I used [nbdev](https://nbdev.fast.ai/) to facilitate this process. This means that the library includes three components that can be explored separately or combined. First, the library was developed through a series of Jupyter notebooks. These interactive documents contain intertwined textual elements and source code, which can be consulted using jupyter lab or other IPython interpreters. Readers can read these documents if they want to explore the basic ideas in this library and the source code that compose all its functions. 
{% include tip.html content='the following link explains how to set up the Jupyter and IPython libraries to use these documents. [Jupyter/IPython Quick Start Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/)' %}
Second, the library also includes its complete documentation, where I review the development of each of its modules. I have structured this documentation as linearly as possible to reflect its development process and the structure that underlines the library. 
Each module's documentation includes several sections that review the main challenges I faced at each development stage. Additionally, at each document's end, there is a summary of the functions each module exports as a solution to these challenges. This summary hides much of the implementation details of each module, which readers can review in the library's source code or its development Jupyter notebooks. 
{% include tip.html content='this documentation can be consulted as an interactive website or a pdf document. I include both versions as appendices to my research project.' %}
Finally, this library is also exported as a traditional python library. This means that readers can find a functioning version of all the module's source code contained in the `sc_training` folder of the library. With this source code anyone can replicateand verify any of the examples and experiments I explore in the documentation and the notebooks.

## Modules and Structure

`sc_training` has various modules that are divided into several sections. The sections respond to the general strategy proposed in SC2 Training Grounds Design Brief. 

### Section 1 Input and Data Structures

Modules 00 to 07 cover an in-depth exploration of the [sc2reader](https://github.com/ggtracker/sc2reader) library. I use this package as the primary interface to extract data from StarCraft II replays and maps as input for SC2 Training Grounds.  

### Section 2 Clustering

In modules XX to XX, I review the clustering component of SC 2 Training Grounds. This component uses the player profiles constructed with Section 1's modules to generate a player classification model based on the players' performance indicators. 

### Section 3 Classifier

The modules in this section explore how I would use supervised learning techniques to generate a classification model based on the initial cluster analysis. This model aims to allow the system to rapidly and efficiently classify players into the categories defined in the previous cluster analysis.

### Section 4 Recommender

This final section explores how the player classification can be used to generate play recommendations for the players. This recommendation's objective is to help players build and follow specific training regimes to improve their performance in StarCraft II online melee matches.
{% include warning.html content='this library is not meant as a complete implementation of the recommender system. Instead, the library has three primary objectives. First, it facilitates exploring some of the technical challenges developers and designers would face when creating a solution like the one described in the *SC2 Training Grounds Desing Brief*. Second, it helps me gauge the possibilities and limitations of the resources I am using. These, in turn, help me scope and design a more realistic interface and experience for the solution in its *User experience Design Document*. Third, as a part of a proof-of-concept, it helps me evaluate the realistic technical feasibility of this project.' %} 

## Setup

As a prelude to the exploration in the following modules, I will like to clarify some aspects of the composition of this document for brevity's and clarity's sake. 

In every case, when I start developing one of this library's modules, I have to include some setup elements at the beginning of each document. Since this process is almost identical in most cases, I will cover it here so that I can hide it in the module's documentation.
{% include note.html content='Remember that any elements that I may hide in these documents can still be consulted and verified in the library&#8217;s development notebooks and the library&#8217;s exported source code.' %}The development of all modules starts with two elements: importing the module's dependencies and loading the development tests and sample data.

Importing the module's dependencies means invoking several libraries used by the modules. The following is an example of these imports.

```python
# This are some of the common libraries for this library's
# development.

# These are some of the libraries of Python's standard library 
# I use to support differnt functionalities. 
from pathlib import Path
from pprint import pprint
from dataclasses import dataclass, astuple, field
from datetime import datetime
from typing import *

# I use the following libries to load and manage data files. 
import csv
import json

# Pymongo allows me to interact with a local MongoDB client to 
# store and manage my document-based database.
import pymongo

# The following libraries offer various utilities for efficient
# data and numeric manipulation, and for data visualisation.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sklearn # Depending on the module I use different modules of
               # scikit-learn library.


# sc2reader facilitates data extraction from replay files
import sc2reader
```

Additionally, to develop each module, I need to load some StarCraft II replay files (marked with the .SC2Replay extension). The game generates these files to store all relevant configuration and game-play information necessary to rebuild and reproduce a match. 

The replays used to test and develop this project are extracted from publicly available datasets. In no case do I access any personal or private information of the users or players. These data sets have been collected using Blizzards developer's API and their client protocol (SC2client-proto), which only gathers them with the express authorisation of the users. The following code illustrates how they are loaded using sc2reader and collected into variables that store `sc2reader.resources.Replay` objects for later processing. I store this data in the library's test_replays folder.
{% include tip.html content='One can load one replay at a time using the `sc2replays.load_replay(<str_file_path>)` method.' %}

```python
# This code sets up the notebook's sample replay.
rps_path = Path(Path.cwd()/'test_replays') \
           if Path('test_replays').exists() \
           else Path('../test_replays')
game_path = str(rps_path/'Jagannatha LE.SC2Replay')
single_replay = sc2reader.load_replay(game_path)
single_replay
```




    <sc2reader.resources.Replay at 0x16af5961d90>



{% include tip.html content='Alternatively, one can use the sc2replays.load_replays(<str_dir_path>) method, which returns a generator of replay objects.' %}

```python
replays = sc2reader.load_replays(str(rps_path))
replays
```




    <generator object SC2Factory.load_all at 0x0000016AF5C2CC10>



Beyond these two initial setup elements, some modules also load data files that store helpful information to organise and configure the modules and their functions. These data files are stored in the library's data folder. The code below illustrates how I load some of these files. 

```python
data_path = Path(Path.cwd()/'data') \
            if Path('data').exists() \
            else Path('../data')

with open(data_path/'unit_names.csv') as f:
    file_reader = csv.reader(f)
    unit_names = next(file_reader)
    
with open(data_path/'changes_names.csv') as f:
    file_reader = csv.reader(f)
    change_names = next(file_reader)
    
with open(data_path/'army_list.json') as f:
    race_armies = json.load(f)

with open(data_path/'buildings_list.json') as f:
    race_buildings = json.load(f)

with open(data_path/'upgrades.json') as f:
    race_upgrades = json.load(f)
```

## Install
{% include warning.html content='THE FOLLOWING 2 SECTIONS ARE INCOMPLETE PLACEHOLDERS. PLEASE DISREGARD FOR NOW' %}
If time allows I will cover the package intallation process and a sample run of the final system in these sections 
{% include note.html content='This is a test quote' %}

`pirpi install sc_traing`

## How to use

Fill me in please! Don't forget code examples:

```python
# This are this module's dependencies.
from pathlib import Path
from pprint import pprint
from dataclasses import dataclass, astuple, field
from datetime import datetime
from typing import *


import sc2reader

```

```python
# This code sets up the notebook's sample replay.
rps_path = Path("./test_replays")
game_path = str(rps_path/"Jagannatha LE.SC2Replay")
single_replay = sc2reader.load_replay(game_path)
single_replay
```




    <sc2reader.resources.Replay at 0x213d3d617f0>



```python
p1 = single_replay.player[1]
```

```python
p1.units[:5]
```




    [BeaconArmy [2640001],
     BeaconDefend [2680001],
     BeaconAttack [26C0001],
     BeaconHarass [2700001],
     BeaconIdle [2740001]]



```python
from nbdev.export import notebook2script
notebook2script()
```

    Converted 00_summarise_rpl.ipynb.
    Converted 01_handle_tracker_events.ipynb.
    Converted 02_macro_econ_parser.ipynb.
    Converted 03_build_parser.ipynb.
    Converted index.ipynb.

