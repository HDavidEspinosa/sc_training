# sc2readertest: Tutorial for sc2reader
> Tutorial that explores the features and characteristics of <a href='https://github.com/ggtracker/sc2reader'>sc2reader</a>


## Introduction

sc2readertest is a python library developed to document, organise and communicate the basic technical specifications and design that supports SC2 Training Grounds.

As such, I develop this library using literate and iterative programming. This means that I try to build the library while simultaneously providing a narrative explanation and documentation for this development, i.e. literate programming. In other words, "the program is its own documentation" (XXX). This approach also helps me keep a journal of the development process, which is especially useful as this library is developed as part of my creative practice PhD project. Furthermore, this methodology allows me to rapidly test and explore many features and ideas while integrating the finalised elements into the library's source code and structure.

In this case, I used nbdev to facilitate this process. This means that the library includes three components that can be explored separately or combined. First, the library was developed through a series of Jupyter notebooks. These interactive documents contain intertwined textual elements and source code, which can be consulted using jupyter lab or other IPython interpreters. Readers can read these documents if they want to explore the basic ideas in this library and the source code that compose all its functions. 
{% include tip.html content='the following link explains how to set up the Jupyter and IPython libraries to use these documents. [Jupyter/IPython Quick Start Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/)' %}
Second, the library also includes its complete documentation, where I review the development of each of its modules. I have structured this documentation as linearly as possible to reflect its development process and the structure that underlines the library. There are separate sections for each module. There, I expand on the main challenges each development stage posed. I also include the documentation developers would need to use the functions each module exports as a solution to these challenges. This documentation hides much of the implementation details of each module, which can be reviewed in the library's source code or its development jupyter notebooks. 
{% include tip.html content='this documentation can be consulted as an interactive website or a pdf document. I include both versions as appendices to my research project.' %}
Finally, this library is also exported as a traditional python library. This means that readers can find a functioning version of all the module's source code contained in the sc2readertest folder of the library. Hence, they can use source code can replicate many of the examples and prototype uses explored in the documentation.
{% include tip.html content='this library contains the same source code as the jupyter notebooks, without examples and narrative explanations.' %}
## Modules and Structure

sc2readertest has various modules that are divided into several sections. The sections respond to the general strategy proposed in SC2 Training Grounds Design Brief. 

### Section 1 Input and Data Structures

Modules 00 to 07 cover an in-depth exploration of the sc2reader library. I use this package as the primary interface to extract data from StarCraft II replays and maps as input for SC2 Training Grounds.  

### Section 2 Clustering

In modules XX to XX, I review the clustering component of SC 2 Training Grounds. This component uses the player profiles constructed with Section 1's modules to generate a player classification model based on the players' performance indicators. 

### Section 3 Classifier

The modules in this section explore how I would use supervised learning techniques to generate a classification model based on the initial cluster analysis. This model aims to allow the system to rapidly and efficiently classify players into the categories defined in the previous cluster analysis.

### Section 4 Recommender

This final section explores how the player classification can be used to generate play recommendations for the players. This recommendation's objective is to help players build and follow specific training regimes to improve their performance in StarCraft II online melee matches.
{% include warning.html content='this library is not meant as a complete implementation of the recommender system. Instead, the library has three primary objectives. First, it facilitates exploring some of the technical challenges developers and designers would face when creating a solution like the one described in the *SC2 Training Grounds Desing Brief*. Second, it helps me gauge the possibilities and limitations of the resources I am using. These, in turn, help me scope and design a more realistic interface and experience for the solution in its *User experience Design Document*. Third, as a part of a proof-of-concept, it helps me evaluate the realistic technical feasibility of this project.' %} 

## Install
{% include warning.html content='incomplete' %}
If time allows I will cover the package intallation process and a sample run of the final system in these sections 

`pip install your_project_name`

## How to use

Fill me in please! Don't forget code examples:

```
1+1
```




    2


