# ======================================================================================================================
# ------------------------ WHITEWATER RIVER WATERSHED, MN, SEDIMENTATION SURVEY DATA DIGITIZER -------------------------
# ------------------------ PRIMARY SCRIPT (1/1) ------------------------------------------------------------------------
# ======================================================================================================================

# For information see program documentation: README Sed_survey_digitizer.rtf.

# ======================================================================================================================
# START! ---------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

print()  # Inserts blank row to provide white space for next display.
print('\033[1m' + 'START!' + '\033[0m')  # Displays string.
print('...')  # Displays string.
print()  # Inserts blank row to provide white space for next display.

# ======================================================================================================================
# PART 0: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT ---------------------------------------------------------------------------------------------------------------

# Modules --------------------------------------------------------------------------------------------------------------

import time  # Imports module enabling the use of time related tools.
import pandas as pd  # Imports module with assignment enabling the use of DataFrames.
import sys  # Imports module enabling the use of system specific tools.
import math  # Imports module enabling the use of Python's standard mathematical tools.
import numpy
import os  # Imports module enabling interaction with the computer's operating system.
import geopandas as gpd  # Imports module enabling the use of geographic data.
import warnings  # Imports module enabling direct warning intervention.

# Signal start
startTime0 = time.time()  # Starts clock to measure program length.
# User note: Enable if information is desired.

# Sedimentation survey data --------------------------------------------------------------------------------------------

srvy_data = pd.read_csv(r'/Users/jimmywood/Desktop/Codes/Current/Range_input_data/WwR_sed_survey_data.csv')  # Imports
# .csv file of all sedimentation survey data.
# User note: Change path directory.

# TOGGLES --------------------------------------------------------------------------------------------------------------

# Stream channel -------------------------------------------------------------------------------------------------------

