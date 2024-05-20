# ======================================================================================================================
# WHITEWATER RIVER VALLEY SEDIMENTATION SURVEYS * ----------------------------------------------------------------------
# SURVEY DATA QUALITY CONTROL VISUALIZATION * --------------------------------------------------------------------------
# PYTHON SCRIPTS * -----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION DATA ENTRY QUALITY CHECK!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from Sd_srvy_fnctns import *  # Imports all functions from outside program.

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Directory
inpt_fldr = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.
otpt_fldr = 'Output'  # Defines variable. Sets name of output folder where all data products will be exported.
qc_fldr = 'Quality Control'  # Defines variable. Sets name of output folder where all geospatial data products will be # exported.

# Data
inpt_fl1 = inpt_fldr + '/Sedimentation_survey_data_only.csv'  # Defines variable. Sets file path to input file.

# Limits of analysis
rng_strt = 5  # Defines variable. Sets start survey range number for operation loop.
rng_end = 6  # Defines variable. Sets end survey range number for operation loop.

# Plot format
wdth = 8  # Defines variable as float. Sets plot window width.
hght = wdth * 1.618  # Defines variable. Sets plot window height.
fg_sz = (hght, wdth)  # Defines object. Sets plot window size.
fntsz = [14, 12]  # Defines list. Sets font size for axes labels and tick marks.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.
ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000', '#648FFF']  # Defines list. Sets IBM colorblind friendly
# palette with Color-hex color codes.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

create_folder(otpt_fldr)  # Creates folder. Calls function. Creates output folder where all data products will be
# exported.
create_folder(otpt_fldr + '/' + qc_fldr)  # Creates folder. Calls function. Creates output folder where all geospatial
# data products will be exported.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

df_srvy_dt = csv_to_DataFrame(inpt_fl1, 0)  # Defines DataFrame. Calls function. Uploads survey data.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Establish spatial selection framework --------------------------------------------------------------------------------

rng_nmbrs = forward_range(rng_strt, rng_end, 1, 0)  # Defines array. Calls function. Sets loop order by transect.

# Select transect data -------------------------------------------------------------------------------------------------

for i in rng_nmbrs:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates coordinates
    # for each range in sequence.

    df_rng_dt = slice_DataFrame_rows('Equals', df_srvy_dt, 'range_number', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single range data.

# Select survey data -----------------------------------------------------------------------------------------------

    prfl_nmbrs = slice_DataFrame_columns('Array', 'Integer', df_rng_dt, 'profile_number', 1, 0, 0)  # Defines array.
    # Calls function. Slices DataFrame to yield survey numbers of range dataset.

    for j in prfl_nmbrs:  # Begins loop. Loops through array elements. Loops through profile numbers. Calculates
        # coordinates for each survey in sequence.
        df_rng_srvy_dt = slice_DataFrame_rows('Equals', df_rng_dt, 'profile_number', j, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range single survey data.

        # Survey data
        df_stns = slice_DataFrame_columns('DataFrame', 'Float', df_rng_srvy_dt, 'station', 0, 0, 0)  # Defines array.
        # Calls function. Slices DataFrame to yield survey stations of survey dataset.
        df_elvtns = slice_DataFrame_columns('DataFrame', 'Float', df_rng_srvy_dt, 'elevation_1', 0, 0, 0)  # Defines
        # array. Calls function. Slices DataFrame to yield survey elevations of survey dataset.

        # Plot metadata
        rng_id = slice_DataFrame_cell('String', df_rng_srvy_dt, 0, '2024_range_id', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield range ID of present dataset. For plot title.
        lbl = slice_DataFrame_cell('String', df_rng_srvy_dt, 0, 'profile_year', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield surface profile year of present dataset. for plot legend.

        # PLOT CROSS-SECTIONS ------------------------------------------------------------------------------------------

        ttl = 'Range ' + rng_id + ' surface profiles'  # Defines variable. Sets plot title.

        indx = np.where(prfl_nmbrs == j)[0][0]  # Defines variable. Selects index of array element. For plot color
        # selection.
        clr = ibm[indx]  # Defines variable. Selects plot color.

        plot_range_data(1, fg_sz, df_stns, df_elvtns, lbl, clr, 'o', 1, 1, 'solid', 0.5, 'best', 2, 0.7, 0.7, fntsz[1],
                        'Station (ft)', 'Elevation (ft)', fntsz[0], lbl_pd, ttl, 2, 1)  # Plots data. Calls function.

        # Export file --------------------------------------------------------------------------------------------------

        if j == prfl_nmbrs[-1]:  # Begins conditional statement. Checks equality. Closes figure after plotting last
            # range dataset.
            fg_nm = '/' + rng_id  # Defines variable. Sets figure name.

            plt.savefig(otpt_fldr + '/' + qc_fldr + fg_nm)  # Saves figure to directory.

            plt.close(1)  # Closes plot.

# ======================================================================================================================
# * --------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================