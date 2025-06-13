# SHARAD Data processing
**Author**: Jordy Dal Corso, RSLab, University of Trento, Italy.

For questions about the code or collaboration inquiries please send an email to jordy.dalcorso@unitn.it.
You are very welcome to improve the code!

This repository contains notebook and scripts that replicate part of the processing done by the SHARAD teams to obtain interpretable radargrams.
In particular we do:
* Range compression as the Italian SHARAD team
* Azimuth compression, comprising range cell migration, as the US SHARAD team.
Dependencies are python, numpy, matplotlib.

## Notebooks
There are the following notebooks in the repository:
* `get_data.ipynb`, which contains a minimal example to extract the raw radargram and topography from SHARAD EDR files.
* `concatenate.ipynb`, which contains cells useful to process raw data from Mars ODE and convert it to numpy arrays
* `range_compression.ipynb`, where range compression is performed and an output .npy file is produced and eventually saved. There is also a torch version of this notebook.
* `azimuth_compression.ipynb`, where azimuth compression is performed. 

## Scripts
Scripts follow the same topics of notebooks but are organized as .py files with parser so that they can be used and modified for a broader purpose. They 
do not aim at computational speed and their objective is to reproduce the range and azimuth processing of radar sounder data.
Scripts are:
* `range.py`, which given raw data in .npy format performs range compression and outputs a range compressed product in .npy format
* `azimuth.py`, which given a range compressed data in .npy format performs range cell migration and azimuth compression

In this way we are implicitly applying the so called Range-Doppler algorithm to perform SAR processing on radar sounder data, which decouples the processing in range and azimuth direction.

We also provide a `launch.sh` that performs processing and requires minimal modifications (the chirp data path), provided that the raw_data.npy and topo.npy have been obtained already (e.g. via notebooks). You can use this script with:

    bash launch.sh <base_folder> [-r,-a]

where `base_folder` is the folder containing all the files without / at the end, `-r` means "compute range compression only", `-a` means "compute azimuth compression only".

Note that **python scripts are slightly more updated than the notebooks** in this repository.

## Data
We provide no data in the repository. The input data format accepted by notebooks and scripts is explicitly stated in the code. Users should eventually modify 
data paths, input and output folders.
You can find raw SHARAD EDR data at [MARS ODE](https://ode.rsl.wustl.edu/mars/index.aspx). Select either Map Search or Data Product Search and look for SHARAD->RAW->EDR.
You can find chirp files for SHARAD at different TX and RX temperatures [here](https://pds-geosciences.wustl.edu/mro/mro-m-sharad-4-rdr-v1/mrosh_1001/calib/).

## Docker
We provide a minimal `dockerfile` and a file `launch_docker.sh` to build and run a container to use the code.
One should just run:

    bash launch_docker.sh <name> <tag>

choosing a name and a tag for the container, and then operate into it (likely in interactive mode). The container contains
a minimal version of Python with numpy and matplotlib. Also ipykernel is installed but notebooks within the container have
not been tested yet, and torch is not yet supported.

## What is missing
Regarding data acquisition, we could add routines to extract way more information from the .dat file, exploiting all the files contained in a particular EDR product folder 
(e.g. [this](https://ode.rsl.wustl.edu/mars/indexproductpage.aspx?product_id=E_0814901_001_SS19_700_A&product_idGeo=26442095)). 
One could, for example, select the correct reference chirp based on TX/RX temperature extracted from ancillary files. Many other ancillary information would help data processing.

Regarding processing, we do not perform chirp scaling as azimuth processing (which is performed by the ITA SHARAD team). Moreover we do not apply any phase correction
to compensate the effect of the ionosphere on acquisitions (which is a game changer in terms of output data quality, see e.g. Campbell et al. 2011). We also do not perform
range migration and azimuth compression taking into account the different positions in range direction. One should have a different RCMC and azimuth reference function
for each range position.

Finally few modifications to the `azimuth.py` arguments should be made in order to process the data with a given aperture (in seconds) and in the given window. The amount of columns processed by `azimuth.py` is currently represented by two arguments (start and end columns) while one may prefer to process the whole radargram. Be careful with choosing these column extrema as the first aperture window is centered in the first column index (same goes for the last one), hence if the aperture goes out of bound (e.g by choosing the starting column as column zero) the script will throw an error.