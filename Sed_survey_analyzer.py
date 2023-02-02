# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.

# START TIMER ----------------------------------------------------------------------------------------------------------

startTime0 = time.time()  # Starts clock. Measures program run time.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time  # Imports time access and conversions module. Enables time related functions.
import os  # Imports miscellaneous operating system interfaces module. Enables interaction with the computer's
# operating system.

# START TIMER ----------------------------------------------------------------------------------------------------------

startTime = time.time()  # Starts clock to measure program length.

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

for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    for b in lvl2_fldrs:  # Begins loop. Loops through each element in list.
        lvl_paths = [a, a + b]  # Defines list. Inserts folder paths into list for each element combination in previous
        # lists.
        for c in lvl_paths:  # Begins loop. Loops through each element in list.
            elm_index = lvl_paths.index(c) + 1  # Defines variable. Sets value based in list element index for display.
            if not os.path.exists(c):  # Checks if directory does not exist. Skips step if directory exists.
                os.mkdir(c)  # Creates directory if it does not exist.
                print('New directory level', elm_index, '\033[0;32m' + c + '\033[0m', 'created')  # Displays string.
                # Makes font green.

# SET UP PARAMETERS ----------------------------------------------------------------------------------------------------

# Data operations ------------------------------------------------------------------------------------------------------

# Calculate sediment thickness
Depth = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate sediment cross-sectional area
Area = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate sediment volume
Volume = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate stream channel hydraulic geometry
Hydraulic_geometry = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Digitize cross-sections
Digitize = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Data selection -------------------------------------------------------------------------------------------------------

# Survey ranges
Range_start = 1
Range_end = 2


# ======================================================================================================================
# PART 2: FUNCTION CALLING ---------------------------------------------------------------------------------------------
# ======================================================================================================================
