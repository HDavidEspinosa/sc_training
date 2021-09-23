# SC2 Training Grounds - Technical Specifications Document



This document explores the technical back-end design for SC2 Training Grounds. It also functions as the development environment for `sc_training`, a prototype Python library that demonstrates parts of a high-level implementation of this design. 
{% include note.html content='this prototype is primarily meant as a tool for reflective practice. This reflection is part of my PhD research project, "Encouraging Play Experience Expansion Through Machine-Learning-Based Recommendations: User-Experience Design considerations in the use of Machine-Learning-Based Recommendation System for Video games".' %}

## Executive Summary

`sc_training` is a python library developed to document, organise and communicate the design of *SC2 Training Grounds'* computer model. The goals of this library's development are:
1. To review the technical challenges associated with the creation of a solution such as *SC2 Training Grounds*.
2. To assess the possibilities and limitations of the resources that could be used to develop this solution. Therefore, allowing me to design a more realistic and grounded user experience for the application. 
3. To provide a proof-of-concept that tests the technical feasibility of the project.

I developed this library using literate and iterative programming. In other words, I built it while simultaneously providing a narrative explanation and documentation of its development (Knuth, 1984; Ramsey, 1994; Literate Programming, 2014; Kery et al., 2018). This methodology allows for the rapid testing exploration of ideas while integrating them into a functioning program (Howard, 2019). Hence, the library is simultaneously the program's documentation and the program itself.
{% include tip.html content='I used [nbdev](https://nbdev.fast.ai/) to facilitate this process. The use of this tool means that this document includes three components that can be explored separately or combined.  **First**, the library was developed through a series of [Jupyter notebooks](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/). These interactive documents contain intertwined textual elements and source code that describe the ideas that support this library and the source code that compose its functions. The static version of these documents is included as a pdf appendix to the PhD project. Meanwhile, the interactive documents can be consulted using jupyter lab or other IPython interpreters (a guide to set up the Jupyter and IPython libraries to use these documents: [Jupyter/IPython Quick Start Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/)). **Second**, the library is also exported as a traditional python library. Readers can find a functioning version of all the module&#8217;s in the `sc_training` folder of the library. Readers can use this code to replicate and verify any examples and experiments explored in the documentation and the notebooks. **Third**, these notebooks produce a website that serves as the library&#8217;s [Interactive Documentation](https://hdavidespinosa.github.io/sc_training/). This documentation omits many technical details focusing on the descriptions of the development process and the library&#8217;s structure.' %} 

## Setup
Before going into the document itself it is important to clarify some aspects of the composition. 

Because of the nature of the documents, each notebook is exported as a module of the `sc_training` library. 

Meanwhile, since each notebook works as a separate module, I have to include some setup elements at the beginning of each document. Since this process is almost identical in most cases, I will cover it here so that I can hide it in the module's documentation.
{% include note.html content='Remember that any elements that I hide in these documents can still be reviewed and verified in the library&#8217;s development notebooks and the library&#8217;s exported source code.' %}
The development of all modules starts with two elements: importing the module's dependencies and loading the development tests and sample data.

Importing the module's dependencies means invoking several libraries used by each module. The following is an example of these imports.

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




    <sc2reader.resources.Replay at 0x239dec65e80>



{% include tip.html content='Alternatively, one can use the sc2replays.load_replays(<str_dir_path>) method, which returns a generator of replay objects.' %}

```python
replays = sc2reader.load_replays(str(rps_path))
replays
```




    <generator object SC2Factory.load_all at 0x00000239E4F4C120>



Beyond these two initial setup elements, some modules also load data files that store helpful information to organise and configure the modules and their functions. These data files are stored in the library's data folder. The code below illustrates how I load some of these files. 

```python
data_path = Path(Path.cwd()/'data') \
            if Path('data').exists() \
            else Path('../../data')

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

## Exportable functions

In each module, I include a section where I compile all the exportable functions that respond to the challenges summarise by each module. Once exported, other modules can call these functions by importing the module that exported them in the first place.

For example, in the following code, I demonstrate how to call the `get_replay_info` function from the `summarise_rpl` module (see <<Chapter 1 - Summarising Replays>>).

```python
from sc_training.summarise_rpl import *

#Note that get_replay_info is defined in the summarise_rpl module.
replay_data = get_replay_info(single_replay)
print(replay_data)
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    ~\AppData\Local\Temp/ipykernel_38380/3927205414.py in <module>
    ----> 1 from sc_training.summarise_rpl import *
          2 
          3 #Note that get_replay_info is defined in the summarise_rpl module.
          4 replay_data = get_replay_info(single_replay)
          5 print(replay_data)


    ModuleNotFoundError: No module named 'sc_training.summarise_rpl'


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




    <sc2reader.resources.Replay at 0x1bed12e7e50>



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



## References

- Howard, J. (2019) nbdev: use Jupyter Notebooks for everything fast.ai, fast.ai. Available at: https://www.fast.ai/2019/12/02/nbdev/ (Accessed: 8 July 2021).
- Kery, M. B. et al. (2018) 'The Story in the Notebook', in Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems. New York, NY, USA: ACM, pp. 1-11. doi: 10.1145/3173574.3173748.
- Knuth, D. E. (1984) 'Literate Programming', The Computer Journal, 27(2), pp. 97-111. doi: 10.1093/comjnl/27.2.97.
- Literate Programming (2014) WikiWiki. Available at: https://wiki.c2.com/?LiterateProgramming (Accessed: 6 July 2021).
- Ramsey, N. (1994) 'Literate programming simplified', IEEE Software, 11(5), pp. 97-105. doi: 10.1109/52.311070.
