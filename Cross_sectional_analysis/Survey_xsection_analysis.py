# ======================================================================================================================
# -------------------* WHITEWATER RIVER WATERSHED, MN, SEDIMENTATION SURVEY CROSS-SECTION ANALYZER *--------------------
# ======================================================================================================================

# For information see program documentation.

# ======================================================================================================================
# START! ---------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

print()  # Inserts blank row to provide white space for next display.
print('\033[1m' + 'START!!!' + '\033[0m', '\n...', '\n')  # Displays string. Makes font bold and adds new lines.
# breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

# ======================================================================================================================
# PART 0: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES & SIGNAL START ----------------------------------------------------------------------------------------

import time  # Imports (time access and conversions) module enabling time related functions.
import pandas as pd  # Imports (python data analysis library) module with assignment enabling DataFrame creation and
# analysis.
from pandas.core.common import SettingWithCopyWarning  # Imports warning identification.
import sys  # Imports (system-specific parameters and functions) module enabling interaction with the interpreter
# system.
import os  # Imports (miscellaneous operating system interfaces) module enabling interaction with the computer's
# operating system.
import matplotlib.pyplot as plt  # Imports (visualization with python) module enabling plotting tools.
import sympy as sy  # Imports module with assignment enabling symbolic math tools.
import  scipy as sc  # Imports module with assignment enabling scientific math tools.
import numpy as np  # Imports module with assignment enabling scientific math tools.
import warnings  # Imports module enabling direct warning intervention.

startTime0 = time.time()  # Starts clock to measure program or step length.

# SET UP DIRECTORIES ---------------------------------------------------------------------------------------------------

# Input data -----------------------------------------------------------------------------------------------------------

inpt_fldr = '/Users/jimmywood/Desktop/Codes/Current/Input/Analysis'  # Sets folder path to input workbook of all
# digitized sedimentation survey data.
inpt_fl = '/Sed_survey_data.csv'  # Sets end file path to input workbook.

# Upload
srvy_data = pd.read_csv(inpt_fldr + inpt_fl)  # Creates DataFrame from .csv file from path.

# Output data ----------------------------------------------------------------------------------------------------------

# Create primary folders
directory = 'Output'  # Sets name of new directory where all data will be exported.
if not os.path.exists(directory):  # Creates new folder with above name or skips step if already exists.
    os.mkdir(directory)
    print('Output directory (OD) Level 1', '\033[0;32m' + directory + '\033[0m', 'created')  # Displays string. Makes
    # font green.

# Set up sub-folders
opt_fldr = '/Users/jimmywood/Desktop/Codes/Current/Output'  # Sets path to output folder for all generated data.
anl_fldr = '/Analysis'  # Sets end path of sub-folder for all analysis products.
xsct_fldr = '/Cross_Sections'  # Sets end path of sub-folder where all cross-section data will be exported.
plts_fldr = '/Plots'  # Sets end path of sub-folder where all cross-section plots will be exported.
plts_sfldr1 = ['/Main_Stem', '/Middle_Fork', '/North_Fork', '/South_Fork', '/Trout_Creek', '/Beaver_Creek',
              '/Logan_Creek', '/Dry_Creek']  # Sets end path of sub-folder where cross-section plots will be
# exported by stream channel.
plts_sfldr2 = ['/Single_Range', '/Single_Survey', '/Shaded_Area_PW', '/Shaded_Area_TMnl', '/Interp_Comparison',
               '/Shaded_Area_Interp']  # Sets end path of sub-folder where cross-section plots will be exported by
# type.
ars_fldr = '/Areas'  # Sets end path of sub-folder where cross-sectional area data will be exported.

# Create sub-folders
if not os.path.exists(opt_fldr + anl_fldr):  # Creates new folder with set name or skips step if already exists.
    os.makedirs(opt_fldr + anl_fldr)
    print('OD Level 2', '\033[0;32m' + '/Output' + anl_fldr + '\033[0m', 'created')  # Displays string. Makes font
    # green.
if not os.path.exists(opt_fldr + anl_fldr + xsct_fldr):  # Creates new folder with set name or skips step if already
    # exists.
    os.makedirs(opt_fldr + anl_fldr + xsct_fldr)
    print('OD Level 3', '\033[0;32m' + '/Output' + anl_fldr + xsct_fldr + '\033[0m', 'created')  # Displays string.
    # Makes font green.
if not os.path.exists(opt_fldr + anl_fldr + xsct_fldr + plts_fldr):  # Creates new folder with set name or skips step
    # if already exists.
    os.makedirs(opt_fldr + anl_fldr + xsct_fldr + plts_fldr)
    print('OD Level 4', '\033[0;32m' + '/Output' + anl_fldr + xsct_fldr + plts_fldr + '\033[0m', 'created')  # Displays
    # string. Makes font green.
for a in plts_sfldr1:
    if not os.path.exists(opt_fldr + anl_fldr + xsct_fldr + plts_fldr + a):  # Creates new folder with set name or
        # skips step if already exists.
        os.makedirs(opt_fldr + anl_fldr + xsct_fldr + plts_fldr + a)
        print('OD Level 5', '\033[0;32m' + '/Output' + anl_fldr + xsct_fldr + plts_fldr + a + '\033[0m', 'created')
        # Displays string. Makes font green.
    for b in plts_sfldr2:
        if not os.path.exists(opt_fldr + anl_fldr + xsct_fldr + plts_fldr + a + b):  # Creates new folder with set name
            # or skips step if already exists.
            os.makedirs(opt_fldr + anl_fldr + xsct_fldr + plts_fldr + a + b)
            print('OD Level 6', '\033[0;32m' + '/Output' + anl_fldr + xsct_fldr + plts_fldr + b + '\033[0m', 'created')
            # Displays string. Makes font green.
if not os.path.exists(opt_fldr + anl_fldr + xsct_fldr + ars_fldr):  # Creates new folder with set name or skips step if
    # already exists.
    os.makedirs(opt_fldr + anl_fldr + xsct_fldr + ars_fldr)
    print('OD Level 4', '\033[0;32m' + '/Output' + anl_fldr + xsct_fldr + ars_fldr + '\033[0m', 'created') # Displays
    # string. Makes font green.

# Check
# print('\033[1m' + 'Output directory created!' + '\033[0m', '\n')  # Displays string. Makes font bold and adds new
# line.
# breakpoint()  # Inserts breakpoint, halting code.

# SET UP TOGGLES -------------------------------------------------------------------------------------------------------

# Data selection -------------------------------------------------------------------------------------------------------

# Stream channel

All_channels = 0  # Pre-selects all survey data for analysis.
Channel_1R = 0  # Pre-selects survey data along the river's main trunk for analysis.
chnl_1R = 'Main Stem'  # Defines variable. Sets associated stream channel.
Channel_2R = 0  # Pre-selects survey data along a main river branch for analysis.
chnl_2R = 'Middle Fork'  # Defines variable. Sets associated stream channel.
Channel_3R = 0  # Pre-selects survey data along a main river branch for analysis.
chnl_3R = 'North Fork'  # Defines variable. Sets associated stream channel.
Channel_4R = 0  # Pre-selects survey data along a main river branch for analysis.
chnl_4R = 'South Fork'  # Defines variable. Sets associated stream channel.
Channel_1T = 0  # Pre-selects survey data along a tributary for analysis.
chnl_1T = 'Trout Creek'  # Defines variable. Sets associated stream channel.
Channel_2T = 0  # Pre-selects survey data along a tributary for analysis.
chnl_2T = 'Beaver Creek'  # Defines variable. Sets associated stream channel.
Channel_3T = 0  # Pre-selects survey data along a tributary for analysis.
chnl_3T = 'Logan Creek'  # Defines variable. Sets associated stream channel.
Channel_4T = 0  # Pre-selects survey data along a tributary for analysis.
chnl_4T = 'Dry Creek'  # Defines variable. Sets associated stream channel.
Custom = 1  # Pre-selects specific survey data for plotting and analysis. Selection may cross river basins.
cstm = 'Custom set '  # Defines variable. Sets associated stream channel.

if All_channels == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 94  # Defines variables with the desired spatial loop limits.
elif Channel_1R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 13  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[0]  # Defines variable as output path.
elif Channel_2R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 14, 26  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[1]  # Defines variable as output path.
elif Channel_3R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 27, 48  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[2]  # Defines variable as output path.
elif Channel_4R == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 49, 69  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[3]  # Defines variable as output path.
elif Channel_1T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 70, 73  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[4]  # Defines variable as output path.
elif Channel_2T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 74, 79  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[5]  # Defines variable as output path.
elif Channel_3T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 80, 87  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[6]  # Defines variable as output path.
elif Channel_4T == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 88, 94  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[7]  # Defines variable as output path.
elif Custom == 1:  # Loop establishing variables for custom selection rules.
    r1, r2 = 1, 2  # Defines variables with the desired spatial loop limits.
    plts_sfldr1 = plts_sfldr1[0]  # Defines variable as output path.
else:
    var = 1 == 1  # Dummy true statement to provide required indentation for else statement.
    sys.exit('Unable to select spatial limits')

# Check
# print('\033[1m' + 'Stream channel dataset selected!' + '\033[0m', '\n')  # Displays string. Makes font bold and adds
# new lines.
# breakpoint()  # Inserts breakpoint, halting code.

# Data operations ------------------------------------------------------------------------------------------------------

