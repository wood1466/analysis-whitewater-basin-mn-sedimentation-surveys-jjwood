# ======================================================================================================================
# ------------------------ WHITEWATER RIVER WATERSHED, MN, SEDIMENTATION SURVEY DATA DIGITIZER -------------------------
# ------------------------ PRIMARY SCRIPT (1/2) ------------------------------------------------------------------------
# ======================================================================================================================

# For information see program documentation: README Range_digitizer.rtf.

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

# IMPORT SURVEY DATA ---------------------------------------------------------------------------------------------------

srvy_data = pd.read_csv(r'/Users/jimmywood/Desktop/Codes/Current/Range_input_data/Range_survey_data_sept19.csv')
# Imports .csv file of all range survey srvy_data.
# User note: Change path directory to match file location on your system.

df_0 = pd.DataFrame(srvy_data)  # Creates DataFrame from previous file import for manipulation in Python.
pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to show all columns. # Enable for check
# only.
# print('All survey data – df_0')  # Displays string. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# print(df_0)  # Displays DataFrame. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# ======================================================================================================================
# LOOPING DIGITIZER ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT LOOP LIMITS ---------------------------------------------------------------------------------------------------

def createlist(limit1, limit2):  # Defines function establishing framework for loop limit assignment.
    return [item for item in range(limit1, limit2 + 1)]

r1, r2 = 19, 19  # Defines variables with the desired loop limits (min r1 = 1, max r2 = 94).
rng_num = createlist(r1, r2)  # Defines list as loop limits.
# print('Digitizer loop limits:', rng_num)  # Displays list. Enable for check only.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# CODE LOOP ------------------------------------------------------------------------------------------------------------

