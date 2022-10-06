# ======================================================================================================================
# ------------------------ WHITEWATER RIVER WATERSHED, MN, SEDIMENTATION SURVEY DATA DIGITIZER -------------------------
# ------------------------ PRIMARY SCRIPT (1/1) ------------------------------------------------------------------------
# ======================================================================================================================

# For information see program documentation.

# ======================================================================================================================
# START! ---------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

print()  # Inserts blank row to provide white space for next display.
print('\033[1m' + 'START!!!' + '\033[0m')  # Displays string.
print('...')  # Displays string.
print()  # Inserts blank row to provide white space for next display.

# ======================================================================================================================
# PART 0: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES & SIGNAL START ----------------------------------------------------------------------------------------

import time  # Imports module enabling the use of time related tools.
import pandas as pd  # Imports module with assignment enabling the use of DataFrames.
import sys  # Imports module enabling the use of system specific tools.
import math  # Imports module enabling the use of Python's standard mathematical tools.
import os  # Imports module enabling interaction with the computer's operating system.
import geopandas as gpd  # Imports module enabling the use of geographic data.
import warnings  # Imports module enabling direct warning intervention.
import matplotlib.pyplot as plt  # Imports module enabling the use of plotting tools.

startTime0 = time.time()  # Starts clock to measure program length.
# User note: Enable if information is desired.

# SET UP DIRECTORIES ---------------------------------------------------------------------------------------------------

# Input ----------------------------------------------------------------------------------------------------------------

newpath0 = '/Users/jimmywood/Desktop/Codes/Current/Input/Digitizer'  # Sets path to input workbook of all sedimentation
# survey data.
newfile0 = '/WW_sed_survey_data.csv'  # Sets name of input workbook .csv.
srvy_data = pd.read_csv(newpath0 + newfile0)  # Imports .csv file of all sedimentation survey data.

# Output ---------------------------------------------------------------------------------------------------------------

directory = 'Output'  # Sets name of new directory where all data will be exported.
if not os.path.exists(directory):  # Creates new folder with above name or skips step if already exists.
    os.mkdir(directory)
    print('Output directory', '\033[0;32m' + directory + '\033[0m', 'created')  # Displays string with
    # directory in green.
newpath1 = '/Users/jimmywood/Desktop/Codes/Current/Output/Digitizer/Workbook'  # Sets path and folder name of new
# directory where updated workbook will be exported.
newfile1 = '/Sed_survey_data.csv'  # Sets name of exported workbook.
newpath2 = '/Users/jimmywood/Desktop/Codes/Current/Output/Digitizer/GIS'  # Sets path and folder name of new
# directory where GIS files will be exported
geopackage = '/WW_sed_surveys.gpkg'  # Sets geopackage name.
newpath3 = newpath2 + geopackage  # Sets path directly to geopackage.
if not os.path.exists(newpath1):  # Creates new folder with above name or skips step if already exists.
    os.makedirs(newpath1)
    print('Secondary folder', '\033[0;32m' + 'Workbook' + '\033[0m', 'created')  # Displays string with
    # directory in green.
if not os.path.exists(newpath2):  # Creates new folder with above name or skips step if already exists.
    os.makedirs(newpath2)
    print('Secondary folder', '\033[0;32m' + 'GIS' + '\033[0m', 'created')  # Displays string with
    # directory in green.
# print()  # Inserts blank row to provide white space for next display.
# breakpoint()  # Inserts breakpoint, halting code.

# SET UP TOGGLES -------------------------------------------------------------------------------------------------------

# Stream channel -------------------------------------------------------------------------------------------------------

All_channels = 0  # Pre-selects all survey data for digitization.
Channel_1R = 0  # Pre-selects survey data along the river's main trunk for digitization.
chnl_1R = 'Main Stem'  # Defines variable. Sets associated stream channel.
Channel_2R = 0  # Pre-selects survey data along a main river branch for digitization.
chnl_2R = 'Middle Fork'  # Defines variable. Sets associated stream channel.
Channel_3R = 0  # Pre-selects survey data along a main river branch for digitization.
chnl_3R = 'North Fork'  # Defines variable. Sets associated stream channel.
Channel_4R = 0  # Pre-selects survey data along a main river branch for digitization.
chnl_4R = 'South Fork'  # Defines variable. Sets associated stream channel.
Channel_1T = 0  # Pre-selects survey data along a tributary for digitization.
chnl_1T = 'Trout Creek'  # Defines variable. Sets associated stream channel.
Channel_2T = 0  # Pre-selects survey data along a tributary for digitization.
chnl_2T = 'Beaver Creek'  # Defines variable. Sets associated stream channel.
Channel_3T = 0  # Pre-selects survey data along a tributary for digitization.
chnl_3T = 'Logan Creek'  # Defines variable. Sets associated stream channel.
Channel_4T = 0  # Pre-selects survey data along a tributary for digitization.
chnl_4T = 'Dry Creek'  # Defines variable. Sets associated stream channel.
Custom = 1  # Pre-selects specific survey data for digitization. Selection may cross river basins.
cstm = 'Custom set '  # Defines variable. Sets associated stream channel.