# Cross-sectional area
A_pwise_mnl = 0   # Pre-selects calculation of area under one cross-section through manual piecewise fitting.
A_trap_mnl = 1   # Pre-selects calculation of area under one cross-section through manual composite trapezoid rule.
A_trap_ato = 1  # Pre-selects calculation of area under one cross-section through automatic composite trapezoid rule.
A_trap_btw = 0    # Pre-selects calculation of area between two cross-sections through manual composite trapezoid rule.

# Plots
colors1 = ['Orange', 'Blue', 'Green', 'Purple', 'Red', 'Yellow']  # Defines list designating primary colors for
# cross-section data. For later selection.
colors2 = ['Red', 'Cyan', 'Yellow', 'Magenta', 'Orange', 'Orange']  # Defines list designating secondary colors for
# cross-section area data. For later selection.
lbl_srvy_cmp = ['Measured', 'Interpolated']  # Defines list designating data source to compare measured vs.
# interpolated datasets. For later selection.

# Check
# print('\033[1m' + 'Plot colors and labels selected!' + '\033[0m', '\n')  # Displays string. Makes font bold and adds
# new lines.
# breakpoint()  # Inserts breakpoint, halting code.

# CREATE PRIMARY DATAFRAME OF INPUT DATA -------------------------------------------------------------------------------

# Master ---------------------------------------------------------------------------------------------------------------

df_all = pd.DataFrame(srvy_data)  # Creates DataFrame from imported workbook. For manipulation in Python.
# pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns. Enable for
# check only.

# Check
# print('\033[1m' + 'All DIGITIZED SURVEY DATA' + '\033[0m', '\n...', '\n', df_all, '\n')  # Displays objects. Makes
# font bold and adds new lines.
# breakpoint()  # Inserts breakpoint, halting code.

# Copy -----------------------------------------------------------------------------------------------------------------

df_all_c = df_all.copy(deep=True)  # Creates copy of DataFrame. For later population and export.

df_all_c = df_all_c.drop(['Srvy_date', 'Brng_R_dir', 'Brng_A', 'Brng_A_dir', 'Brng_fnctl',
                          'cBrng_A', 'Brng_rd', 'cBrng_rd', 'Nm_samples', 'Sample_num', 'Sm_elev_ft', 'Sm_off_ft',
                          'Sm_desc', 'BM_Sm_site', 'S_bor_ordr', 'Srvy_stat', 'Monument_1', 'Mn1_desc', 'Monument_2',
                          'Mn2_desc', 'Mn1_off_ft', 'Mn2_off_ft', 'S_bor1_off', 'S_borF_off', 'Mn1_East_m', 'Mn1_Nor_m',
                          'Mn2_East_m', 'Mn2_Nor_m', 'cSm_off_ft', 'cSm_off_m', 'Delta_East', 'Delta_Nor', 'Delta_off',
                          'Dlt_o_meas', 'Dlt_o_dff', 'cl_Brng_A', 'Brng_A_dff', 'cl_Brng_rd', 'Brng_R_dff', 'Sin',
                          'Cos', 'Sm_off_E', 'Sm_off_N', 'Sm_East', 'Sm_Nor', 'cMn2_East', 'cMn2_Nor', 'cMn2_E_dff',
                          'cMn2_N_dff'], axis=1)  # Drops columns from DataFrame. To eliminate data not relevant to
# the present analyses.

new_columns = ['X1_ft_pw', 'X2_ft_pw', 'Y1_ft_pw', 'Y2_ft_pw', 'DeltaY_ft', 'DeltaX_ft', 'Slope', 'B1_ft', 'B2_ft',
               'B_int_ft', 'A_intvl_pw', 'A_net_pw', 'X1_ft_tm', 'X2_ft_tm', 'Y1_ft_tm', 'Y2_ft_tm', 'A_intvl_tm',
               'A_net_tm', 'A_net_ta']  # Creates list of column labels to add to DataFrame.

df_all_c[new_columns] = ''  # Adds empty columns to DataFrame.

# Check
# print('\033[1m' + 'All DIGITIZED SURVEY DATA, TRUNCATED COPY' + '\033[0m', '\n...', '\n', df_all_c, '\n')  # Displays
# objects. # Makes font bold and adds new lines.
# breakpoint()  # Inserts breakpoint, halting code.

df_interpolated_all = pd.DataFrame()  # Creates new DataFrame. For later population.

new_columns = ['Str_chnnl', 'Range_num', 'Srvy_num1', 'Srvy_num2', 'X1_in', 'X2_in', 'Y1_1', 'Y1_2', 'Y2_1', 'Y2_2',
               'A_intvl_in', 'A_net_in', 'A_net_pos', 'A_net_neg']  # Creates list of column  # Creates list of column
# labels to add to DataFrame.

df_interpolated_all[new_columns] = ''  # Adds empty columns to DataFrame.

df_interpolated_all_c = df_interpolated_all.copy(deep=True)  # Creates copy of DataFrame. For later population and
# export.

# Check
# print('\033[1m' + 'ALL INTERPOLATED SURVEY DATA!' + '\033[0m', '\n...', df_interpolated, '\n')  # Displays objects.
# Makes font bold and adds new lines.
# breakpoint()  # Inserts breakpoint, halting code.

# ESTABLISH SPATIAL LOOP LIMITS ----------------------------------------------------------------------------------------

def createlist(limit1, limit2):  # Defines function establishing framework for loop limit assignment.
    return [item for item in range(limit1, limit2 + 1)]


r1, r2 = r1, r2  # Defines variables with the desired loop limits.
rng_num = createlist(r1, r2)  # Defines list between loop limits.

# Check
# print('\033[1m' + 'Spatial loop limits:' + '\033[0m', 'Survey ranges', r1,  '&',  r2, '\n')  # Displays objects.
# Makes font bold and adds new lines.
# breakpoint()  # Inserts breakpoint, halting code.

# ======================================================================================================================
# PART 1: DATA SELECTION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