All_channels = 0  # Pre-selects all survey data for digitization.
Channel_1R = 1  # Pre-selects survey data along the river's main trunk (Main Stem, WW only) for digitization.
Channel_2R = 0  # Pre-selects survey data along a main river branch (Middle Fork, WW only) for digitization.
Channel_3R = 0  # Pre-selects survey data along a main river branch (North Fork, WW only) for digitization.
Channel_4R = 0  # Pre-selects survey data along a main river branch (South Fork, WW only) for digitization.
Channel_1T = 0  # Pre-selects survey data along a tributary (Trout Creek, WW only) for digitization.
Channel_2T = 0  # Pre-selects survey data along a tributary (Beaver Creek, WW only) for digitization.
Channel_3T = 0  # Pre-selects survey data along a tributary (Logan Creek, WW only) for digitization.
Channel_4T = 0  # Pre-selects survey data along a tributary (Dry Creek, WW only) for digitization.
Custom = 0  # Pre-selects specific survey data for digitization. Selection may cross river basins.

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

    df_01 = df_1.loc[:, 'Srvy_num']
    df_01 = df_01.drop_duplicates(keep = 'first')

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
        print('\033[1m' + 'Survey range' + '\033[0m', i,
              '(', 'Number', i,')')  # Display strings in bold and variable values.
        srvy_dt = df_2.loc[index[0], 'Srvy_date']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        print('\033[1m' + 'Survey number' + '\033[0m', k, 'of', srvy_yr[-1], ',',
              'surveyed on', srvy_dt)  # Displays strings in bold and variable values.
        brng_ref = df_2.loc[index[0], 'Brng_R_dir']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        brng_angl = df_2.loc[index[0], 'Brng_angle']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        brng_dir = df_2.loc[index[0], 'Brng_A_dir']  # Defines variable as the first element of specified DataFrame
        # column with specified index.
        print('\033[1m' + 'Range bearing:' + '\033[0m', brng_ref, brng_angl, brng_dir)  # Displays string in bold and
        # variable values.
        print('\033[1m' + 'Measurements recorded:' + '\033[0m', max_num)  # Displays string in bold and variable value.
        print('---------------------------')  # Displays string.
        # print()  # Inserts blank row to grant space for next displayed items.

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
        DeltaOff = deltaOff_meas - deltaOff_ft  # Defines variable. Calculates difference between distance between
        # benchmark estimates.

        # Check
        # print('\033[1m' + 'Benchmark separation:' + '\033[0m')  # Displays string in bold.
        # print('Calculated:', '%.2f' % deltaOff_ft, 'ft')  # Displays string and variable value.
        # print('Measured:', '%.2f' % deltaOff_meas, 'ft')  # Displays string and variable value.
        if abs(DeltaOff) > 3.281:  # Sets loop for variable value reporting.
            print('\033[1;31m' + 'Benchmark separation difference:', '%.2f' % DeltaOff + 'ft' + '\033[0m')  # Displays
            # string in bold and variable value, setting font to red when absolute value of difference exceeds specified
            # threshold of 1 m (3.281 ft).
        else:
            print('Benchmark separation difference:', '%.2f' % DeltaOff, 'ft')  # Displays string and variable value.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # SURVEY HEADING -----------------------------------------------------------------------------------------------

        # Field measured -----------------------------------------------------------------------------------------------

        convertDtR = math.pi / 180  # Defines variable. Sets conversion factor from degrees to radians.

        bearing_deg = brng_angl  # Defines variable as measured survey bearing.

        if brng_ref == 'N':  # Establishes loop where bearing reference is North.
            if brng_dir == 'E':  # Establishes loop wher bearing direction is East.
                # print('\033[1m' + 'Measured heading - 1st quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                deg_min = 1  # Defines variable as lowest true membership value in quadrant.
                deg_max = 89  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                # Enablefor check only.
                # print('Bearing angle inside, shift to corresponding azimuth')  # Displays string. Enable for check
                # only.
                bearing_deg = deg_max + 1 - bearing_deg  # Defines variable. Calculates corrected bearing.
            elif brng_dir == 'W':  # Establishes loop wher bearing direction is West.
                # print('\033[1m' + 'Measured heading - 2nd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                deg_min = 91  # Defines variable as lowest true membership value in quadrant.
                deg_max = 179  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                # Enable for check only.
                if deg_max > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant max.
                    if deg_min > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant
                        # min.
                        # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        bearing_deg = bearing_deg + deg_min - 1  # Defines variable. Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check
                        # only.
        elif brng_ref == 'S':  # Establishes loop where bearing reference is South.
            if brng_dir == 'W':  # Establishes loop wher bearing direction is West.
                # print('\033[1m' + 'Measured heading - 3rd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                deg_min = 181  # Defines variable as lowest true membership value in quadrant.
                deg_max = 269  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                # Enable for check only.
                if deg_max > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant max.
                    if deg_min > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant
                        # min.
                        # print('Bearing angle outside of, shift to correct quadrant')  # Displays string. Enable for
                        # check only/
                        bearing_deg = deg_max + 1 - bearing_deg  # Defines variable. Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
            elif brng_dir == 'E':  # Establishes loop wher bearing direction is East.
                # print('\033[1m' + 'Measured heading - 4th quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                deg_min = 271  # Defines variable as lowest true membership value in quadrant.
                deg_max = 359  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', deg_min, '-', deg_max, 'degrees')  # Displays string and variable values.
                # Enable for check only.
                if deg_max > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant max.
                    if deg_min > bearing_deg:  # Establishes loop to determine relative value of bearing to quadrant
                        # min.
                        # print('Bearing angle outside of, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        bearing_deg = deg_min - 1 + bearing_deg  # Defines variable. Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
        bearing_rad = bearing_deg * convertDtR  # Defines variable. Converts units from degrees to radians
        # print('Corrected bearing:', bearing_deg, 'degrees, or,', '%.2f' % bearing_rad, 'radians')  # Displays string
        # and variable value. Enable for check only.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # GPS Interpolated ---------------------------------------------------------------------------------------------

        exp_bearing_rad = math.atan(deltaN / deltaE)  # Defines variable. Calculates survey heading between monuments in
        # radians.

        # Check
        # print('\033[1m' + 'Bearing:' + '\033[0m', '%.2f' % bearing_rad, 'radians')  # Displays string in bold.
        # print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        if deltaN > 1:
            if deltaE > 1:
                # print('\033[1m' + 'Calculated heading - 1st quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                rad_min = 1 * convertDtR  # Defines variable as lowest true membership value in quadrant.
                rad_max = 89 * convertDtR  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', '%.2f' % rad_min, '-', '%.2f' % rad_max, 'radians')  # Displays string and
                # variable values. Enable for check only.
                # print('Bearing angle inside, shift to corresponding azimuth')  # Displays string. Enable for check
                # only.
                exp_bearing_rad = rad_max + (1 * convertDtR) - abs(exp_bearing_rad)  # Defines variable. Calculates
                # corrected bearing.
            elif deltaE < 1:
                # print('\033[1m' + 'Calculated heading - 2nd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                rad_min = 91 * convertDtR  # Defines variable as lowest true membership value in quadrant.
                rad_max = 179  * convertDtR  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', '%.2f' % rad_min, '-', '%.2f' % rad_max, 'radians')  # Displays string and
                # variable values. Enable for check only.
                if rad_max > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant max.
                    if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                        # quadrant min.
                        # print('Bearing angle outside, shift to correct quadrant')  # Displays string. Enable for check
                        # only.
                        exp_bearing_rad = rad_min - (1 * convertDtR) + abs(exp_bearing_rad)  # Defines variable.
                        # Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
        if deltaN < 1:
            if deltaE < 1:
                # print('\033[1m' + 'Calculated heading - 3rd quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only.
                rad_min = 181 * convertDtR  # Defines variable as lowest true membership value in quadrant.
                rad_max = 269 * convertDtR  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', rad_min, '-', rad_max, 'radians')  # Displays string and variable values.
                # Enable for check only.
                if rad_max > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant max.
                    if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                        # quadrant min.
                        # print('Bearing angle outside of, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        exp_bearing_rad = rad_max + (1 * convertDtR) - abs(exp_bearing_rad)  # Defines variable.
                        # Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
            if deltaE > 1:
                # print('\033[1m' + 'Calculated heading - 4th quadrant' + '\033[0m')  # Displays string in bold. Enable
                # for check only/
                rad_min = 271 * convertDtR  # Defines variable as lowest true membership value in quadrant.
                rad_max = 359 * convertDtR  # Defines variable as highest true membership value in quadrant.
                # print('Angular swath:', rad_min, '-', rad_max, 'radians')  # Displays string and variable values.
                # Enable for check only.
                if rad_max > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                    # quadrant max.
                    if rad_min > abs(exp_bearing_rad):  # Establishes loop to determine relative value of bearing to
                        # quadrant min.
                        # print('Bearing angle outside of, shift to correct quadrant')  # Displays string. Enable for
                        # check only.
                        exp_bearing_rad = rad_min - (1 * convertDtR) + abs(exp_bearing_rad)  # Defines variable.
                        # Calculates corrected bearing.
                        # print('Angle inside, equals corresponding azimuth')  # Displays string. Enable for check only.
        exp_bearing_deg = exp_bearing_rad * (1/convertDtR)  # Defines variable. Converts units from radians to degrees.
        # print('Corrected bearing:', '%.2f' % exp_bearing_rad, 'radians, or,', '%.2f' % exp_bearing_deg, 'degrees')
        # Displays string and variable values.

        deltaB_deg = exp_bearing_deg - bearing_deg  # Defines variable. Calculates difference between recorded and
        # calculated bearings in degrees.
        deltaB_rad = exp_bearing_rad - bearing_rad  # Defines variable. Calculates difference between
        # recorded and calculated bearings in radians.
        if deltaB_deg != 0:  # Sets loop for variable value reporting.
            if deltaB_deg != 0:
                print('\033[1;31m' 'Heading difference:', '%.2f' % deltaB_deg, 'degrees',
                      '&', '%.2f' % deltaB_rad, 'radians' + '\033[0m')  # Displays string in bold and variable value,
                # setting font to red when absolute value of difference exceeds specified threshold.
        else:
            print('Heading difference:', '%.2f' % deltaB_deg, 'degrees', '&', '%.2f' % deltaB_rad, 'radians')
            # Displays string in bold and variable value, setting font to red when absolute value of difference exceeds
            # specified threshold.
            # breakpoint()  # Inserts breakpoint, halting code.
        print()  # Inserts blank row to grant space for next displayed items.
        # breakpoint()  # Inserts breakpoint, halting code.

        # MEASUREMENT OFFSET COMPONENTS --------------------------------------------------------------------------------

        # Trigonometric Multipliers ------------------------------------------------------------------------------------

        if brng_meas == 1:
            bearing_rad = bearing_rad
        else:
            bearing_rad = exp_bearing_rad

        sin = math.sin(bearing_rad)  # Calculates Sine of heading.
        cos = math.cos(bearing_rad)  # Calculates Cosine of heading.

        # Check
        # print('\033[1m' + 'Sine of heading:' + '\033[0m', '%.2f' % sin)  # Displays string in bold and
        # # variable value.
        # print('\033[1m' + 'Cosinee of heading:' + '\033[0m', '%.2f' % cos,)  # Displays string in bold and
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

        df_3m = df_3 * 1/convertMtF  # Creates new DataFrame. Converts corrected offsets from feet to meters.

        # Check
        # print('\033[1m' + 'SURVEY OFFSETS CORRECTED & CONVERTED:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(df_3m)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Offset Components --------------------------------------------------------------------------------------------

        offsets_East = cos * abs(df_3m)  # Creates new DataFrame. Calculates Easting offsets between each survey
        # measurement point and zero point.

        # Check
        # print('\033[1m' + 'MEASUREMENT EAST COMPONENTS:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(offsets_East)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        offsets_North = sin * abs(df_3m)  # Creates new DataFrame. Calculates Northing offsets between each survey
        # measurement point and zero point.

        # Check
        # print('\033[1m' + 'MEASUREMENT NORTH COMPONENTS:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(offsets_North)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # MEASUREMENT COORDINATES --------------------------------------------------------------------------------------

        meas_eastings = Mn1_East_std + offsets_East  # Creates new DataFrame. Calculates Easting coordinate for all survey
        # points.

        # Check
        # print('\033[1m' + 'MEASUREMENT EASTING COORDINATES:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(meas_eastings)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        meas_northings = Mn1_North_std + offsets_North  # Creates new DataFrame. Calculates Northing coordinate for all survey
        # points.

        # Check
        # print('\033[1m' + 'MEASUREMENT NORTHING COORDINATES:' + '\033[0m', 'Year', k)  # Displays string in bold.
        # print('...')  # Displays string.
        # print(meas_northings)  # Displays DataFrame.
        # print()  # Inserts blank row to provide white space for next display.
        # breakpoint()  # Inserts breakpoint, halting code.

        # DATAFRAME POPULATION -----------------------------------------------------------------------------------------

        # Heading and components ---------------------------------------------------------------------------------------
        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Nm_samples'] = max_num  # Selects all rows of original
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

        df_0.loc[(df_0['Range_num'] == i) & (df_0['Srvy_num'] == k), 'Sm_East'] = meas_eastings  # Selects all rows of original DataFrame
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
        max_num = len(df_2.index)  # Collates number of rows in DataFrame.
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
