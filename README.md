# sc_training
> This library is a prototype meant to facilitate the exploration of the technical feasibility, requirements, possibilities and limitations of developing an in-game recommender system for StarCraft II, i.e. SC2 Training Grounds.


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

## Install
{% include warning.html content='THE FOLLOWING 2 SECTIONS ARE INCOMPLETE PLACEHOLDERS. PLEASE DISREGARD FOR NOW' %}
If time allows I will cover the package intallation process and a sample run of the final system in these sections 

`pirpi install sc_traing`

## How to use

Fill me in please! Don't forget code examples:

```
1+1
```




    2