for i in rng_num:  # Establishes framework for loop through range numbers.

    # CREATE DATAFRAME OF INDIVIDUAL RANGE DATA ------------------------------------------------------------------------

    df_rng = df_all[(df_all['Range_num'] == i)]  # Creates new Dataframe from slice of pre-existing DataFrame. All rows
    # satisfying selection.

    # Check
    # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY DATA' + '\033[0m', '\n...', '\n', df_rng, '\n')  # Displays
    # objects. Makes font bold and adds new lines.
    # breakpoint()  # Inserts breakpoint, halting code.

    # SELECT & ESTABLISH TEMPORAL LOOP LIMITS --------------------------------------------------------------------------

    df_srvy_nums = df_rng.loc[:, 'Srvy_num']  # Creates new DataFrame from slice of pre-existing DataFrame of all rows
    # satisfying selection.

    df_srvy_nums = df_srvy_nums.drop_duplicates(keep='first')  # Updates DataFrame by dropping all duplicate values in
    # columns.
    srvy_list = df_srvy_nums.values.tolist()  # Creates list from DataFrame elements.

    # Check
    # print('\033[1m' + 'Survey numbers for range number ' + str(i) + ': \033[0m', srvy_list, '\n') # Displays objects.
    # Makes font bold and adds new lines.
    # breakpoint()  # Inserts breakpoint, halting code.

    s1 = int(srvy_list[0])  # Defines variable as integer of first and last elements of list.
    s2 = int(srvy_list[-1])  # Defines variable as integer of first and last elements of list.

    def createlist(limit1, limit2):  # Defines function establishing framework for second loop limit assignment.
        return [item for item in range(limit1, limit2 + 1)]


    s1, s2 = s1, s2  # Defines variables with the desired loop limits.
    srvy_num = createlist(s1, s2)  # Defines list as loop limits.

    # Check
    # print('\033[1m' + 'Temporal loop limits:' + '\033[0m', 'Surveys', s1,  '&',  s2, '\n') # Displays objects. Makes
    # font bold and adds new lines.
    # breakpoint()  # Inserts breakpoint, halting code.

    df_srvy_yrs = df_rng.loc[:, 'Srvy_year']  # Creates new DataFrame from slice of pre-existing DataFrame of all rows
    # satisfying selection. For later visualization.
    df_srvy_yrs = df_srvy_yrs.drop_duplicates(keep='first')  # Updates DataFrame, dropping all duplicate values.
    srvy_yrList = df_srvy_yrs.values.tolist()  # Creates list from DataFrame elements.

    # Check
    # print('\033[1m' + 'Survey years for range number ' + str(i) + ': \033[0m', srvy_yrList, '\n') # Displays objects.
    # Makes font bold and adds new lines.
    # breakpoint()  # Inserts breakpoint, halting code.


    for j in srvy_num:  # Establishes framework for loop through survey numbers.

        # CREATE DATAFRAME OF INDIVIDUAL SURVEY DATA -------------------------------------------------------------------

        # Master -------------------------------------------------------------------------------------------------------

        df_srvy = df_rng[df_rng['Srvy_num'] == j]  # Creates new DataFrame from slice of pre-existing DataFrame of all
        # rows satisfying selection.

        # Check
        # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' DATA' + '\033[0m', '\n...', '\n', df_srvy, '\n')
        # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        # Copy ---------------------------------------------------------------------------------------------------------

        df_srvy_c = df_all_c[(df_all_c['Range_num'] == i) & (df_all_c['Srvy_num'] == j)]  # Creates new DataFrame from
        # slice of pre-existing DataFrame of all rows satisfying selection. For later population and export.

        # Check
        # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' DATA COPY' + '\033[0m', '\n...', '\n',
        # df_srvy_c, '\n') # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        # SELECT XY DATA -----------------------------------------------------------------------------------------------

        # From field data ----------------------------------------------------------------------------------------------

        x_set = df_srvy.loc[:, 'Sm_off_ft']  # Creates new DataFrame from slice of pre-existing DataFrame of all rows
        # satisfying selection.
        y_set = df_srvy.loc[:, 'Sm_elev_ft']  # Creates new DataFrame from slice of pre-existing DataFrame of all rows
        # satisfying selection.

        # Check
        # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + '\033[0m', '\n...', '\nX values', '\n', x_set,
        #       '\nY values', '\n', y_set, '\n')  # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        x_list = x_set.tolist()  # Create list from DataFrame elements.
        y_list = y_set.tolist()  # Create list from DataFrame elements.

        if j == 1:   # Establishes condition where operations below executed.

            x_lists = []  # Creates empty list.
            y_lists = []  # Creates empty list.
            x_lists.append(x_list)  # Appends list to list. For later comparison.
            y_lists.append(y_list)  # Appends list to list. For later comparison.

        elif j != 1:   # Establishes condition where operations below executed.

            x_lists.append(x_list)  # Appends list to list. For later comparison.
            y_lists.append(y_list)  # Appends list to list. For later comparison.

        # Check
        # print('\033[1m' + 'Range ' + str(i) + ' Survey ' + str(j) + '\033[0m', '\n...', '\nX values:', x_list,
        #       '\nY values:', y_list, '\n')  # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        # From interpolated data ---------------------------------------------------------------------------------------

        if A_trap_btw == 1:   # Establishes condition where operations below executed.

            f = sc.interpolate.interp1d(x_list, y_list, kind='linear')  # Defines function framework for linear
            # interpolation between x and y datasets.

            x_list_intp = range(int(x_list[0]), int(x_list[-1]), 1)  # Defines list as range between limits and step.

            y_list_intp = f(x_list_intp)  # Defines list by interpolating over x range.

            x_rng_intp = x_list_intp[-1] - x_list_intp[0]  # Defines variable as range of x values. For later data
            # selection.

            if j == 1:   # Establishes condition where operations below executed.

                x_lists_intp = []  # Creates empty list.
                y_lists_intp = []  # Creates empty list.
                x_rng_list_intp = []  # Creates empty list.

                x_lists_intp.append(x_list_intp)  # Appends list to list. For later comparison.
                y_lists_intp.append(y_list_intp)  # Appends list to list. For later comparison.
                x_rng_list_intp.append(x_rng_intp)  # Appends list to list. For later comparison.

            elif j != 1:   # Establishes condition where operations below executed.

                x_lists_intp.append(x_list_intp)  # Appends list to list. For later comparison.
                y_lists_intp.append(y_list_intp)  # Appends list to list. For later comparison.
                x_rng_list_intp.append(x_rng_intp)  # Appends list to list. For later comparison.

        elif A_trap_btw != 1:   # Establishes condition where operations below executed.

            # REPORT SURVEY DATA SUBSET  -------------------------------------------------------------------------------

            index1 = df_srvy.index  # Retrieves row indices of DataFrame.

            # Check
            # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + 'INDICES' + '\033[0m', '\n...', '\n', index1,
            # '\n')  # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            print('\n=====================')  # Displays string.
            str_chnnl = df_rng.loc[index1[0], 'Str_chnnl']  # Defines variable as element of DataFrame cell that
            # satisfies selection .
            print('\033[1m' + 'Stream channel:' + '\033[0m', str_chnnl)  # Displays objects. Makes font bold.
            srvy_rng = df_rng.loc[index1[0], 'Srvy_range']  # Defines variable as element of DataFrame cell that
            # satisfies selection .
            print('\033[1m' + 'Survey range number' + '\033[0m', i)  # Displays objects. Makes font bold.
            print('\033[1m' + 'Survey' + '\033[0m', j, 'of', srvy_num[-1])  # Displays objects. Makes font bold and
            # adds new line.
            print('=====================')  # Displays string.
            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # PLOT SELECTED DATASET ----------------------------------------------------------------------------------------

        clrs_num = j - 1  # Defines variable for automated color selection.
        lbl_num = clrs_num  # Defines variable for automated label selection.

        plt.figure(1, figsize=(5, 3))  # Creates figure 1. Sets size.
        ax1 = plt.gca()  # Retrieves current axes instance of figure.

        ax1.plot(x_set, y_set, label=srvy_yrList[lbl_num], c=colors1[clrs_num], marker='o', alpha=0.5)  # Creates line
        # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
        ax1.legend()  # Creates legend through automatic label detection.

        plt.xlabel('Offset (ft)', fontsize=8)  # Creates x-axis label. Sets font size.
        plt.ylabel('Elevation (ft)', fontsize = 8)  # Creates y-axis label. Sets font size.
        plt.title('Sedimentation Survey Cross-Sections: ' 'Range ' + str(i)) # Creates plot title.

        # Check
        plt.pause(0.00001)  # Displays and updates active figure before pausing for interval seconds.
        # plt.show()  # Displays plot and blocks code.

        # Export figure ------------------------------------------------------------------------------------------------

        expt_fldr = opt_fldr + anl_fldr + xsct_fldr + plts_fldr + plts_sfldr1  # Defines path of exported figure.

        if j == srvy_num[-1]:   # Establishes condition where operations below executed.

            path_end = plts_sfldr2[0]  # Defines variable as element of list. Sets end path folder destination.

            plt.figure(1)  # Calls figure 1 making it the active plot.

            fig_name = '/R' + str(i) + '_Xscts.pdf'  # Sets name of exported figure.

            plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

            plt.close()  # Closes active figure.

        # ==============================================================================================================
        # PART 2: CALCULATE CROSS-SECTIONAL AREA -----------------------------------------------------------------------
        # ==============================================================================================================

        # PART 2A: AREA UNDER SINGLE SURVEY THROUGH PIECEWISE CURVES ===================================================

        if A_pwise_mnl == 1:   # Establishes condition where operations below executed.

            print('\033[1m' + 'Cross-sectional area method 1 - piecewise functions' + '\033[0m')  # Displays string.
            # Makes font bold.

            # SET COORDINATE PAIR LOOP LIMITS --------------------------------------------------------------------------

            index1_len = len(index1)  # Defines variable as length of index.
            index2 = range(0, index1_len, 1)  # Defines list as range between limits and step.
            index2_max = max(index2)  # Defines variable as max value from list.
            index2_min = min(index2)  # Defines variable as min value from list.

            # Check
            # print('\033[1m' + 'Coordinate loop limit:' + '\033[0m', index2_max)  # Displays objects. Makes font bold.
            # breakpoint()  # Inserts breakpoint, halting code.

            # PLOT SURVEY CROSS-SECTION --------------------------------------------------------------------------------

            plt.figure(2, figsize=(5, 3))  # Creates figure 2. Sets size.
            ax2 = plt.gca()  # Retrieves current axes instance of figure.

            ax2.plot(x_set, y_set, label=srvy_yrList[lbl_num], c=colors1[clrs_num], marker='o', alpha=0.5)  # Creates
            # line plot of arrays from axes instance. Sets label, color, marker type, and transparency.
            ax2.legend()  # Creates legend through automatic label detection.

            plt.xlabel('Offset (ft)', fontsize=8)  # Creates x-axis label. Sets font size.
            plt.ylabel('Elevation (ft)', fontsize=8)  # Creates y-axis label. Sets font size.
            plt.title('Sedimentation Survey Cross-Section: ' 'Range ' + str(i) + ' - Survey ' + str(j))  # Creates plot
            # title.

            # Check
            # plt.pause(0.00001)  # Displays and updates active figure before pausing for interval seconds.
            # plt.show()  # Displays plot and blocks code.

            # Export figure --------------------------------------------------------------------------------------------

            path_end = plts_sfldr2[1]  # Defines variable as element of list. Sets end path folder destination.

            fig_name = '/R' + str(i) + '_S' + str(j) + '_Xsct.pdf'  # Sets name of exported figure.

            plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

            # Check
            plt.pause(1)  # Displays and updates active figure before pausing for specified interval seconds.

            # FIT LINEAR PIECEWISE FUNCTIONS ---------------------------------------------------------------------------

            for a in index2:  # Establishes framework for loop through coordinate pair indices.

                b = a + 1  # Defines variable to enable selection of two coordinate pairs per loop.

                if a < index2_max:  # Establishes framework for loop through coordinate pair indices until condition
                    # satisfied.

                    # Check
                    # print('\033[1m' + 'Sub-area interval:' + '\033[0m', a, '-', b)  # Displays objects. Makes font
                    # bold.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # Select adjacent coordinate pairs -----------------------------------------------------------------

                    x_1 = x_list[a]  # Defines variable as first element of x values list.
                    x_2 = x_list[b]  # Defines variable as last element of x values list.
                    y_1 = y_list[a]  # Defines variable as first element of y values list.
                    y_2 = y_list[b]  # Defines variable as last element of y values list.

                    # Check
                    # print('\033[1m' + 'Coordinate values:' + '\033[0m', '\nX 1 & 2:', x_1, '&', x_2, '\nY 1 & 2:',
                    # y_1, '&', y_2)  # Displays objects. Makes font bold and adds new line.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # Calculate slope between coordinate pairs ---------------------------------------------------------

                    deltaY = y_2 - y_1  # Calculates rise between coordinate pairs.
                    deltaX = x_2 - x_1  # Calculates run between coordinate pairs.

                    m = deltaY / deltaX  # Calculates slope between coordinate pairs.

                    # Check
                    # print('\033[1m' + 'Rise & run:' + '\033[0m', '%.5f' % deltaY, '&', '%.5f' % deltaX) # Displays
                    # objects. Makes font bold and sets decimal places.
                    # print('\033[1m' + 'Slope:' + '\033[0m', '%.5f' % m)  # Displays string. Makes font bold and
                    # sets decimal places.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # Calculate y-intercept ----------------------------------------------------------------------------

                    b1 = y_1 - m * x_1  # Calculates y-intercepts for first coordinate pair.
                    b2 = y_2 - m * x_2  # Calculates y-intercepts for second coordinate pair.

                    if b1 == b2:  # Establishes variable definition when condition specified.

                        b_int = b1  # Defines variable.

                        # Check
                        # print('\033[1;36m' + 'Y-intercepts equal, true value:' + '\033[0m', '%.4f' % b_int, '\n')
                        # Displays objects. Makes font bold and cyan and sets decimal places.

                    elif 0.9998 * b2 < b1 < 0.9999 * b2:  # Establishes variable definition when condition
                        # specified.

                        b_array = np.array([b1, b2])  # Creates an array of two elements. For later operation.
                        b_int = np.mean(b_array)  # Defines variable as mean of array elements.

                        # Check
                        # print('\033[1;31m' + 'Y-intercepts within 99%, estimated value:' + '\033[0m', '%.4f' % b_int,
                        # '\n')  # Displays objects. Makes font bold and red and sets decimal places.
                        # breakpoint()  # Inserts breakpoint, halting code.

                    # Check
                    # print('\033[1m' + 'Function fit:' + '\033[0m', 'y =', '%.4f' % m + 'x +', '%.4f' % b_int)
                    # Displays objects. Makes font bold.

                    # PLOT PIECEWISE FUNCTIONS -------------------------------------------------------------------------

                    # Create arrays to plot ----------------------------------------------------------------------------

                    x_list_pw = [x_1, x_2]  # Define list of x coordinates.
                    y_list_pw = [y_1, y_2]  # Define list of y coordinates.
                    y_min1 = min(y_list)  # Defines variable as least y value.
                    y_min1 = y_min1 - 1  # Redefines variable. For ease of visualization.

                    # Plot ---------------------------------------------------------------------------------------------

                    # Check
                    # plt.figure(2)  # Calls figure 2 making it the active plot.
                    # ax2.plot(x_list_pw, y_list_pw, c=colors1[clrs_num], alpha=0.3)  # Creates line plot of arrays from
                    # axes instance. Sets label, color, marker type, and transparency.
                    # plt.pause(0.0001)  # Displays and updates active figure before pausing for specified interval
                    # seconds.
                    # plt.show()  # Displays plot and blocks code.

                    # INTEGRATE AREA UNDER CURVES ----------------------------------------------------------------------

                    def f(x):  # Defines function establishing framework for piecewise integration over the x range.
                        return m * x + b_int


                    x = sy.Symbol('x')  # Defines symbol to be used in above math expression.
                    A_int = sy.integrate(f(x), (x, x_1, x_2))  # Defines variable as the output of the integration.

                    # Check
                    # print('\033[1m' + 'Area under piecewise:' + '\033[0m', '%.2f' % A_int, 'sqft')  # Displays
                    # objects. Makes font bold and sets decimal places.
                    # print('\n--------------------------------------------')  # Displays string.
                    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

                    # Save calculations --------------------------------------------------------------------------------

                    if a == index2_min:   # Establishes condition where operations below executed.

                        # Create objects for population
                        x_1List = ['null']  # Creates empty list.
                        x_2List = ['null']  # Creates empty list.
                        y_1List = ['null']  # Creates empty list.
                        y_2List = ['null']  # Creates empty list.
                        deltaYList = ['null']  # Creates empty list.
                        deltaXList = ['null']  # Creates empty list.
                        mList = ['null']  # Creates empty list.
                        b1List = ['null']  # Creates empty list.
                        b2List = ['null']  # Creates empty list.
                        b_intList = ['null']  # Creates empty list.
                        A_List = [0]  # Creates list.

                        # Populates objects
                        x_1List.append(x_1)  # Appends list with specified value.
                        x_2List.append(x_2)  # Appends list with specified value.
                        y_1List.append(y_1)  # Appends list with specified value.
                        y_2List.append(y_2)  # Appends list with specified value.
                        deltaYList.append(deltaY)  # Appends list with specified value.
                        deltaXList.append(deltaX)  # Appends list with specified value.
                        mList.append(m)  # Appends list with specified value.
                        b1List.append(b1)  # Appends list with specified value.
                        b2List.append(b2)  # Appends list with specified value.
                        b_intList.append(b_int)  # Appends list with specified value.
                        A_List.append(A_int)  # Appends list with specified value.

                        # Plot integration regions ---------------------------------------------------------------------

                        plt.figure(2)  # Calls figure 2 making it the active plot.

                        ax2.fill_between(x_list_pw, y_list_pw, y_min1, label ='Integration region',
                                         color=colors1[clrs_num], alpha=0.1)  # Creates shaded area plot of arrays from
                        # axes instance. Sets label, color, marker type, and transparency.

                        ax2.legend()  # Creates legend through automatic label detection.

                        # Check
                        # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing for interval
                        # seconds.
                        # plt.show()  # Displays plot and blocks code.

                        # Save calculations ----------------------------------------------------------------------------

                    elif a != index2_min:   # Establishes condition where operations below executed.

                        # Populate objects
                        x_1List.append(x_1)  # Appends list with specified value.
                        x_2List.append(x_2)  # Appends list with specified value.
                        y_1List.append(y_1)  # Appends list with specified value.
                        y_2List.append(y_2)  # Appends list with specified value.
                        deltaYList.append(deltaY)  # Appends list with specified value.
                        deltaXList.append(deltaX)  # Appends list with specified value.
                        mList.append(m)  # Appends list with specified value.
                        b1List.append(b1)  # Appends list with specified value.
                        b2List.append(b2)  # Appends list with specified value.
                        b_intList.append(b_int)  # Appends list with specified value.
                        A_List.append(A_int)  # Appends list with specified value.

                        # Plot integration regions ---------------------------------------------------------------------

                        ax2.fill_between(x_list_pw, y_list_pw, y_min1, color=colors1[clrs_num], alpha=0.3)  # Creates
                        # shaded area plot of arrays from axes instance. Sets label, color, marker type, and
                        # transparency.

                        # Check
                        # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing for interval
                        # seconds.
                        # plt.show()  # Displays plot and blocks code.

                # Export figures ---------------------------------------------------------------------------------------

                elif a == index2_max:  # Establishes framework for loop through coordinate pair indices until condition
                    # satisfied.

                    path_end = plts_sfldr2[2]  # Defines variable as element of list. Selects final folder
                    # destination.

                    fig_name = '/R' + str(i) + '_S' + str(j) + '_FlShd.pdf'  # Sets name of exported figure.

                    plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets
                    # file format.

                    # Calculate total area -----------------------------------------------------------------------------

                    A_tot_mnl = sum(A_List)  # Defines variable as sum of list elements.

                    print('\033[1m' + 'Area under cross-section:' + '\033[0m', '%.2f' % A_tot_mnl, 'sqft')  # Displays
                    # string. Makes font bold and sets decimal places.
                    print('---------------------------------------------------')  # Displays string.

                    plt.close()  # Closes active figure.

            # POPULATE DATAFRAMES --------------------------------------------------------------------------------------

            # For survey set -------------------------------------------------------------------------------------------

            warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

            df_srvy_c['X1_ft_pw'] = x_1List  # Populates DataFrame column with list elements.
            df_srvy_c['X2_ft_pw'] = x_2List  # Populates DataFrame column with list elements.
            df_srvy_c['Y1_ft_pw'] = y_1List  # Populates DataFrame column with list elements.
            df_srvy_c['Y2_ft_pw'] = y_2List  # Populates DataFrame column with list elements.
            df_srvy_c['DeltaY_ft'] = deltaYList  # Populates DataFrame column with list elements.
            df_srvy_c['DeltaX_ft'] = deltaXList  # Populates DataFrame column with list elements.
            df_srvy_c['Slope'] = mList  # Populates DataFrame column with list elements.
            df_srvy_c['B1_ft'] = b1List  # Populates DataFrame column with list elements.
            df_srvy_c['B2_ft'] = b2List  # Populates DataFrame column with list elements.
            df_srvy_c['B_int_ft'] = b_intList  # Populates DataFrame column with list elements.
            df_srvy_c['A_intvl_pw'] = A_List  # Populates DataFrame column with list elements.
            df_srvy_c.loc[:, 'A_net_pw'] = A_tot_mnl  # Populates DataFrame column and rows with list elements.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' UPDATED SURVEY DATA' + '\033[0m', '\n...',
            # '\n', df_srvy_c, '\n') # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # For export -----------------------------------------------------------------------------------------------

            df_all_c.loc[(df_all_c['Range_num'] == i) & (df_all_c['Srvy_num'] == j)] = df_srvy_c  # Populates DataFrame
            # slice of rows satisfying selection.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'All DIGITIZED SURVEY DATA UPDATED' + '\033[0m', '\n...', '\n', df_all_c, '\n')
            # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # EXPORT DATA ----------------------------------------------------------------------------------------------

            wbk_name = '/X_sectional_area_sngl.csv'  # Sets name of exported file.

            df_all_c.to_csv(opt_fldr + anl_fldr + xsct_fldr + ars_fldr + wbk_name, index = False)  # Exports DataFrame
            # as .csv to specified folder without row indices.

            # Check
            # breakpoint()  # Inserts breakpoint, halting code.

        # PART 2B: AREA UNDER SINGLE SURVEY THROUGH MANUAL COMPOSITE TRAPEZOID RULE ====================================

        if A_trap_mnl == 1:  # Establishes condition where operations below executed.

            print('\033[1m' + 'Cross-sectional area method 2 - manual composite trapezoids' + '\033[0m')  # Displays
            # string. Makes font bold.

            # SET COORDINATE PAIR LOOP LIMITS --------------------------------------------------------------------------

            index1_len = len(index1)  # Defines variable as length of index.
            index2 = range(0, index1_len, 1)  # Defines list as range between limits and step.
            index2_max = max(index2)  # Defines variable as max value from list.
            index2_min = min(index2)  # Defines variable as min value from list.

            # Check
            # print('\033[1m' + 'Coordinate loop limit:' + '\033[0m', index2_max)  # Displays objects. Makes font bold.
            # breakpoint()  # Inserts breakpoint, halting code.

            # PLOT SURVEY CROSS-SECTION --------------------------------------------------------------------------------

            plt.figure(2, figsize=(5, 3))  # Creates figure 2. Sets size.
            ax2 = plt.gca()  # Retrieves current axes instance of figure.

            ax2.plot(x_set, y_set, label=srvy_yrList[lbl_num], c=colors1[clrs_num], marker='o', alpha=0.5)  # Creates
            # line plot of arrays from axes instance. Sets label, color, marker type, and transparency.
            ax2.legend()  # Creates legend through automatic label detection.

            plt.xlabel('Offset (ft)', fontsize=8)  # Creates x-axis label. Sets font size.
            plt.ylabel('Elevation (ft)', fontsize=8)  # Creates y-axis label. Sets font size.
            plt.title('Sedimentation Survey Cross-Section: ' 'Range ' + str(i) + ' - Survey ' + str(j))  # Creates plot
            # title.

            # Check
            # plt.pause(0.00001)  # Displays and updates active figure before pausing for interval seconds.
            # plt.show()  # Displays plot and blocks code.

            # Export figure --------------------------------------------------------------------------------------------

            path_end = plts_sfldr2[1]  # Defines variable as element of list. Sets end path folder destination.

            fig_name = '/R' + str(i) + '_S' + str(j) + '_Xsct.pdf'  # Sets name of exported figure.

            plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

            # Check
            plt.pause(1)  # Displays and updates active figure before pausing for specified interval seconds.

            # SELECT ADJACENT COORDINATE PAIRS -------------------------------------------------------------------------

            for a in index2:  # Establishes framework for loop through coordinate pair indices.

                b = a + 1  # Defines variable to enable selection of two coordinate pairs per loop.

                if a < index2_max:  # Establishes framework for loop through coordinate pair indices until condition
                    # satisfied.

                    # Check
                    print('\033[1m' + 'Sub-area interval:' + '\033[0m', a, '-', b)  # Displays objects. Makes font
                    # bold.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    x_1 = x_list[a]  # Defines variable as first element of x values list.
                    x_2 = x_list[b]  # Defines variable as last element of x values list.
                    y_1 = y_list[a]  # Defines variable as first element of y values list.
                    y_2 = y_list[b]  # Defines variable as last element of y values list.

                    # Check
                    print('\033[1m' + 'Coordinate values:' + '\033[0m', '\nX 1 & 2:', x_1, '&', x_2, '\nY 1 & 2:',
                    y_1, '&', y_2)  # Displays objects. Makes font bold and adds new line.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # INTEGRATE TRAPEZOIDAL AREA UNDER CURVE -----------------------------------------------------------

                    # Reorder x-values ---------------------------------------------------------------------------------

                    if x_1 < 0 or x_2 < 0:  # Establishes loop for the correct reordering of x-values. To avoid negative
                        # areas.

                        if abs(x_1) > abs(x_2):  # Establishes condition where operations below executed.
                            x_0 = abs(x_2)  # Defines first integration limit.
                            x_f = abs(x_1)  # Defines second integration limit.
                        elif abs(x_1) < abs(x_2):  # Establishes condition where operations below executed.
                            x_0 = abs(x_1)  # Defines first integration limit.
                            x_f = abs(x_2)  # Defines second integration limit.

                    elif x_1 > 0 and x_2 > 0:  # Establishes condition where operations below executed.

                        x_0 = x_1  # Defines first integration limit.
                        x_f = x_2  # Defines second integration limit.

                    x_rng = abs(abs(x_1) - abs(x_2))
                    # print(x_1, x_2)
                    # print(x_rng)

                    x_0 = 0
                    x_f = x_rng

                    # Check
                    print('\033[1m' + 'Integration limits:' + '\033[0m', '\nX 1 & 2:', x_0, '&', x_f)  # Displays
                    # objects. Makes font bold and adds new line.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # Integrate ----------------------------------------------------------------------------------------

                    def f(x):  # Defines function establishing framework for integration of the area of a trapezoid
                        # over the x range.
                        return (y_1 + y_2)/2 * x


                    x = sy.Symbol('x')  # Defines symbol to be used in above math expression.
                    A_int = sy.integrate(f(x), (x, x_0, x_f))  # Defines variable as the output of the integration.

                    # Check
                    print('\033[1m' + 'Area in trapezoid:' + '\033[0m', '%.2f' % A_int, 'sqft')  # Displays
                    # objects. Makes font bold and sets decimal places.
                    print('\n--------------------------------------------')  # Displays string.
                    # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

                    # Save calculations --------------------------------------------------------------------------------

                    if a == index2_min:   # Establishes condition where operations below executed.

                        # Create objects for population
                        x_1List = ['null']  # Creates empty list.
                        x_2List = ['null']  # Creates empty list.
                        y_1List = ['null']  # Creates empty list.
                        y_2List = ['null']  # Creates empty list.
                        A_List = [0]  # Creates list.

                        # Populates objects
                        x_1List.append(x_1)  # Appends list with specified value.
                        x_2List.append(x_2)  # Appends list with specified value.
                        y_1List.append(y_1)  # Appends list with specified value.
                        y_2List.append(y_2)  # Appends list with specified value.
                        A_List.append(A_int)  # Appends list with specified value.

                        # Plot integration regions ---------------------------------------------------------------------

                        # Create arrays
                        x_list_tm = [x_1, x_2]  # Define list of x coordinates.
                        y_list_tm = [y_1, y_2]  # Define list of y coordinates.
                        y_min1 = min(y_list)  # Defines variable as least y value.
                        y_min1 = y_min1 - 1  # Redefines variable for visualization.

                        # Plot
                        ax2.fill_between(x_list_tm, y_list_tm, y_min1, label ='Integration region',
                                         color=colors1[clrs_num], alpha=0.3)  # Creates shaded area plot between
                        # arrays from axes instance with specified color, marker type, and transparency.
                        ax2.legend()  # Creates legend through automatic label detection.

                        # Check
                        # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing for interval
                        # seconds.
                        # plt.show()  # Displays plot and blocks code.

                    elif a != index2_min:   # Establishes condition where operations below executed.

                        # Populate objects -----------------------------------------------------------------------------

                        x_1List.append(x_1)  # Appends list with specified value.
                        x_2List.append(x_2)  # Appends list with specified value.
                        y_1List.append(y_1)  # Appends list with specified value.
                        y_2List.append(y_2)  # Appends list with specified value.
                        A_List.append(A_int)  # Appends list with specified value.

                        # Plot integration regions ---------------------------------------------------------------------

                        # Create lists
                        x_list_Tm = [x_1, x_2]  # Define list of x coordinates.
                        y_list_Tm = [y_1, y_2]  # Define list of y coordinates.
                        y_min1 = min(y_list)  # Defines variable as least y value.
                        y_min1 = y_min1 - 1  # Redefines variable for visualization.

                        # Plot
                        plt.figure(2)  # Calls figure 2 making it the active plot.

                        ax2.fill_between(x_list_Tm, y_list_Tm, y_min1, label ='Integration region',
                                         color=colors1[clrs_num], alpha=0.1)  # Creates shaded area plot of arrays from
                        # axes instance. Sets label, color, marker type, and transparency.

                        # Check
                        # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing for interval
                        # seconds.
                        # plt.show()  # Displays plot and blocks code.

                # Export figures ---------------------------------------------------------------------------------------

                elif a == index2_max:  # Establishes framework for loop through coordinate pair indices until condition
                    # satisfied.

                    path_end = plts_sfldr2[3]  # Defines variable as element of list. Selects final folder
                    # destination.

                    fig_name = '/R' + str(i) + '_S' + str(j) + '_FlShd.pdf'  # Sets name of exported figure.

                    plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file
                    # format.

                    # Calculate total area -----------------------------------------------------------------------------

                    A_tot_mnl = sum(A_List)  # Defines variable as sum of list elements.

                    print('\033[1m' + 'Area under cross-section:' + '\033[0m', '%.2f' % A_tot_mnl, 'sqft')  # Displays
                    # string. Makes font bold and sets decimal places.
                    print('-----------------------------------------------------------')  # Displays string.

                    plt.close()  # Closes active figure.

            # POPULATE DATAFRAMES --------------------------------------------------------------------------------------

            # For survey set -------------------------------------------------------------------------------------------

            warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
            # For survey set

            df_srvy_c['X1_ft_tm'] = x_1List  # Populates DataFrame column with list elements.
            df_srvy_c['X2_ft_tm'] = x_2List  # Populates DataFrame column with list elements.
            df_srvy_c['Y1_ft_tm'] = y_1List  # Populates DataFrame column with list elements.
            df_srvy_c['Y2_ft_tm'] = y_2List  # Populates DataFrame column with list elements.
            df_srvy_c['A_intvl_tm'] = A_List  # Populates DataFrame column with list elements.
            df_srvy_c.loc[:, 'A_net_tm'] = A_tot_mnl  # Populates DataFrame column and rows with list elements.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' UPDATED SURVEY DATA' + '\033[0m', '\n...',
            # '\n', df_srvy_c, '\n') # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # For export -----------------------------------------------------------------------------------------------

            df_all_c.loc[(df_all_c['Range_num'] == i) & (df_all_c['Srvy_num'] == j)] = df_srvy_c  # Populates DataFrame
            # slice of rows satisfying selection.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'All DIGITIZED SURVEY DATA UPDATED' + '\033[0m', '\n...', '\n', df_all_c, '\n')
            # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # EXPORT DATA ----------------------------------------------------------------------------------------------

            wbk_name = '/X_sectional_area_sngl.csv'  # Sets name of exported file.

            df_all_c.to_csv(opt_fldr + anl_fldr + xsct_fldr + ars_fldr + wbk_name, index=False)  # Exports DataFrame
            # as .csv to specified folder without row indices.

            # Check
            # breakpoint()  # Inserts breakpoint, halting code.

        # PART 2C: AREA UNDER SINGLE SURVEY THROUGH AUTOMATIC COMPOSITE TRAPEZOID RULE =================================

        if A_trap_ato == 1:  # Establishes condition where operations below executed.

            print('\033[1m' + 'Cross-sectional area method 3 - automatic composite trapezoids' + '\033[0m')  # Displays
            # string. Makes font bold.

            # CALCULATE TOTAL AREA -------------------------------------------------------------------------------------

            A_tot_ato = np.trapz(y_set, x_set)  # Defines variable with integration along arrays following composite
            # trapezoidal rule.

            print('\033[1m' + 'Area under cross-section:' + '\033[0m', '%.2f' % A_tot_ato, 'sqft')  # Displays
            # string. Makes font bold and sets decimal places.
            print('--------------------------------------------------------------')  # Displays string.

            # POPULATE DATAFRAMES --------------------------------------------------------------------------------------

            # For survey set -------------------------------------------------------------------------------------------

            warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

            df_srvy_c.loc[:, 'A_net_ta'] = A_tot_ato  # Populates DataFrame column and rows with list elements.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' UPDATED SURVEY DATA' + '\033[0m', '\n...',
            # '\n', df_srvy_c, '\n') # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # For export -----------------------------------------------------------------------------------------------

            df_all_c.loc[(df_all_c['Range_num'] == i) & (df_all_c['Srvy_num'] == j)] = df_srvy_c  # Populates DataFrame
            # slice of rows satisfying selection.

            # Check
            # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all columns.
            # print('\033[1m' + 'All DIGITIZED SURVEY DATA UPDATED' + '\033[0m', '\n...', '\n', df_all_c, '\n')
            # Displays objects. Makes font bold and adds new lines.
            # breakpoint()  # Inserts breakpoint, halting code.

            # EXPORT DATA ----------------------------------------------------------------------------------------------

            wbk_name = '/X_sectional_area_sngl.csv'  # Sets name of exported file.

            df_all_c.to_csv(opt_fldr + anl_fldr + xsct_fldr + ars_fldr + wbk_name, index=False)  # Exports DataFrame
            # as .csv to specified folder without row indices.

            # Check
            # breakpoint()  # Inserts breakpoint, halting code.

    # PART 2D: AREA BETWEEN TWO SURVEYS THROUGH MANUAL COMPOSITE TRAPEZOID RULE ========================================

    if A_trap_btw == 1:   # Establishes condition where operations below executed.

        # REPORT SURVEY DATA SUBSET  -----------------------------------------------------------------------------------

        index1 = df_srvy.index  # Retrieves row indices of DataFrame.

        # Check
        # print('\033[1m' + 'RANGE ' + str(i) + ' SURVEY ' + str(j) + 'INDICES' + '\033[0m', '\n...', '\n', index1,
        # '\n')  # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        print('=====================')  # Displays string.
        str_chnnl = df_rng.loc[index1[0], 'Str_chnnl']  # Defines variable as element of DataFrame cell that
        # satisfies selection .
        print('\033[1m' + 'Stream channel:' + '\033[0m', str_chnnl)  # Displays objects. Makes font bold.
        srvy_rng = df_rng.loc[index1[0], 'Srvy_range']  # Defines variable as element of DataFrame cell that
        # satisfies selection .
        print('\033[1m' + 'Survey range number' + '\033[0m', i)  # Displays objects. Makes font bold.
        print('\033[1m' + 'Cross-sectional area method 4 - manual & interpolated composite trapezoids' + '\033[0m')
        # Displays string. Makes font bold.
        print('==========================================================================')  # Displays string.
        # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

        # SET DATASET PAIR LOOP LIMITS ---------------------------------------------------------------------------------

        dataset1_num = np.array(srvy_list)  # Defines array from list.

        dataset1_num = dataset1_num - 1  # Redefines array. For selecting correct dataset.

        # dataset1_num = np.array([2,3])  # Defines array from list.

        # Check
        # print('\033[1m' + 'Indices for:' + '\033[0m', '\nDataset:', dataset1_num, '\nArea interval:', A_intvl_num,
        # '\n')  # Displays objects. Makes font bold and adds new lines.
        # breakpoint()  # Inserts breakpoint, halting code.

        # PLOT SURVEY CROSS-SECTIONS -----------------------------------------------------------------------------------

        for a in dataset1_num:   # Establishes condition where operations below executed.

            print('\n...')  # Displays string.

            # By survey ------------------------------------------------------------------------------------------------

            plt.figure(3, figsize=(5, 3))  # Creates figure 3. Sets size.
            ax3 = plt.gca()  # Retrieves current axes instance of figure.

            ax3.plot(x_lists_intp[a], y_lists_intp[a], label=lbl_srvy_cmp[1], c=colors1[a], marker='o',
                     alpha=0.5)  # Creates line plot of arrays from axes instance. Sets label, color, marker
            # type, and transparency.
            ax3.plot(x_lists[a], y_lists[a], label=lbl_srvy_cmp[0], c=colors2[a], marker='o',  alpha=0.7)
            # Creates line plot of arrays from axes instance. Sets label, color, marker type, and transparency.
            ax3.legend()  # Creates legend through automatic label detection.

            plt.xlabel('Offset (ft)', fontsize=8)  # Creates x-axis label. Sets font size.
            plt.ylabel('Elevation (ft)', fontsize=8)  # Creates y-axis label. Sets font size.
            plt.title('Sedimentation Survey Cross-Sections: Range ' + str(i) + ' Survey ' + str(srvy_num[a]))
            # Creates plot title.

            # Check
            # plt.show()  # Displays plot and blocks code.

            # Export figure
            path_end = plts_sfldr2[4]  # Defines variable as element of list. Sets end path folder destination.

            fig_name = '/R' + str(i) + '_S' + str(srvy_num[a]) + '_Xsct.pdf'  # Sets name of exported figure.

            plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

            plt.close()  # Closes active figure.

            # By area interval -----------------------------------------------------------------------------------------

            if a != dataset1_num[-1]:   # Establishes condition where operations below executed.

                aa = a + 1  # Defines variable to enable selection of two datasets per loop.

                dataset2_num = np.delete(dataset1_num, np.s_[:aa], 0)  # Defines variable. Deletes values from array.

                # dataset2_num = np.array([3,3])

                # Check
                # print('\033[1m' + 'Dataset comparisons:' + '\033[0m', 'Dataset:', a, 'to', dataset2_num)  # Displays
                # objects. Makes font bold and adds new lines.
                # breakpoint()  # Inserts breakpoint, halting code.

                for b in dataset2_num:   # Establishes condition where operations below executed.

                    c = b + 1  # Defines variable to enable selection of two survey numbers per loop. For later
                    # DataFrame population.

                    # print('\033[1m' + 'Present comparison:' + '\033[0m', 'Dataset', a, 'to', b, '\n...')  # Displays
                    # objects. Makes font bold and adds new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    plt.figure(4, figsize=(6, 3))  # Creates figure 4. Sets size.
                    ax4 = plt.gca()  # Retrieves current axes instance of figure.

                    ax4.plot(x_lists_intp[a], y_lists_intp[a], label=srvy_yrList[a], c=colors1[a], marker='o', alpha=1)
                    # Creates line plot of arrays from axes instance. Sets label, color, marker type, and transparency.
                    ax4.plot(x_lists_intp[b], y_lists_intp[b], label=srvy_yrList[b], c=colors1[b], marker='o', alpha=1)
                    # Creates line plot of arrays from axes instance. Sets label, color, marker type, and transparency.
                    ax4.legend()  # Creates legend through automatic label detection.

                    plt.xlabel('Offset (ft)', fontsize=8)  # Creates x-axis label. Sets font size.
                    plt.ylabel('Elevation (ft)', fontsize=8)  # Creates y-axis label. Sets font size.
                    plt.title('Sedimentation Survey Cross-Sections: Range ' + str(i) + ' Surveys ' + str(srvy_num[a])
                              + ' & ' + str(srvy_num[b]))  # Creates plot title.

                    # Check
                    # plt.pause(0.00001)  # Displays and updates active figure before pausing for interval seconds.
                    # plt.show()  # Displays plot and blocks code.

                    # Export figure
                    path_end = plts_sfldr2[5]  # Defines variable as element of list. Sets end path folder destination.

                    fig_name = '/R' + str(i) + '_S' + str(srvy_num[a]) + '&' + str(srvy_num[b]) + '_Xscts.pdf' # Sets
                    # name of exported figure.

                    plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory. Sets file
                    # format.

                    # SELECT INTEGRATION LIMITS ------------------------------------------------------------------------

                    x_rng1 = x_rng_list_intp[a]  # Defines variable as element of list.
                    x_rng2 = x_rng_list_intp[b]  # Defines variable as element of list.

                    # Check
                    # print('\033[1m' + 'X range:' + '\033[0m', '\nDataset 1:', x_rng1,'\nDataset 2:', x_rng2)
                    # Displays objects. Makes font bold and adds new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    if x_rng1 > x_rng2:  # Establishes condition where operations below executed.

                        x_int_rng = x_lists_intp[b]  # Defines variable as element of list.

                        # Reassign y datasets --------------------------------------------------------------------------

                        g = sc.interpolate.interp1d(x_lists[a], y_lists[a], kind='linear')  # Defines function
                        # framework for linear interpolation between x and y datasets.

                        y_new1 = g(x_int_rng)  # Defines list by interpolating over x range.
                        y_new2 = y_lists_intp[b]  # Defines list as list element.

                    elif x_rng1 < x_rng2:  # Establishes condition where operations below executed.

                        x_int_rng = x_lists_intp[a]  # Defines variable as element of list.

                        # Reassign y datasets --------------------------------------------------------------------------

                        g = sc.interpolate.interp1d(x_lists[b], y_lists[b], kind='linear')  # Defines function
                        # framework for linear interpolation between x and y datasets.

                        y_new1 = y_lists_intp[a]  # Defines list as list element.
                        y_new2 = g(x_int_rng)  # Defines list by interpolating over x range.

                    elif x_rng1 == x_rng2:  # Establishes condition where operations below executed.

                        x_int_rng = x_lists_intp[a]  # Defines variable as element of list.

                        # Reassign y datasets --------------------------------------------------------------------------

                        y_new1 = y_lists_intp[a]  # Defines list as list element.
                        y_new2 = y_lists_intp[b]  # Defines list as list element.

                    # Check
                    # x_rng_new = x_int_rng[-1] - x_int_rng[0]  # Defines variable as range of values.
                    # print('\033[1m' + 'Shared x range:' + '\033[0m', x_int_rng[0], 'to', x_int_rng[-1], ',',
                    #       x_rng_new, 'total points')  # Displays objects. Makes font bold and adds new lines.
                    # print('\033[1m' + 'New y datasets:' + '\033[0m', '\nDataset 1:', y_new1, '\nDataset 2:',
                    #       y_new2)  # Displays objects. Makes font bold and adds new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # SET COORDINATE PAIR LOOP LIMITS ------------------------------------------------------------------

                    indexInt_len = len(x_int_rng)  # Defines variable as length of integration values.
                    index2 = range(0, indexInt_len, 1) # Defines list with limits and step.
                    index2_max = max(index2)
                    index2_min = min(index2)

                    # Check
                    # print('\033[1m' + 'Coordinate loop limit:' + '\033[0m', index2_max)  # Displays objects. Makes
                    # font bold.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # Populate DataFrame -------------------------------------------------------------------------------

                    # df_interpolated_all.iloc[index2_max, 'Str_chnnl'] == str_chnnl  # Populates DataFrame column and
                    # rows with variable.
                    # df_interpolated_all.loc['Str_chnnl'] == str_chnnl
                    # df_interpolated_all['Range_num'] == i  # Populates DataFrame column and rows with
                    #  variable.

                    # Check
                    # pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all
                    # columns.
                    # print('\033[1m' + 'ALL INTERPOLATED DATA' + '\033[0m', '\n...', '\n', df_interpolated_all, '\n')
                    # Displays objects. Makes font bold and adds new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # SELECT ADJACENT COORDINATE PAIRS -----------------------------------------------------------------

                    for d in index2:  # Establishes framework for loop through coordinate pair indices.

                        e = d + 1  # Defines variable to enable selection of two coordinate pairs per loop.

                        if d < index2_max:  # Establishes framework for loop through coordinate pair indices until
                            # condition satisfied.

                            # Check
                            # print('\033[1m' + 'Sub-area interval:' + '\033[0m', d, '-', e)  # Displays string. Makes
                            # font bold.
                            # breakpoint()  # Inserts breakpoint, halting code.

                            x_1 = x_int_rng[d]  # Defines variable as first element of x values list.
                            x_2 = x_int_rng[e]  # Defines variable as last element of x values list.
                            y1_1 = y_new1[d]  # Defines variable as first element of y values list.
                            y1_2 = y_new1[e]  # Defines variable as last element of y values list.
                            y2_1 = y_new2[d]  # Defines variable as first element of y values list.
                            y2_2 = y_new2[e]  # Defines variable as last element of y values list.

                            # Check
                            # print('\033[1m' + 'Coordinate values:' + '\033[0m', '\nX 1 & 2:', x_1, '&', x_2,
                            #       '\nY top & bottom:', '\n%.4f' % y1_1, '&', '%.4f' % y1_2,
                            #       '\n%.4f' % y2_1, '&', '%.4f' % y2_2)  # Displays string. Makes font bold, sets
                            # decimal places, and adds new line.
                            # breakpoint()  # Inserts breakpoint, halting code.

                            y_left = y1_1 - y2_1  # Defines variable as difference between y values. Defines height of
                            # left side of trapezoid.
                            y_right = y1_2 - y2_2  # Defines variable as difference between y values. Defines height of
                            # right side of trapezoid.

                            # Check
                            # print('\033[1m' + 'Trapezoid heights:' + '\033[0m', '\nLeft:', '%.4f' % y_left,
                            #       '\nRight:', '%.4f' % y_right)  # Displays string. Makes font bold, sets decimal
                            # places, and adds new line.
                            # breakpoint()  # Inserts breakpoint, halting code.

                            # INTEGRATE AREA BETWEEN CURVES ------------------------------------------------------------

                            # Reorder x-values -------------------------------------------------------------------------

                            if x_1 < 0 or x_2 < 0:  # Establishes loop for the correct reordering of x-values. To avoid
                                # negative areas.

                                if abs(x_1) > abs(x_2):  # Establishes condition where operations below executed.

                                    x_0 = abs(x_2)  # Defines first integration limit.
                                    x_f = abs(x_1)  # Defines second integration limit.

                                elif abs(x_1) < abs(x_2):  # Establishes condition where operations below executed.

                                    x_0 = abs(x_1)  # Defines first integration limit.
                                    x_f = abs(x_2)  # Defines second integration limit.

                            elif x_1 >= 0 and x_2 >= 0:  # Establishes condition where operations below executed.

                                x_0 = x_1  # Defines first integration limit.
                                x_f = x_2  # Defines second integration limit.

                            x_0 = 0
                            x_f = 1

                            # Integrate --------------------------------------------------------------------------------

                            def f(x):  # Defines function establishing framework for integration of the area of a
                                # trapezoid over the x range.
                                return (y_left + y_right)/2 * x


                            x = sy.Symbol('x')  # Defines symbol to be used in above math expression.
                            A_int = sy.integrate(f(x), (x, x_0, x_f))  # Defines variable as the output of the
                            # integration.

                            # Categorize integration result
                            if A_int < 0:   # Establishes condition where operations below executed.

                                A_neg = A_int  # Defines variable. For later analysis.

                                process = 'Erosion'  # Defines variable.

                            elif A_int > 0:  # Defines variable. For later analysis.

                                A_pos = A_int   # Establishes condition where operations below executed.

                                process = 'Deposition'  # Defines variable.

                            # Check
                            # print('\033[1m' + 'Area in trapezoid between curves:' + '\033[0m', '%.2f' % A_int, 'sqft',
                            #       '(' + str(process) + ')')  # Displays objects. Makes font bold and sets decimal
                            # places.
                            # print('\n--------------------------------------------')  # Displays string.
                            # breakpoint()  # Inserts breakpoint, halting code. Enable for check only.

                            # Save calculations ------------------------------------------------------------------------

                            if d == index2_min:   # Establishes condition where operations below executed.

                                # Create objects for population
                                x_1List = []  # Creates empty list.
                                x_2List = []  # Creates empty list.
                                y1_1List = []  # Creates empty list.
                                y1_2List = []  # Creates empty list.
                                y2_1List = []  # Creates empty list.
                                y2_2List = []  # Creates empty list.
                                y2_2List = []  # Creates empty list.
                                A_posList = []  # Creates empty list.
                                A_negList = []  # Creates empty list.
                                A_netList = []  # Creates empty list.

                                # Populates objects
                                x_1List.append(x_1)  # Appends list with specified value.
                                x_2List.append(x_2)  # Appends list with specified value.
                                y1_1List.append(y1_1)  # Appends list with specified value.
                                y1_2List.append(y1_2)  # Appends list with specified value.
                                y2_1List.append(y2_1)  # Appends list with specified value.
                                y2_2List.append(y2_2)  # Appends list with specified value.

                                try:
                                    A_pos
                                except NameError:
                                    1 == 1
                                else:
                                    A_posList.append(A_pos)  # Appends list with specified value.
                                    del A_pos

                                try:
                                    A_neg
                                except NameError:
                                    1 == 1
                                else:
                                    A_negList.append(A_neg)  # Appends list with specified value.
                                    del A_neg

                                A_netList.append(A_int)  # Appends list with specified value.

                                # Plot integration regions -------------------------------------------------------------

                                # Create arrays
                                x_list_int = [x_1, x_2]  # Define list of x coordinates.
                                y_list_top = [y1_1, y1_2]  # Define list of y coordinates.
                                y_list_bot = [y2_1, y2_2]  # Define list of y coordinates.

                                # Plot
                                ax4.fill_between(x_list_int, y_list_top, y_list_bot, label='Integration region',
                                                 color='Gray', alpha=0.1)  # Creates shaded area
                                # plot between arrays from axes instance with specified color, marker type, and
                                # transparency.
                                ax4.legend()  # Creates legend through automatic label detection.

                                # Check
                                # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing
                                # for interval seconds.
                                # plt.show()  # Displays plot and blocks code.

                            elif d != index2_min:  # Establishes condition where operations below executed.

                                # Populate objects ---------------------------------------------------------------------

                                x_1List.append(x_1)  # Appends list with specified value.
                                x_2List.append(x_2)  # Appends list with specified value.
                                y1_1List.append(y1_1)  # Appends list with specified value.
                                y1_2List.append(y1_2)  # Appends list with specified value.
                                y2_1List.append(y2_1)  # Appends list with specified value.
                                y2_2List.append(y2_2)  # Appends list with specified value.

                                try:
                                    A_pos
                                except NameError:
                                    1 == 1
                                else:
                                    A_posList.append(A_pos)  # Appends list with specified value.
                                    del A_pos

                                try:
                                    A_neg
                                except NameError:
                                    1 == 1
                                else:
                                    A_negList.append(A_neg)  # Appends list with specified value.
                                    del A_neg
                                    # print(A_negList)

                                A_netList.append(A_int)  # Appends list with specified value.



                                # Plot integration regions -------------------------------------------------------------

                                # Create lists
                                x_list_int = [x_1, x_2]  # Define list of x coordinates.
                                y_list_top = [y1_1, y1_2]  # Define list of y coordinates.
                                y_list_bot = [y2_1, y2_2]  # Define list of y coordinates.

                                # Plot
                                ax4.fill_between(x_list_int, y_list_top, y_list_bot, label='Integration region',
                                                 color='Gray', alpha=0.1)  # Creates shaded area
                                # plot between arrays from axes instance with specified color, marker type, and
                                # transparency.

                                # Check
                                # plt.pause(0.0000000000000001)  # Displays and updates active figure before pausing
                                # for interval seconds.
                                # plt.show()  # Displays plot and blocks code.

                        # Export figures -------------------------------------------------------------------------------

                        elif d == index2_max:  # Establishes framework for loop through coordinate pair indices until
                            # condition satisfied.

                            path_end = plts_sfldr2[5]  # Defines variable as element of list. Selects final folder
                            # destination.

                            fig_name = '/R' + str(i) + '_S' + str(srvy_num[a]) + '&' + str(srvy_num[b]) + '_FlShd.pdf'
                            # Sets name of exported figure.
                            plt.savefig(expt_fldr + path_end + fig_name, format='pdf')  # Saves figure to directory.
                            # Sets file format.

                            # Calculate total area ---------------------------------------------------------------------

                            A_tot_mnl = sum(A_netList)  # Defines variable as sum of list elements.
                            A_tot_pos = sum(A_posList)  # Defines variable as sum of list elements.
                            A_tot_neg = abs(sum(A_negList))  # Defines variable as absolute value of sum of list
                            # elements.

                            print('\033[1m' + 'Area between cross-sections (sqft) ' + str(srvy_num[a]) + ' & '
                                  + str(srvy_num[b]),  '\033[0m', '\nNet:', '%.2f' % A_tot_mnl, '\nDeposition:',
                                  '%.2f' % A_tot_pos, '\nErosion:', '%.2f' % A_tot_neg)  # Displays string.
                            # Makes font bold and sets decimal places.
                            print('---------------------------------')  # Displays string.

                            plt.close()  # Closes active figure.

                    # POPULATE DATAFRAMES ------------------------------------------------------------------------------

                    # For survey set -----------------------------------------------------------------------------------

                    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
                    # For survey set

                    df_interpolated = pd.DataFrame()  # Creates new DataFrame. For later population.

                    df_interpolated['X1_in'] = x_1List # Populates DataFrame column with list elements.
                    df_interpolated['X2_in'] = x_2List  # Populates DataFrame column with list elements.
                    df_interpolated['Y1_1'] = y1_1List  # Populates DataFrame column with list elements.
                    df_interpolated['Y1_2'] = y1_2List  # Populates DataFrame column with list elements.
                    df_interpolated['Y2_1'] = y2_1List  # Populates DataFrame column with list elements.
                    df_interpolated['Y2_2'] = y2_2List  # Populates DataFrame column with list elements.
                    df_interpolated['A_intvl_in'] = A_netList  # Populates DataFrame column with list elements.
                    df_interpolated.loc[:index2_max,'A_net_in'] = A_tot_mnl  # Populates DataFrame column and rows with
                    # list elements.
                    df_interpolated.loc[:index2_max, 'A_net_pos'] = A_tot_pos  # Populates DataFrame column and rows
                    # with list elements.
                    df_interpolated.loc[:index2_max, 'A_net_neg'] = A_tot_neg  # Populates DataFrame column and rows
                    # with list elements.
                    df_interpolated.loc[:index2_max, 'Str_chnnl'] = str_chnnl  # Populates DataFrame column and rows
                    # with variable.
                    df_interpolated.loc[:index2_max, 'Range_num'] = i  # Populates DataFrame column and rows with
                    #  variable.

                    aa = a + 1   # Defines variable. For selecting correct data year.

                    df_interpolated.loc[:index2_max, 'Srvy_num1'] = aa  # Populates DataFrame column and rows with
                    #  variable.

                    bb = b + 1  # Defines variable. For selecting correct data year.

                    df_interpolated.loc[:index2_max, 'Srvy_num2'] = bb  # Populates DataFrame column and rows with
                    #  variable.

                    # Check
                    pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all
                    # columns.
                    # print('\033[1m' + 'RANGE ' + str(i) + ' AREA INTERVAL ' + str(b) + ' INTERPOLATED DATA' +
                    #       '\033[0m', '\n...', '\n', df_interpolated, '\n') # Displays objects. Makes font bold and adds
                    # new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # For export ---------------------------------------------------------------------------------------

                    df_interpolated_all = pd.concat([df_interpolated_all, df_interpolated])

                    # Check
                    pd.set_option('display.max_columns', None)  # Adjusts DataFrame display settings to display all
                    # columns.
                    # print('\033[1m' + 'ALL INTERPOLATED DATA' + '\033[0m', '\n...', '\n', df_interpolated_all, '\n')
                    # Displays objects. Makes font bold and adds new lines.
                    # breakpoint()  # Inserts breakpoint, halting code.

                    # EXPORT DATA --------------------------------------------------------------------------------------

                    wbk_name = '/X_sectional_area_btwn.csv'  # Sets name of exported file.

                    df_interpolated_all.to_csv(opt_fldr + anl_fldr + xsct_fldr + ars_fldr + wbk_name, index=False)
                    # Exports DataFrame as .csv to specified folder without row indices.

                    # Check
                    # breakpoint()  # Inserts breakpoint, halting code.

