# ======================================================================================================================
# WHITEWATER RIVER VALLEY SEDIMENTATION SURVEYS * ----------------------------------------------------------------------
# SURVEY DATA COORDINATE GEOMETRY DIGITIZER * --------------------------------------------------------------------------
# PYTHON SCRIPTS * -----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION DATA DIGITIZATION!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from Sd_srvy_fnctns import *  # Imports all functions from outside program.

# SELECT OPERATIONS ----------------------------------------------------------------------------------------------------

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Input data -----------------------------------------------------------------------------------------------------------

inpt_fldr = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.

inpt_fl1 = inpt_fldr + '/Survey data new.csv'  # Defines variable. Sets file path to input file.
inpt_fl2 = inpt_fldr + '/Monument metadata inferred new.csv'  # Defines variable. Sets file path to input file.

# Limits of analysis ---------------------------------------------------------------------------------------------------

rng_strt = 1  # Defines variable. Sets start survey range number for operation loop.
rng_end = 2  # Defines variable. Sets end survey range number for operation loop.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

create_folder('Output')  # Creates folder. Calls function. Sets name of output folder where all data products will be
# exported.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Input file(s) --------------------------------------------------------------------------------------------------------

df_srvy_dt = csv_to_DataFrame(inpt_fl1, 0)  # Defines DataFrame. Calls function. Uploads survey data.
df_mnmnt_dt = csv_to_DataFrame(inpt_fl2, 0)  # Defines DataFrame. Calls function. Uploads monument metadata.

# Establish spatial selection framework
rng_nums = forward_range(rng_strt, rng_end, 1, 0)  # Defines array. Calls function. Sets loop order by transect.

# Select transect dataset
for i in rng_nums:  # Begins loop. Loops through array elements. Loops through transect numbers.
    df_rng_dt = slice_DataFrame_rows('Equals', df_srvy_dt, 'Range_num', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single range data.

    # Retrieve metadata
    df_rng_mtdt = slice_DataFrame_rows('Equals', df_mnmnt_dt, 'Range_num', i, 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single range metadata.

    # Select survey dataset
    srvy_nmbrs = slice_DataFrame_columns('Array', 'Integer', df_rng_dt, 'Srvy_num', 1, 0, 0)  # Defines array. Calls
    # function. Slices DataFrame to yield survey numbers of range dataset.

    for j in srvy_nmbrs:  # Begins loop. Loops through array elements. Loops through survey numbers.
        df_rng_srvy_dt = slice_DataFrame_rows('Equals', df_rng_dt, 'Srvy_num', j, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range single survey data.

        # Retrieve metadata
        df_rng_srvy_mtdt = slice_DataFrame_rows('Equals', df_rng_mtdt, 'Srvy_num', j, 1)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range survey metadata.

        retrieve_metadata(df_rng_srvy_mtdt, 1)  # Calls function. Displays and retrieves metadata.