if All_channels == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 94  # Defines variables with the desired spatial  loop limits.
elif Channel_1R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 13  # Defines variables with the desired spatial  loop limits.
elif Channel_2R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 14, 26  # Defines variables with the desired spatial  loop limits.
elif Channel_3R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 27, 48  # Defines variables with the desired spatial  loop limits.
elif Channel_4R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 49, 69  # Defines variables with the desired spatial  loop limits.
elif Channel_1T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 70, 73  # Defines variables with the desired spatial  loop limits.
elif Channel_2T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 74, 79  # Defines variables with the desired spatial  loop limits.
elif Channel_3T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 80, 87  # Defines variables with the desired spatial  loop limits.
elif Channel_4T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 88, 94  # Defines variables with the desired spatial  loop limits.
elif Custom == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 2  # Defines variables with the desired spatial  loop limits.
else:
    print()
    sys.exit('Unable to select spatial limits')
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# Bearing --------------------------------------------------------------------------------------------------------------

brng_meas = 0  # Selects bearing value. True = field measured. False = code calculated.

# ======================================================================================================================
# DIGITIZER ------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

# CREATE PRIMARY DATAFRAME ---------------------------------------------------------------------------------------------

df_0 = pd.DataFrame(srvy_data)  # Creates DataFrame from imported workbook for manipulation in Python.
pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.

# Check
# print('\033[1m' + 'All SURVEY DATA' + '\033[0m')  # Displays string in bold.
# print('...')  # Displays string.
# print(df_0)  # Displays DataFrame.
# print()  # Inserts blank row to provide white space for next display.
# breakpoint()  # Inserts breakpoint, halting code.

# SELECT SPATIAL LOOP LIMITS -------------------------------------------------------------------------------------------

def createlist(limit1, limit2):  # Defines function establishing framework for first loop limit assignment.
    return [item for item in range(limit1, limit2 + 1)]

r1, r2 = r1, r2   # Defines variables with the desired loop limits.
rng_num = createlist(r1, r2)  # Defines list as loop limits.

# Check
# print('\033[1m' + 'Spatial loop limits:' + '\033[0m', 'Survey ranges', rng_num[0],  '&',  rng_num[-1])  # Displays
# string and limits of list.
# print()  # Inserts blank row to provide white space for next display.
# breakpoint()  # Inserts breakpoint, halting code.

# PRIMARY LOOP =========================================================================================================

