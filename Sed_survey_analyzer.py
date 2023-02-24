# ======================================================================================================================
# WHITEWATER RIVER VALLEY, MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * --------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os, sys
# Imports "Time and access conversions", "Miscellaneous operating system interfaces", and "System specific parameters
# and functions". Enables use of various time–related functions and operating system dependent functionality.
import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sc
# Imports "Python data analysis library", a numerical mathematics library, a plotting interface, and a scientific
# mathematics library, with alias. Enables use of DataFrames, various mathematical functions, and data plotting.
from Functions import *  # Imports all functions from outside program.

# START TIMER ----------------------------------------------------------------------------------------------------------

strt_tm0 = time.time()  # Starts clock. Measures program run time.

# CHOOSE OPERATIONS ----------------------------------------------------------------------------------------------------

# Single cross-section -------------------------------------------------------------------------------------------------

Sngl = 0  # Defines variable as integer. Sets binary toggle. Undergoes analysis of single cross-section.

# Plot single cross-section
Plt_sngl = 0  # Defines variable as integer. Sets binary toggle.

# Calculate channel hydraulic geometry
Clc_hydro_geom = 0  # Defines variable as integer. Sets binary toggle.

# Plot hydraulic radius
Plt_hydro_rad = 0  # Defines variable as integer. Sets binary toggle. 1D plot symbolized by survey year.

# Subsequent cross-sections --------------------------------------------------------------------------------------------

Dbl = 1  # Defines variable as integer. Sets binary toggle. Undergoes analysis cross-sections as subsequent pairs.

# Plot subsequent cross-sections
Plt_dbl = 0  # Defines variable as integer. Sets binary toggle.
Plt_dbl_intrp = 0  # Defines variable as integer. Sets binary toggle. Plots interpolated datasets.
Plt_dbl_reintrp = 0  # Defines variable as integer. Sets binary toggle. Plots reinterpolated datasets over coincident
# x-range.

# Calculate sediment thickness
Dpth = 1  # Defines variable as integer. Sets binary toggle.

# Plot sediment thickness
Plt_dpth = 0  # Defines variable as integer. Sets binary toggle. 1D plot symbolized by survey year.

# Analyze sediment distribution
Sed_dist = 1  # Defines variable as integer. Sets binary toggle.

# Plot sediment distribution
# Plt_sed_dist = 1  # Defines variable as integer. Sets binary toggle. Plots reinterpolated datasets with depth insets.
Plt_dbl_reintrp2 = 1
Plt_dbl_reintrp3 = 1
Plt_sed_dist = 1
# SET PARAMETERS -------------------------------------------------------------------------------------------------------

# Data selection -------------------------------------------------------------------------------------------------------

# Set range limits
rng_strt = 70  # Defines variable as integer. Sets start range for analysis loop.
rng_end = 73  # Defines variable as integer. Sets end range for analysis loop.

# Set survey limits
srvy_strt = 5  # Defines variable as integer. Sets starting survey for analysis loop.
srvy_end = 2  # Defines variable as integer. Sets end survey for analysis loop.

# Data visualization ---------------------------------------------------------------------------------------------------

# Set general plot format
wdth = 4.5  # Defines variable as float. Sets plot width.
hght = wdth * 1.618  # Defines variable. Sets plot height. Uses golden ratio.
fig_sz = (hght, wdth)  # Defines object. Sets plot size.
fntsz_tcks = 8  # Defines variable as integer. Sets font size for axes tick marks.
fntsz_ax = 10  # Defines variable as integer. Sets font size for axes labels.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Set data display format
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDDD']
# Defines list. Sets Paul Tol muted colorblind friendly palette via hex color codes.
lin_wdth = 2  # Defines variable as integer. Sets plot line width.
mrkrs = [' ', 'v', 'P', 'o', 'X', 's', '^', 'D', '<', '>', '8', 'p', 'h', 'H', 'd']  # Defines list. Sets matplotlib
# plot markers.
mrkr_sz = 4  # Defines variable as integer. Sets plot marker size.
alpha = 0.5  # Defines variable as float. Sets plotted object transparency.
alpha_fl = 0.3  # Defines variable as float. Sets plotted object transparency.

# Set legend display format
lctn = 'best'  # Defines variable as string. Sets legend location on plot. Automatically chosen.
mrkr_scl = 2  # Defines variable as integer. Sets marker size.
frm_alpha = 0.7  # Defines variable as float. Sets box transparency.
lbl_spcng = 0.7  # Defines variable as float. Sets object spacing.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Levels ---------------------------------------------------------------------------------------------------------------

inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Folders --------------------------------------------------------------------------------------------------------------

lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. To enable looped folder creation.

for i in lvl1_fldrs:  # Begins loop through elements of list. Loops through paths.
    lvl = 1  # Defines variable as integer. For function input.

    create_folder(lvl, i)  # Creates folders. Calls function.

# ======================================================================================================================
# PART 2: CROSS-SECTIONAL ANALYSIS - SINGLE ----------------------------------------------------------------------------
# ======================================================================================================================

# PART 2A: DATA SELECTION ----------------------------------------------------------------------------------------------

# UPLOAD DATA ----------------------------------------------------------------------------------------------------------

inpt_fl = inpt_fldr + '/Trout_Creek_survey_data.csv'  # Defines string. Sets file path to input file.

df_srvy_dt = upload_csv(inpt_fl, 'TROUT CREEK ', 0)  # Defines DataFrame. Calls function. Uploads survey data.

# ESTABLISH DATA SELECTION FRAMEWORK -----------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------

rgn_nums = forward_range(rng_strt, rng_end, 1, 'Range numbers', 0)  # Defines array. Calls function. Sets loop
# order by range.

# Temporal -------------------------------------------------------------------------------------------------------------

srvy_nums = reverse_range(srvy_strt, srvy_end, -1, 'Survey numbers', 0)  # Defines array. Calls function. Sets
# loop order by survey.

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Range dataset --------------------------------------------------------------------------------------------------------

