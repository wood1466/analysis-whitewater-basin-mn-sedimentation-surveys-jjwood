# ======================================================================================================================
# ------------------------ WHITEWATER RIVER WATERSHED, MN, SEDIMENTATION SURVEY DATA DIGITIZER -------------------------
# ------------------------ PRIMARY SCRIPT (1/1) ------------------------------------------------------------------------
# ======================================================================================================================

# For information see program documentation: README Sed_survey_digitizer.rtf.

# ======================================================================================================================
# START! ---------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

print()  # Inserts blank row to provide white space for next display.
print('START!')  # Displays string signaling the start of the program.
print('...')  # Displays string indicating program is working.
print()  # Inserts blank row to provide white space for next display.

# ======================================================================================================================
# PART 0: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES & SIGNAL START ----------------------------------------------------------------------------------------

import time  # Imports module enabling the use of time related tools.
import pandas as pd  # Imports module with assignment enabling the use of DataFrames.
import sys  # Imports module enabling the use of system specific tools.
import math  # Imports module enabling the use of Python's standard mathematical tools.
import numpy
import os  # Imports module enabling interaction with the computer's operating system.
import geopandas as gpd  # Imports module enabling the use of geographic data.
import warnings  # Imports module enabling direct warning intervention.

startTime0 = time.time()  # Starts clock to measure program length.
# User note: Enable if information is desired.

# TOGGLES --------------------------------------------------------------------------------------------------------------

bearing_meas = True

# All_channels = True  # Pre-selects all survey data for code to digitize.
# Channel_1R = False  # Pre-selects survey data along the Main Stem only for code to digitize.
# Channel_2R = False  # Pre-selects survey data along the Middle Fork only for code to digitize.
# Channel_3R = False  # Pre-selects survey data along the North Fork only for code to digitize.
# Channel_4R = False  # Pre-selects survey data along the South Fork only for code to digitize.
# Channel_1T = False  # Pre-selects survey data along the Trout Creek only for code to digitize.
# Channel_2T = False  # Pre-selects survey data along the Beaver Creek only for code to digitize.
# Channel_3T = False  # Pre-selects survey data along the Logan Creek only for code to digitize.
# Channel_4T = False  # Pre-selects survey data along the Dry Creek only for code to digitize.
# Custom = False  # Pre-selects survey data for code to digitize.
# if Custom == True:
#     R1, R2 = 1, 2  # Defines variables with the desired loop limits.
# else:
#     Custom == False

# IMPORT SURVEY DATA ---------------------------------------------------------------------------------------------------

srvy_data = pd.read_csv(r'/Users/jimmywood/Desktop/Codes/Current/Range_input_data/WwR_sed_survey_data.csv')
# Imports .csv file of all range survey srvy_data.
# User note: Change path directory to match file location on your system.

df_0 = pd.DataFrame(srvy_data)  # Creates DataFrame from previous file import for manipulation in Python.
pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to show all columns. # Enable for check
# only.
# print('All survey data')  # Displays string. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# print(df_0)  # Displays DataFrame. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# ======================================================================================================================
# LOOPING DIGITIZER ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT LOOP LIMITS ---------------------------------------------------------------------------------------------------


def createlist(limit1, limit2):  # Defines function establishing framework for first loop limit assignment.
    return [item for item in range(limit1, limit2 + 1)]

r1, r2 = 1, 2  # Defines variables with the desired loop limits.
rng_num = createlist(r1, r2)  # Defines list as loop limits.
# print('Spatial loop limits:', 'Survey ranges', rng_num[0],  '&',  rng_num[1])  # Displays list. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.

# CODE LOOP ------------------------------------------------------------------------------------------------------------