for i in rng_num:  # Begins primary spatial loop through all selected range numbers.

    # ==================================================================================================================
    # PART 1: DATA SELECTION -------------------------------------------------------------------------------------------
    # ==================================================================================================================

    # SELECT RANGE SUB-DATASET -----------------------------------------------------------------------------------------

    df_1 = df_0[df_0['Range_num'] == i]  # Creates new DataFrame of individual range data from original DataFrame with
    # specified selection.

    # Check
    # print('\033[1m' + 'SINGLE RANGE SURVEY DATA' + '\033[0m')  # Displays string in bold.
    # print('...')  # Displays string.
    # print(df_1)  # Displays DataFrame.
    # print()  # Inserts blank row to provide white space for next display.
    # breakpoint()  # Inserts breakpoint, halting code.

    # SELECT TEMPORAL LOOP LIMITS --------------------------------------------------------------------------------------

    df_01 = df_1.loc[:, 'Srvy_num']  # Creates new DataFrame from all rows of specified column of specified DataFrame.
    df_01 = df_01.drop_duplicates(keep = 'first')  # Drops all duplicate values from DataFrame.

    # Check
    # print('\033[1m' + 'RANGE SURVEY NUMBERS' + '\033[0m')  # Displays string in bold.
    # print('...')  # Displays string.
    # print(df_01)  # Displays DataFrame.
    # print()  # Inserts blank row to provide white space for next display.
    # breakpoint()  # Inserts breakpoint, halting code.

    srvy_num_list = df_01.values.tolist()

    # Check
    # print('\033[1m' + 'RANGE SURVEY NUMBERS' + '\033[0m')  # Displays string in bold.
    # print('...')  # Displays string.
    # print(srvy_num_list)  # Displays list.
    # print()  # Inserts blank row to provide white space for next display.
    # breakpoint()  # Inserts breakpoint, halting code.

    s1 = int(srvy_num_list[0])  # Assigns variable as integer of first element of specified list.
    s2 = int(srvy_num_list[-1])  # Assigns variable as integer of last element of specified list.

    # Check
    # print(s1, s2)  # Displays variable values.
    # print()  # Inserts blank row to provide white space for next display.
    # breakpoint()  # Inserts breakpoint, halting code.

    def createlist(limit1, limit2):  # Defines function establishing framework for second loop limit assignment.
        return [item for item in range(limit1, limit2 + 1)]

    s1, s2 = s1, s2  # Defines variables with the desired loop limits.
    srvy_yr = createlist(s1, s2)  # Defines list as loop limits.

    # Check
    # print('\033[1m' + 'Temporal loop limits:' + '\033[0m', 'Survey years', rng_num[0],  '&',  rng_num[-1])  # Displays
    # string and limits of list.
    # print()  # Inserts blank row to provide white space for next display.
    # breakpoint()  # Inserts breakpoint, halting code.

    # SECONDARY LOOP ===================================================================================================

    for k in srvy_yr:  # Establishes secondary temporal loop through all survey years.

        # SELECT SURVEY YEAR SUB-SUB-DATASET ---------------------------------------------------------------------------

        df_2 = df_1[df_1['Srvy_num'] == k]  # Creates new DataFrame of individual survey data from individual range
        # DataFrame with specified selection.

        # Check
        # print('\033[1m' + 'SINGLE SURVEY DATA:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_2)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # ESTABLISH INDEXING FRAMEWORK ---------------------------------------------------------------------------------

        max_num = len(df_2.index)  # Collates number of rows in DataFrame.
        index = df_2.index  # Returns index information about DataFrame.

        # Check
        # print('\033[1m' + 'NUMBER OF SURVEY MEASUREMENTS) -' + '\033[0m', 'Year', k, ':', max)  # Displays string and
        # variable value.
        # print('\033[1m' + 'INDEX:' + '\033[0m', 'Year', k)  # Displays string and variable value.
        # print('...')  # Displays string.
        # print(index)  # Displays index values for whole DataFrame.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # REPORT SURVEY DATA SUB-SUBSET INFORMATION --------------------------------------------------------------------

        str_chnnl = df_2.loc[index[0], 'Str_chnnl']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        print('\033[1m' + 'Stream channel:' + '\033[0m', str_chnnl)   # Displays string in bold and variable value.
        srvy_rng = df_2.loc[index[0], 'Srvy_range']  # Assigns variable to the first element of specified DataFrame
        # column with specified index.
        print('\033[1m' + 'Survey range number' + '\033[0m', i)  # Display strings in bold and variable values.
        srvy_dt = df_2.loc[index[0], 'Srvy_date']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        print('\033[1m' + 'Survey number' + '\033[0m', k, 'of', srvy_yr[-1], ',',
              'surveyed on', srvy_dt)  # Displays strings in bold and variable values.
        brng_ref = df_2.loc[index[0], 'Brng_R_dir']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        brng_angl = df_2.loc[index[0], 'Brng_A']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        brng_dir = df_2.loc[index[0], 'Brng_A_dir']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        brng_fnctl = df_2.loc[index[0], 'Brng_fnctl']
        print('\033[1m' + 'Range bearing:' + '\033[0m', brng_ref, brng_angl, brng_dir)  # Displays string in bold and
        # variable values.
        print('\033[1m' + 'Measurements recorded:' + '\033[0m', max_num)  # Displays string in bold and variable value.
        print()  # Inserts blank row to grant space for next displayed items.

        # Check
        # breakpoint()  # Inserts breakpoint, halting code.

        # SELECT BENCHMARK POSITIONS -----------------------------------------------------------------------------------

        Mn1_East_std = df_2.loc[index[0], 'Mn1_East_m']  # Defines variable (endpoint 1 Easting standard value) as the
        # first element of specified DataFrame column with specified index.
        Mn1_North_std = df_2.loc[index[0], 'Mn1_Nor_m']  # Defines variable (endpoint 1 Northing standard value) as the
        # first element of specified DataFrame column with specified index.
        Mn2_East_std = df_2.loc[index[0], 'Mn2_East_m']  # Defines variable (endpoint 2 Easting standard value) as the
        # first element of specified DataFrame column with specified index.
        Mn2_North_std = df_2.loc[index[0], 'Mn2_Nor_m']  # Defines variable (endpoint 2 Northing standard value) as the
        # first element of specified DataFrame column with specified index.

        # Check
        # print('\033[1m' + 'Benchmark 1 coordinates:' + '\033[0m',  Mn1_East_std, 'm E, &', Mn1_North_std, 'm N')
        # Displays string in bold and variable values.
        # print('\033[1m' + 'Benchmark 2 coordinates:' + '\033[0m', Mn2_East_std, 'm E, &', Mn2_North_std, 'm N')
        # Displays string in bold and variable values.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # ==============================================================================================================
        # PART 2: COORDINATE CALCULATIONS ------------------------------------------------------------------------------
        # ==============================================================================================================

        # SURVEY OFFSETS -----------------------------------------------------------------------------------------------

        deltaE = Mn2_East_std - Mn1_East_std  # Defines variable. Calculates Easting change between benchmarks.
        deltaN = Mn2_North_std - Mn1_North_std  # Defines variable. Calculates Northing change between benchmarks.
        deltaOff = math.sqrt(deltaE ** 2 + deltaN ** 2)  # Defines variable. Calculates range-line distance between
        # benchmarks.
        convertMtF = 3.281 / 1  # Defines variable. Sets conversion factor from meters to feet.
        deltaOff_ft = deltaOff * convertMtF  # Defines variable. Converts units of variable from meters to feet.

        # Check
        # print('\033[1m' + 'Change in Easting:' + '\033[0m', '%.2f' % deltaE, 'm')  # Displays string in bold and
        # variable value.
        # print('\033[1m' + 'Change in Northing:' + '\033[0m', '%.2f' % deltaN, 'm')  # Displays string in bold and
        # variable value.
        # print('\033[1m' + 'Conversion factor m-ft:' + '\033[0m', '%.4f'%convertMtF, 'm/ft') # Displays string.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        Mn1_offset = df_2.loc[index[0], 'Mn1_off_ft']  # Defines variable (endpoint 1 survey offset) as the first
        # element of specified DataFrame column with specified index.
        Mn2_offset = df_2.loc[index[0], 'Mn2_off_ft']  # Defines variable (endpoint 2 survey offset) as the first
        # element of specified DataFrame column with specified index.
        deltaOff_meas = Mn2_offset - Mn1_offset  # Defines variable. Calculates range-line distance between benchmarks
        # from survey data.
        DeltaOff = abs(deltaOff_meas - deltaOff_ft)  # Defines variable. Calculates difference between distance between
        # benchmark estimates.

        # Check
        # print('\033[1m' + 'Benchmark separation:' + '\033[0m')  # Displays string in bold.
        # print('Calculated:', '%.2f' % deltaOff_ft, 'ft')  # Displays string and variable value.
        # print('Measured:', '%.2f' % deltaOff_meas, 'ft')  # Displays string and variable value.

        if abs(DeltaOff) > 3.281:  # Sets loop for variable value reporting.
            print('\033[0;30m' + 'Benchmark separation difference:' + '\033[0;31m', '%.2f' % DeltaOff, 'ft' + '\033[0m')
            # Displays string in bold and variable value, setting font to red when absolute value of difference exceeds
            # specified threshold of 1 m.
        else:
            print('\033[0;30m' + 'Benchmark separation difference:' + '\033[0;36m', '%.2f' % DeltaOff, 'ft' + '\033[0m')
            # Displays string in bold and variable value, setting font to cyan when value of difference lies within
            # specified threshold.
            # User note: Color Codes: Dark gray = 30, Bright red = 31, Bright green = 32, Yellow = 33, Bright blue = 34,
            # Bright magenta = 35, Bright cyan = 36, White = 37.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # SURVEY HEADING -----------------------------------------------------------------------------------------------

        # Field measured -----------------------------------------------------------------------------------------------

        convertDtR = math.pi / 180  # Defines variable. Sets conversion factor from degrees to radians.

        bearing_deg = brng_angl  # Defines variable as measured survey bearing.
        bearing_rad = bearing_deg * convertDtR  # Defines variable. Converts units to radians.

        if brng_ref == 'N':  # Establishes loop to correct bearing angle where bearing reference is North.
            if brng_dir == 'E':  # Establishes loop to correct bearing angle where bearing direction is East.
                if brng_fnctl == 'NE' or 'SW':  # Establishes loop to correct bearing angle where functional bearing
                    # satisfies condition.
                    # print('\033[1m' + 'Measured heading - 1st quadrant or equivalent' + '\033[0m')  # Displays string
                    # in bold. Enable for check only.
                    # deg_min = 0  # Defines variable as lowest true membership value in quadrant. Enable for check
                    # only.
                    deg_max = 90  # Defines variable as highest true membership value in quadrant.
                    # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                    # Enable for check only.
                    if deg_max > bearing_deg:
                        # print('Bearing angle inside, shift to corresponding azimuth')  # Displays string. Enable for
                        # check only.
                        cBearing_deg = deg_max - bearing_deg  # Defines variable. Calculates corrected bearing.
                    else:
                        print()
                        sys.exit('Heading exceeds limits')
            elif brng_dir == 'W':  # Establishes loop to correct bearing angle where bearing direction is West.
                if brng_fnctl == 'NW' or 'SE':  # Establishes loop to correct bearing angle where functional bearing
                    # satisfies condition.
                    # print('\033[1m' + 'Measured heading - 2nd quadrant or equivalent' + '\033[0m')  # Displays string
                    # in bold. Enable for check only.
                    deg_min = 90  # Defines variable as lowest true membership value in quadrant.
                    # deg_max = 180  # Defines variable as highest true membership value in quadrant. Enable for check
                    # only.
                    # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                    # Enable for check only.
                    if deg_min > bearing_deg:
                        # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        cBearing_deg = deg_min + bearing_deg  # Defines variable. Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check
                        # only.
                    else:
                        print()
                        sys.exit('Heading exceeds limits')
        elif brng_ref == 'S':  # Establishes loop to correct bearing angle where bearing reference is South.
            if brng_dir == 'W':  # Establishes loop to correct bearing angle where bearing direction is West.
                if brng_fnctl == 'SW' or 'NE':  # Establishes loop to correct bearing angle where functional bearing
                    # satisfies condition.
                    # print('\033[1m' + 'Measured heading - 3rd quadrant, equivalent to 1st' + '\033[0m')  # Displays
                    # string in bold. Enable for check only.
                    deg_min = 180  # Defines variable as lowest true membership value in quadrant.
                    deg_max = 270  # Defines variable as highest true membership value in quadrant.
                    # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                    # Enable for check only.
                    if deg_min > bearing_deg:
                        # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                        # check only/
                        cBearing_deg = deg_max - deg_min - bearing_deg  # Defines variable. Calculates corrected
                        # bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
                    else:
                        print()
                        sys.exit('Heading exceeds limits')
            elif brng_dir == 'E':  # Establishes loop to correct bearing angle where bearing direction is East.
                if brng_fnctl == 'SE' or 'NW':  # Establishes loop to correct bearing angle where functional bearing
                    # satisfies condition.
                    # print('\033[1m' + 'Measured heading - 4th quadrant' + '\033[0m')  # Displays string in bold.
                    # Enable for check only.
                    deg_min = 270  # Defines variable as lowest true membership value in quadrant.
                    deg_max = 360  # Defines variable as highest true membership value in quadrant.
                    # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                    # Enable for check only.
                    if deg_min > bearing_deg:
                        # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        cBearing_deg = deg_min - (deg_max/2) + bearing_deg  # Defines variable. Calculates corrected
                        # bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
                    else:
                        print()
                        sys.exit('Heading exceeds limits')
        cBearing_rad = cBearing_deg * convertDtR  # Defines variable. Converts units from degrees to radians
        # print('Corrected bearing, measured:', cBearing_deg, 'degrees, or,', '%.2f' % cBearing_rad, 'radians')
            # Displays string and variable value. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # GPS Interpolated ---------------------------------------------------------------------------------------------

        exp_bearing_rad = abs(math.atan(deltaN / deltaE))  # Defines variable. Calculates survey heading between monuments in
        # radians.
        # exp_bearing_rad = exp_bearing_rad + math.pi
        # Check
        # print('\033[1m' + 'Bearing:' + '\033[0m', '%.2f' % exp_bearing_rad, 'radians')  # Displays string in bold.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        if deltaN > 1:
            if deltaE > 1:
                # print('\033[1m' + 'Calculated heading - 1st quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                # rad_min = 0  # Defines variable as lowest true membership value in quadrant. Enable for check only.
                # Enable for check only.
                rad_max = math.pi/2  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', '%.2f' % rad_min, '-', '%.2f' % rad_max, 'radians')  # Displays string and
                # variable values. Enable for check only.
                if rad_max > exp_bearing_rad:
                    # print('Bearing angle inside, equals corresponding azimuth')  # Displays string. Enable for check
                    # only.
                    exp_bearing_rad = exp_bearing_rad  # Defines variable. # Calculates corrected bearing.
                else:
                    print()
                    sys.exit('Heading exceeds limits')
            elif deltaE < 1:
                # print('\033[1m' + 'Calculated heading - 2nd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                rad_min = math.pi/2   # Defines variable as lowest true membership value in quadrant.
                rad_max = math.pi  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', '%.2f' % rad_min, '-', '%.2f' % rad_max, 'radians')  # Displays string and
                # variable values. Enable for check only.
                if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant max.
                    # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for check
                    # only.
                    exp_bearing_rad = rad_max - exp_bearing_rad  # Defines variable. # Calculates corrected
                    # bearing.
                    # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
                else:
                    print()
                    sys.exit('Heading exceeds limits')
        if deltaN < 1:
            if deltaE < 1:
                # print('\033[1m' + 'Calculated heading - 3rd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                rad_min = math.pi  # Defines variable as lowest true membership value in quadrant.
                # rad_max = 3/2 * math.pi  # Defines variable as highest true membership value in quadrant. Enable for
                # check only.
                # print('Angular swath:', rad_min, '-', rad_max, 'radians')  # Displays string and variable values.
                # Enable for check only.
                if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant min.
                    # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                    # check only.
                    exp_bearing_rad = rad_min + exp_bearing_rad  # Defines variable.
                    # Calculates corrected bearing.
                    # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
                else:
                    print()
                    sys.exit('Heading exceeds limits')
            if deltaE > 1:
                # print('\033[1m' + 'Calculated heading - 4th quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only/
                rad_min = 3/2 * math.pi  # Defines variable as lowest true membership value in quadrant.
                rad_max = 2 * math.pi  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', rad_min, '-', rad_max, 'radians')  # Displays string and variable values.
                # Enable for check only.
                if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant min.
                    # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                    # check only.
                    exp_bearing_rad = rad_max + exp_bearing_rad  # Defines variable.
                    # Calculates corrected bearing.
                    # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
                else:
                    print()
                    sys.exit('Heading exceeds limits')
        exp_bearing_deg = exp_bearing_rad * convertDtR ** -1  # Defines variable. Converts units from radians to degrees.
        # print('Corrected bearing, experimental:', '%.2f' % exp_bearing_deg, 'degrees, or,', '%.2f' % exp_bearing_rad,
        #       'radians')  # Displays string and variable values.

        deltaB_deg = abs(exp_bearing_deg - cBearing_deg)  # Defines variable. Calculates difference between recorded and
        # calculated bearings in degrees.
        deltaB_rad = abs(exp_bearing_rad - cBearing_rad)  # Defines variable. Calculates difference between recorded and
        # calculated bearings in radians.
        if deltaB_deg != 0:  # Sets loop for variable value reporting if it equals anything other than zero.
            if deltaB_rad != 0:  # Sets loop for variable value reporting if it equals anything other than zero.
                print('\033[0;30m' 'Heading difference:' + '\033[0;31m', '%.2f' % deltaB_deg, 'degrees',
                      '&', '%.2f' % deltaB_rad, 'radians' + '\033[0m')  # Displays string in bold and variable values,
                # setting font to red when absolute value of difference exceeds specified threshold.
        else:
            print('\033[0;30m' + 'Heading difference:' + '\033[0;36m', '%.2f' % deltaB_deg, 'degrees',
                  '&', '%.2f' % deltaB_rad, 'radians' +'\033[0m')  # Displays string in bold and variable value, setting
            # font to cyan when value of difference lies within specified threshold.
            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.
        # print()  # Inserts blank row to grant space for next displayed items. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # MEASUREMENT OFFSET COMPONENTS --------------------------------------------------------------------------------

        # Trigonometric Multipliers ------------------------------------------------------------------------------------

        if brng_meas == 1:  # Loop establishing variable selection for bearing via initial toggle.
            bearing = cBearing_rad  # Selects variable value if condition is met.
        else:
            bearing = exp_bearing_rad  # Selects variable value if conditions is not met.

        sin = math.sin(bearing)  # Calculates Sine of heading.
        cos = math.cos(bearing)  # Calculates Cosine of heading.

        # Check
        # print('\033[1m' + 'Sine of heading:' + '\033[0m', '%.2f' % sin)  # Displays string in bold and
        # # variable value.
        # print('\033[1m' + 'Cosine of heading:' + '\033[0m', '%.2f' % cos,)  # Displays string in bold and
        # # variable value.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Offset Correction --------------------------------------------------------------------------------------------

        df_3 = df_2['Sm_off_ft']  # Creates new single column DataFrame of survey data offsets from individual survey
        # DataFrame with specified selection.

        # Check
        # print('\033[1m' + 'SINGLE SURVEY OFFSETS:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_3)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        df_3 = df_3 - Mn1_offset  # Creates new DataFrame. Calculates corrected survey offsets to set benchmark position
        # at 0.

        # Check
        # print('\033[1m' + 'SURVEY OFFSETS CORRECTED:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_3)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        df_3m = df_3 * convertMtF ** -1  # Creates new DataFrame. Converts corrected offsets from feet to meters.

        # Check
        # print('\033[1m' + 'SURVEY OFFSETS CORRECTED & CONVERTED:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_3m)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Offset Components --------------------------------------------------------------------------------------------

        offsets_East = cos * df_3m  # Creates new DataFrame. Calculates Easting offsets between each survey
        # measurement point and zero point.

        # Check
        # print('\033[1m' + 'MEASUREMENT EAST COMPONENTS:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(offsets_East)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        offsets_North = sin * df_3m  # Creates new DataFrame. Calculates Northing offsets between each survey
        # measurement point and zero point.

        # Check
        # print('\033[1m' + 'MEASUREMENT NORTH COMPONENTS:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(offsets_North)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # MEASUREMENT COORDINATES --------------------------------------------------------------------------------------

        meas_eastings = Mn1_East_std + offsets_East  # Creates new DataFrame. Calculates Easting coordinate for all
        # survey points.

        # Check
        # print('\033[1m' + 'MEASUREMENT EASTING COORDINATES:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(meas_eastings)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        meas_northings = Mn1_North_std + offsets_North  # Creates new DataFrame. Calculates Northing coordinate for all
        # survey points.

        # Check
        # print('\033[1m' + 'MEASUREMENT NORTHING COORDINATES:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(meas_northings)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # ==============================================================================================================
        # PART 3: ERROR ANALYSIS CALCULATIONS --------------------------------------------------------------------------
        # ==============================================================================================================

        # GENERATE NEW DATAFRAME 1 -------------------------------------------------------------------------------------

        # Create -------------------------------------------------------------------------------------------------------

        df_02 = df_2.copy(deep = True)  # Creates new DataFrame. Copies individual survey DataFrame for population to
        # then populate empty DataFrame .

        # Check
        # print('\033[1m' + 'ALL DATA:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_02)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Populate -----------------------------------------------------------------------------------------------------

        # Index
        df_02['Nm_samples'] = max_num  # Appends specified DataFrame column with specified variable.

        # Survey Offsets
        df_02['Delta_East'] = deltaE  # Appends specified DataFrame column with specified variable.
        df_02['Delta_Nor'] = deltaN  # Appends specified DataFrame column with specified variable.
        df_02['Delta_off'] = deltaOff_ft  # Appends specified DataFrame column with specified variable.
        df_02['Dlt_o_meas'] = deltaOff_meas  # Appends specified DataFrame column with specified variable.
        df_02['Dlt_o_dff'] = DeltaOff  # Appends specified DataFrame column with specified variable.

        # Survey Heading
        df_02['cBrng_A'] = bearing_deg  # Appends specified DataFrame column with specified variable.
        df_02['Brng_rd'] = bearing_rad  # Appends specified DataFrame column with specified variable.
        df_02['cBrng_rd'] = cBearing_rad  # Appends specified DataFrame column with specified variable.
        df_02['cl_Brng_A'] = exp_bearing_deg  # Appends specified DataFrame column with specified variable.
        df_02['Brng_A_dff'] = deltaB_deg  # Appends specified DataFrame column with specified variable.
        df_02['cl_Brng_rd'] = exp_bearing_rad  # Appends specified DataFrame column with specified variable.
        df_02['Brng_R_dff'] = deltaB_rad  # Appends specified DataFrame column with specified variable.

        # Trigonometric Multipliers
        df_02['Sin'] = sin  # Appends specified DataFrame column with specified variable.
        df_02['Cos'] = cos  # Appends specified DataFrame column with specified variable.

        # Offset Corrections
        df_02['cSm_off_ft'] = df_3  # Appends specified DataFrame column with specified variable.
        df_02['cSm_off_m'] = df_3m  # Appends specified DataFrame column with specified variable.

        # Offset Components
        df_02['Sm_off_E'] = offsets_East  # Appends specified DataFrame column with specified variable.
        df_02['Sm_off_N'] = offsets_North  # Appends specified DataFrame column with specified variable.

        # Measurement Coordinates
        df_02['Sm_East'] = meas_eastings  # Appends specified DataFrame column with specified variable.
        df_02['Sm_Nor'] = meas_northings  # Appends specified DataFrame column with specified variable.

        # Check
        # print('\033[1m' + 'APPENDED DATA:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_02)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # BENCHMARK POSITIONAL ERROR -----------------------------------------------------------------------------------

        index = df_02.index[df_02['Sm_off_ft'] == Mn2_offset].tolist()  # Returns index information about specified
        # DataFrame element and returns as list.
        index = index[0]  # Defines variable as list element.

        # Check
        # print('\033[1m' + 'Position index of benchmark offset - ' + '\033[0m', 'Year', k, ':', index)  # Displays
        # string in bold and specified list element.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        Mn2_East_calc = df_02.loc[index, 'Sm_East']  # Defines variable from indexed DataFrame element of specified
        # column.
        Mn2_North_calc = df_02.loc[index, 'Sm_Nor']  # Defines variable from indexed DataFrame element of specified
        # column.

        # Check
        # print('\033[1m' + 'Benchmark 2 measured coordinates:' + '\033[0m',
        #       '%.2f' % Mn2_East_std, 'm E, &', '%.2f' % Mn2_North_std, 'm N')  # Displays string in bold and
        # variable values.
        # print('\033[1m' + 'Benchmark 2 calculated coordinates:' + '\033[0m',
        #       '%.2f' % Mn2_East_calc, 'm E, &', '%.2f' % Mn2_North_calc, 'm N')  # Displays string in bold and
              # variable values.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        Mn2_deltaE = abs(Mn2_East_std - Mn2_East_calc)  # Defines variable. Calculates difference between standard and
        # experimental Eastings.
        Mn2_deltaN = abs(Mn2_North_std - Mn2_North_calc)  # Defines variable. Calculates difference between standard and
        # experimental Northings.

        if Mn2_deltaE > 1:  # Sets loop for variable value reporting if difference exceeds specified threshold of 1 m.
            print('\033[0;30m' + 'Easting difference:' + '\033[0;31m', '%.2f' % Mn2_deltaE, 'm' + '\033[0m')
            # Displays string in bold and variable value, setting font to red when value of difference exceeds
            # specified threshold.
        else:
            print('\033[0;30m' + 'Easting difference:' + '\033[0;36m',  '%.2f' % Mn2_deltaE, 'm' + '\033[0m')
            # Displays string in bold and variable value, setting font to cyan when value of difference lies within
            # specified threshold.
        if Mn2_deltaN > 1:  # Sets loop for variable value reporting if difference exceeds specified threshold of 1 m.
            print('\033[0;30m' + 'Northing difference:' + '\033[0;31m', '%.2f' % Mn2_deltaN, 'm' + '\033[0m')
            # Displays string in bold and variable value, setting font to red when value of difference exceeds
            # specified threshold.
        else:
            print('\033[0;30m' + 'Northing difference:' + '\033[0;36m', '%.2f' % Mn2_deltaN, 'm' + '\033[0m')
            # Displays string in bold and variable value, setting font to cyan when value of difference lies within
            # specified threshold.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Check
        # plt.figure(figsize = (4.5, 3.5))  # Creates plot of specified size.
        # ax = plt.gca()  # Defines variable. Gets current axes instance.
        # ax.scatter(meas_eastings, meas_northings, s = 5, c = 'Orange', marker = 'o', alpha = 0.5)  # Creates scatter
        # plot of specified arrays from axes instance with specified marker size, color, type, and transparency,
        # respectively.
        # ax.scatter(Mn1_East_std, Mn1_North_std, s=5, c='Blue', marker='o', alpha=0.5)  # Creates scatter plot of
        # specified arrays from axes instance with specified marker size, color, type, and transparency, respectively.
        # ax.scatter(Mn2_East_std, Mn2_North_std, s=5, c='Blue', marker='o', alpha=0.5)  # Creates scatter plot of
        # specified arrays from axes instance with specified marker size, color, type, and transparency, respectively.
        # plt.xlabel('Easting (m)', fontsize = 8)  # Creates x axis label specified by string and font size.
        # plt.ylabel('Northing (m)', fontsize = 8)  # Creates y axes label specified by string and font size.
        # plt.title('Starting and Interpolated Coordinates Range ' + str(i) + ' Year ' + str(k),  fontsize = 8)
        # Creates plot title specified by string and font size.
        # plt.show()  # Displays plot.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # GENERATE NEW DATAFRAME 2 -------------------------------------------------------------------------------------

        # Create -------------------------------------------------------------------------------------------------------

        df_00 = df_0.copy(deep = True)  # Creates new DataFrame. Copies original, empty, input DataFrame for population.

        # Check
        # print('\033[1m' + 'OUTPUT WORKBOOK:' + '\033[0m')  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_00)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Populate -----------------------------------------------------------------------------------------------------

        # Experimental benchmark Coordinates
        df_02['cMn2_East'] = Mn2_East_calc  # Appends specified DataFrame column with specified variable.
        df_02['cMn2_Nor'] = Mn2_North_calc  # Appends specified DataFrame column with specified variable.

        # Coordinate errors
        df_02['cMn2_E_dff'] = Mn2_deltaE  # Appends specified DataFrame column with specified variable.
        df_02['cMn2_N_dff'] = Mn2_deltaN  # Appends specified DataFrame column with specified variable.

        # Check
        # print('\033[1m' + 'APPENDED DATA:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_02)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        df_00.loc[(df_00['Range_num'] == i) & (df_00['Srvy_num'] == k)] = df_02

        # Check
        # print('\033[1m' + 'ALL DATA APPENDED:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_00)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # ==============================================================================================================
        # PART 4: GIS SHAPEFILE GENERATION -----------------------------------------------------------------------------
        # ==============================================================================================================

        # CREATE GEODATAFRAME ------------------------------------------------------------------------------------------

        gdf = gpd.GeoDataFrame(df_02, geometry = gpd.points_from_xy(df_02.Sm_East, df_02.Sm_Nor), crs = 'EPSG:26915')
        # Creates GeoDataframe from specified DataFrame columns and with geographic coordinate system assignment.

        # Check
        # print('\033[1m' + 'GEODATAFRAME:' + '\033[0m', 'Range number', i, 'Year', k)  # Displays string in bold.
        # print('Coordinate system:', gdf.crs)  # Displays string and geographic coordinate system.
        # print('...')  # Displays string.
        # # print(gdf)  # Displays GeoDataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # ==============================================================================================================
        # PART 5: DATA EXPORT ------------------------------------------------------------------------------------------
        # ==============================================================================================================

        # WORKBOOK -----------------------------------------------------------------------------------------------------

        df_00.to_csv(newpath1 + newfile1, index = False)  # Exports DataFrame as .csv to specified folder without row
        # indices.
        # print()  # Inserts blank row to provide white space for next display. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # GIS FILES ----------------------------------------------------------------------------------------------------

        shapefile = 'R' + str(i) + '_S' + str(k) + '.shp'  # Sets name of shapefile.

        gdf.to_file(newpath3, driver = 'GPKG', index = False)  # Creates and exports geopackage at specified path.
        gdf.to_file(newpath3, layer = shapefile, index = False)  # Exports shapefile to geopackage.
        # print()  # Inserts blank row to provide white space for next display. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

    print('-----------------------------------------------------------------------------------------------------------')
    print()  # Inserts blank row to grant space for next displayed items.

    # CODE PROGRESS TIMING =============================================================================================

    if All_channels == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 13:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
            startTime1 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 26:  # Establishes loop when condition met.
            executionTime1 = (time.time() - startTime1)  # Calculates how long it took to run since clock start.
            startTime2 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 48:  # Establishes loop when condition met.
            executionTime2 = (time.time() - startTime2)  # Calculates how long it took to run since clock start.
            startTime3 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 69:  # Establishes loop when condition met.
            executionTime3 = (time.time() - startTime3)  # Calculates how long it took to run since clock start.
            startTime4 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 73:  # Establishes loop when condition met.
            executionTime4 = (time.time() - startTime4)  # Calculates how long it took to run since clock start.
            startTime5 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 79:  # Establishes loop when condition met.
            executionTime5 = (time.time() - startTime5)  # Calculates how long it took to run since clock start.
            startTime6 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 87:  # Establishes loop when condition met.
            executionTime6 = (time.time() - startTime6)  # Calculates how long it took to run since clock start.
            startTime7 = time.time()  # Starts new clock to measure how long script takes.
        elif i == 94:  # Establishes loop when condition met.
            executionTime7 = (time.time() - startTime7)  # Calculates how long it took to run since clock start.
    elif Channel_1R == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 13:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_2R == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 26:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_3R == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 48:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_4R == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 69:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_1T == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 73:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_2T == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 79:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_3T == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 87:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Channel_4T == 1:  # Establishes nested loop for progress timing when condition met.
        if i == 94:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    elif Custom == 1:  # Establishes nested loop for progress timing when condition met.
        if i == r2:  # Establishes loop when condition met.
            executionTime0 = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    # print()  # Inserts blank row to provide white space for next display. Enable for check only.
    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# CODE PROGRESS REPORTING ==============================================================================================