for i in rgn_nums:  # Begins loop through array elements. Loops through range numbers.
    df_rng = slice_DataFrame_rows('equals', df_srvy_dt, 'Range_num', i, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield singular range data.

    # Retrieve metadata
    rng_name1 = slice_DataFrame_cell(df_rng, 0, 'Srvy_range', 'Range', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield range number of present dataset.
    strm_stat1 = slice_DataFrame_cell(df_rng, 0, 'Srvy_stat', 'Stream station', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey station of reach.

    df_srvy_nums1 = slice_DataFrame_columns(df_rng, 'Srvy_num', 1, 'SURVEY NUMBER', 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield survey numbers of present dataset.

    srvy_num_max = max_value_DataFrame(df_srvy_nums1, 'Survey', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield total number of range surveys of present dataset.

    # Survey dataset ---------------------------------------------------------------------------------------------------

    for j in srvy_nums:  # Begins loop through array elements. Loops through survey numbers.
        if j > 1:  # Conditional statement. Executes lines below if dataset is not last survey.
            df_srvy1 = slice_DataFrame_rows('equals', df_rng, 'Srvy_num', j, 'SURVEY NUMBER', 0)  # Defines DataFrame. Calls
            # function. Slices DataFrame to yield singular survey data.

            # Retrieve metadata
            srvy_yr1 = slice_DataFrame_cell(df_srvy1, 0, 'Srvy_year', 'Survey year', 0)  # Defines variable. Calls
            # function. Slices DataFrame to yield survey year of present dataset.
            srvy_dt1 = slice_DataFrame_cell(df_srvy1, 0, 'Srvy_date', 'Survey date', 0)  # Defines variable. Calls
            # function. Slices DataFrame to yield survey date of present dataset.

            # Survey measurements --------------------------------------------------------------------------------------

            df_offst1 = slice_DataFrame_columns(df_srvy1, 'Offset_ft', 0, 'OFFSET', 0)  # Defines DataFrame. Calls
            # function. Slices DataFrame to yield survey offsets of present dataset.
            df_elvtn1 = slice_DataFrame_columns(df_srvy1, 'Elv_geo_ft', 0, 'ELEVATION', 0)  # Defines DataFrame. Calls
            # function. Slices DataFrame to yield survey elevations of present dataset.

            # Retrieve metadata
            offst_min1 = min_value_DataFrame(df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield first offset of present dataset.
            offst_max1 = max_value_DataFrame(df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield last offset of present dataset.
            elvtn_min1 = min_value_DataFrame(df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield lowest elevation of present dataset.
            elvtn_max1 = max_value_DataFrame(df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield highest elevation of present dataset.

            num_smpls1 = slice_DataFrame_cell(df_srvy1, -1, 'Sample_num', 'Total number of samples', 0)  # Defines
            # variable. Calls function. Slices DataFrame to yield number of measurements of present dataset.

            num_smpls1 = num_smpls1  # Redefines variable. Converts to integer.

            # Calculate metadata
            rng_lngth1 = offst_max1 - offst_min1  # Defines variable. Calculates survey length.
            srvy_rlf1 = elvtn_max1 - elvtn_min1  # Defines variable. Calculates survey relief.

            # DISPLAY DATA ---------------------------------------------------------------------------------------------

            if Sngl == 1:  # Conditional statement. Executes analysis of single cross-section.
                # Metadata ---------------------------------------------------------------------------------------------

                print('==================================================')  # Displays objects.
                print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
                # objects.
                print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1))  # Displays objects.
                print('\033[1m' + 'Range survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(j) + ' of ' +
                      str(srvy_num_max) + ')')  # Displays objects.
                print('\033[1m' + 'Survey date(s): ' + '\033[0m' + str(srvy_dt1))  # Displays objects.
                print('\033[1m' + 'Survey length: ' + '\033[0m' + str(rng_lngth1) + ' ft')  # Displays objects.
                print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' ft')  # Displays objects.
                print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1))  # Displays objects.
                print('--------------------------------------------------')  # Displays objects.

                # Cross-section plot -----------------------------------------------------------------------------------

                if Plt_sngl == 1:  # Conditional statement. Plots single cross-section.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                    # plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets plot
                    # marker type.
                    title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + ' survey '  # Defines string. Sets plot
                    # title.

                    plot_lines(1, 1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz, lin_wdth, alpha, 0,
                               lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)', fntsz_ax,
                               lbl_pd, 'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                    # EXPORT FIGURE ------------------------------------------------------------------------------------

                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Single']  # Defines
                    # list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '_' + str(srvy_yr1) + '.pdf'  # Defines
                    # variable as strIng. Sets name of figure for export.

                    export_file_to_directory(1, 'figure', 4, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1,
                                             'pdf', None, None, 'Cross-sectional plot', 0)  # Creates directory and
                    # exports figure. Calls function.

                # ======================================================================================================
                # PART 2B: DATA ANALYSIS - HYDRAULIC GEOMETRY ----------------------------------------------------------

                # CALCULATE CHANNEL GEOMETRY ---------------------------------------------------------------------------

                if Clc_hydro_geom == 1:  # Conditional statement. Calculates hydraulic geometry.
                    df_strm = slice_DataFrame_rows('equals', df_srvy1, 'Gmrph_dsc', 'Stream channel', 'RANGE ' + str(i), 0)
                    # Defines DataFrame. Calls function. Slices DataFrame to yield stream channel data.

                    dt_lbl1 = 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' STREAM CHANNEL OFFSET'  # Defines string.
                    dt_lbl5 = 'RANGE ' + str(i) + ' SURVEY ' + str(j) + ' STREAM CHANNEL ELEVATION'  # Defines string.

                    wdth, dpth, hydro_rad = hydraulic_geometry(df_strm, 'Offset_ft', dt_lbl1, 'Offset',
                                                               'Channel dimensions', ' (ft)', 'Width: ', 'Elv_geo_ft',
                                                               dt_lbl5, 'Elevation', 'Depth: ',
                                                               'Bankfull hydraulic radius: ', 1)  # Defines variable.
                    # Calls function. Calculates stream channel geometry quantities.

                    # PREPARE DATA FOR EXPORT --------------------------------------------------------------------------

                    # Lists --------------------------------------------------------------------------------------------

                    # Create empty lists
                    if i == rng_strt:  # Conditional statement. Executes for first range only.
                        if j == srvy_strt:  # Conditional statement. Executes for first survey only.
                            rng_name1_list = []  # Defines list. Empty for looped population.
                            srvy_yr1_list = []  # Defines list. Empty for looped population.
                            strm_stat_list = []  # Defines list. Empty for looped population.
                            hydro_rad_list = []  # Defines list. Empty for looped population.
                            wdth_list = []  # Defines list. Empty for looped population.
                            dpth_list = []  # Defines list. Empty for looped population.
                            dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, strm_stat_list, wdth_list, dpth_list,
                                               hydro_rad_list]  # Defines list. Nested to enable looped population.

                    # Populate lists
                    dtfrm_pop_values = [rng_name1, srvy_yr1, strm_stat1, wdth, dpth, hydro_rad]  # Defines list. Sets
                    # values to populate lists.
                    dtfrm_pop_dt_lbl=['Range name', 'Survey year', 'Stream station', 'Width', 'Depth',
                                      'Hydraulic radius']  # Defines list. Sets labels for display.
                    dtfrm_pop_clm_lbl=['Srvy_range', 'Srvy_year', 'Strm_stat', 'Strm_W_ft', 'Strm_D_ft', 'R_h_ft']
                    # Defines list. Sets column labels for DataFrame.

                    for x in dtfrm_pop_lists:  # Begins loop through list elements. Loops through empty lists.
                        index = dtfrm_pop_lists.index(x)  # Defines variable. Retrieves index of list element for
                        # appropriate selection.

                        x = create_appended_list(dtfrm_pop_values[index], dtfrm_pop_dt_lbl[index], x,
                                                 'New list appended: ', 0)  # Redefines lists. Calls function.

                    if i == rng_end:  # Conditional statement. Executes for last range only.
                        if j == srvy_end:  # Conditional statement. Executes for first survey only.
                            dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, strm_stat_list, wdth_list, dpth_list,
                                               hydro_rad_list]  # Redefines list. With populated lists.

                            # DataFrame --------------------------------------------------------------------------------

                            dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array for
                            # operation.
                            dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array for
                            # DataFrame dimensional compatibility.

                            df_hydro_geom = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl, 'HYDRAULIC GEOMETRY',
                                                             0)  # Defines DataFrame. Calls function. Creates DataFrame
                            # of hydraulic radius results.

                            # EXPORT FILE ------------------------------------------------------------------------------

                            fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Hydraulic_geometry']
                            # Defines list. Sets folder labels for directory to be made.

                            fl_name = '/Hydraulic_geometry.csv'  # Defines variable as strIng. Sets name and extension
                            # of file for export.

                            export_file_to_directory(1, 'table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                     fl_name, 1, None, df_hydro_geom, False, 'Hydraulic radius table',
                                                     0)  # Creates directory and exports figure. Calls function.

                            # PLOT DATA --------------------------------------------------------------------------------

                            if Plt_hydro_rad == 1:  # Conditional statement. Plots hydraulic radius, by year, as a
                                # function of distance upstream.

                                df_srvy_yrs = slice_DataFrame_columns(df_hydro_geom, 'Srvy_year', 1, 'Survey years', 0)
                                # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present
                                # dataset.
                                srvy_yrs = df_srvy_yrs.tolist()  # Defines list. Converts DataFrame to list.

                                for x in srvy_yrs:  # Begins loop through list elements. Loops through survey years.
                                    df_chnl_geom_x = slice_DataFrame_rows('equals', df_hydro_geom, 'Srvy_year', x,
                                                                           'HYDRAULIC GEOMETRY', 0)  # Defines
                                    # DataFrame. Calls function. Slices DataFrame to yield stream channel data of by
                                    # year.

                                    df_h_rad_x = slice_DataFrame_columns(df_chnl_geom_x, 'R_h_ft', 0,
                                                                         'HYDRAULIC RADIUS', 0)  # Defines DataFrame.
                                    # Calls function. Slices DataFrame to yield hydraulic radius data by year.
                                    df_strm_stat_x = slice_DataFrame_columns(df_chnl_geom_x, 'Strm_stat', 0,
                                                                             'STREAM STATION', 0)  # Defines DataFrame.
                                    # Calls function. Slices DataFrame to yield stream station data.

                                    df_h_rad_x = df_h_rad_x.astype(float)  # Redefines DataFrame. Converts values to
                                    # float.

                                    srvy_yr = slice_DataFrame_cell(df_chnl_geom_x, 0, 'Srvy_year', 'Survey year', 0)
                                    # Defines variable. Calls function. Slices DataFrame to yield suvey year of present
                                    # dataset.

                                    clr1 = get_plot_feature_by_year(srvy_yr, tol_mtd, 0)  # Defines variable. Calls
                                    # function. Sets plot color.
                                    mrkr1 = get_plot_feature_by_year(srvy_yr, mrkrs, 1)  # Defines variable. Calls
                                    # function. Sets plot marker type.

                                    title = 'Hydraulic radius evolution: Trout Creek'  # Defines string. Sets plot
                                    # title.

                                    plot_lines(1, 2, fig_sz, df_strm_stat_x, df_h_rad_x, srvy_yr, clr1, mrkr1, mrkr_sz,
                                               lin_wdth, alpha, 1, lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks,
                                               'River station', fntsz_ax, lbl_pd, 'Hydraulic radius (ft)', title, 1,
                                               1)  # Defines function. For cross-section plotting.

                                    # EXPORT FIGURE --------------------------------------------------------------------

                                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Hydraulic_radius']  # Defines
                                    # list. Sets folder labels for directory to be made.

                                    fig_name = '/R_h_' + str(srvy_yrs[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                    # variable as strIng. Sets name of figure for export.

                                    export_file_to_directory(1, 'figure', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                             fig_name, 2, 'pdf', None, None, 'Hydraulic radius plot',
                                                             0)  # Creates directory and exports figure. Calls
                                    # function.

            # ==========================================================================================================
            # PART 3: CROSS-SECTIONAL ANALYSIS - DOUBLE ----------------------------------------------------------------
            # ==========================================================================================================

            # PART 3A: DATA SELECTION ----------------------------------------------------------------------------------

            # SELECT DATA ----------------------------------------------------------------------------------------------

            if Dbl == 1:  # Conditional statement. Executes analysis of cross-sections as subsequent pairs.
                k = j - 1  # Defines variable as integer. Allows for selection of second dataset.

                if j > 2:  # Conditional statement. Executes lines below if dataset is not second to last survey.
                    # Survey dataset -----------------------------------------------------------------------------------

                    df_srvy2 = slice_DataFrame_rows('equals', df_rng, 'Srvy_num', k, 'SURVEY NUMBER', 0)  # Defines DataFrame.
                    # Calls function. Slices DataFrame to yield singular survey data.

                    # Retrieve metadata
                    srvy_yr2 = slice_DataFrame_cell(df_srvy2, 0, 'Srvy_year', 'Survey year', 0)  # Defines variable.
                    # Calls function. Slices DataFrame to yield survey year of present dataset.
                    srvy_dt2 = slice_DataFrame_cell(df_srvy2, 0, 'Srvy_date', 'Survey date', 0)  # Defines variable.
                    # Calls function. Slices DataFrame to yield survey date of present dataset.

                    # Survey measurements ------------------------------------------------------------------------------

                    df_offst2 = slice_DataFrame_columns(df_srvy2, 'Offset_ft', 0, 'OFFSET', 0)  # Defines DataFrame.
                    # Calls function. Slices DataFrame to yield survey offsets of present dataset.
                    df_elvtn2 = slice_DataFrame_columns(df_srvy2, 'Elv_geo_ft', 0, 'ELEVATION', 0)  # Defines
                    # DataFrame. Calls function. Slices DataFrame to yield survey elevations of present dataset.

                    # Retrieve metadata
                    offst_min2 = min_value_DataFrame(df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield first offset of present dataset.
                    offst_max2 = max_value_DataFrame(df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield last offset of present dataset.
                    elvtn_min2 = min_value_DataFrame(df_elvtn2, 'Elevation', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield lowest elevation of present dataset.
                    elvtn_max2 = max_value_DataFrame(df_elvtn2, 'Elevation', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield highest elevation of present dataset.

                    num_smpls2 = slice_DataFrame_cell(df_srvy2, -1, 'Sample_num', 'Total number of samples', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield number of measurements of present
                    # dataset.

                    # Calculate metadata
                    rng_lngth2 = offst_max2 - offst_min2  # Defines variable. Calculates survey length.
                    srvy_rlf2 = elvtn_max2 - elvtn_min2  # Defines variable. Calculates survey relief.

                    # DISPLAY DATA -------------------------------------------------------------------------------------

                    # Metadata -----------------------------------------------------------------------------------------

                    print('==================================================')  # Displays objects.
                    print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
                    # objects.
                    print('\033[1m' + 'Range surveys: ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' +
                          str(j) + '–' + str(k) + ' of ' + str(srvy_num_max) + ')')  # Displays objects.
                    print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))  # Displays
                    # objects.
                    print('\033[1m' + 'Survey lengths: ' + '\033[0m' + str(rng_lngth1) + ' & ' + str(rng_lngth2) +
                          ' ft')  # Displays objects.
                    print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' & ' +
                          str('%.1f' % srvy_rlf2) + ' ft')  # Displays objects.
                    print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1) + ' & ' + str(num_smpls2))
                    # Displays objects.
                    print('--------------------------------------------------')  # Displays objects.

                    # Cross-section plot -------------------------------------------------------------------------------

                    if Plt_dbl == 1:  # Conditional statement. Plots cross-sections as subsequent pairs.
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets
                        # plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 0)  # Defines variable. Calls function. Sets
                        # plot marker type.

                        title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' surveys'
                        # Defines string. Sets title of plot.  # Defines string. Sets plot title.

                        plot_lines(2, 3, fig_sz, [df_offst1, df_offst2], [df_elvtn1, df_elvtn2], [srvy_yr1, srvy_yr2],
                                   [clr1, clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, 0, lctn, mrkr_scl,
                                   frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd,
                                   'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                        # EXPORT FIGURE --------------------------------------------------------------------------------

                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/Measured']
                        # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                                   str(srvy_yr2) + '.pdf'  # Defines variable as strIng. Sets name of figure for
                        # export.

                        export_file_to_directory(1, 'figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 3, 'pdf', None, None, 'Cross-sectional plot', 0)  # Creates directory
                        # and exports figure. Calls function.

                    # INTERPOLATE DATASETS -----------------------------------------------------------------------------

                    offsts_int1, elvtns_int1, x_rng_int1, num_smpls_int1 = interpolate_cross_section('dataframe',
                                                                                                     df_offst1,
                                                                                                     df_elvtn1, None,
                                                                                                     None, 'linear',
                                                                                                     0.01, 2, 0)
                    # Defines variables and interpolates cross-section. Calls function.

                    offsts_int2, elvtns_int2, x_rng_int2, num_smpls_int2 = interpolate_cross_section('dataframe',
                                                                                                     df_offst2,
                                                                                                     df_elvtn2, None,
                                                                                                     None, 'linear',
                                                                                                     0.01, 2, 0)
                    # Defines variables and interpolates cross-section. Calls function.

                    # PLOT DATA ----------------------------------------------------------------------------------------

                    if Plt_dbl_intrp == 1:  # Conditional statement. Plots interpolated cross-sections as subsequent
                        # pairs.
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets
                        # plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 0)  # Defines variable. Calls function. Sets
                        # plot marker type.

                        title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                ' interpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                        # plot title.

                        plot_lines(2, 4, fig_sz, [offsts_int1, offsts_int2], [elvtns_int1, elvtns_int2],
                                   [srvy_yr1, srvy_yr2], [clr1, clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, 0,
                                   lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)', fntsz_ax,
                                   lbl_pd, 'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                        # EXPORT FIGURE --------------------------------------------------------------------------------

                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double',
                                     '/Interpolated']  # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' \
                                   + str(srvy_yr2) + '_Interp' + '.pdf'  # Defines variable as strIng. Sets name of
                        # figure for export.

                        export_file_to_directory(1, 'figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 4, 'pdf', None, None, 'Cross-sectional plot', 0)  # Creates directory
                        # and exports figure. Calls function.

                    # SELECT CALCULATION RANGE -------------------------------------------------------------------------

                    start, end, srvy_lngth_shrd = select_coincident_x_range('dataframe', df_offst1, df_offst2,
                                                                            ' ft', 0)  # Defines variales. Calls
                    # function. Identifies shared x values of individual datasets.

                    # REINTERPOLATE DATASETS -----------------------------------------------------------------------

                    offsts_int1, elvtns_int1, x_rng_int1, num_smpls_int1 = interpolate_cross_section('limits',
                                                                                                     df_offst1,
                                                                                                     df_elvtn1,
                                                                                                     start, end,
                                                                                                     'linear',
                                                                                                     0.01, 2, 0)
                    # Defines variables and interpolates cross-section. Calls function.
                    offsts_int2, elvtns_int2, x_rng_int2, num_smpls_int2 = interpolate_cross_section('limits',
                                                                                                     df_offst2,
                                                                                                     df_elvtn2,
                                                                                                     start, end,
                                                                                                     'linear',
                                                                                                     0.01, 2, 0)
                    # Defines variables and interpolates cross-section. Calls function.

                    # PLOT DATA ----------------------------------------------------------------------------------------

                    if Plt_dbl_reintrp == 1:  # Conditional statement. Plots reinterpolated cross-sections as
                        # subsequent pairs.
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 1)  # Defines variable. Calls function. Sets
                        # plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 0)  # Defines variable. Calls function. Sets
                        # plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 0)  # Defines variable. Calls function. Sets
                        # plot marker type.

                        title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                ' reinterpolated surveys'  # Defines string. Sets title of plot.  # Defines string.
                        # Sets plot title.

                        plot_lines(2, 5, fig_sz, [offsts_int1, offsts_int2], [elvtns_int1, elvtns_int2],
                                   [srvy_yr1, srvy_yr2], [clr1, clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, 0,
                                   lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)',
                                   fntsz_ax, lbl_pd, 'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls
                        # function.

                        # EXPORT FIGURE --------------------------------------------------------------------------------

                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double',
                                     '/Reinterpolated']  # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) \
                                   + '–' + str(srvy_yr2) + '_Reinterp' + '.pdf'  # Defines variable as strIng. Sets
                        # name of figure for export.

                        export_file_to_directory(1, 'figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 5, 'pdf', None, None, 'Cross-sectional plot', 0)  # Creates directory
                        # and exports figure. Calls function.

                    # ==================================================================================================
                    # PART 3B. DATA ANALYSIS - SEDIMENT THICKNESS ------------------------------------------------------

                    if Dpth == 1:  # Conditional statement. Calculates sediment thicknkess between cross-sections.
                        # SELECT COORDINATE PAIRS ----------------------------------------------------------------------

                        end = end + 0.01  # Defines variable. Resets end of range so array includes final input value.

                        index1 = np.arange(0, len(offsts_int1), 1, dtype=int)  # Defines array. Creates array of
                        # index values for looped calculation.

                        for x in index1:  # Begins loop through array. Loops through coordinate indices.
                            offst1, elvtn1_top, elvtn1_btm = get_coordinate_pairs('depth', x, None, offsts_int1,
                                                                                  elvtns_int1, elvtns_int2, 0)
                            # Defines variables. Calls function.

                            # CALCULATE SEDIMENT THICKNESS -------------------------------------------------------------

                            # At a point -------------------------------------------------------------------------------

                            dpth1, prcs1 = sediment_thickness('depth', elvtn1_top, elvtn1_btm, None, None,
                                                              'Sediment thickness: ', 0)  # Defines variables. Calls
                            # function.

                            # Averaged over cross-section --------------------------------------------------------------

                            # Create empty list
                            if x == index1[0]:  # Conditional statement. Executes for first coordinate only.
                                dpth1_list = []  # Defines list. Empty for looped population.

                            # Populate list
                            dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_list,
                                                              'New list appended: ', 0)  # Redefines list. Calls
                            # function.

                            if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.
                                dpth_avg = np.sum(dpth1_list) / x  # Defines variable. Calculates average sediment
                                # thickness.

                                dpth_max = max(dpth1_list)  # Defines variable. Retrieves max value from list.
                                dpth_min = min(dpth1_list)  # Defines variable. Retrieves min value from list.

                            # PREPARE DATA FOR EXPORT ------------------------------------------------------------------

                            # Lists ------------------------------------------------------------------------------------

                            # Create empty lists
                            if i == rng_strt:  # Conditional statement. Executes for first range only.
                                if j == srvy_strt:  # Conditional statement. Executes for first survey only.
                                    rng_name1_list = []  # Defines list. Empty for looped population.
                                    srvy_yr1_list = []  # Defines list. Empty for looped population.
                                    srvy_yr2_list = []  # Defines list. Empty for looped population.
                                    strm_stat_list = []  # Defines list. Empty for looped population.
                                    dpth_avg_list = []  # Defines list. Empty for looped population.
                                    dpth_max_list = []  # Defines list. Empty for looped population.
                                    dpth_min_list = []  # Defines list. Empty for looped population.
                                    dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, srvy_yr2_list, strm_stat_list,
                                                       dpth_avg_list, dpth_max_list, dpth_min_list]  # Defines list.
                                    # Nested to enable looped population.

                            # Populate lists
                            if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.
                                dtfrm_pop_values = [rng_name1, srvy_yr1, srvy_yr2, strm_stat1, dpth_avg, dpth_max,
                                                    dpth_min]  # Defines list. Sets values to populate lists.

                                for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to
                                    # populate lists.
                                    index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list
                                    # element.

                                    y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                             'New list appended: ', 0)  # Redefines list. Calls
                                    # function.

                        if i == rng_end:  # Conditional statement. Executes for last range only.
                            if k == srvy_end:  # Conditional statement. Executes for last survey only.
                                dtfrm_pop_clm_lbl=['Srvy_range', 'Srvy_year1', 'Srvy_year2', 'Strm_stat', 'D_avg_ft',
                                                   'D_max_ft', 'D_min_ft']  # Defines list. Sets column labels for
                                # DataFrame.

                                dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, srvy_yr2_list, strm_stat_list,
                                                   dpth_avg_list, dpth_max_list, dpth_min_list]  # Redefines list. With
                                # populated lists.

                                # DataFrame ----------------------------------------------------------------------------

                                dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array
                                # for operation.
                                dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array
                                # for DataFrame dimensional compatibility.

                                df_sed_thck = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl, 'SEDIMENT THICKNESS',
                                                               0)  # Defines DataFrame. Calls function. Creates
                                # DataFrame of average sediment thickness results.

                                # EXPORT FILE --------------------------------------------------------------------------

                                fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Sediment_thickness']
                                # Defines list. Sets folder labels for directory to be made.

                                fl_name = '/Sediment_thickness.csv'  # Defines variable as strIng. Sets name and
                                # extension of file for export.

                                export_file_to_directory(1, 'table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                         fl_name, 1, None, df_sed_thck, False,
                                                         'Sediment thickness table', 0)  # Creates directory and
                                # exports figure. Calls function.

                                # PLOT DATA ----------------------------------------------------------------------------

                                if Plt_dpth == 1:  # Conditional statement. Plots sediment thickness, by year, as a
                                    # function of distance upstream.

                                    df_srvy_yrs = slice_DataFrame_columns(df_sed_thck, 'Srvy_year1', 1, 'Survey years',
                                                                          0)  # Defines DataFrame. Calls function.
                                    # Slices DataFrame to yield survey years of present dataset.

                                    srvy_yrs = df_srvy_yrs.tolist()  # Defines list. Converts DataFrame to list.

                                    for x in srvy_yrs:  # Begins loop through list elements. Loops through survey
                                        # years.
                                        df_sed_thck_x = slice_DataFrame_rows('equals', df_sed_thck, 'Srvy_year1', x,
                                                                              'SEDIMENT THICKNESS', 0)  # Defines
                                        # DataFrame. Calls function. Slices DataFrame to yield sediment thickness data
                                        # by year.

                                        df_dpth_x = slice_DataFrame_columns(df_sed_thck_x, 'D_avg_ft', 0,
                                                                            'SEDIMENT THICKNESS', 0)  # Defines
                                        # DataFrame. Calls function. Slices DataFrame to yield sediment thickness data
                                        # by year.

                                        df_strm_stat_x = slice_DataFrame_columns(df_sed_thck_x, 'Strm_stat', 0,
                                                                                 'STREAM STATION', 0)  # Defines
                                        # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                                        df_dpth_x = df_dpth_x.astype(float)  # Redefines DataFrame. Converts values to
                                        # float.

                                        srvy_yr = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year1', 'Survey year',
                                                                       0)  # Defines variable. Calls function. Slices
                                        # DataFrame to yield suvey year of present dataset.

                                        clr1 = get_plot_feature_by_year(srvy_yr, tol_mtd, 0)  # Defines variable. Calls
                                        # function. Sets plot color.
                                        mrkr1 = get_plot_feature_by_year(srvy_yr, mrkrs, 1)  # Defines variable. Calls
                                        # function. Sets plot marker type.

                                        title = 'Sediment thickness evolution: Trout Creek'  # Defines string. Sets
                                        # plot title.

                                        plot_lines(1, 6, fig_sz, df_strm_stat_x, df_dpth_x, srvy_yr, clr1, mrkr1,
                                                   mrkr_sz, lin_wdth, alpha, 1, lctn, mrkr_scl, frm_alpha, lbl_spcng,
                                                   fntsz_tcks, 'River station', fntsz_ax, lbl_pd,
                                                   'Sediment accumulation between surveys (ft)', title, 1, 1)
                                        # Creates plot. Calls function.

                                    # Process regions ------------------------------------------------------------------

                                    df_strm_stat = slice_DataFrame_columns(df_sed_thck, 'Strm_stat', 1,
                                                                           'STREAM STATION', 0)  # Defines DataFrame.
                                    # Calls function. Slices DataFrame to yield stream station data.
                                    strm_stat = df_strm_stat.tolist()  # Defines string. Converts DataFrame to list.

                                    max_dpth_avg = max(dpth_avg_list)  # Defines variable. Retrieves max average
                                    # sediment thickness.
                                    min_dpth_avg = min(dpth_avg_list)  # Defines variable. Retrieves min average
                                    # sediment thickness.

                                    clr2 = get_plot_feature_by_year('Shaded area', tol_mtd, 0)  # Defines variable.
                                    # Calls function. Sets plot color.

                                    plot_fill(6, 2, strm_stat, [0, 0], [max_dpth_avg, min_dpth_avg],
                                              ['Deposition', 'Erosion'], [clr2, '#BBBBBB'],
                                              alpha_fl, lctn, mrkr_scl, frm_alpha, lbl_spcng, 1, 5)  # Creates plot.
                                    # Calls function.

                                    # EXPORT FIGURE --------------------------------------------------------------------

                                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                    # Defines list. Sets folder labels for directory to be made.

                                    fig_name = '/D_' + str(srvy_yrs[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                    # variable as strIng. Sets name of figure for export.

                                    export_file_to_directory(1, 'figure', 3, fldr_lbls, opt_fldr,
                                                             'Directories named: ', fig_name, 6, 'pdf', None, None,
                                                             'Average sediment thickness plot', 0)  # Creates directory
                                    # and exports figure. Calls function.

                    # ==================================================================================================
                    # PART 3C. DATA ANALYSIS - SEDIMENT DISTRIBUTION ---------------------------------------------------

                    if Sed_dist == 1:
                        # interpolate data
                        # SELECT CALCULATION RANGE -------------------------------------------------------------------------

                        start, end, srvy_lngth_shrd = select_coincident_x_range('dataframe', df_offst1, df_offst2,
                                                                                ' ft', 0)  # Defines variales. Calls
                        # function. Identifies shared x values of individual datasets.

                        # REINTERPOLATE DATASETS -----------------------------------------------------------------------

                        offsts_int1, elvtns_int1, x_rng_int1, num_smpls_int1 = interpolate_cross_section('limits',
                                                                                                         df_offst1,
                                                                                                         df_elvtn1,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)
                        # Defines variables and interpolates cross-section. Calls function.
                        offsts_int2, elvtns_int2, x_rng_int2, num_smpls_int2 = interpolate_cross_section('limits',
                                                                                                         df_offst2,
                                                                                                         df_elvtn2,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)
                        # Defines variables and interpolates cross-section. Calls function.

                        # PLOT DATA ----------------------------------------------------------------------------------------

                        if Plt_dbl_reintrp2 == 1:  # Conditional statement. Plots reinterpolated cross-sections as
                            # subsequent pairs.
                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd,
                                                            0)  # Defines variable. Calls function. Sets
                            # plot color.
                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs,
                                                             1)  # Defines variable. Calls function. Sets
                            # plot marker type.
                            clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd,
                                                            0)  # Defines variable. Calls function. Sets
                            # plot color.
                            mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs,
                                                             0)  # Defines variable. Calls function. Sets
                            # plot marker type.

                            title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                    ' reinterpolated surveys'  # Defines string. Sets title of plot.  # Defines string.
                            # Sets plot title.

                            plot_lines(2, 5, fig_sz, [offsts_int1, offsts_int2], [elvtns_int1, elvtns_int2],
                                       [srvy_yr1, srvy_yr2], [clr1, clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, 0,
                                       lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)',
                                       fntsz_ax, lbl_pd, 'Surface elevation (ft)', title, 0, 1)  # Creates plot. Calls
                            # function.

                        # select stream banks
                        df_bnks_srvy1 = slice_DataFrame_rows('equals', df_srvy1, 'Strm_bnks', 'Bank', 'STREAM BANKS',0)  # Defines DataFrame. Calls
                        # df_bnks_srvy2 = slice_DataFrame_rows('equals', df_srvy2, 'Strm_bnks', 'Bank', 'STREAM BANKS',0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield singular survey data.

                        bnk_R_srvy1 = slice_DataFrame_cell(df_bnks_srvy1, 0, 'Offset_ft', 'Offset',0)  # Defines variable. Calls function. Slices
                        bnk_r_srvy1 = slice_DataFrame_cell(df_bnks_srvy1, 0, 'Elv_geo_ft', 'Elevation',
                                                           0)  # Defines variable. Calls function. Slices
                        # bnk_R_srvy2 = slice_DataFrame_cell(df_bnks_srvy2, 0, 'Offset_ft', 'Offset',0)  # Defines variable. Calls function. Slices
                        # DataFrame to yield range number of present dataset.
                        # bnk_r_srvy2 = slice_DataFrame_cell(df_bnks_srvy1, 0, 'Elv_geo_ft', 'Elevation',
                        #                                    0)  # Defines variable. Calls function. Slices
                        bnk_L_srvy1 = slice_DataFrame_cell(df_bnks_srvy1, -1, 'Offset_ft', 'Offset',0)  # Defines variable. Calls function. Slices
                        bnk_l_srvy1 = slice_DataFrame_cell(df_bnks_srvy1, -1, 'Elv_geo_ft', 'Elevation',0)  # Defines variable. Calls function. Slices
                        # bnk_L_srvy2 = slice_DataFrame_cell(df_bnks_srvy2, -1, 'Offset_ft', 'Offset',0)  # Defines variable. Calls function. Slices
                        # DataFrame to yield range number of present dataset.

                        # select floodplains + hillslopes

                        df_fldplnR1 = slice_DataFrame_rows('less than', df_srvy1, 'Offset_ft', bnk_R_srvy1,'STREAM BANKS', 0)  # Defines DataFrame. Calls
                        # df_fldplnR2 = slice_DataFrame_rows('less than', df_srvy2, 'Offset_ft', bnk_R_srvy1,'STREAM BANKS', 0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield singular survey data.
                        df_fldplnL1 = slice_DataFrame_rows('more than', df_srvy1, 'Offset_ft', bnk_L_srvy1, 'STREAM BANKS', 0)  # Defines DataFrame. Calls
                        # df_fldplnL2 = slice_DataFrame_rows('more than', df_srvy2, 'Offset_ft', bnk_L_srvy1, 'STREAM BANKS', 0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield singular survey data.

                        # select floodhill offsets and elevations

                        df_offstR1 = slice_DataFrame_columns(df_fldplnR1, 'Offset_ft', 0, 'OFFSET', 0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey offsets of present dataset.
                        offstR1 = df_offstR1.to_numpy()
                        offstR1 = np.append(offstR1, bnk_R_srvy1)
                        # offstR1 = offstR1 - bnk_R_srvy1
                        df_elvtnR1 = slice_DataFrame_columns(df_fldplnR1, 'Elv_geo_ft', 0, 'ELEVATION', 0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey elevations of present dataset.
                        elvtnR1 = df_elvtnR1.to_numpy()
                        elvtnR1 = np.append(elvtnR1, bnk_r_srvy1)


                        df_offstL1 = slice_DataFrame_columns(df_fldplnL1, 'Offset_ft', 0, 'OFFSET',0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey offsets of present dataset.
                        offstL1 = df_offstL1.to_numpy()
                        offstL1=np.flip(offstL1)
                        offstL1 = np.append(offstL1, bnk_L_srvy1)
                        offstL1=np.flip(offstL1)
                        df_elvtnL1 = slice_DataFrame_columns(df_fldplnL1, 'Elv_geo_ft', 0, 'ELEVATION',0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey elevations of present dataset.
                        elvtnL1 = df_elvtnL1.to_numpy()
                        elvtnL1 = np.flip(elvtnL1)
                        elvtnL1 = np.append(elvtnL1, bnk_l_srvy1)
                        elvtnL1 = np.flip(elvtnL1)
                        # df_offstR2 = slice_DataFrame_columns(df_fldplnR2, 'Offset_ft', 0, 'OFFSET',
                        #                                      0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey offsets of present dataset.
                        # offstR2 = df_offstR2.to_numpy()
                        # offstR2 = np.append(offstR2, bnk_R_srvy2)
                        # offstR2 = offstR2 - bnk_R_srvy2
                        # df_elvtnR2 = slice_DataFrame_columns(df_fldplnR2, 'Elv_geo_ft', 0, 'ELEVATION',
                        #                                      0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey elevations of present dataset.

                        # df_offstL2 = slice_DataFrame_columns(df_fldplnL2, 'Offset_ft', 0, 'OFFSET',
                        #                                      0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey offsets of present dataset.
                        # df_elvtnL2 = slice_DataFrame_columns(df_fldplnL2, 'Elv_geo_ft', 0, 'ELEVATION',
                        #                                      0)  # Defines DataFrame. Calls
                        # function. Slices DataFrame to yield survey elevations of present dataset.

                        # select coincident ranges
                        # SELECT CALCULATION RANGE -------------------------------------------------------------------------

                        start, end, srvy_lngth_shrd = select_coincident_x_range('dataframe', offstR1, df_offst2,
                                                                                ' ft', 1)  # Defines variales. Calls
                        # function. Identifies shared x values of individual datasets.

                        # REINTERPOLATE DATASETS -----------------------------------------------------------------------

                        offsts_intR1, elvtns_intR1, x_rng_intR1, num_smpls_intR1 = interpolate_cross_section('limits',
                                                                                                         offstR1,
                                                                                                         elvtnR1,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)
                        # Defines variables and interpolates cross-section. Calls function.
                        offsts_intR2, elvtns_intR2, x_rng_intR2, num_smpls_intR2 = interpolate_cross_section('limits',
                                                                                                         df_offst2,
                                                                                                         df_elvtn2,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)
                        # # Defines variables and interpolates cross-section. Calls function.
                        start, end, srvy_lngth_shrd = select_coincident_x_range('dataframe', offstL1, df_offst2,
                                                                                ' ft', 0)  # Defines variales. Calls
                        # function. Identifies shared x values of individual datasets.

                        # REINTERPOLATE DATASETS -----------------------------------------------------------------------

                        offsts_intL1, elvtns_intL1, x_rng_intL1, num_smpls_intL1 = interpolate_cross_section('limits',
                                                                                                         offstL1,
                                                                                                         elvtnL1,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)
                        # Defines variables and interpolates cross-section. Calls function.
                        offsts_intL2, elvtns_intL2, x_rng_intL2, num_smpls_intL2 = interpolate_cross_section('limits',
                                                                                                         df_offst2,
                                                                                                         df_elvtn2,
                                                                                                         start, end,
                                                                                                         'linear',
                                                                                                         0.01, 2, 0)

                        # PLOT DATA ----------------------------------------------------------------------------------------

                        if Plt_dbl_reintrp3 == 1:  # Conditional statement. Plots reinterpolated cross-sections as
                            # subsequent pairs.
                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                            # plot color.
                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 1)  # Defines variable. Calls function. Sets
                            # plot marker type.
                            clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 0)  # Defines variable. Calls function. Sets
                            # plot color.
                            mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 0)  # Defines variable. Calls function. Sets
                            # plot marker type.

                            title = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                    ' reinterpolated surveys, no channel'  # Defines string. Sets title of plot.  # Defines string.
                            # Sets plot title.

                            plot_lines(4, 5, fig_sz, [offsts_intR1, offsts_intR2, offsts_intL1,offsts_intL2], [elvtns_intR1, elvtns_intR2, elvtns_intL1,elvtns_intL2],
                                       [srvy_yr1, srvy_yr2,None,None], [clr1, clr2,clr1,clr2], [' ', ' ',' ', ' '], mrkr_sz, lin_wdth, alpha, 0,
                                       lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)',
                                       fntsz_ax, lbl_pd, 'Surface elevation (ft)', title, 0, 5)  # Creates plot. Calls
                            # function.

                        # SELECT COORDINATE PAIRS ----------------------------------------------------------------------

                        offsts_int1 = np.append(offsts_intR1, offsts_intL1)
                        elvtns_int1 = np.append(elvtns_intR1, elvtns_intL1)
                        offsts_int2 = np.append(offsts_intR2, offsts_intL2)
                        elvtns_int2 = np.append(elvtns_intR2, elvtns_intL2)

                        end = end + 0.01  # Defines variable. Resets end of range so array includes final input value.

                        index1 = np.arange(0, len(offsts_int1), 1, dtype=int)  # Defines array. Creates array of
                        # index values for looped calculation.

                        for x in index1:  # Begins loop through array. Loops through coordinate indices.
                            offst1, elvtn1_top, elvtn1_btm = get_coordinate_pairs('depth', x, None, offsts_int1,
                                                                                  elvtns_int1, elvtns_int2, 0)
                            # Defines variables. Calls function.


                            # CALCULATE SEDIMENT THICKNESS -------------------------------------------------------------

                            # At a point -------------------------------------------------------------------------------

                            dpth1, prcs1 = sediment_thickness('depth', elvtn1_top, elvtn1_btm, None, None,
                                                              'Sediment thickness: ', 0)  # Defines variables. Calls
                            # function.
                            # Averaged over cross-section --------------------------------------------------------------

                            # Create empty list
                            if x == index1[0]:  # Conditional statement. Executes for first coordinate only.
                                dpth1_list = []  # Defines list. Empty for looped population.
                                offstR_list = []

                            # Populate list
                            dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_list,
                                                              'New list appended: ', 0)  # Redefines list. Calls
                            # function.
                            offstR_list = create_appended_list(offst1, 'Sediment thickness', offstR_list,
                                                              'New list appended: ', 0)  # Redefines list. Calls
                            if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.
                                dpth_avg = np.sum(dpth1_list) / x  # Defines variable. Calculates average sediment
                                # thickness.

                                dpth_max = max(dpth1_list)  # Defines variable. Retrieves max value from list.
                                dpth_min = min(dpth1_list)  # Defines variable. Retrieves min value from list.
                                index2 = offstR_list.index(bnk_R_srvy1)
                                offstR1_list = offstR_list[0: index2]

                                dpthR1_list=dpth1_list[0:index2]
                                index3 = offstR_list.index(bnk_L_srvy1)
                                offstL1_list = offstR_list[index3:-1]

                                dpthL1_list = dpth1_list[index3:-1]
                                if Plt_sed_dist == 1:
                                    plot_lines(2, 7, fig_sz, [offstR1_list,offstL1_list], [dpthR1_list,dpthL1_list],
                                               [None,None], ['cyan','cyan'], [' ',' '], mrkr_sz, lin_wdth, alpha, 0,
                                               lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)',
                                               fntsz_ax, lbl_pd, 'Sediment thickness (ft)', None, 1,
                                               1)  # Creates plot. Calls

                                    # Process regions ------------------------------------------------------------------

                                    max_dpth_avg = max(dpth1_list)  # Defines variable. Retrieves max average
                                    # sediment thickness.
                                    min_dpth_avg = min(dpth1_list)  # Defines variable. Retrieves min average
                                    # sediment thickness.

                                    clr2 = get_plot_feature_by_year('Shaded area', tol_mtd, 0)  # Defines variable.
                                    # Calls function. Sets plot color.

                                    plot_fill(7, 2, offstR_list, [0, 0], [max_dpth_avg, min_dpth_avg],
                                              ['Deposition', 'Erosion'], [clr2, '#BBBBBB'],
                                              alpha_fl, lctn, mrkr_scl, frm_alpha, lbl_spcng, 1, 10)  # Creates plot.
                                    # Calls function.

