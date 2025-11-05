# Stream and valley sedimentation survey transect data analysis

[![Release version](https://img.shields.io/badge/Release-1.0.0-brightgreen)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Python version](https://img.shields.io/badge/python-3.10.4-yellow)](https://www.python.org/downloads/release/python-3104/)
[![Progress](https://img.shields.io/badge/Progress-Complete-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Update frequency](https://img.shields.io/badge/Updates-as--needed-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main)
[![License](https://img.shields.io/badge/License-MIT-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main/LICENSE)

## Background

These programs were developed to augment and analyze topographic floodplain transect data collected in Minnesota's Whitewater River Valley (U.S.), between 1939 and 1994, through (1) geospatial digitization, (2) derivative calculations, and (3) statistical tests.

<img width="561.25" height="302.25" align="right" alt="2_3_8plots" src="https://github.com/user-attachments/assets/df71b17f-f69c-4efa-be20-82a849f75460" />

The historical data was collected by federal agencies during stream and valley sedimentation surveys aimed at investigating accelerated erosion and deposition and/or increased flooding in the basin; this dataset is inherently geomorphic in nature so these programs pursue analyses primarily of interest to the earth scientist. 

All data associated with this project has been published by Wood et al. (2025a) and is described in Wood et al. (2025b; in development). 

The hillslope–floodplain–channel cross-section to the right displays the kind of transect data these programs operate on—surface profiles (i.e., elevation data).

This repository (analysis-whitewater-basin-mn-sedimentation-surveys-jjwood) includes 4 programs:
- **transect_cogo_digitizer.py:** Performs coordinate geometry (COGO) calculations to digitize tabular transect elevation data into GIS files.
- **transect_sed_rate_calculator.py:** Calculates mean transect elevation change rates between successive elevation datasets to measure topographic change.
- **transect_sed_rate_statistics.py:** Performs Analysis of Variance (ANOVA) hypothesis testing suites to compare all mean elevation change rates over the time interval represented in this dataset—1855–1994.
- **transect_analysis_functions.py:** The user-defined functions (UDFs) executed in the other programs.

We will briefly describe how these programs operate and how to use them; see the programs' line comments for in depth descriptions of their contents. Retreive and use the input data files from Wood et al. (2025a) as you follow along. The relevant files per program will be identified by screenshot.

## transect_cogo_digitizer.py
[![GeoPandas version](https://img.shields.io/badge/geopandas-1.1.0-yellow)](https://pypi.org/project/geopandas/1.1.0/)
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General

The maps below highlight this program's function. The left one—starting condition—displays a transect's GNSS surveyed monuments (cyan circles) and the transect's trace extending between them (dashed line). The right map—post-run condition—displays that transect trace populated with elevation measurements (magenta circles). This program compares the monuments' and elevations' positional data to calculate coordinates for the elevation data (Easting, Northing [m]). Its output is a GeoPackage of elevation point layers grouped by data year—1855, 1939, 1965, 1975, 1978, and 1994 for the Whitewater data.

<img width="6781" height="3474" alt="Digitizer1" src="https://github.com/user-attachments/assets/f03cc682-5fc8-4c56-8c2a-f0165f1a5ea3" />

### Initialization

<img width="665" height="301" align="right" alt="Screenshot 2025-08-28 at 2 20 52 PM" src="https://github.com/user-attachments/assets/a3699570-c97c-4ef8-90d8-01dfe2ca18e8" />

In the same location as the digitizer program, create a new folder named *'Input'* where you will store the code's required input files. 
There are three:
1. The elevation data,
2. monument/reference coordinate data,
3. and reference coordinate metadata.

Each is converted into a pandas DataFrame at the end of the *Initialization* section to enable program manipulation.

Also, set the names of your output GIS files: *GPKG_NAME* and *LAYER_NAME1_PRE*.

Output folders are automatically created at the end of the *Initialization* section.

<img width="665" height="239" align="right" alt="Screenshot 2025-08-28 at 2 47 31 PM" src="https://github.com/user-attachments/assets/a2db389b-80c2-4528-9f6a-7e8c022b9d84" />

Lastly, you'll need to set the program's spatial operational limits and the coordinate reference system (CRS) of the output GeoPackage.

*TRANSECT_NUM_START* and *TRANSECT_NUM_END*, together, determine which transect datasets are digitized. Their input is a *transect number*, an integer ID that provides a convenient framework for looping the digitizer through each transect. (Two different numbers must be set for the loop to function). Starting at *1* and an ending at *107* will digitize every Whitewater transect elevation dataset.

Declare the *CRS* with its unique EPSG (European Petroleum Survey Group) code. *'EPSG:26915'* sets the *CRS* to *NAD83 / UTM zone 15N* for Minnesota.

### Data operations

<img width="647" height="161" align="right" alt="Screenshot 2025-08-29 at 12 08 43 PM" src="https://github.com/user-attachments/assets/fc8dd66f-50cd-4d8e-a7e2-54181efbebba" />

This section begins the digitization loop at your starting transect. First it begins slicing through your three starting DataFrames to select the data required to complete the COGO calculations:
1. The survey stations (measurement positions) of the first elevation dataset,
2. the transect monuments' cartesian coordinate pairs,
3. and the station/position of the first, or survey start, monument.

(All DataFrame slicing is accomplished with UDFs, as shown.)

<img width="656" height="300" align="right" alt="Screenshot 2025-08-29 at 12 53 33 PM" src="https://github.com/user-attachments/assets/65468943-a5fc-4a23-af77-b27a45d11163" />

Second, the program consults a UDF to check if the monument coordinates must be replaced by synthetic reference coordinates. 

Typically, transects in the Whitewater Watershed extend in a line directly between (and often beyond) its two monuments. On the left map below, this is labeled the *expected trace*. Occassionally, monuments were shifted off of the actual line, the *measured trace*. In this example, the monument was established 10 ft East of the measured transect. 

<img width="6781" height="3474" alt="Digitizer2" src="https://github.com/user-attachments/assets/2a631dcb-6f9e-4aa8-b27a-136c8a4abb1f" />

To compensate for these shifts, the program first compares a monument's estimated coordinate accuracy to its shift magnitude. On the right map, the cyan buffer corresponds to an *XY accuracy* of 0.25 m and the yellow buffer to a *shift radius* of 3 m (10 ft). The *shift radius* does not lie within the *XY accuracy* buffer (i.e., *XY accuracy*<*shift radius*); therefore, the horizontal resolution of the GNSS coordinates are capable of meaningfully representing a locational shift of 3 m. 

With that being the case, the program calculates a new pair of synthetic reference coordinates via COGO. Here, the monument's X (Easting) coordinate is reduced by 3 m (10 ft) and its Y (Northing) coordinate remains the same. Subsequent digitization places the elevation data on the *measured trace*. 

(This program does not compensate for composite directional shifts [i.e., *NW*, *Upstream*, etc.].) 

With the requisite data selected, a message displays which dataset will be digitized by identifying the transect ID and elevation data year.

<img width="639" height="97" alt="Screenshot 2025-08-29 at 9 59 26 AM" src="https://github.com/user-attachments/assets/ded0d0fc-ea56-4c7e-a873-61f69b24a8af" />

&#8202;

To perform its COGO calculations the program takes the three data components selected previously and first calculates:

1. the transect azimuth between monuments (*θ*),
2. and the distance between each elevation station and the starting monument (*r*, for the example below).  

<img width="512.5" height="3475" align="right" alt="Digitizer3" src="https://github.com/user-attachments/assets/3e2b6e7f-feaf-4ab3-9065-625186ba7234" />

With a cartesian coordinate system, *θ*, in general, can be calculated with,

$θ = tan\biggl(\frac{x2-x1}{y2-y1}\biggr)^{-1}$,

where *(x1, y1)* and *(x2, y2)* are the starting and ending coordinates, respectively.

Each *r<sub>i</sub> = elevation station<sub>i</sub> - starting monument station*.

The program then calculates the component displacements North (*Δy*) and East (*Δx*) required to travel an *r<sub>i</sub>* length down the transect to the elevation station. Its subsequent coordinates are:

*Northing<sub>i</sub> = Δy + y1*,

and *Easting<sub>i</sub> = Δx + x1*.

The newly calculated elevation coordinates are compiled and appended onto the input elevation DataFrame to use the points' precompiled metadata as attribute fields and values.

Lastly, the DataFrame is converted into a GeoPandas GeoDataFrame with the preselected *CRS*.

When the message below is visible, your output GeoPackage is stored in a folder named *GIS*. 

&#8202;
<img width="624" height="51" alt="Screenshot 2025-08-29 at 4 18 46 PM" src="https://github.com/user-attachments/assets/226512e1-3446-4413-9c64-dda8a643e587" />

## transect_sed_rate_calculator.py
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General

<img width="640" height="480" align="right" alt="2_3_rateplots" src="https://github.com/user-attachments/assets/287b5414-4637-4c8d-bb7b-46abb547f28f" />
<img width="436" height="360" align="right" alt="Screenshot 2025-09-09 at 6 41 24 PM" src="https://github.com/user-attachments/assets/cb0794c9-92d8-4593-99e1-45cf5dbc3b71" />

The maps below highlight this program's function. The left one displays a transect's GNSS surveyed monuments (cyan circles) and the transect's trace extending between them (dashed line)—the starting condition. The right map displays that transect trace populated with elevation measurements (magenta circles)—the post-run condition. This program compares the monuments' and elevations' positional data to calculate coordinates for the elevation data (Easting, Northing [m]). Its output is a GeoPackage of elevation point layers grouped by data year—1855, 1939, 1965, 1975, 1978, and 1994 for the Whitewater data.


### Initialization

### Data operations

## transect_sed_rate_statistics.py
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)
[![pingouin version](https://img.shields.io/badge/pingouin-0.5.5-brightgreen)](https://pypi.org/project/pingouin/0.5.5/)
[![scikit-posthocs version](https://img.shields.io/badge/scikit--posthocs-0.11.4-brightgreen)](https://pypi.org/project/scikit-posthocs/)
[![SciPy version](https://img.shields.io/badge/scipy-1.15.3-yellow)](https://pypi.org/project/scipy/1.15.3/)
[![statsmodels version](https://img.shields.io/badge/statsmodels-0.14.4-brightgreen)](https://pypi.org/project/statsmodels/)

### General

### Initialization

### Data operations

## transect_analysis_functions.py

[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

## General information

**Documentation date:** 20250829

**Date finalized:** 20250703

**Author:** Jimmy J. Wood
- Institution: University of Minnesota Twin Cities, Saint Anthony Falls Laboratory
- Email: <jimmyjwood24@gmail.com>
- ORCID: 0009-0009-7263-433X

**Related publications**
- **Wood, J. J.,** Svien, L., Christianson, D. & Claas, L. Historical stream and valley sedimentation survey data for the Whitewater River Valley, Minnesota, United States (1855–1994). *University of Minnesota Twin Cities Data Repository for U of M* https://doi.org/10.13020/2ggx-qk28 (2025a).
- **Wood, J. J.,** Wickert, A. D., Larson, P. H. & Svien, L. A 140-year record of stream and valley sedimentation in the Whitewater River Valley, Minnesota, United States. (2025b). [In development].
  
**Funding sources**
- Legislative-Citizen Commission on Minnesota Resources (LCCMR) Environment and Natural Resources Trust Fund (ENTRF) grant 2022-163.
- National Science Foundation grant 1944782.
- UMN College of Science & Engineering Inclusion Fellowship.
