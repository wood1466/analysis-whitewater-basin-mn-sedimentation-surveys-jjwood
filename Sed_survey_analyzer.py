# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------
import pandas as pd

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time
    #, os  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.
# import pandas as pd  # Imports "Python data analysis library" with alias. Enables DataFrame array functionality.
from Cross_section_analyzer import *


# START TIMER ----------------------------------------------------------------------------------------------------------

strtTm0 = time.time()  # Starts clock. Measures program run time.

# SET UP PARAMETERS ----------------------------------------------------------------------------------------------------

# Data operations ------------------------------------------------------------------------------------------------------

# Calculate sediment thickness
Dpth = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate sediment cross-sectional area
Area = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate sediment volume
Volm = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate stream channel hydraulic geometry
Hydr_geom = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Digitize cross-sections
Dgtz = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Data selection -------------------------------------------------------------------------------------------------------

# Survey ranges
rng_strt = 70
rng_end = 71
start=rng_strt
end=rng_end
step=1

rgn_nums = forward_range(start,end,step)

srvy_strt = 4
srvy_end = 3

start= srvy_strt
end= srvy_end
step=-1

srvy_nums = reverse_range(start,end,step)

# SET UP DIRECTORIES ---------------------------------------------------------------------------------------------------

# Name level 1
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Name level 2
xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where
# cross-sectional analysis data will be located.
dgtz_fldr = '/Digitization'  # Defines variable as string. Sets name of new directory where digitization data will be
# located.

# Name level 3+
clcs_fldr = '/Calculations'  # Defines variable as string. Sets name of new directory where calculations will be
# exported.
figs_fldr = '/Figures'  # Defines variable as string. Sets name of new directory where figures will be exported.

# Create (sub) folders
lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.
lvl2_fldrs = [xsctn_fldr, dgtz_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.

# mak drs
for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    for b in lvl2_fldrs:  # Begins loop. Loops through each element in list.
        lvl_paths = [a, a + b]  # Defines list. Inserts folder paths into list for each element combination in previous
        # lists.
        for c in lvl_paths:  # Begins loop. Loops through each element in list.
            level = lvl_paths.index(c) + 1  # Defines variable. Sets value based in list element index for display.

            create_folder(level, c)

#make dataframe
path = '/Users/jimmywood/github/Whitewater_MN_sedimentation/PyCharm_Venv/Input/Cross_sectional_analysis/Trout_Creek_survey_data.csv'
label = 'TROUT CREEK! '
df_srvy_dt = upload_csv(path, label)

for a in rgn_nums:
    for b in srvy_nums:
        slice1 = a
        slice2 = b
        dataframe = df_srvy_dt
        column1 = 'Range_num'
        label1 = 'RANGE NUMBER'
        column2 = 'Srvy_num'
        label2 = 'SURVEY NUMBER'
        df_srvy = slice_DataFrame_rows2(dataframe, column1,slice1,label1,column2,slice2,label2)

        column1='Offset_ft'
        label1 = 'OFFSET'
        dataframe=df_srvy

        df_offst = slice_DataFrame_column1(dataframe,column1,label1)

        df_elvtn = slice_DataFrame_column1(df_srvy, 'Elv_lcl_ft', 'ELEVATION')

        number=1
        figure_size=(5,3)
        x=df_offst
        y=df_srvy
        label=1994
        color='Blue'
        marker='o'
        alpha=0.9
        xlabel='Survey offset (ft)'
        fontsize_axis=8
        ylabel='Local elevation (ft)'
        title='Survey cross-section'
        pause=0
        fig1 = plot_line(1, (5,3), df_offst, df_elvtn, 1994, 'Cyan', marker, alpha, xlabel, fontsize_axis, ylabel, title,pause)