for i in rng_num:  # Begins loop through all range numbers.

    # ==================================================================================================================
    # PART 1: DATA SELECTION -------------------------------------------------------------------------------------------
    # ==================================================================================================================

    # RANGE DATASET ----------------------------------------------------------------------------------------------------

    df_1 = df_0[df_0['Range_num'] == i]  # Creates new DataFrame of individual range data from original DataFrame column.
    # print('Selected survey data')  # Displays string and DataFrame. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # print(df_1)  # Displays DataFrame. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

    df_01 = df_1.loc[:, 'Srvy_num']
    # df_01 = df_01.drop_duplicates(keep = 'first')
    # print(df_01)  # Displays DataFrame. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
    srvy_num_list = df_01.values.tolist()
    # print(srvy_num_list)
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
    s1 = int(srvy_num_list[0])
    s2 = int(srvy_num_list[-1])
    # print(s1, s2)
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

    def createlist(limit1, limit2):  # Defines function establishing framework for second loop limit assignment.
        return [item for item in range(limit1, limit2 + 1)]

    s1, s2 = s1, s2  # Defines variables with the desired loop limits (min r1 = 1, max r2 = 94).
    srvy_yr = createlist(s1, s2)  # Defines list as loop limits.
    # print('Temporal loop limits:', 'Survey years', srvy_yr[0], '&', srvy_yr[-1])  # Displays list. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

    # SURVEY NUMBER DATASET --------------------------------------------------------------------------------------------

    for k in srvy_yr:  # Establishes loop to select monument coordinates from DataFrame.

        # Data sub-set selection and initial condition reporting -------------------------------------------------------

        df_2 = df_1[df_1['Srvy_num'] == k]  # Creates new DataFrame of individual range data from original DataFrame
        # column for each survey year.
        # print('Selected survey data by year:', k)  # Displays string and DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_2)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        max = len(df_2.index)  # Collates number of rows in DataFrame.
        max = max - 1  # Calculates true max nunmber of measurements for survey year subtracting by 1 to eliminate
        # indexed header.
        index = df_2.index  # Returns index information about DataFrame.
        # print(index)  # Returns index values for whole DataFrame.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        str_chnnl = df_2.loc[index[0], 'Str_chnnl']
        print('Stream channel:', str_chnnl)
        srvy_rng = df_2.loc[index[0], 'Srvy_range']
        print('Survey range:', srvy_rng)
        print('Range number:', i)
        print('Survey number:', k, 'of', srvy_yr[-1])
        srvy_dt = df_2.loc[index[0], 'Srvy_date']  # Defines variable by selecting first element under specified column in
        # DataFrame.
        print('Date:', srvy_dt)  # Displays variable. Enable for check only.
        brng_ref = df_2.loc[index[0], 'Brng_R_dir']
        brng_angl = df_2.loc[index[0], 'Brng_angle']
        brng_dir = df_2.loc[index[0], 'Brng_A_dir']
        print('Range bearing:', brng_ref, brng_angl, brng_dir)
        print('Measurements recorded:', max)  # Displays variable. Enable for check only.
        print('---------------------------')  # Displays string.
        print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # Monument coordinates -------------------------------------------------------------------------------

        Mn1_East_std = df_2.loc[index[0], 'Mn1_East_m']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        Mn1_North_std = df_2.loc[index[0], 'Mn1_Nor_m']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        Mn2_East_std = df_2.loc[index[0], 'Mn2_East_m']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        Mn2_North_std = df_2.loc[index[0], 'Mn2_Nor_m']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        # print('Benchmark 1 coordinates:', Mn1_East_std, 'm E, &', Mn1_North_std, 'm N')
        # print('Benchmark 2 coordinates:', Mn2_East_std, 'm E, &', Mn2_North_std, 'm N')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # END PROCESS DISPLAY ------------------------------------------------------------------------------------------

        # print('Monument coordinates selected!')  # Displays string signaling the end of
        # # # part 1 for the current range and how long it took to run with a reduced number of significant figures.
        # # # Enable for check only.
        # print('Part 1 of 4 done!')  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # ==============================================================================================================
        # PART 2: COORDINATE CALCULATIONS -------------------------------------------------------------------------------
        # ==============================================================================================================

        # RANGE OFFSET COMPONENTS & HEADING ----------------------------------------------------------------------------
        deltaE = abs(Mn2_East_std - Mn1_East_std)  # Easting change between monuments.
        # User note: Absolute value calculated because range heading will control sign, and we desire positive values
        # for later arithmetic.
        # print('Change in Easting:', '%.2f'%deltaE, 'm')  # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        deltaN = abs(Mn2_North_std - Mn1_North_std)  # Northing change between monuments.
        # print('Change in Northing:', '%.2f'%deltaN, 'm') # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        delta_off = math.sqrt(deltaE ** 2 + deltaN ** 2)  # Distance
        # between monuments along range-line. Calculated for later error analysis.
        # print('Range-line offset:', '%.2f'%delta_off, 'm') # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        if bearing_meas == True:
            bearing_deg = brng_angl
            bearing_rad = brng_angl * math.pi/180 + math.pi/2
            # print(bearing_rad)
            # breakpoint()
        else:
            bearing_rad = math.atan(deltaN / deltaE)  # Calculates range survey heading between monuments in radians.
            # print('Range bearing:', '%.2f'%bearing_rad, 'radians')  # Displays variable with a reduced number of significant.
            # figures. Enable for check only.
            # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

            # Correction
            bearing_rad = math.pi - bearing_rad  # Range survey heading corrected to match compass direction of survey.
            # User note: Important step considering that the heading calculated initially considers is derived from the
            # unit circle and not a compass system.
            # print('Corrected bearing:', '%.2f'%bearing_rad, 'radians')  # Displays variable with a reduced number of
            # significant figures . Enable for check only.
            # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
            # bearing_deg = bearing_rad * 180/math.pi
            # print('Corrected bearing:' '%.2f'%bearing_deg, 'degrees')
            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # SAMPLE OFFSETS --------------------------------------------------------------------------------------------------

        # Multipliers ------------------------------------------------------------------------------------

        sin = math.sin(bearing_rad)  # Calculates Sine of heading.
        cos = math.cos(bearing_rad)  # Calculates Cosine of heading.
        # print('Sine of heading:', '%.2f'%sin) # Displays variable. Enable for check only.
        # print('Cosine of heading:', '%.2f'%cos) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # Base correction -------------------------------------------------------------------------------------------------------

        df_3 = df_2['Sm_off_ft']  # Create new DataFrame of measurement offsets.
        # print('Sample offsets (ft) for survey', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_3)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        Mn1_offset = df_2.loc[index[0], 'Mn1_off_ft']
        # print('Benchmark 1 offset for survey', k, ':', Mn1_offset, 'ft')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        df_3 = df_3 - Mn1_offset
        # print('Corrected sample offset (ft) for survey', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_3)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        convertFtM = 1 / 3.281  # Conversion factor from feet to meters.
        # print('Conversion factor: ft-m:', '%.4f'%convertFtM, 'm/ft') # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        df_3m = df_3 * convertFtM  # Converts corrected offsets from ft to m. The desired units.
        # print('Corrrected sample offset (m) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_3)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # Components -------------------------------------------------------------------------------------------------------

        offsets_east = cos * abs(df_3m)  # Calculates easting offset in m between each survey measurement point and start.
        # User note: The absolute value is used here to simplify future arithmetic.
        # print('Sample offsets east (m) for survey', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(offsets_east) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        offsets_north = sin * abs(df_3m)  # Calculates northing offset in m between each survey measurement point and start.
        # User note: The absolute value is used here to simplify future arithmetic.
        # print('Sample offsets north (m) for survey', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(offsets_north) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # SAMPLE COORDINATES ----------------------------------------------------------------------------------------------------------

        eastings = Mn1_East_std + offsets_east  # Creates a new DataFrame calculating easting coordinates for all survey
        # measurement points.
        # print('Sample Eastings for survey', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(eastings) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        northings = Mn1_North_std + offsets_north  # Creates new DataFrame calculating northing coordinates for all survey
        # measurement points.
        # print('Sample Eastings for survey', k)  # Displays string. Enable for check only.
        # print(northings) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # DATAFRAME POPULATION -----------------------------------------------------------------------------------------

        # Heading and components -----------------------------------------------------------------------------------------------------------
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Nm_samples'] = max  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Delta_East'] = deltaE  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Delta_Nor'] = deltaN  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Delta_off'] = delta_off  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Calc_azim'] = bearing_rad  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Offset multipliers ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Azim_sin'] = sin  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Azim_cos'] = cos  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Net offsets and components ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cSm_off_ft'] = df_3  # Populates the selected column with the selected variable for the entire
        # DataFrame.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cSm_off_m'] = df_3m  # Populates the selected column with the selected variable for the entire
        # DataFrame.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Sm_off_E'] = offsets_east  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Sm_off_N'] = offsets_north  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Measurement coordinates ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Sm_East'] = eastings  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Sm_Nor'] = northings  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # END PROCESS DISPLAY ------------------------------------------------------------------------------------------

        # print('Survey measurement coordinates calculated!')  # Displays string signaling the
        # # end of part 2 for the current range and how long it took to run with a reduced number of significant figures.
        # # Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Part 2 of 4 done!')  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # ==================================================================================================================
        # PART 3: ERROR ANALYSIS CALCULATIONS -------------------------------------------------------------------------------------------
        # ==================================================================================================================

        # MONUMENT 2 POSITIONAL ERROR ---------------------------------------------------------------------------------------

        df_2 = df_0[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k)]  # Creates new DataFrame of individual range
        # data from original DataFrame column for each survey year.
        # print('Selected survey data by year:', k)  # Displays string and DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_2)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        max = len(df_2.index)  # Collates number of rows in DataFrame.
        index = df_2.index  # Returns index information about DataFrame.
        # print('Index:', index)  # Returns index values for whole DataFrame.
        # print(index[0])  # Returns first index value for whole DataFrame.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        Mn2_offset = df_2.loc[index[0], 'Mn2_off_ft']
        # print('Benchmark 2 offset for survey', k, ':', Mn2_offset, 'ft')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        index = df_2.index[df_2['Sm_off_ft'] == Mn2_offset].tolist()
        # print('New index:', index)  # Returns index values for whole DataFrame.
        # print(index[0])  # Returns first index value for whole DataFrame.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        Mn2_East_calc = df_2.loc[index[0], 'Sm_East']
        Mn2_North_calc = df_2.loc[index[0], 'Sm_Nor']
        # print('Benchmark 2 calculated coordinates:', Mn2_East_calc, 'm E, &', Mn2_North_calc, 'm N')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        Mn2_deltaE = Mn2_East_std - Mn2_East_calc
        Mn2_deltaN = Mn2_North_std - Mn2_North_calc
        # print('Coordinate differences for survey', k)
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Easting:', Mn2_deltaE, 'm')
        # print('Northing:', Mn2_deltaN, 'm')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # DATAFRAME POPULATION AND EXPORT -----------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cMn2_E_dff'] = Mn2_deltaE  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cMn2_N_dff'] = Mn2_deltaN  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cMn2_East'] = Mn2_East_calc  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'cMn2_Nor'] = Mn2_North_calc  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        df_0.to_csv('/Users/jimmywood/Desktop/Codes/Current/Range_input_data/WwR_sed_survey_data.csv', index=False)
        # Exports DataFrame to path updating the original srvy_data sheet.
        # User note: Change path directory if running program on your own system.
        # print('Range data updated!')  # Displays string. Enable for check only
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_0)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # END PROCESS DISPLAY ------------------------------------------------------------------------------------------

        # print('Monument 2 coordinate error calculated!')  # Displays string signaling the
        # end of part 3 for the current range and how long it took to run with a reduced number of significant figures.
        # Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Part 3 of 4 done!')  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # ==================================================================================================================
        # PART 4: GIS SHAPEFILE GENERATION ---------------------------------------------------------------------------------
        # ==================================================================================================================

        # SET UP DIRECTORY -------------------------------------------------------------------------------------------------

        directory = 'GIS_output'  # Sets name of new directory where GIS srvy_data will be exported.
        if not os.path.exists(directory):  # Creates new folder with above name or skips step if already exists.
            os.mkdir(directory)
            print('OUTPUT DIRECTORY', directory, 'CREATED')
        newpath = '/Users/jimmywood/Desktop/Codes/Current/GIS_output/Survey_Data'  # Sets specific path and name of new
        # directory where the GIS srvy_data will be exported.
        if not os.path.exists(newpath):  # Creates new folder with above name or skips step if already exists.
            os.makedirs(newpath)
            print('OUTPUT DIRECTORY', 'Survey_Data', 'CREATED')

    # CREATE GEODATAFRAME & EXPORT VECTOR FILE ----------------------------------------------------------------------------------------------

        df_2 = df_0[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k)]  # Creates new DataFrame of individual range
        # data from original DataFrame column for each survey year.
        # print(df_2)  # Displays DataFrame. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        gdf = gpd.GeoDataFrame(df_2, geometry = gpd.points_from_xy(df_2.Sm_East, df_2.Sm_Nor), crs = 'EPSG:26915')
        # Creates GeoDataFrame from DataFrame of survey measurements. Coordinate system designated via crs assignment.
        # print(gdf.crs)  # Displays GeoDataFrame coordinate system. Enable for check only.
        # print(gdf['geometry'].head())  # Displays GeoDataFrame geometry GeoSeries. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        if bearing_meas == True:
            gdf.to_file('/Users/jimmywood/Desktop/Codes/Current/GIS_output/Survey_Data/R' + str(i) + '_S' + str(k) + 'mBear' + '.shp', index=False)
        else:
            gdf.to_file('/Users/jimmywood/Desktop/Codes/Current/GIS_output/Survey_Data/R' + str(i) + '_S' + str(k) + '.shp', index=False)

        # Exports shapefile.
        # gdf_k.to_file("Digitized_sedimentation_surveys.gpkg", layer = 'R1_1994', driver = 'GPKG' ) # Exports to
        # Geopackage.

    # for j in srvy_yr:
#         for k in list_index:  # Loop creating DataFrames for each survey year of a range to be converted to
#             # GeoDataFrames.
#             df_8k = df[(df['Range #'] == i) & (df['Survey year'] == j)]  # Creates new DataFrame from select
#             # columns of master DataFrame .
#             # print(df_8k)  # Displays DataFrame. Enable for check only.
#             # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
#             gdf_k = gpd.GeoDataFrame(df_8k, geometry=gpd.points_from_xy(df_8k.Easting, df_8k.Northing),
#                                      crs='EPSG:26915')
#             # Creates GeoDataFrame from DataFrame of survey measurements. Coordinate system designated via crs
#             # assignment
#             # print(gdf.crs)  # Displays GeoDataFrame coordinate system. Enable for check only.
#             # print(gdf['geometry'].head())  # Displays GeoDataFrame geometry GeoSeries. Enable for check only.
#             # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
#             # for j in srvy_yr:  # Begins loop establishing rules for naming exported shapefiles.
#             # Current_Date = datetime.datetime.today().strftime('%b-%d-%Y')  # Creates timestamp for shapefiles.
#             # print(Current_Date)  # Displays variable. Enable for check only.
#             # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
#             warnings.filterwarnings('ignore', '.*Column names.*', )  # Ignores warnings related to the length of column
#             # names for each exported shapefile.
#             # User notes: Warning indicates column headers will be truncated by shapefile formatting rules. Unimportant
#             # so ignored.
#             # gdf_k.to_file('/Users/jimmywood/Desktop/Codes/Current/GIS_output/Survey_Data/R' + str(i) + '_' + str(j)
#             #               + '_'
#             #               + str(Current_Date) + '.shp',
#             #               index=False)
#             gdf_k.to_file('/Users/jimmywood/Desktop/Codes/Current/GIS_output/Survey_Data/R'
#                           + str(i) + '_' + str(j) + '.shp', index=False)
#             # Exports shapefile.
#             # gdf_k.to_file("Digitized_sedimentation_surveys.gpkg", layer = 'R1_1994', driver = 'GPKG' ) # Exports to
#             # Geopackage.
#
#     # End process display
#     # executionTime = (time.time() - startTime)  # Calculates how long it took Part 1 to run.
#     # print('Survey srvy_data converted to GIS file & exported!:', '%.4f' % executionTime,
#     #       's')  # Displays string signaling the
#     # end of part 4 for the current range and how long it took to run with a reduced number of significant figures.
#     # print('Part 4 of 4 done!')  # Displays string. Enable for check only.
#     print('Survey srvy_data converted to GIS file & exported!')  # Displays string.
#     print()  # Inserts blank row to grant space for next displayed items.
#
#     print('-----------------------------------------------------------------------------------------------------------')
#     print()  # Inserts blank row to grant space for next displayed items.
#
#     # Progress timing
#     if i == 13:
#         executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
#         startTime1 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 26:
#         executionTime1 = (time.time() - startTime1)  # Calculates how long it took to run since clock start.
#         startTime2 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 48:
#         executionTime2 = (time.time() - startTime2)  # Calculates how long it took to run since clock start.
#         startTime3 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 69:
#         executionTime3 = (time.time() - startTime3)  # Calculates how long it took to run since clock start.
#         startTime4 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 73:
#         executionTime4 = (time.time() - startTime4)  # Calculates how long it took to run since clock start.
#         startTime5 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 79:
#         executionTime5 = (time.time() - startTime5)  # Calculates how long it took to run since clock start.
#         startTime6 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 87:
#         executionTime6 = (time.time() - startTime6)  # Calculates how long it took to run since clock start.
#         startTime7 = time.time()  # Starts clock to measure how long whole script takes.
#     elif i == 94:
#         executionTime7 = (time.time() - startTime7)  # Calculates how long it took to run since clock start.
#         startTime4 = time.time()  # Starts clock to measure how long whole script takes.
#
# # Script end process display
# print('Main Stem srvy_data digitized in', '%.4f' % executionTime0, 's',
#       '!')  # Displays string signalling the end of Main
# # Stem digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('Middle Fork srvy_data digitized in', '%.4f' % executionTime1, 's', '!')  # Displays string signalling the end of
# # Middle Fork digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('North Fork srvy_data digitized in', '%.4f' % executionTime2, 's', '!')  # Displays string signalling the end of
# # North Fork digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('South Fork srvy_data digitized in', '%.4f' % executionTime3, 's', '!')  # Displays string signalling the end of
# # South Fork digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('Trout Creek srvy_data digitized in', '%.4f' % executionTime4, 's', '!')  # Displays string signalling the end of
# # Trout Creek digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('Beaver Creek srvy_data digitized in', '%.4f' % executionTime5, 's', '!')  # Displays string signalling the end
# # of Beaver Creek digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('Logan Creek srvy_data digitized in', '%.4f' % executionTime6, 's', '!')  # Displays string signalling the end
# # of Logan Creek digitization and how long it took with modified significant figures.
# # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
# print('Dry Creek srvy_data digitized in', '%.4f' % executionTime7, 's', '!')  # Displays string signalling the end of
# # Dry Creek digitization and how long it took with modified significant figures.
# print()  # Inserts blank row to grant space for next displayed items.
# executionTimeEnd = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
# if executionTimeEnd > 60:  # Loop for reporting variable.
#     executionTimeEnd = executionTimeEnd / 60
# print('All sedimentation survey srvy_data digitized!:', '%.4f' % executionTimeEnd,
#       'min')  # Displays string signalling the
# # end of digitization and how long it took with modified significant figures.
# print()  # Inserts blank row to grant space for next displayed items.
# print('END!')  # Displays string signaling the end of the program.
#
# # ======================================================================================================================
# # END! -----------------------------------------------------------------------------------------------------------------
# # ======================================================================================================================