if All_channels == 1:  # Establishes nested loop for progress timing when condition met.
    print(chnl_1R + 'surveys digitized in', '%.4f' % executionTime0, 's','!')  # Displays string.
    print(chnl_2R + 'surveys digitized in', '%.4f' % executionTime1, 's', '!')  # Displays string.
    print(chnl_3R + 'surveys digitized in', '%.4f' % executionTime2, 's', '!')  # Displays string.
    print(chnl_4R + 'surveys digitized in', '%.4f' % executionTime3, 's', '!')  # Displays string.
    print(chnl_1T + 'surveys digitized in', '%.4f' % executionTime4, 's', '!')  # Displays string.
    print(chnl_2T + 'surveys digitized in', '%.4f' % executionTime5, 's', '!')  # Displays string.
    print(chnl_3T + 'surveys digitized in', '%.4f' % executionTime6, 's', '!')  # Displays string.
    print(chnl_4T + 'surveys digitized in', '%.4f' % executionTime7, 's', '!')  # Displays string.
    executionTimeEnd = (time.time() - startTime0)  # Calculates how long it took to run since clock start.
    if executionTimeEnd > 60:  # Establishes loop for progress timing when condition met.
        executionTimeEnd = executionTimeEnd / 60  # Converts execution time to minutes.
    print('All sedimentation survey srvy_data digitized!:', '%.4f' % executionTimeEnd, 'min')  # Displays string.
elif Channel_1R == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_1R + 'surveys digitized in', '%.4f' % executionTime0, 's','!')  # Displays string.
elif Channel_2R == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_2R + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_3R == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_3R + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_4R == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_4R + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_1T == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_1T + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_2T == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_2T + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_3T == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_3T + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Channel_4T == 1:  # Establishes loop for progress timing when condition met.
    print(chnl_4T + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
elif Custom == 1:  # Establishes loop for progress timing when condition met.
    print(cstm + 'surveys digitized in', '%.4f' % executionTime0, 's', '!')  # Displays string.
# print()  # Inserts blank row to provide white space for next display. Enable for check only.
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

print()  # Inserts blank row to grant space for next displayed items.
print('...')  # Displays string.
print('\033[1m' + 'END!!!' + '\033[0m')  # Displays string in bold signaling the end of the program.

# ======================================================================================================================
# END! -----------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
