# Group-Project-Sequence
[![CI](https://github.com/jufischi/Group-Project-Sequence/actions/workflows/main.yml/badge.svg)](https://github.com/jufischi/Group-Project-Sequence/actions/workflows/main.yml)

This repository contains the source code and the LaTeX documents for the 2022/23 winter term group project of the Bioinformatics masters program of the University of Tübingen.

The goal is to reproduce the results of [Reimering et al](https://github.com/hzi-bifo/Phylogeography_Paper), that is, to reproduce the geographic origins of the 2009 H1N1 influenca A pandemic using Sankoff's algorithm for parsimony.

## Organization
This repository is organized as follows:

- the `data` folder is a placeholder for all data that is needed as input or computet as output by the scripts and algrorithms in this repo. Do not put data their manually as it will be overwritten.
- the `src` folder contains all scripts that are needed to download the data, perform the computation and render the results.
- the `doc` folder contains the LaTeX documentation of this project.

## Getting started
### Required Software
This project requires Python >= 3.7 as well as the following packages: 
- requests
- numpy
- geopandas
- matplotlib
- pycountry
- airportsdata

### Downloading the data
To calculate the geographic origins of the pandemic, some data is needed, i.e. a phylogenetic tree that describes the relations between different samples of H1N1, a mapping that lists at which airport the samples were taken as well as distance matrices that describe the geographic (or effective) distances between various airports. You can obtain that data by executing 

```
$ python3 ensure_data.py --clean --download
```
from within the `src` folder. This will download the corresponding data into the `data` folder.

### Calculating the tree labels
To calculate the labels for the internal nodes of the input tree, i.e. to find plausible geographic locations of the common ancestors of the samples, you can execute

```
$ python3 phylogeographics.py
```
This will calculate four different internal labellings using four different distance matrices and store them in the `data` folder. After each tree is calculated, a image is rendered to plot the geographic spread onto the world map. The trees are not re-calculated if there exists already a copy of that tree in the `data` folder.
