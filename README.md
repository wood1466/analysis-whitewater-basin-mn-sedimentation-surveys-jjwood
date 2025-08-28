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

All data associated with this project has been published by Wood et al. (2025a) and is described in Wood et al. (2025b; manuscript in development). 

The hillslope-floodplain-channel cross-section to the right displays the kind of transect data these programs operate on—topographic surface profiles (i.e., elevation data).

This repository (analysis-whitewater-basin-mn-sedimentation-surveys-jjwood) includes 4 programs:
- **transect_cogo_digitizer.py:** Performs coordinate geometry (COGO) calculations to digitize tabular transect elevation data into GIS files.
- **transect_sed_rate_calculator.py:** Calculates mean transect elevation change rates between successive elevation datasets to measure topographic change.
- **transect_sed_rate_statistics.py:** Performs Analysis of Variance (ANOVA) hypothesis testing suites to compare mean elevation change rates over the time interval represented in this dataset—1855–1994.
- **transect_analysis_functions.py:** Houses the user-defined functions (UDFs) executed in the previous programs.

We will briefly describe each program.

## transect_cogo_digitizer.py
[![GeoPandas version](https://img.shields.io/badge/geopandas-1.1.0-yellow)](https://pypi.org/project/geopandas/1.1.0/)
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

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
- **Wood, J. J.,** Wickert, A. D., Larson, P. H. & Svien, L. A 140-year record of stream and valley sedimentation in the Whitewater River Valley, Minnesota, United States. (2025b). [Manuscript in development].
  
**Funding sources**
- Legislative-Citizen Commission on Minnesota Resources (LCCMR) Environment and Natural Resources Trust Fund (ENTRF) grant 2022-163.
- National Science Foundation grant 1944782.
- UMN College of Science & Engineering Inclusion Fellowship.