# CODE PROGRESS TIMING =================================================================================================

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
    print(chnl_1R + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's','!')  # Displays objects.
    print(chnl_2R + 'cross-sectional areas calculated in', '%.4f' % executionTime1, 's', '!')  # Displays objects.
    print(chnl_3R + 'cross-sectional areas calculated in', '%.4f' % executionTime2, 's', '!')  # Displays objects.
    print(chnl_4R + 'cross-sectional areas calculated in', '%.4f' % executionTime3, 's', '!')  # Displays objects.
    print(chnl_1T + 'cross-sectional areas calculated in', '%.4f' % executionTime4, 's', '!')  # Displays objects.
    print(chnl_2T + 'cross-sectional areas calculated in', '%.4f' % executionTime5, 's', '!')  # Displays objects.
    print(chnl_3T + 'cross-sectional areas calculated in', '%.4f' % executionTime6, 's', '!')  # Displays objects.
    print(chnl_4T + 'cross-sectional areas calculated in', '%.4f' % executionTime7, 's', '!')  # Displays objects.
    executionTimeEnd = (time.time() - startTime0)  # Calculates how long it took to run since clock start.

    if executionTimeEnd > 60:  # Establishes loop for progress timing when condition met.

        executionTimeEnd = executionTimeEnd / 60  # Converts execution time to minutes.

    print('All sedimentation survey srvy_data digitized!:', '%.4f' % executionTimeEnd, 'min')  # Displays objects.

elif Channel_1R == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_1R + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's','!')  # Displays objects.
elif Channel_2R == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_2R + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_3R == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_3R + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_4R == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_4R + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_1T == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_1T + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_2T == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_2T + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_3T == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_3T + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Channel_4T == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(chnl_4T + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.
elif Custom == 1:  # Establishes loop for progress timing when condition met.
    if executionTime0 > 60:  # Establishes loop for progress timing when condition met.
        executionTime0 = executionTime0 / 60  # Converts execution time to minutes.
    print(cstm + 'cross-sectional areas calculated in', '%.4f' % executionTime0, 's', '!')  # Displays objects.

# Check
# print()  # Inserts blank row to provide white space for next display.
# breakpoint()  # Inserts breakpoint, halting code.

print()  # Inserts blank row to grant space for next displayed items.
print('...')  # Displays string.
print('\033[1m' + 'END!!!' + '\033[0m')  # Displays string in bold signaling the end of the program.

# ======================================================================================================================
# END! -----------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
