# Stream and valley sedimentation survey transect data analysis

[![Release version](https://img.shields.io/badge/Release-1.0.0-brightgreen)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Python version](https://img.shields.io/badge/python-3.10.4-yellow)](https://www.python.org/downloads/release/python-3104/)
[![Progress](https://img.shields.io/badge/Progress-Complete-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Update frequency](https://img.shields.io/badge/Updates-as--needed-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main)
[![License](https://img.shields.io/badge/License-MIT-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main/LICENSE)

## Background

These programs were developed to augment and analyze floodplain transect data collected in Minnesota's Whitewater River Valley (U.S.), between 1939 and 1994, through (1) geospatial digitization, (2) derivative calculations, and (3) statistical tests. 

<img width="561.25" height="302.25" align="right" alt="2_3_8plots" src="https://github.com/user-attachments/assets/df71b17f-f69c-4efa-be20-82a849f75460" />

The historical data was collected by federal agencies during stream and valley sedimentation surveys aimed at investigating accelerated erosion and deposition and/or increased flooding in the basin; this dataset is inherently geomorphic in nature so these programs pursue analyses primarily of interest to the earth scientist. 

All data associated with this project has been published by Wood et al. (2025a) and is described in Wood et al. (2025b; in development). 

The hillslope-floodplain-channel cross-section to the right displays the kind of transect data these programs operate on—topographic surface profiles (i.e., elevation data).

This repository (analysis-whitewater-basin-mn-sedimentation-surveys-jjwood) includes 4 programs:
- **transect_cogo_digitizer.py:** Performs coordinate geometry (COGO) calculations to digitize tabular transect elevation data into GIS files.
- **transect_sed_rate_calculator.py:** Calculates mean transect elevation change rates between successive elevation datasets to measure topographic change.
- **transect_sed_rate_statistics.py:** Performs Analysis of Variance (ANOVA) hypothesis testing suites to compare mean elevation change rates over the time interval represented in this dataset—1855–1994.
- **transect_analysis_functions.py:** Houses the user-defined functions (UDFs) executed in the previous programs.

We will briefly describe how to use each program. Retreive and use the input data files from Wood et al. (2025a) as you follow along. The relevant files are identified in screenshots below.

## transect_cogo_digitizer.py
[![GeoPandas version](https://img.shields.io/badge/geopandas-1.1.0-yellow)](https://pypi.org/project/geopandas/1.1.0/)
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General

The maps below highlight this program's function. The left one displays a transect's GNSS surveyed monuments (cyan circles) and the transect's trace extending between them, for reference. This program takes information about the monuments' position and a table of elevation data and yields what is displayed in the right map, the transect trace populated with elevation measurements (magenta circles). The program's output is a GeoPackage of elevation point layers grouped by data year.

<img width="6781" height="3474" alt="Digitizer1" src="https://github.com/user-attachments/assets/f03cc682-5fc8-4c56-8c2a-f0165f1a5ea3" />

### Initialization

<img width="665" height="301" align="right" alt="Screenshot 2025-08-28 at 2 20 52 PM" src="https://github.com/user-attachments/assets/a3699570-c97c-4ef8-90d8-01dfe2ca18e8" />

In the same location as the digitizer program, create a new folder named *'Input'* where you will store the code's required input files. 
There are three:
1. The elevation data,
2. Monument/reference coordinate data,
3. And reference coordinate metadata.

Each is converted into a pandas DataFrame at the end of the *Initialization* section to enable their manipulation.

Also, set the names of your output GIS files.

<img width="665" height="239" align="right" alt="Screenshot 2025-08-28 at 2 47 31 PM" src="https://github.com/user-attachments/assets/a2db389b-80c2-4528-9f6a-7e8c022b9d84" />

Lastly, you'll need to set the program's spatial operational limits and the coordinate reference system (CRS) of the output GeoPackage.

*TRANSECT_NUM_START* and *TRANSECT_NUM_END*, together, determine which transect datasets are digitized. Their input is a *transect number*, an integer ID that provides a convenient framework for looping the digitizer through each transect. (two different numbers must be set for the loop to function). Starting at *1* and an ending at *107* will digitize every transect elevation dataset.

Declare the *CRS* with its unique EPSG (European Petroleum Survey Group) code. *'EPSG:26915'* sets the *CRS* to NAD83 / UTM zone 15N for Minnesota.

### Data operations

Calculate station coordinate geometry

Prepare data for digitization

Digitize data
&#8202;
# end

## transect_sed_rate_calculator.py
*include example figure of calculation*
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

## transect_sed_rate_statistics.py
*include example figure of test result*
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)
[![pingouin version](https://img.shields.io/badge/pingouin-0.5.5-brightgreen)](https://pypi.org/project/pingouin/0.5.5/)
[![scikit-posthocs version](https://img.shields.io/badge/scikit--posthocs-0.11.4-brightgreen)](https://pypi.org/project/scikit-posthocs/)
[![SciPy version](https://img.shields.io/badge/scipy-1.15.3-yellow)](https://pypi.org/project/scipy/1.15.3/)
[![statsmodels version](https://img.shields.io/badge/statsmodels-0.14.4-brightgreen)](https://pypi.org/project/statsmodels/)

## transect_analysis_functions.py

[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

## General information

**Documentation date:** 20250828

**Date finalized:** 20250703

**Author:** Jimmy J. Wood
- Institution: University of Minnesota Twin Cities (UMN), Saint Anthony Falls Laboratory
- Email: <jimmyjwood24@gmail.com>
- ORCID: 0009-0009-7263-433X

**Related publications**
- **Wood, J. J.,** Svien, L., Christianson, D. & Claas, L. Historical stream and valley sedimentation survey data for the Whitewater River Valley, Minnesota, United States (1855–1994). *University of Minnesota Twin Cities Data Repository for U of M* https://doi.org/10.13020/2ggx-qk28 (2025a).
- **Wood, J. J.,** Wickert, A. D., Larson, P. H. & Svien, L. A 140-year record of stream and valley sedimentation in the Whitewater River Valley, Minnesota, United States. (2025b). [In development].
  
**Funding sources**
- Legislative-Citizen Commission on Minnesota Resources (LCCMR) Environment and Natural Resources Trust Fund (ENTRF) grant 2022-163.
- National Science Foundation grant 1944782.
- UMN College of Science & Engineering Inclusion Fellowship.
