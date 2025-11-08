# Geomorphic floodplain transect data analysis

[![Release version](https://img.shields.io/badge/Release-1.0.0-brightgreen)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Python version](https://img.shields.io/badge/python-3.10.4-yellow)](https://www.python.org/downloads/release/python-3104/)
[![Progress](https://img.shields.io/badge/Progress-Complete-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentmgmation-surveys-jjwood/blob/main)
[![Update frequency](https://img.shields.io/badge/Updates-as--needed-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main)
[![License](https://img.shields.io/badge/License-MIT-informational)](https://github.com/wood1466/analysis-whitewater-basin-mn-sedimentation-surveys-jjwood/blob/main/LICENSE)

## Background

These programs were developed to augment and analyze topographic floodplain transect data collected in Minnesota's Whitewater River Valley (U.S.), between 1939 and 1994, through (1) geospatial digitization, (2) derivative calculations, and (3) statistical tests.

The historical data was collected by federal agencies during stream and valley sedimentation surveys aimed at investigating accelerated erosion and deposition and/or increased flooding in the basin; this dataset is inherently geomorphic in nature so these programs pursue analyses primarily of interest to the earth scientist. 

All data associated with this project has been published by Wood et al. (2025a) and is described in Wood et al. (2025b; in development). 

The hillslope–floodplain–channel cross-section below displays the kind of transect data these programs operate on—surface profiles (i.e., elevation data).

<p align="center">
  <img width="561.25" height="302.25" alt="2_3_8plots" src="https://github.com/user-attachments/assets/df71b17f-f69c-4efa-be20-82a849f75460" />
</p>

This repository (analysis-whitewater-basin-mn-sedimentation-surveys-jjwood) includes 4 programs:
- **transect_cogo_digitizer.py:** Performs coordinate geometry (COGO) calculations to digitize tabular transect elevation data into GIS files.
- **transect_sed_rate_calculator.py:** Calculates mean transect elevation change rates between successive elevation datasets to measure topographic change.
- **transect_sed_rate_statistics.py:** Performs Analysis of Variance (ANOVA) hypothesis testing suites to compare all mean elevation change rates over the time interval represented in this dataset—1855–1994.
- **transect_analysis_functions.py:** The user-defined functions (UDFs) executed in the other programs.

We will briefly describe how these programs operate and how to use them; see the programs' line comments for in-depth descriptions of their contents. Retreive and use the input data files from Wood et al. (2025a) as you follow along. The relevant files per program will be identified by screenshot.

## transect_cogo_digitizer.py
[![GeoPandas version](https://img.shields.io/badge/geopandas-1.1.0-yellow)](https://pypi.org/project/geopandas/1.1.0/)
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General

The maps below highlight this program's function. The left one—starting condition—displays a transect's GNSS surveyed monuments (cyan circles) and the transect's trace extending between them (dashed line). The right map—post-run condition—displays that transect trace populated with elevation measurements (magenta circles). This program takes the monuments' GNSS coordinates and compares their field-surveyed transect positions to that of the elevations' to calculate coordinates for the elevation data (Easting and Northing). Its output is a GeoPackage of elevation point layers grouped by data year—1855, 1939, 1965, 1975, 1978, and 1994 (for the Whitewater data).

<p align="center">
  <img width="6781" height="3474" alt="Digitizer1" src="https://github.com/user-attachments/assets/f03cc682-5fc8-4c56-8c2a-f0165f1a5ea3" />
<p/>

### Initialization

In the same location as the digitizer program, create a new folder named *Input* where you will store the code's required input files:
1. The elevation data to be digitized,
2. monument/reference coordinate data, and
3. reference coordinate metadata.

<p align="center">
  <img width="665" height="301" alt="Screenshot 2025-08-28 at 2 20 52 PM" src="https://github.com/user-attachments/assets/a3699570-c97c-4ef8-90d8-01dfe2ca18e8" />
<p/>
  
Each is converted into a pandas DataFrame at the end of the *Initialization* section to enable program manipulation. 

Prior to run, delete the data below from the input files to avoid erroneous digitization:
1. *WRV_MN_1855_1994_sedimentation_elevations.csv*: NF-21 (original) and NF-28B (original).
2. *WRV_MN_2008_2014_sedimentation_coordinates.csv*: MF-26B (1994).

Then, set the names of your output GIS files: *GPKG_NAME* and *LAYER_NAME1_PRE*. These will be stored in the *GIS* folder automatically created at the end of the *Initialization* section.
  
Lastly, you'll need to set the program's spatial operational limits and the coordinate reference system (CRS) of the output GeoPackage.

<p align="center">
  <img width="665" height="239" alt="Screenshot 2025-08-28 at 2 47 31 PM" src="https://github.com/user-attachments/assets/a2db389b-80c2-4528-9f6a-7e8c022b9d84" />
<p/>
  
*TRANSECT_NUM_START* and *TRANSECT_NUM_END*, together, determine which transect datasets are digitized. Their input is a *transect number*, an integer ID that provides a convenient framework for looping the digitizer through each transect (two different numbers must be set for the loop to function). Starting at *1* and an ending at *107* will digitize every Whitewater transect elevation dataset.

Declare the CRS with its unique EPSG (European Petroleum Survey Group) code. *EPSG:26915* sets the CRS to *NAD83 / UTM zone 15N* for Minnesota.

### Data operations
  
This section begins the digitization loop at the starting transect. 

<p align="center">
  <img width="647" height="161" alt="Screenshot 2025-08-29 at 12 08 43 PM" src="https://github.com/user-attachments/assets/fc8dd66f-50cd-4d8e-a7e2-54181efbebba" />
<p/> 
  
First, it begins a series of slices through the three starting DataFrames to select the data required to complete the COGO calculations:
1. The survey stations (measurement positions) of the first (earliest) elevation dataset,
2. the transect monuments' cartesian coordinate pairs, and
3. the station/position of the first, or survey start, monument.

The first slice to derive the survey stations is shown above.
  
Second, the program consults a UDF to check if the monument coordinates must be replaced by synthetic reference coordinates. 

<p align="center">
  <img width="656" height="300" alt="Screenshot 2025-08-29 at 12 53 33 PM" src="https://github.com/user-attachments/assets/65468943-a5fc-4a23-af77-b27a45d11163" />
<p/>
  
Typically, transects in the Whitewater Watershed extend in a line directly between (and often beyond) its two monuments. On the left map below, this is labeled the *expected trace*. Occassionally, monuments were shifted off of the actual measured line, the *shifted trace*. In the example below, the monument was established 10 ft East of the measured line. 

<p align="center">
  <img width="6781" height="3474" alt="Digitizer2" src="https://github.com/user-attachments/assets/2a631dcb-6f9e-4aa8-b27a-136c8a4abb1f" />
<p/>
  
To compensate for these shifts, the program first compares a monument's estimated coordinate accuracy to its shift magnitude. On the right map, the cyan buffer corresponds to an *XY accuracy* of 0.25 m and the yellow buffer to a *shift radius* of 3 m (10 ft). The *shift radius* does not lie within the *XY accuracy* buffer (i.e., *XY accuracy*<*shift radius*); therefore, the horizontal resolution of the GNSS coordinates are capable of meaningfully representing a locational shift of 3 m. 

With that being the case, the program calculates a new pair of synthetic reference coordinates via COGO. Here, the monument's X (Easting) coordinate is reduced by 3 m (10 ft) and its Y (Northing) coordinate remains the same. Subsequent digitization places the elevation data on the *shifted trace*. 

This program does not compensate for composite directional shifts (i.e., *NW*, *Upstream*, etc.). 

With the requisite data selected, a message displays which dataset will be digitized by identifying the transect ID and elevation data year.

<p align="center">
  <img width="639" height="97" alt="Screenshot 2025-08-29 at 9 59 26 AM" src="https://github.com/user-attachments/assets/ded0d0fc-ea56-4c7e-a873-61f69b24a8af" />
<p/>

To perform its COGO calculations the program takes the three data components selected previously and first calculates:

1. The transect azimuth between monuments (*θ*), and
2. the distance between each elevation station and the starting monument (*r*, for the example below).  

<p align="center">
  <img width="512.5" height="3475" alt="Digitizer3" src="https://github.com/user-attachments/assets/3e2b6e7f-feaf-4ab3-9065-625186ba7234" />
<p/>
  
With a cartesian coordinate system, *θ*, in general, can be calculated with,

$θ = tan\biggl(\frac{x2-x1}{y2-y1}\biggr)^{-1}$,
  
where (*x<sub>1</sub>*, *y<sub>1</sub>*) and (*x<sub>2</sub>*, *y<sub>2</sub>*) are the starting and ending coordinates, respectively.

Each *r<sub>i</sub>* = *elevation station<sub>i</sub>* - *starting monument station*.

The program then calculates the component displacements North (*Δy*) and East (*Δx*) required to travel an *r<sub>i</sub>* length down the transect to the ith elevation station. Its subsequent coordinates are:

*Northing<sub>i</sub>* = *Δy* + *y<sub>1</sub>*, and

*Easting<sub>i</sub>* = *Δx* + *x<sub>1</sub>*.

The newly calculated elevation coordinates are compiled and appended onto the input elevation DataFrame to use the points' precompiled metadata as attribute fields and values.

Lastly, the DataFrame is converted into a GeoPandas GeoDataFrame with the preselected CRS.

When the message below is visible, your output GeoPackage has been exported. 

<p align="center">
  <img width="624" height="51" alt="Screenshot 2025-08-29 at 4 18 46 PM" src="https://github.com/user-attachments/assets/226512e1-3446-4413-9c64-dda8a643e587" />
<p/>
  
## transect_sed_rate_calculator.py
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General
  
This code compares successive elevation datasets to measure vertical topograpic change over time on a transect. The paired cross-sections below show the typical data year comparions: 1855–1939, 1939–1965, and 1965–1994. The program's output is a table of mean transect elevation change in terms of depths (f and cm) and rates (cm/y).

<p align="center">
  <img width="640" height="480" alt="2_3_rateplots" src="https://github.com/user-attachments/assets/287b5414-4637-4c8d-bb7b-46abb547f28f" />
<p/>
  
### Initialization

In the same location as the rate calculator program, create a new folder named *Input*, if one does not yet exist, where you will store the code's required input files. 
There are two:
1. The elevation data from which to calculate change rates, and
2. transect calculation exclusion zones.
   
<p align="center">
  <img width="644" height="182" alt="Screenshot 2025-11-05 at 6 32 23 AM" src="https://github.com/user-attachments/assets/0e8f1fcd-9fae-4051-93d2-75ec0416fc4f" />
<p/>

Each is converted into a pandas DataFrame at the end of the *Initialization* section to enable program manipulation. 

Prior to run, delete the data below from the input files to avoid erroneous calculation:
1. *WRV_MN_1855_1994_sedimentation_elevations.csv*: NF-21 (original) and NF-28B (original).

Then, set the name of your output table and it's column labels: *CALC_NAME* and *DATAFRAME_COLUMNS*. The table will be stored in the *Calculations* folder automatically created at the end of the *Initialization* section.

Lastly, set the program's spatial operational limits—*TRANSECT_NUM_START* and *TRANSECT_NUM_END*—and the interpolation interval for pre-calculation resampling.

<p align="center">
  <img width="643" height="221" alt="Screenshot 2025-11-05 at 5 50 33 PM" src="https://github.com/user-attachments/assets/5e90700b-b0df-4cbf-982f-ed1be8ab7682" />
<p/>

### Data operations
  
This section begins the calculation loop at the starting transect. 

First, it slices through the elevation DataFrame to select the cross-section components required to complete the elevation change rate calculations:
1. The survey stations of the first elevation dataset (time 1),
2. the elevations of the first dataset, 
3. the survey stations of a second elevation dataset (time 2), and
4. the elevations of the second dataset.

With the requisite data selected, a message displays which transect data pair the mean elevation change rate will be calculated for by identifying the transect ID and elevation data years.

<p align="center">
  <img width="640" height="99" alt="Screenshot 2025-11-07 at 4 34 15 PM" src="https://github.com/user-attachments/assets/cf01b779-9b12-483b-adcc-029c246e987a" />
<p/>

Second, the program resamples the two cross-sections onto the same set of survey stations via linear interpolation. 

<p align="center">
  <img width="655" height="121" alt="Screenshot 2025-11-07 at 4 23 59 PM" src="https://github.com/user-attachments/assets/6b60e1cb-f5cd-4245-b34c-34a7d8e591df" />
<p/>

The top subplot below shows that transect elevations are not measured at the same points (stations) between sedimentation surveys. To measure vertical elevation change, the two points must coincide; therefore, we resample the datasets onto their shared range of stations with a systematic spacing of 0.1 ft. The bottom subplot displays the interpolated elevation data. The apparent increase in line thickness is an artifact of the much smaller sample spacing post interpolation—the measurement circles overlap. 

<p align="center">
  <img width="640" height="480" alt="2_interp" src="https://github.com/user-attachments/assets/b2c5579b-a189-4e87-a420-2acb7c188133" />
<p/>

In this example, note how part of the 1965 dataset, plotted in gray, was not interpolated. The relevant points do not share any stations measurements with the 1939 dataset and so were excluded from the interpoltion step. Any transect data excluded from this step, by default, is not included in later elevation change calculations.

Next, the program begins the calculation procedure. In general, it will first calculate elevation change rates at each interpolation point in the cross-section and, upon completion, will then calculate their mean.

Prior to the interpolation point calculations, it will slice through the second starting DataFrame to see if we have chosen to exclude any parts of our survey data pair from consideration. The resulting exclusion zone is simply a range of stations.

<p align="center">
  <img width="658" height="380" alt="Screenshot 2025-11-07 at 5 09 28 PM" src="https://github.com/user-attachments/assets/eaab15cf-e367-4cc6-b6e9-4c0d716f7a25" />
<p/>

The choice to exclude any part of a survey dataset from the rate calculations are either specific to the transect or that dataset's data year. In general, we set exclusion zones for the following reasons: 
1. The existence of elevation-measurement discontinuities due to sampling gaps or, for 1855 datasets, the limits of detectable legacy sediment (see Wood et al., 2025b). Any elevation change calculated over such discontinuities are meaningless.  
2. When calculated elevation changes are negative and one of the input elevation datasets is derived from historical borings (1855 and sometimes 1939; see Wood et al., 2025b). Surface profiles partially derived from boring data cannot capture any erosion so neither can calculations using their data. 
4. When calculated elevation changes record channel deposition between 1939 boring derived elevations and 1965 elevations. Surface profiles partially derived from boring data cannot capture channel geometry, just floodplain elevations, which makes any measured channel filling an artifact.

With potential exclusion zones checked, the program calculates the elevation change at each ith interpolation point with,

*Δz<sub>i</sub> = z<sub>2</sub> - z<sub>1</sub>*,

where *z<sub>1</sub>* and *z<sub>2</sub>* are the elevations of time 1 and 2, respectively.

If an exclusion zone for one of the present datasets was recovered, the program compares the interpolation point station with the exclusion range. If it is within the range, the interpolation point calculation is excluded from the mean. 

The program then calculates the mean elevation change of all interpolation points (*Δz*) and then the mean elevation change rate with,

$η = \frac{Δz}{Δt} = \frac{Δz}{t2-t1}$,

where *t<sub>1</sub>* and *t<sub>2</sub>* are the data years of time 1 and 2, respectively.

The newly calculated mean elevation change quantities and identifying info such as transect and data years are compiled into a new DataFrame.

When the message below is visible, your output DataFrame (previewed) has been exported.

<p align="center">
  <img width="642" height="48" alt="Screenshot 2025-11-07 at 6 28 40 PM" src="https://github.com/user-attachments/assets/3146ff6e-f1d4-4725-889f-17cdfb2b20a7" />
<p/>
  
## transect_sed_rate_statistics.py
[![Matplotlib version](https://img.shields.io/badge/matplotlib-3.10.3-brightgreen)](https://pypi.org/project/matplotlib/)
[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)
[![pingouin version](https://img.shields.io/badge/pingouin-0.5.5-brightgreen)](https://pypi.org/project/pingouin/0.5.5/)
[![scikit-posthocs version](https://img.shields.io/badge/scikit--posthocs-0.11.4-brightgreen)](https://pypi.org/project/scikit-posthocs/)
[![SciPy version](https://img.shields.io/badge/scipy-1.15.3-yellow)](https://pypi.org/project/scipy/1.15.3/)
[![statsmodels version](https://img.shields.io/badge/statsmodels-0.14.4-brightgreen)](https://pypi.org/project/statsmodels/)

### General

This code performs a suite of ANOVA tests to compare mean transect elevation rates by time interval to determine if they are significantly different. For the Whitewater Watershed data, our rates groups are 1855–1939, 1939–1965, and 1965–1994. The program's output are various tables of *p*-values and test statistics—they are printed rather than exported. 

### Initialization

In the same location as the statistics program, create a new folder named *Input*, if one does not yet exist, where you will store the code's required input files. 
There is one:
1. The mean transect elevation change rates to be tested.
   
<p align="center">
  <img width="646" height="240" alt="Screenshot 2025-11-08 at 8 46 30 AM" src="https://github.com/user-attachments/assets/0f9841a7-725e-4906-b201-219b2a32ae7d" />
<p/>

It is converted into a pandas DataFrame at the end of the *Initialization* section to enable program manipulation. 

Then, set the level of significance (*α*) and identify the column labels, from the input file, that identify your data groups—*GROUP_COLUMN_1, etc.*

### Data operations

This section begins the statistical hypohtesis testing. 

First, it slices through the rate DataFrame to select the time intervals required to complete the ANOVA tests:
1. The mean transect elevation change rates of interval 1,
2. the mean transect elevation change rates of interval 2, and
3. the mean transect elevation change rates of interval 3.

<p aling="center">
  <img width="645" height="180" alt="Screenshot 2025-11-08 at 9 31 42 AM" src="https://github.com/user-attachments/assets/23f1ebd7-c0d9-4d81-9c01-7a696f89ba24" />
<p/>
  
Second, the program investigates the datas' distribution characteristics to verify whether or not ANOVA's corresponding underlying assumptions are being violated:
1. Group normality, and
2. group homoscedasticity (variance equality).

This step is necessary to properly decide which ANOVA suite is applicable and lend meaning to our results.  

The program checks for normality visually with histograms, box plots, and Q-Q plots, and statistically with the Kolomogorov–Smirnov test. It then checks for variance equality with the Brown–Forsythe test. 

The results of these, and all of the following tests, is printed on screen.

<p align="center">
  <img width="633" height="78" alt="Screenshot 2025-11-08 at 9 18 56 AM" src="https://github.com/user-attachments/assets/eb1eed2c-ee29-4257-b663-fda60d51073d" />
<p/>

The code performs three ANOVA test suites to account for assumption violations and/or to cross-reference results. The three suites are:
1. Kruskal–Wallis H- omnibus test and Dunn's post-hoc pairwise comparison test (nonparametric),
2. traditional ANOVA omnibus test and Tukey's HSD post-hoc pairwise comparison test (parametric), and
3. Welch's ANOVA omnibus test and Games–Howell's post-hoc pairwise comparison test (parametric, allows for unequal variances).

When the message below is visible, your tests have completed.

<p align="center">
  <img width="633" height="55" alt="Screenshot 2025-11-08 at 9 29 48 AM" src="https://github.com/user-attachments/assets/85b6316a-de4c-4575-a243-ee3d1ff0139d" />
<p/>

## transect_analysis_functions.py

[![NumPy version](https://img.shields.io/badge/numpy-2.2.6-yellow)](https://pypi.org/project/numpy/2.2.6/)
[![pandas version](https://img.shields.io/badge/pandas-2.3.0-brightgreen)](https://pypi.org/project/pandas/)

### General

This code houses the user-defined functions, for repetitive or specialized tasks, called in the previous three programs. 

## General information

**Documentation date:** 20251108

**Date finalized:** 202501108

**Author:** Jimmy J. Wood
- Institution: University of Minnesota Twin Cities, Saint Anthony Falls Laboratory
- Email: <jimmyjwood24@gmail.com>
- ORCID: [0009-0009-7263-433X](https://orcid.org/0009-0009-7263-433X)

**Related publications**
- **Wood, J. J.,** Svien, L., Christianson, D. & Claas, L. Historical stream and valley sedimentation survey data for the Whitewater River Valley, Minnesota, United States (1855–1994). *University of Minnesota Twin Cities Data Repository for U of M* https://doi.org/10.13020/2ggx-qk28 (2025a).
- **Wood, J. J.,** Wickert, A. D., Larson, P. H. & Svien, L. A 140-year record of stream and valley sedimentation in the Whitewater River Valley, Minnesota, United States. (2025b). [In development].
  
**Funding sources**
- Legislative-Citizen Commission on Minnesota Resources (LCCMR) Environment and Natural Resources Trust Fund (ENTRF) grant 2022-163.
- National Science Foundation grant 1944782.
- UMN College of Science & Engineering Inclusion Fellowship.
