# SHARAD Data processing
**Author**: Jordy Dal Corso, RSLab, University of Trento, Italy.

For questions about the code or collaboration inquiries please send an email to jordy.dalcorso@unitn.it.

This repository contains notebook and scripts that replicate part of the processing done by the SHARAD teams to obtain interpretable radargrams.
In particular we do:
* Range compression as the Italian SHARAD team
* Azimuth compression, comprising range cell migration, as the US SHARAD team.
Dependencies are python, numpy, matplotlib.

## Notebooks
There are three notebooks in the repository:
* `concatenate.ipynb`, which contains cells useful to process raw data from Mars ODE and convert it to numpy arrays
* `range_compression.ipynb`, where range compression is performed and an output .npy file is produced and eventually saved
* `azimuth_compression.ipynb`, where azimuth compression is performed. 

## Scripts
Scripts follow the same topics of notebooks but are organized as .py files with parser so that they can be used and modified for a broader purpose. They 
do not aim at computational speed and their objective is to reproduce the range and azimuth processing of radar sounder data.
Scripts are:
* `range.py`, which given raw data in .npy format performs range compression and outputs a range compressed product in .npy format
* `azimuth.py`, which given a range compressed data in .npy format performs range cell migration and azimuth compression

In this way we are implicitly applying the so called Range-Doppler algorithm to perform SAR processing on radar sounder data, which decouples the processing
in range and azimuth direction.

## Data
We provide no data in the repository. The input data format accepted by notebooks and scripts is explicitly stated in the code. Users should eventually modify 
data paths, input and output folders.

## What is missing
First of all, we do not perform chirp scaling as azimuth processing (which is performed by the ITA SHARAD team). Moreover we do not apply any phase correction
to compensate the effect of the ionosphere on acquisitions (which is a game changer in terms of output data quality, see e.g. Campbell et al. 2011). We also do not perform
range migration and azimuth compression taking into account the different positions in range direction. One should have a different RCMC and azimuth reference function
for each range position.