for i in rng_num:  # Begins loop through all range numbers.

    # ==================================================================================================================
    # PART 1: DATA SELECTION -------------------------------------------------------------------------------------------
    # ==================================================================================================================

    # SET INITIAL CONDITIONS -------------------------------------------------------------------------------------------

    if 1 <= i <= 13:  # Loop to display general range geographic information.
        # User note: This is purely for visualization. Enable if information is desired.
        print('Stream channel: Main Stem')  # Displays string detailing stream channel range lies on.
        print('Range number:', i)  # Displays string detailing range number.
    elif 14 <= i <= 26:
        print('Stream channel: Middle Fork')
        print('Range number:', i)
    elif 27 <= i <= 48:
        print('Stream channel: North Fork')
        print('Range number:', i)
    elif 49 <= i <= 69:
        print('Stream channel: South Fork')
        print('Range number:', i)
    elif 70 <= i <= 73:
        print('Stream channel: Trout Creek')
        print('Range number:', i)
    elif 74 <= i <= 79:
        print('Stream channel: Beaver Creek')
        print('Range number:', i)
    elif 80 <= i <= 87:
        print('Stream channel: Logan Creek')
        print('Range number:', i)
    elif 88 <= i <= 94:
        print('Stream channel: Dry Creek')
        print('Range number:', i)
    else:
        print('Unknown stream channel')   # Displayed string when error occurs.
        sys.exit('Loop limits error')  # Error immediately stops code.

    if i < 13:  # Loop to display general range survey information.
        srvy_yr = [1994, 1964, 1939, 1850]  # Defines list with years surveyed.
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', srvy_yr[2], ',', '&', srvy_yr[3])  # Displays string
        # detailing years surveyed.
        print()  # Inserts blank row to provide white space for next display. Enable for check only.
    elif i == 13:
        srvy_yr = [1994, 1978, 1975, 1964, 1939, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', srvy_yr[2], ',', srvy_yr[3], ',',
              srvy_yr[4], ',', '&', srvy_yr[5])
    elif 14 <= i <= 19:
        srvy_yr = [1994, 1964, 1939, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', srvy_yr[2], ',', '&', srvy_yr[3])
        print()
    elif 20 <= i <= 26:
        srvy_yr = [1994, 1850]
        print('Surveyed in', srvy_yr[0], ',', '&', srvy_yr[1])
        print()
    elif 27 <= i <= 37:
        srvy_yr = [1994, 1964, 1939, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', srvy_yr[2], ',', '&', srvy_yr[3])
        print()
    elif 38 <= i <= 48:
        srvy_yr = [1994, 1964, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', '&', srvy_yr[2])
        print()
    elif 49 <= i <= 55:
        srvy_yr = [1994, 1964, 1939, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', srvy_yr[2], ',', '&', srvy_yr[3])
        print()
    elif 56 <= i <= 69:
        srvy_yr = [1994, 1964, 1850]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', '&', srvy_yr[2])
        print()
    elif 70 <= i <= 77:
        srvy_yr = [1994, 1964, 1939]
        print('Surveyed in', srvy_yr[0], ',', srvy_yr[1], ',', '&', srvy_yr[2])
        print()
    elif 78 <= i <= 94:
        srvy_yr = [1994, 1964]
        print('Surveyed in', srvy_yr[0], ',', '&', srvy_yr[1])
        print()

    # SELECT DATA ------------------------------------------------------------------------------------------------------

    # Range ------------------------------------------------------------------------------------------------------------

    df_1 = df_0[df_0['Range_num'] == i]  # Creates new DataFrame of individual range data from original DataFrame column.
    # print('Selected survey data - df_1')  # Displays string and DataFrame. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # print(df_1)  # Displays DataFrame. Enable for check only.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.

    # Monuments --------------------------------------------------------------------------------------------------------

    for k in srvy_yr:  # Establishes loop to select monument coordinates from DataFrame.
        df2_k = df_1[df_1['Srvy_year'] == k]  # Creates new DataFrame of individual range data from original DataFrame
        # column for each survey year.
        # print('Selected survey data by year:', k)  # Displays string and DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df2_k)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        max = len(df2_k.index)  # Collates number of rows in DataFrame.
        # print('Number of survey measurements during', k, ':', max)  # Displays string and number of rows in DataFrame,
        # also the number of survey measurement points. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        index = df2_k.index  # Returns index information about DataFrame.
        mon_1_offset = df2_k.loc[index[0], 'Mn1_off_ft']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        # print('Monument 1 offset for', k, ':' mon_1_offset, 'ft')  # Displays string and value. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df2_k1 = df2_k[df2_k['Sm_off_ft'] == mon_1_offset]  # Creates new single row DataFrame of individual monument 1
        # data from previous DataFrame where survey measurement offset point matches monument 1 offset.
        # column for each survey year.
        # print('Monument 1 data for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df2_k1) # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df3_k = df2_k1.loc[:, 'Mn1_East_m':'Mn2_Nor_m']  # Creates DataFrame of monument coordinates through specified
        # columns of previous DataFrame.
        # print('Monument coordinates for', k) # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df3_k)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        mon1_Easting = df3_k.loc[index[0], 'Mn1_East_m']
        mon1_Northing = df3_k.loc[index[0], 'Mn1_Nor_m']
        mon2_Easting = df3_k.loc[index[0], 'Mn2_East_m']
        mon2_Northing = df3_k.loc[index[0], 'Mn2_Nor_m']
        # print('Monument 1 coordinates:', mon1_Easting, 'm', mon1_Northing, 'm')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Monument 2 coordinates:', mon1_Easting, 'm', mon1_Northing, 'm')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # END PROCESS DISPLAY ------------------------------------------------------------------------------------------

        # print('Monument coordinates selected!')  # Displays string signaling the end of
        # # part 1 for the current range and how long it took to run with a reduced number of significant figures.
        # # Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Part 1 of 4 done!')  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # ==============================================================================================================
        # PART 2: COORDINATE CALCULATIONS -------------------------------------------------------------------------------
        # ==============================================================================================================

        # RANGE OFFSET COMPONENTS & HEADING ----------------------------------------------------------------------------

        deltaE = abs(mon2_Easting - mon1_Easting)  # Easting change between monuments.
        # User note: Absolute value calculated because range heading will control sign, and we desire positive values
        # for later arithmetic.
        # print('Change in Easting:', '%.2f'%deltaE, 'm')  # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        deltaN = abs(mon2_Northing - mon1_Northing)  # Northing change between monuments.
        # print('Change in Northing:', '%.2f'%deltaN, 'm') # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        delta_off = math.sqrt((mon2_Easting - mon1_Easting) ** 2 + (mon2_Northing - mon1_Northing) ** 2)  # Distance
        # between monuments along range-line. Calculated for later error analysis.
        # print('Change in range-line offset:', '%.2f'%delta_off, 'm') # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        heading_rad = math.atan(deltaN / deltaE)  # Calculates range survey heading between monuments in radians.
        # print('Range heading:', '%.2f'%heading_rad, 'radians')  # Displays variable with a reduced number of significant
        # figures. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.

        # Correction
        heading_rad = math.pi - heading_rad  # Range survey heading corrected to match compass direction of survey.
        # User note: Important step considering that the heading calculated initially considers is derived from the
        # unit circle and not a compass system.
        # print('Corrected heading:', '%.2f'%heading_rad, 'radians')  # Displays variable with a reduced number of
        # # significant figures . Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.

        # SAMPLE OFFSETS --------------------------------------------------------------------------------------------------

        # Multipliers ------------------------------------------------------------------------------------

        sin = math.sin(heading_rad)  # Calculates Sine of heading.
        cos = math.cos(heading_rad)  # Calculates Cosine of heading.
        # print('Sine of heading:', '%.2f'%sin) # Displays variable. Enable for check only.
        # print('Cosine of heading:', '%.2f'%cos) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.

        # Base correction -------------------------------------------------------------------------------------------------------

        df_4 = df2_k['Sm_off_ft']  # Create new DataFrame of measurement offsets.
        # print('Sample offsets (ft) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_4)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df_5 = df_4 - mon_1_offset
        # print('Corrected sample offset (ft) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_5)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        convertFtM = 1 / 3.281  # Conversion factor from feet to meters.
        # print('Conversion factor: ft-m:', '%.4f'%convertFtM, 'm/ft') # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df_5m = df_5 * convertFtM  # Converts corrected offsets from ft to m. The desired units.
        # print('Corrrected sample offset (m) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_5m)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # Components -------------------------------------------------------------------------------------------------------

        offsets_east = cos * abs(df_5m)  # Calculates easting offset in m between each survey measurement point and start.
        # User note: The absolute value is used here to simplify future arithmetic.
        # print('Sample offsets east (m) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(offsets_east) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        offsets_north = sin * abs(df_5m)  # Calculates northing offset in m between each survey measurement point and start.
        # User note: The absolute value is used here to simplify future arithmetic.
        # print('Sample offsets north (m) for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(offsets_north) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.

        # SAMPLE COORDINATES ----------------------------------------------------------------------------------------------------------

        eastings = mon1_Easting + offsets_east  # Creates a new DataFrame calculating easting coordinates for all survey
        # measurement points.
        # print('Sample Eastings for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(eastings) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.
        northings = mon1_Northing + offsets_north  # Creates new DataFrame calculating northing coordinates for all survey
        # measurement points.
        # print('Sample Eastings for', k)  # Displays string. Enable for check only.
        # print(northings) # Displays variable. Enable for check only.
        # print() # Inserts blank row to grant space for next displayed items. Enable for check only.

        # DATAFRAME POPULATION -----------------------------------------------------------------------------------------

        # Heading and components -----------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Delta_East'] = deltaE  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Delta_Nor'] = deltaN  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Delta_off'] = delta_off  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Rng_hdng'] = heading_rad  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Offset multipliers ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Hdng_sin'] = sin  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Hdng_cos'] = cos  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Net offsets and components ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cSm_off_ft'] = df_5  # Populates the selected column with the selected variable for the entire
        # DataFrame.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cSm_off_m'] = df_5m  # Populates the selected column with the selected variable for the entire
        # DataFrame.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Sm_off_E'] = offsets_east  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Sm_off_N'] = offsets_north  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # Measurement coordinates ---------------------------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Sm_East'] = eastings  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'Sm_Nor'] = northings  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        # END PROCESS DISPLAY ------------------------------------------------------------------------------------------

        # print('Survey measurement coordinates calculated!')  # Displays string signaling the
        # end of part 2 for the current range and how long it took to run with a reduced number of significant figures.
        # Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Part 2 of 4 done!')  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # ==================================================================================================================
        # PART 3: ERROR ANALYSIS CALCULATIONS -------------------------------------------------------------------------------------------
        # ==================================================================================================================

        # MONUMENT 2 POSITIONAL ERROR ---------------------------------------------------------------------------------------

        df2_k = df_0[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k)]
        # Creates new DataFrame of individual range data from original DataFrame
        # column for each survey year.
        # print('Selected survey data by year:', k)  # Displays string and DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df2_k)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        max = len(df2_k.index)  # Collates number of rows in DataFrame.
        # print('Number of survey measurements during', k, ':', max)  # Displays string and number of rows in DataFrame,
        # also the number of survey measurement points. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        index2 = df2_k.index  # Returns index information about DataFrame.
        mon_2_offset = df2_k1.loc[index2[0], 'Mn2_off_ft']  # Defines variable by selecting first element under specified
        # column in specified DataFrame.
        # print('Monument 2 offset for', k, ':', mon_2_offset, 'ft')  # Displays string and value. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df2_k1 = df2_k[df2_k['Sm_off_ft'] == mon_2_offset]  # Creates new single row DataFrame of individual monument 1
        # data from previous DataFrame where survey measurement offset point matches monument 2 offset.
        # column for each survey year.
        # print('Monument 2 data for', k)  # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df2_k1) # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df3_k = df2_k1.loc[:, 'Sm_East':'Sm_Nor']  # Creates DataFrame of monument coordinates through specified
        # columns of previous DataFrame.
        # print('Calculated monument 2 coordinates for', k) # Displays string. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df3_k)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        df3_k = df3_k.to_numpy()
        # print(df3_k)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        cMon2_Easting = df3_k[0][0]
        cMon2_Northing = df3_k[0][1]
        # print('Calculated monument 2 coordinates:', cMon2_Easting, 'm', cMon2_Northing, 'm')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        delta_mon2_East = mon2_Easting - cMon2_Easting
        delta_mon2_Nor = mon2_Northing - cMon2_Northing
        # print('Coordinate differences for', k)
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print('Easting:', delta_mon2_East, 'm')
        # print('Northing:', delta_mon2_Nor, 'm')
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

        # DATAFRAME POPULATION AND EXPORT -----------------------------------------------------------------------------------------

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cMn2_E_dff'] = delta_mon2_East  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cMn2_N_dff'] = delta_mon2_Nor  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cMn2_East'] = cMon2_Easting  # Selects all rows of original
        # DataFrame pertaining to the appropriate range number and populates the selected column with the selected variable.
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_year'] == k), 'cMn2_Nor'] = cMon2_Northing  # Selects all rows of original DataFrame
        # pertaining to the appropriate range number and populates the selected column with the selected variable.

        df_0.to_csv('/Users/jimmywood/Desktop/Codes/Current/Range_input_data/Range_survey_data_sept19.csv', index=False)
        # Exports DataFrame to path updating the original srvy_data sheet.
        # User note: Change path directory if running program on your own system.
        # print('Range data updated!')  # Displays string. Enable for check only
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # print(df_0)  # Displays DataFrame. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.

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

#     # CREATE GEODATAFRAME & EXPORT VECTOR FILE ----------------------------------------------------------------------------------------------
#
#     for j in srvy_yr:
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
