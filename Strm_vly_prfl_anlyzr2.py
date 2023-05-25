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

import time, os, sys, math
# Imports "Time and access conversions". Enables time related functions.
# Imports "Miscellaneous operating system interfaces" & "System specific parameters and functions". Enables operating
# system dependent functionality.
# Imports "Mathematical functions".
import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sc, geopandas as gpd
# Imports "Python data analysis library" with alias. Enables use of DataFrames.
# Imports numerical mathematics library and a scientific mathematics library, with alias.
# Imports a plotting interface with alias.
# Imports a geographic data libray with alias. Enables spatial operations.
import Functions as fn  # Imports program with alias.
from Functions import *  # Imports all functions from outside program.

# SELECT OPERATIONS ----------------------------------------------------------------------------------------------------

# Single cross-section analysis ----------------------------------------------------------------------------------------

Sngl = 0  # Defines variable as integer. Sets binary toggle.

# Plot single cross-section
Plt_sngl = 0  # Defines variable as integer. Sets binary toggle.
# Plot all cross-sections
Plt_all = 0 # Defines variable as integer. Sets binary toggle.

# Calculate coordinate geometry
Crdnts = 0  # Defines variable as integer. Sets binary toggle.

# Plot measurement coordinates
Plt_crdnts = 1  # Defines variable as integer. Sets binary toggle.

# Dual cross-sections analysis -----------------------------------------------------------------------------------------

Dbl = 1  # Defines variable as integer. Sets binary toggle.

# Plot dual cross-sections
Plt_dbl = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual interpolated cross-sections
Plt_intrp = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual re-interpolated cross-sections
Plt_reintrp = 0  # Defines variable as integer. Sets binary toggle.

# Calculate sediment thickness
Dpth = 1  # Defines variable as integer. Sets binary toggle.

# Plot sediment thickness
Plt_dpth = 0  # Defines variable as integer. Sets binary toggle.
# Plot sedimentation rate
Plt_dpth_rt = 0  # Defines variable as integer. Sets binary toggle.
# Plot sediment thickness vs. drainage area
Plt_dpth_vs_wshd = 1  # Defines variable as integer. Sets binary toggle.
# Plot sediment thickness vs. transect width.
Plt_dpth_vs_vlly = 1  # Defines variable as integer. Sets binary toggle.

# SELECT INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Limits of analysis ---------------------------------------------------------------------------------------------------

rvr_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one river channel only.
rng_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one survey range only.
xtra_srvys = 0  # Defines variable as integer. Sets binary toggle. Analyzes extra survey data for range 11B (13).
rng_strt = 1  # Defines variable as integer. Sets start survey range number for analysis loop.
rng_end = 26  # Defines variable as integer. Sets end survey range number for analysis loop.

# Conversion factors ---------------------------------------------------------------------------------------------------

deg_to_rad = math.pi / 180  # Defines variable as float. Converts between degrees and radians.
ft_to_m = 3.281  # Defines variable as float. Converts between international feet meters.
in_to_ft = 12  # Defines variable as integer. Converts between inches and feet.
mi_to_km = 1.609  # Defines variable as float. Converts between miles and kilometers.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Name folders
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Create folders
lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. To enable looped folder creation.

for i in lvl1_fldrs:  # Begins loop through elements of list. Loops through paths.
    lvl = 1  # Defines variable as integer. For function input.

    create_folder(lvl, i)  # Creates folders. Calls function.

# ======================================================================================================================
# PART 2: CROSS-SECTIONAL ANALYSIS - SINGLE ----------------------------------------------------------------------------
# ======================================================================================================================

# ======================================================================================================================
# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Input file(s) --------------------------------------------------------------------------------------------------------

inpt_fl1 = inpt_fldr + '/Test_data.csv'  # Defines string. Sets file path to input file.

df_srvy_dt = csv_to_DataFrame(inpt_fl1, 'TEST DATA', 0)  # Defines DataFrame. Calls function. Uploads survey data.

inpt_fl2 = inpt_fldr + '/Drainage_areas.csv'  # Defines string. Sets file path to input file.

df_wshd_A_dt = csv_to_DataFrame(inpt_fl2, 'WATERSHED AREA DATA', 0)  # Defines DataFrame. Calls function. Uploads
# transect drainage area data.

# Establish spatial selection framework
if rng_nly == 1:  # Conditional statement. Executes lines if condition satisfied.
    rng_nums = [rng_strt]  # Defines list. One element to enable analyses of single survey range.
    rng_end = rng_strt  # Redefines variable as integer. For display.
elif rng_nly == 0:  # Conditional statement. Executes lines if condition satisfied.
    rng_nums = forward_range(rng_strt, rng_end, 1, 'Range numbers', 0)  # Defines array. Calls function. Sets loop
    # order by transect.

# Select transect dataset
for i in rng_nums:  # Establishes loop through array elements. Loops through transect numbers.
    df_rng = slice_DataFrame_rows('Equals', df_srvy_dt, 'Range_num', i, 'TRANSECT NUMBER', 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield singular range data.
    df_wshd_A = slice_DataFrame_rows('Equals', df_wshd_A_dt, 'Range_num', i, 'TRANSECT NUMBER', 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield singular range data.

    # Retrieve metadata
    chnl_name = slice_DataFrame_cell('String', 0, None, df_rng, 0, 'Chnl_name', 'Stream channel', 0)  # Defines
    # variable. Calls function. Slices DataFrame to yield stream channel name of present dataset.

    chnl_abrv = slice_DataFrame_cell('String', 0, None, df_rng, 0, 'Chnl_abrv', 'Stream channel', 0)  # Defines
    # variable. Calls function. Slices DataFrame to yield stream channel abbreviation of present dataset.

    rng_name1 = slice_DataFrame_cell('String', 0, None, df_rng, 0, 'Srvy_range', 'Range', 0)  # Defines variable. Calls
    # function. Slices DataFrame to yield transect name of present dataset.

    strm_stat1, strm_stat1_m = slice_DataFrame_cell('Integer', 1, 1/ft_to_m,  df_rng, 0, 'Srvy_stat', 'Stream station',
                                                    0)  # Defines variable. Calls function. Slices DataFrame to yield
    # survey station of transect on reach.

    wshd_A, wshd_A_mi = slice_DataFrame_cell('Float', 1, (1/mi_to_km)**2, df_wshd_A, 0, 'Wshd_A_sqkm',
                                             'Transect drainage area', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield drainage area of transect on reach.

    srvy_nums1 = slice_DataFrame_columns('List', 'Integer', df_rng, 'Srvy_num', 1, 'SURVEY NUMBERS', 0)  # Defines
    # list. Calls function. Slices DataFrame to yield survey numbers of present dataset.

    if xtra_srvys == 1:  # Conditional statement. Modifies survey years under analysis. For transect 11B (13) with
        # extra survey years compared to all other ranges.
        pass  # Pass command. Moves on to next line.
    elif xtra_srvys == 0:  # Conditional statement. Modifies survey years under analysis.
        if i == 13:  # Conditional statement.
            srvy_nums1.remove(5)  # Redefines list. Removes survey inconsistent survey year.
            srvy_nums1.remove(4)  # Redefines list. Removes survey inconsistent survey year.

    srvy_nums_max = max(srvy_nums1)  # Defines variable. Selects maximum survey number.

    # Select survey dataset
    for j in srvy_nums1:  # Establishes loop through array elements. Loops through survey numbers.
        df_srvy1 = slice_DataFrame_rows('Equals', df_rng, 'Srvy_num', j, 'SURVEY NUMBER', 0)  # Defines DataFrame.
        # Calls function. Slices DataFrame to yield singular survey data.

        # Retrieve metadata
        srvy_yr1 = slice_DataFrame_cell('Integer', 0, None, df_srvy1, 0, 'Srvy_year', 'Survey year', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey year of present dataset.
        srvy_dt1 = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Srvy_date', 'Survey date', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey date of present dataset.
        srvy_typ1 = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Srvy_type', 'Survey type', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey type of present dataset.
        # Select survey measurements
        df_offst1 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy1, 'Offset_ft', 0, 'OFFSET', 0)  # Defines
        # DataFrame. Calls function. Slices DataFrame to yield survey offsets of present dataset.
        df_elvtn1 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy1, 'Elv_geo_ft', 0, 'ELEVATION', 0)  # Defines
        # DataFrame. Calls function. Slices DataFrame to yield survey elevations of present dataset.

        # Retrieve metadata
        offst_min1 = min_value_DataFrame('Float', df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
        # DataFrame to yield first offset of present dataset.
        offst_max1 = max_value_DataFrame('Float', df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
        # DataFrame to yield last offset of present dataset.
        elvtn_min1 = min_value_DataFrame('Float', df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield lowest elevation of present dataset.
        elvtn_max1 = max_value_DataFrame('Float', df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield highest elevation of present dataset.
        num_smpls1 = df_srvy1.shape[0]  # Defines variable. Returns dimensionality of DataFrame.
        brng_r_dir = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_R_dir',
                                          'Bearing reference direction: ', 0)   # Defines variable. Calls function.
        # Slices DataFrame to yield bearing reference direction of present dataset.
        brng_angl = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'Brng_A', 'Bearing angle: ', 0)   # Defines
        # variable. Calls function. Slices DataFrame to yield bearing angle of present dataset.
        brng_a_dir = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_A_dir', 'Bearing angle direction: ', 0)
        # Defines variable. Calls function. Slices DataFrame to yield bearing angle direction of present dataset.
        brng_fnctl = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_fnctl', 'Functional bearing: ', 0)
        # Defines variable. Calls function. Slices DataFrame to yield functional bearing directions of present dataset.
        rng_lngth1 = offst_max1 - offst_min1  # Defines variable. Calculates survey length.
        rng_lngth1_m = rng_lngth1 / ft_to_m  # Defines variable. Converts to meters.
        srvy_rlf1 = elvtn_max1 - elvtn_min1  # Defines variable. Calculates survey relief.
        srvy_rlf1_m = srvy_rlf1 / ft_to_m  # Defines variable. Converts to meters.

        # DISPLAY DATA -------------------------------------------------------------------------------------------------

        if Sngl == 1:  # Conditional statement. Executes analysis of single cross-section.
            # Metadata -------------------------------------------------------------------------------------------------

            print('==================================================')  # Displays objects.
            print('\033[1m' + 'Stream channel: ' + '\033[0m' + str(chnl_name))  # Displays objects.
            print('\033[1m' + 'Field transect: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
            # objects.
            print('\033[1m' + 'Transect bearing: ' + '\033[0m' + str(brng_r_dir) + str(brng_angl) + str(brng_a_dir) +
                  ' (' +str(brng_fnctl) +')')  # Displays objects.
            print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1) + ' ft' +
                  ' (' + str('%.0f' % strm_stat1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Drainage area: ' + '\033[0m' + str('%.0f' % wshd_A_mi) + ' sqmi' +
                  ' (' + str('%.0f' % wshd_A) + ' sqkm)')  # Displays objects.
            print('\033[1m' + 'Transect survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(j) + ' of ' +
                  str(srvy_nums_max) + ')')  # Displays objects.
            print('\033[1m' + 'Survey type: ' + '\033[0m' + str(srvy_typ1))  # Displays objects.
            print('\033[1m' + 'Survey date(s): ' + '\033[0m' + str(srvy_dt1))  # Displays objects.
            print('\033[1m' + 'Survey length: ' + '\033[0m' + str('%.2f' % rng_lngth1) + ' ft' +
                  ' (' + str('%.0f' % rng_lngth1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Survey relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' ft' +
                  ' (' + str('%.0f' % srvy_rlf1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.
            breakpoint()
            # Cross-section --------------------------------------------------------------------------------------------

            if Plt_sngl == 1:  # Conditional statement. Plots single cross-section.
                if j != 0:  # Conditional statement.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color ', 1)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker ', 1)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')' + ' ' + str(srvy_yr1) + ' survey '
                    # Defines string. Sets plot title.

                    plot_lines(1, 1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, fn.mrkr_sz[0],
                               fn.lin_wdth[0], fn.lin_styl[0], fn.alpha[0], 0, fn.lctn, fn.mrkr_scl, fn.alpha[1],
                               fn.lbl_spcng, 0, fn.fntsz[1], 'Survey offset (ft)', fn.fntsz[0], fn.lbl_pd,
                               'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Single', '/' + chnl_name]
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '_' + str(srvy_yr1) + '.pdf'  # Defines variable
                    # as strIng. Sets name of figure for export.

                    export_file_to_directory(1, 'Figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1,
                                             'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)  # Creates
                    # directory and exports figure. Calls function.

            # All cross-sections ---------------------------------------------------------------------------------------

            if Plt_all == 1:  # Conditional statement. Plots all cross-sections on transect.
                if j != 0:  # Conditional statement.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')'  # Defines string. Sets plot title.

                    plot_lines(1, 2, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, fn.mrkr_sz[0],
                               fn.lin_wdth[0], fn.lin_styl[0], fn.alpha[0], 1, fn.lctn, fn.mrkr_scl, fn.frm_alpha,
                               fn.lbl_spcng, 0, fn.fntsz[-1], 'Survey offset (ft)', fn.fntsz[0], fn.lbl_pd,
                               'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                    # Export data
                    if j == srvy_nums1[-1]:  # Conditional statement. Exports only when final cross-section has been
                        # plotted.
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/All', '/' + chnl_name]
                        # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '.pdf'  # Defines variable as strIng. Sets name of figure for
                        # export.

                        export_file_to_directory(1, 'Figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 2, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                        # Creates directory and exports figure. Calls function.

            # ==========================================================================================================
            # DIGITIZE SURVEY MEASUREMENTS -----------------------------------------------------------------------------

            if Crdnts == 1:  # Conditional statement. Digitizes survey measurements.
                if srvy_typ1 != 'Lidar':  # Conditional statement. Performs calculations for field data only.
                    # SELECT BENCHMARK DATA ----------------------------------------------------------------------------

                    # Coordinates --------------------------------------------------------------------------------------

                    BM1_e = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM1_east_m',
                                                 'Benchmark 1 Easting (m): ', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield easting coordinate of first benchmark of present dataset.
                    BM1_n = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM1_nrth_m',
                                                 'Benchmark 1 Northing (m): ', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield northing coordinate of first benchmark of present dataset.
                    BM2_e = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM2_east_m',
                                                 'Benchmark 2 Easting (m): ', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield easting coordinate of second benchmark of present dataset.
                    BM2_n = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM2_nrth_m',
                                                 'Benchmark 2 Northing (m): ', 0)  # Defines variable. Calls function.
                    # Slices DataFrame to yield northing coordinate of second benchmark of present dataset.

                    # Position -----------------------------------------------------------------------------------------

                    BM1_off = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM1_off_tp',
                                                   'Benchmark 1 top offset (ft): ', 0)  # Defines variable. Calls
                    # function. Slices DataFrame to yield offset of first benchmark of present dataset.
                    BM2_off = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM2_off_tp',
                                                   'Benchmark 2 top offset (ft): ', 0)  # Defines variable. Calls
                    # function. Slices DataFrame to yield offset of second benchmark of present dataset.
                    BM1_crd_off = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'BM1_crd_off',
                                                       'Benchmark 1 GPS top offset (ft): ', 0)  # Defines variable.
                    # Calls function. Slices DataFrame to yield GPS offset of first benchmark of present dataset.

                    # CALCULATE TRANSECT ORIENTATION -------------------------------------------------------------------

                    sin, cos = transect_orientation(BM1_e, BM2_e, BM1_n, BM2_n, brng_r_dir, brng_a_dir, brng_angl,
                                                    brng_fnctl, 'Directional data', 1)  # Defines variables. Calls
                    # function. Calculates trigonometric components of transect from GPS points.

                    # TRANSFORM MEASUREMENT OFFSETS --------------------------------------------------------------------
                    if BM1_off == BM1_crd_off:  # Conditonal statement. Selects standard to transform offsets.
                        df_offst1_shft = df_offst1 - BM1_off  # Defines DataFrame. Shifts measurement offsets by
                        # benchmark position.
                    else:  # Conditional statement.
                        df_offst1_shft = df_offst1 - BM1_crd_off  # Defines DataFrame. Shifts measurement offsets by
                        # benchmark position.
                    df_offst1_shft_m = df_offst1_shft / ft_to_m  # Defines DataFrame. Converts feet to meters.

                    # CALCULATE COORDINATES ----------------------------------------------------------------------------

                    # Directional offsets ------------------------------------------------------------------------------

                    df_offsts_e = cos * df_offst1_shft_m  # Defines DataFrame. Calculates measurement easting offsets.
                    df_offsts_n = sin * df_offst1_shft_m  # Defines DataFrame. Calculates measurement northing offsets.

                    # Coordinates --------------------------------------------------------------------------------------

                    df_e = BM1_e + df_offsts_e  # Defines DataFrame. Calculates measurement easting.
                    df_e = df_e.rename('Easting_m')  # Redefines DataFrame. Renames column.
                    df_n = BM1_n + df_offsts_n  # Defines DataFrame. Calculates measurement northing.
                    df_n = df_n.rename('Northing_m')  # Redefines DataFrame. Renames column.

                    # CALCULATE ERROR ----------------------------------------------------------------------------------

                    crd1_e = slice_DataFrame_cell('Float', 0, None, df_e, 0, None, 'Measurement 1 Easting (m): ', 1)
                    # Defines variable. Calls function. Slices DataFrame to yield easting coordinate of first
                    # measurement of present dataset.
                    crd1_n = slice_DataFrame_cell('Float', 0, None, df_n, 0, None, 'Measurement 1 Northing (m): ', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield northing coordinate of first
                    # measurement of present dataset.
                    crd2_e = slice_DataFrame_cell('Float', 0, None, df_e, -1, None, 'Measurement 2 Easting (m): ', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield easting coordinate of last
                    # measurement of present dataset.
                    crd2_n = slice_DataFrame_cell('Float', 0, None, df_n, -1, None, 'Measurement 2 Northing (m): ', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield northing coordinate of last
                    # measurement of present dataset.

                    lgnth_prcnt_dff = coordinate_error(crd1_e, crd2_e, crd1_n, crd2_n, rng_lngth1_m, 1)  # Defines
                    # variable. Calculates percent difference between field measured and GPS calculated transect
                    # lengths.

                    # UPDATE FILE --------------------------------------------------------------------------------------

                    df_srvy1 = pd.concat([df_srvy1, df_e, df_n], axis=1)  # Redefines DataFrame. Concatenates
                    # coordinates to survey DataFrame.

                    # DISPLAY DATA -------------------------------------------------------------------------------------

                    if Plt_crdnts == 1:  # Conditional statement. Plots all measurement coordinates on transect.
                        plot_scatter(3, fn.fig_sz, df_e, df_n, 'Predicted', fn.tol_mtd[6], fn.tol_mtd[6], fn.mrkrs[3],
                                     fn.mrkr_sz[0], fn.lin_wdth[1], fn.alpha[0], 0, fn.lctn, fn.mrkr_scl, fn.alpha[1],
                                     fn.lbl_spcng, 'equal', 'box', fn.fntsz[1], fn.fntsz[0], fn.lbl_pd, 'Easting (m)',
                                     'Northing (m)', 'Coordinates', 1, 1)  # Creates plot. Calls
                        # function.
                        if j == srvy_nums1[-1]:  # Conditional statement. Plots benchmark GPS coordinates.
                            plot_scatter(3, fn.fig_sz, BM1_e, BM1_n, None, fn.tol_mtd[1], fn.tol_mtd[0], fn.mrkrs[3],
                                         fn.mrkr_sz[0], fn.lin_wdth[1], fn.alpha[2], 0, fn.lctn, fn.mrkr_scl,
                                         fn.alpha[1], fn.lbl_spcng, 'equal', 'box', fn.fntsz[1], fn.fntsz[0],
                                         fn.lbl_pd, 'Easting (m)', 'Northing (m)', 'Coordinates', 1, 1)  # Creates
                            # plot. Calls function.
                            plot_scatter(3, fn.fig_sz, BM2_e, BM2_n, 'Original gps', fn.tol_mtd[1], fn.tol_mtd[0],
                                         fn.mrkrs[3], fn.mrkr_sz[0], fn.lin_wdth[1], fn.alpha[2], 0, fn.lctn,
                                         fn.mrkr_scl, fn.alpha[1], fn.lbl_spcng, 'equal', 'box', fn.fntsz[1],
                                         fn.fntsz[0], fn.lbl_pd, 'Easting (m)', 'Northing (m)', 'Coordinates', 1, 1)
                            # Creates plot. Calls function.

                    # DIGITIZE COORDINATES -----------------------------------------------------------------------------

                    gdf_srvy = gpd.GeoDataFrame(df_srvy1, geometry=gpd.points_from_xy(df_srvy1.Easting_m,
                                                df_srvy1.Northing_m), crs='EPSG:26915')  # Defines GeoDataFrame.
                    # Creates GIS layer from DataFrame and coordinate geometry.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Geographic_data', '/Cross_sections', '/Points',
                                 '/' + chnl_name ]  # Defines list. Sets folder labels for directory to be made.

                    lyr_name = 'R_' + str(rng_name1) + '_'+ str(srvy_yr1)  # Defines variable as string. Sets name of
                    # layer for export.

                    gpckg = '/' + chnl_abrv + '_survey_points.gpkg'  # Defines variable as string. Sets name and
                    # location of GeoPackage.

                    export_file_to_directory(1, 'Geospatial', 5, fldr_lbls, opt_fldr, 'Directiories named: ', lyr_name,
                                             None, None, None, False, 'GIS layer', gdf_srvy, gpckg, 'GPKG', 0)
                    # Creates directory and exports figure. Calls function.

        # ==============================================================================================================
        # PART 3: CROSS-SECTIONAL ANALYSIS - DOUBLE --------------------------------------------------------------------
        # ==============================================================================================================

        # SELECT DATA --------------------------------------------------------------------------------------------------

        if Dbl == 1:  # Conditional statement. Executes analysis of cross-sections as pairs.
            if j > 1:  # Conditional statement. Performs operations for all but the last survey.
                index1 = srvy_nums1.index(j)  # Defines variable. Retrieves index of survey number from list. Enables
                # selection of second survey.

                index1 = index1 + 1  # Redefines variable. Retrieves index for second dataset selection.

                k = srvy_nums1[index1]  # Defines variable as integer. Allows for selection of second dataset.

                # Select second survey dataset
                df_srvy2 = slice_DataFrame_rows('Equals', df_rng, 'Srvy_num', k, 'SURVEY NUMBER', 0)  # Defines
                # DataFrame. Calls function. Slices DataFrame to yield singular survey data.

                # Retrieve metadata
                srvy_yr2 = slice_DataFrame_cell('Integer', 0, None, df_srvy2, 0, 'Srvy_year', 'Survey year', 0)
                # Defines variable. Calls function. Slices DataFrame to yield survey year of present dataset.
                srvy_dt2 = slice_DataFrame_cell('String', 0, None, df_srvy2, 0, 'Srvy_date', 'Survey date', 0)
                # Defines variable. Calls function. Slices DataFrame to yield survey date of present dataset.
                srvy_typ2 = slice_DataFrame_cell('String', 0, None, df_srvy2, 0, 'Srvy_type', 'Survey type', 0)
                # Defines variable. Calls function. Slices DataFrame to yield survey type of present dataset.
                # Select survey measurements
                df_offst2 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy2, 'Offset_ft', 0, 'OFFSET', 0)
                # Defines DataFrame. Calls function. Slices DataFrame to yield survey offsets of present dataset.
                df_elvtn2 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy2, 'Elv_geo_ft', 0, 'ELEVATION', 0)
                # Defines DataFrame. Calls function. Slices DataFrame to yield survey elevations of present dataset.
                # Retrieve metadata
                offst_min2 = min_value_DataFrame('Float', df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                # Slices DataFrame to yield first offset of present dataset.
                offst_max2 = max_value_DataFrame('Float', df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                # Slices DataFrame to yield last offset of present dataset.
                elvtn_min2 = min_value_DataFrame('Float', df_elvtn2, 'Elevation', 0)  # Defines variable. Calls
                # function. Slices DataFrame to yield lowest elevation of present dataset.
                elvtn_max2 = max_value_DataFrame('Float', df_elvtn2, 'Elevation', 0)  # Defines variable. Calls
                # function. Slices DataFrame to yield highest elevation of present dataset.
                num_smpls2 = df_srvy2.shape[0]  # Defines variable. Returns dimensionality of DataFrame.
                rng_lngth2 = offst_max2 - offst_min2  # Defines variable. Calculates survey length.
                rng_lngth2_m = rng_lngth2 / ft_to_m  # Defines variable. Converts to meters.
                srvy_rlf2 = elvtn_max2 - elvtn_min2  # Defines variable. Calculates survey relief.
                srvy_rlf2_m = srvy_rlf2 / ft_to_m  # Defines variable. Converts to meters.

                # DISPLAY DATA -----------------------------------------------------------------------------------------

                # Metadata ---------------------------------------------------------------------------------------------

                print('==================================================')  # Displays objects.
                print('\033[1m' + 'Stream channel: ' + '\033[0m' + str(chnl_name))  # Displays objects.
                print('\033[1m' + 'Field transect: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
                # objects.
                print(
                    '\033[1m' + 'Transect bearing: ' + '\033[0m' + str(brng_r_dir) + str(brng_angl) + str(brng_a_dir) +
                    ' (' + str(brng_fnctl) + ')')  # Displays objects.
                print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1) + ' ft' +
                      ' (' + str('%.0f' % strm_stat1_m) + ' m)')  # Displays objects.
                print('\033[1m' + 'Drainage area: ' + '\033[0m' + str('%.0f' % wshd_A_mi) + ' sqmi' +
                      ' (' + str('%.0f' % wshd_A) + ' sqkm)')  # Displays objects.
                print('\033[1m' + 'Transect survey: ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' +
                      str(j) + '–' + str(k) + ' of ' + str(srvy_nums_max) + ')')  # Displays objects.
                print('\033[1m' + 'Survey types: ' + '\033[0m' + str(srvy_typ1) + ' & ' + str(srvy_typ2))  # Displays
                # objects.
                print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))  # Displays
                # objects.
                print('\033[1m' + 'Survey lengths: ' + '\033[0m' + str('%.1f' % rng_lngth1) + ' & ' + str(
                    '%.1f' % rng_lngth2) +
                      ' ft' + ' (' + str('%.0f' % rng_lngth1_m) + ' & ' + str(
                    '%.0f' % rng_lngth2_m) + ' m)')  # Displays objects.
                print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' & ' +
                      str('%.1f' % srvy_rlf2) + ' ft' + ' (' + str('%.0f' % srvy_rlf1_m) + ' & ' + str(
                    '%.0f' % srvy_rlf2_m) + ' m)')  # Displays objects.
                print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1) + ' & ' + str(num_smpls2))
                # Displays objects.
                print('--------------------------------------------------')  # Displays objects.

                # Two cross-sections -------------------------------------------------------------------------------

                if Plt_dbl == 1:  # Conditional statement. Plots cross-sections as dual pairs.
                    clr1 = get_plot_feature_by_year(srvy_yr1, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.
                    clr2 = get_plot_feature_by_year(srvy_yr2, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr2 = get_plot_feature_by_year(srvy_yr2, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                            ' surveys'  # Defines string. Sets title of plot.

                    plot_lines(2, 3, fn.fig_sz, [df_offst2, df_offst1], [df_elvtn2, df_elvtn1], [srvy_yr2, srvy_yr1],
                               [clr2, clr1], [mrkr2, mrkr1], fn.mrkr_sz[0], fn.lin_wdth[0],
                               [fn.lin_styl[0], fn.lin_styl[0]], fn.alpha[0], fn.lctn, fn.mrkr_scl, fn.alpha[1],
                               fn.lbl_spcng, 0, fn.fntsz[-1], 'Survey offset (ft)', fntsz[0], fn.lbl_pd,
                               'Surface elevation (ft)', title, 1, 1)  # Creates plot. Calls function.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                 '/Measured']  # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                               str(srvy_yr2) + '.pdf'  # Defines variable as strIng. Sets name of figure for export.

                    export_file_to_directory(1, 'figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                             3, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                    # Creates directory and exports figure. Calls function.

                # INTERPOLATE DATA -------------------------------------------------------------------------------------

                df_off_i1, df_elv_i1, x_rng_i1 = interpolate_cross_section('DataFrame', df_offst1, df_elvtn1, None,
                                                                           None, 'linear', 0.01, 2, 0)  # Defines
                # variables. Calls function. Interpolates cross-section.

                df_off_i2, df_elv_i2, x_rng_i2 = interpolate_cross_section('DataFrame', df_offst2, df_elvtn2, None,
                                                                           None, 'linear', 0.01, 2, 0)  # Defines
                # variables. Calls function. Interpolates cross-section.

                # DISPLAY DATA -----------------------------------------------------------------------------------------

                # Two cross-sections (Interpolated) --------------------------------------------------------------------

                if Plt_intrp == 1:  # Conditional statement. Plots cross-sections as interpolated dual pairs.
                    clr1 = get_plot_feature_by_year(srvy_yr1, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.
                    clr2 = get_plot_feature_by_year(srvy_yr2, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr2 = get_plot_feature_by_year(srvy_yr2, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) +') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                            ' interpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                    # plot title.

                    plot_lines(2, 4, fn.fig_sz, [df_off_i2, df_off_i1], [df_elv_i2, df_elv_i1], [srvy_yr2, srvy_yr1],
                               [clr2, clr1], [mrkr2, mrkr1], fn.mrkr_sz[0], fn.lin_wdth[0], [lin_styl[0], lin_styl[0]],
                               fn.alpha[0], 0, fn.lctn, fn.mrkr_scl, fn.alpha[1], fn.lbl_spcng, fn.fntsz[1],
                               'Survey offset (ft)', fn.fntsz[0], fn.lbl_pd, 'Surface elevation (ft)', title, 1, 4)
                    # Creates plot. Calls function.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                 '/Interpolated']  # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                               str(srvy_yr2) + '_Interp' + '.pdf'  # Defines variable as strIng. Sets name of figure
                    # for export.

                    export_file_to_directory(1, 'figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                             4, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                    # Creates directory and exports figure. Calls function.

                # SELECT CALCULATION RANGE -----------------------------------------------------------------------------

                start, end, shrd_rng = select_coincident_x_range('dataframe', df_offst1, df_offst2, ' ft', 0)
                # Defines variables. Calls function. Identifies shared x values of individual datasets.

                shrd_rng_m = shrd_rng / ft_to_m  # Defines variable. Converts feet to meters.

                # REINTERPOLATE DATA -----------------------------------------------------------------------------------

                df_off_i1, df_elv_i1, x_rng_i1 = interpolate_cross_section('Limits', df_offst1, df_elvtn1, start, end,
                                                                           'linear', 0.01, 2, 0)  # Defines  variables.
                # Calls function. Interpolates cross-section.

                df_off_i2, df_elv_i2, x_rng_i2 = interpolate_cross_section('Limits', df_offst2, df_elvtn2, start, end,
                                                                           'linear', 0.01, 2, 0)  # Defines  variables.
                # Calls function. Interpolates cross-section.

                # DISPLAY DATA -----------------------------------------------------------------------------------------

                # Two cross-sections (reinterpolated) ------------------------------------------------------------------

                if Plt_reintrp == 1:  # Conditional statement. Plots cross-sections as reinterpolated dual pairs.
                    # subsequent pairs.
                    clr1 = get_plot_feature_by_year(srvy_yr1, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.
                    clr2 = get_plot_feature_by_year(srvy_yr2, fn.tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr2 = get_plot_feature_by_year(srvy_yr2, fn.mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                            ' reinterpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                    # plot title.

                    plot_lines(2, 5, fn.fig_sz, [df_off_i2, df_off_i1], [df_elv_i2, df_elv_i1], [srvy_yr2, srvy_yr1],
                               [clr2, clr1], [mrkr2, mrkr1], mrkr_sz[0], lin_wdth[0],
                               [lin_styl[0], lin_styl[0]], alpha[0], 0, lctn, mrkr_scl, alpha[1],
                               lbl_spcng, fntsz[1], 'Survey offset (ft)', fntsz[0], lbl_pd,
                               'Surface elevation (ft)', title, 0, 1)  # Creates plot. Calls function.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                 '/Reinterpolated']  # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                               str(srvy_yr2) + '_Reinterp' + '.pdf'  # Defines variable as strIng. Sets name of  figure
                    # for export.

                    export_file_to_directory(0, 'Figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                             5, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                    # Creates directory and exports figure. Calls function.

                # ======================================================================================================
                # CALCULATE SEDIMENTATION ------------------------------------------------------------------------------

                if Dpth == 1:  # Conditional statement. Calculates sediment thickness between cross-sections.
                    # SELECT COORDINATE PAIRS --------------------------------------------------------------------------

                    index1 = np.arange(0, len(df_off_i1), 1, dtype=int)  # Defines array. Creates array of index values
                    # for coordinate pair selection.

                    for x in index1:  # Begins loop through array. Loops through coordinate indices.
                        off1, elv1_top, elv1_btm = get_coordinate_pairs('Depth', x, None, df_off_i1, df_elv_i1,
                                                                        df_elv_i2, 0)  # Defines variables. Calls
                        # function.

                        # CALCULATE SEDIMENT THICKNESS -----------------------------------------------------------------

                        # At a point -----------------------------------------------------------------------------------

                        dpth1, prcs1, dpth_rt1, prcs_rt1, tm_intrvl = sediment_thickness(elv1_top, elv1_btm, srvy_yr1,
                                                                                         srvy_yr2,
                                                                                         'Sedimentation over ', 0)
                        # Defines variables. Calls function.

                        # Save data
                        if x == index1[0]:  # Conditional statement. Executes on first calculation only.
                            dpth1_lst=[]  # Defines list. Empty for looped population.
                            dpth_rt1_lst=[]  # Defines list. Empty for looped population.

                        dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_lst,
                                                          'New list appended: ', 0)  # Redefines list. Calls function.
                        # Populates list.
                        dpth_rt1_lst=create_appended_list(dpth_rt1, 'Aggradation rate', dpth_rt1_lst,
                                                          'New list appended: ', 0)  # Redefines list. Calls function.
                        # Populates list.

                        # Over cross-section ---------------------------------------------------------------------------

                        if x == index1[-1]:  # Conditional statement. Executes on last calculation only.
                            if srvy_yr2 == '1850s':  # Conditional statement. Corrects values in list.
                                dpth1_lst = list(filter(lambda y : y > 0, dpth1_lst))  # Redefines list. Removes
                                # erroneous erosion values from list.

                            dpth_avg = np.sum(dpth1_lst) / x  # Defines variable. Calculates average sediment
                            # thickness on transect.

                            dpth_avg_m = dpth_avg / ft_to_m  # Defines variable. Converts units to meters.

                            dpth_mdn = np.median(dpth1_lst)  # Defines variable. Calculates median sediment thickness
                            # of transect.

                            dpth_rt_avg = np.sum(dpth_rt1_lst) / x  # Defines variable. Calculates average
                            # sedimentation rate on transect.

                            dpth_rt_avg = dpth_rt_avg * in_to_ft  # Defines variable. Converts units to inches.

                            dpth_max = max(dpth1_lst)  # Defines variable. Retrieves max value from list.
                            dpth_min = min(dpth1_lst)  # Defines variable. Retrieves min value from list.

                        # Save data
                        if i == rng_strt:  # Conditional statement. Executes for first range only.
                            if j == srvy_nums1[0]:  # Conditional statement. Executes for first survey only.
                                if x == index1[0]:  # Conditional statement. Executes for first calculation only.
                                    df_sed_thck = pd.DataFrame()  # Defines DataFrame. Creates new DataFrame.
                        if j == srvy_nums1[0]:  # Conditional statement. Executes for first survey only.
                            if x == index1[0]:  # Conditional statement. Executes for first calculation only.
                                rng_name1_lst = []  # Defines list. Empty for looped population.
                                rng_num_lst = []  # Defines list. Empty for looped population.
                                srvy_yr1_lst = []  # Defines list. Empty for looped population.
                                srvy_yr2_lst = []  # Defines list. Empty for looped population.
                                tm_intrvl_lst = []  # Defines list. Empty for looped population.
                                strm_stat_lst = []  # Defines list. Empty for looped population.
                                dpth_avg_lst = []  # Defines list. Empty for looped population.
                                dpth_avg_m_lst = []  # Defines list. Empty for looped population.
                                dpth_mdn_lst = []  # Defines list. Empty for looped population.
                                dpth_rt_avg_lst = []  # Defines list. Empty for looped population.
                                dpth_max_lst = []  # Defines list. Empty for looped population.
                                dpth_min_lst = []  # Defines list. Empty for looped population.
                                wshd_A_lst = []  # Defines list. Empty for looped population.
                                vlly_W_lst = []  # Defines list. Empty for looped population.

                        dtfrm_pop_lists = [rng_name1_lst, rng_num_lst, srvy_yr1_lst, srvy_yr2_lst, tm_intrvl_lst,
                                           strm_stat_lst, dpth_avg_lst, dpth_avg_m_lst, dpth_mdn_lst, dpth_max_lst,
                                           dpth_min_lst, dpth_rt_avg_lst, wshd_A_lst, vlly_W_lst]  # Defines list.
                        # Nested to enable looped population.

                        if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.
                            dtfrm_pop_values = [str(rng_name1), int(i), srvy_yr1, srvy_yr2, str(tm_intrvl), strm_stat1,
                                                dpth_avg, dpth_avg_m, dpth_mdn, dpth_max, dpth_min, dpth_rt_avg,
                                                wshd_A, shrd_rng_m]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ', 0)  # Redefines list. Calls function.

                            if k == srvy_nums1[-1]:  # Conditional statement. Executes on last survey.
                                dtfrm_pop_clm_lbl = ['Srvy_range', 'Range_num', 'Srvy_year1', 'Srvy_year2', 'Tm_intvl',
                                                     'Strm_stat', 'D_avg_ft', 'D_avg_m', 'D_mdn_ft', 'D_avg_in/y',
                                                     'D_max_ft', 'D_min_ft', 'Wshd_A_sqkm', 'Vlly_W_m']  # Defines
                                # list. Sets column labels for DataFrame.

                                dtfrm_pop_lists = [rng_name1_lst, rng_num_lst, srvy_yr1_lst, srvy_yr2_lst,
                                                   tm_intrvl_lst, strm_stat_lst, dpth_avg_lst, dpth_avg_m_lst,
                                                   dpth_mdn_lst, dpth_rt_avg_lst, dpth_max_lst, dpth_min_lst,
                                                   wshd_A_lst, vlly_W_lst]  # Redefines list. With populated lists.

                                dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array for
                                # operation.

                                dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array for
                                # DataFrame dimensional compatibility.

                                df_sed_thck_rng = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl,
                                                                   'SEDIMENT THICKNESS', 1)  # Defines DataFrame. Calls
                                # function. Creates DataFrame of sediment thickness results for single transect.

                                # CALCULATE SEDIMENTATION RATE CHANGE --------------------------------------------------

                                dpth_rt_chng_lst = []  # Defines list. Empty for looped population.

                                index1 = df_sed_thck_rng.index  # Defines array. Retrieves index of DataFrame.

                                rt_0 = slice_DataFrame_cell('Float', 0, None, df_sed_thck_rng, index1[-1],
                                                            'D_avg_in/y', 'Average sedimentation rate', 0)  # Defines
                                # variable. Calls function. Slices DataFrame to yield first sedimentation rate.

                                for x in index1:  # Begins loop through array.
                                    rt_x = slice_DataFrame_cell('Float', 0, None, df_sed_thck_rng, index1[x],
                                                                'D_avg_in/y', 'Average aggradation rate', 0)  # Defines
                                    # variable. Calls function. Slices DataFrame to yield sedimentation rate for
                                    # comparison.

                                    rt_chng_x = rt_x / rt_0  # Defines variable. Calculates change in sedimentation
                                    # rate.

                                    # Save data
                                    dpth_rt_chng_lst = create_appended_list(rt_chng_x, 'Aggradation rate change',
                                                                            dpth_rt_chng_lst, 'New list appended: ', 0)
                                    # Redefines list. Calls function.

                                dtfrm_pop_clm_lbl = ['D_chng_in/y']  # Defines list. Sets column labels for DataFrame.

                                df_sed_chng = create_DataFrame(dpth_rt_chng_lst, dtfrm_pop_clm_lbl,
                                                               'SEDIMENTATION CHANGE', 0)  # Defines DataFrame. Calls
                                # function. Creates DataFrame of sedimentation change results for single transect.

                                df_sed_thck_rng = pd.concat([df_sed_thck_rng, df_sed_chng], axis=1)  # Redefines
                                # DataFrame. Concatenates two together along columns.

                                df_sed_thck = pd.concat([df_sed_thck, df_sed_thck_rng], axis=0)  # Redefines DataFrame.
                                # Concatenates two together along rows.

                                del rt_0, rt_x, rt_chng_x, df_sed_chng, df_sed_thck_rng  # Deletes variables. For
                                # reuse.

                            if i == rng_end:  # Conditional statement. Executes for last range only.
                                if k == srvy_nums1[-1]:  # Conditional statement. Executes for last survey only.
                                    print(df_sed_thck)  # Displays object. For check only.

                                    # Export data
                                    fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Sediment_thickness']
                                    # Defines list. Sets folder labels for directory to be made.

                                    if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                        fl_name = '/Sediment_thickness_' + str(chnl_name) + '.csv'  # Defines variable
                                        # as string.
                                    if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                        fl_name = '/Sediment_thickness_' + str(rng_name1) + '.csv'  # Defines variable
                                        # as string.
                                    else:  # Conditional statement.
                                        fl_name = '/Sediment_thickness.csv'  # Defines variable as string.

                                    export_file_to_directory(1, 'Table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                             fl_name, 1, None, df_sed_thck, False,
                                                             '1D sedimentation table', None, None, None, 0)  # Creates
                                    # directory and exports file. Calls function.

                                    # DISPLAY DATA ---------------------------------------------------------------------

                                    # Sediment thickness ---------------------------------------------------------------

                                    if Plt_dpth == 1:  # Conditional statement. Plots sediment thickness by time
                                        # interval against of distance upstream.

                                        srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                              'Srvy_year1', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                               'Srvy_year2', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        for x in srvy_yrs_lst:  # Begins loop through list elements. Loops through
                                            # survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('Equals', df_sed_thck, 'Srvy_year1',
                                                                                 x, 'SEDIMENT THICKNESS', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                            # data by first survey year.

                                            df_sed_thck_x = df_sed_thck_x.reset_index(drop=True)  # Redefines
                                            # DataFrame. Resets indices to begin at 0.

                                            df_dpth_x = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_x,
                                                                                'D_avg_ft', 0, 'SEDIMENT THICKNESS', 1)
                                            # Defines DataFrame. Calls function. Slices DataFrame to yield sediment
                                            # thickness data.
                                            df_strm_stat_x = slice_DataFrame_columns('DataFrame', 'Integer',
                                                                                     df_sed_thck_x, 'Strm_stat', 0,
                                                                                     'STREAM STATION', 1)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                                            # df_strm_stat_x = df_strm_stat_x.iloc[::-1]  # Redefines DataFrame. Inverts
                                            # values. For plotting sedimentation in the downstream direction.
                                            df_strm_stat_x = df_strm_stat_x.divide(1000)  # Redefines DataFrame.
                                            # Modifies values to be displayed in scientific notation.

                                            # df_dpth_x = df_dpth_x.iloc[::-1]  # Redefines DataFrame. Inverts values.
                                            # For plotting sedimentation in the downstream direction.

                                            srvy_yr1 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year1', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            srvy_yr2 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year2', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines
                                            # variable. Calls function. Sets plot marker type.

                                            title = 'Average sediment thickness'  # Defines string. Sets plot title.

                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)  # Defines string. Sets plot
                                            # object labels.

                                            plot_lines(1, 6, fig_sz, df_strm_stat_x, df_dpth_x, lbl, clr1, mrkr1,
                                                       mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 1, lctn,
                                                       mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                                                       'River station (1 x 10^3 ft)', fntsz[0], lbl_pd,
                                                       'Average sediment thickness (ft)', title, 1, 1)  # Creates plot.
                                            # Calls function.

                                        plt.figure(6)  # Creates plot window. Sets figure size.
                                        ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
                                        ax.invert_xaxis()  # Inverts x-axis.

                                        # Export data
                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.

                                        if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                                       str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                                        if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                                       str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                                        else:  # Conditional statement.
                                            fig_name = '/D_' + str(srvy_yrs2_lst[-1]) + '_' + str(srvy_yrs_lst[0]) + \
                                                       '.pdf'  # Defines variable as string.

                                        export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 6, 'pdf', None,
                                                                 None, 'Average sediment thickness plot', None,
                                                                 None, None, 0)  # Creates directory and exports
                                        # figure. Calls function.

                                    # Sedimentation rate ---------------------------------------------------------------

                                    if Plt_dpth_rt == 1:  # Conditional statement. Plots sedimentation rate by time
                                        # interval against of distance upstream.
                                        srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                               'Srvy_year1', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                                'Srvy_year2', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        for x in srvy_yrs_lst:  # Begins loop through list elements. Loops through
                                            # survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('Equals', df_sed_thck, 'Srvy_year1',
                                                                                 x, 'SEDIMENT THICKNESS', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                            # data by first survey year.

                                            df_sed_thck_x = df_sed_thck_x.reset_index(drop=True)  # Redefines
                                            # DataFrame. Resets indices to begin at 0.

                                            df_dpth_rt_x = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_x,
                                                                                'D_avg_in/y', 0, 'SEDIMENT THICKNESS',
                                                                                   1)  # Defines DataFrame. Calls
                                            # function. Slices DataFrame to yield sediment thickness data.

                                            df_strm_stat_x = slice_DataFrame_columns('DataFrame', 'Integer',
                                                                                     df_sed_thck_x, 'Strm_stat', 0,
                                                                                     'STREAM STATION', 1)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                                            df_strm_stat_x = df_strm_stat_x.iloc[::-1]  # Redefines DataFrame. Inverts
                                            # values. For plotting sedimentation in the downstream direction.
                                            df_strm_stat_x = df_strm_stat_x.divide(1000)  # Redefines DataFrame.
                                            # Modifies values to be displayed in scientific notation.

                                            df_dpth_rt_x = df_dpth_rt_x.iloc[::-1]  # Redefines DataFrame. Inverts
                                            # values.  For plotting sedimentation in the downstream direction.

                                            srvy_yr1 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year1', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            srvy_yr2 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year2', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines
                                            # variable. Calls function. Sets plot marker type.

                                            title = 'Average sedimentation rate'  # Defines string. Sets plot title.

                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)  # Defines string. Sets plot
                                            # object labels.

                                            plot_lines(1, 7, fig_sz, df_strm_stat_x, df_dpth_rt_x, lbl, clr1, mrkr1,
                                                       mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 1, lctn,
                                                       mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                                                       'River station (1 x 10^3 ft)', fntsz[0], lbl_pd,
                                                       'Average sedimentation rate (in/y)', title, 1, 1)  # Creates
                                            # plot. Calls function.

                                        plt.figure(7)  # Creates plot window. Sets figure size.
                                        ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
                                        ax.invert_xaxis()  # Inverts x-axis.

                                        # Export data
                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sedimentation_rate']
                                        # Defines list. Sets folder labels for directory to be made.

                                        if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_rt_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) + '_' \
                                                       + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                                        if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_rt_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) + '_' \
                                                       + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                                        else:  # Conditional statement.
                                            fig_name = '/D_rt_' + str(srvy_yrs2_lst[-1]) + '_' + str(srvy_yrs_lst[0]) \
                                                       + '.pdf'  # Defines variable as string.

                                        export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 7, 'pdf', None,
                                                                 None, 'Average sediment thickness plot', None,
                                                                 None, None, 0)  # Creates directory and exports
                                        # figure. Calls function.

                                    # Sediment thickness vs. drainage area ---------------------------------------------

                                    if Plt_dpth_vs_wshd == 1:  # Conditional statement. Plots sediment thickness
                                        # against drainage area.
                                        srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                               'Srvy_year1', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                                'Srvy_year2', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        for x in srvy_yrs_lst:  # Begins loop through list elements. Loops through
                                            # survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('Equals', df_sed_thck, 'Srvy_year1',
                                                                                 x, 'SEDIMENT THICKNESS', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                            # data by first survey year.

                                            df_sed_thck_x = df_sed_thck_x.reset_index(drop=True)  # Redefines
                                            # DataFrame. Resets indices to begin at 0.

                                            df_dpth_x = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_x,
                                                                                   'D_avg_m', 0, 'SEDIMENT THICKNESS',
                                                                                   0)  # Defines DataFrame. Calls
                                            # function. Slices DataFrame to yield sediment thickness data.

                                            df_wshd_A_x = slice_DataFrame_columns('DataFrame', 'Float',
                                                                                     df_sed_thck_x, 'Wshd_A_sqkm', 0,
                                                                                     'DRAINAGE AREA', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield drainage area data.

                                            srvy_yr1 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year1', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            srvy_yr2 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year2', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines
                                            # variable. Calls function. Sets plot marker type.

                                            # title = 'Average sediment thickness vs. drainage area'  # Defines string.
                                            # Sets plot title.

                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)  # Defines string. Sets plot
                                            # object labels.

                                            plot_scatter(8, fig_sz, df_wshd_A_x, df_dpth_x, lbl, clr1, clr1, mrkr1,
                                                        mrkr_sz[0], lin_wdth[1], alpha[0], 1, lctn, mrkr_scl, alpha[1],
                                                        lbl_spcng, None, None, fntsz[1], fntsz[0], lbl_pd,
                                                         'Drainage area (sqkm)', 'Average sediment thickness (m)',
                                                         None, 1, 1)  # Creates plot. Calls function.

                                        # Export data
                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.

                                        if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_vs_wshd_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) \
                                                       + '_' + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as
                                            # string.
                                        if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_vs_wshd_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) \
                                                       + '_' + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as
                                            # string.
                                        else:  # Conditional statement.
                                            fig_name = '/D_vs_wshd_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                                       str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.

                                        export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 8, 'pdf', None,
                                                                 None,
                                                                 'Average sediment thickness vs. drainage area plot',
                                                                 None, None, None, 0)  # Creates directory and exports
                                        # figure. Calls function.

                                    # Sediment thickness vs. valley width ----------------------------------------------

                                    if Plt_dpth_vs_vlly == 1:  # Conditional statement. Plots sediment thickness
                                        # against valley width.
                                        srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                               'Srvy_year1', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                                'Srvy_year2', 1, 'Survey years', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                        # present dataset.

                                        for x in srvy_yrs_lst:  # Begins loop through list elements. Loops through
                                            # survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('Equals', df_sed_thck, 'Srvy_year1',
                                                                                 x, 'SEDIMENT THICKNESS', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                            # data by first survey year.

                                            df_sed_thck_x = df_sed_thck_x.reset_index(drop=True)  # Redefines
                                            # DataFrame. Resets indices to begin at 0.

                                            df_dpth_x = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_x,
                                                                                   'D_avg_m', 0, 'SEDIMENT THICKNESS',
                                                                                   0)  # Defines DataFrame. Calls
                                            # function. Slices DataFrame to yield sediment thickness data.

                                            df_vlly_W_x = slice_DataFrame_columns('DataFrame', 'Float',
                                                                                     df_sed_thck_x, 'Vlly_W_m', 0,
                                                                                     'VALLEY WIDTH', 0)  # Defines
                                            # DataFrame. Calls function. Slices DataFrame to yield valley width data.

                                            srvy_yr1 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year1', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            srvy_yr2 = slice_DataFrame_cell('String', 0, None, df_sed_thck_x, 0,
                                                                            'Srvy_year2', 'Survey year', 0)  # Defines
                                            # variable. Calls function. Slices DataFrame to yield survey year of
                                            # present dataset.

                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines
                                            # variable. Calls function. Sets plot marker type.

                                            # title = 'Average sediment thickness vs. drainage area'  # Defines string.
                                            # Sets plot title.

                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)  # Defines string. Sets plot
                                            # object labels.

                                            plot_scatter(8, fig_sz, df_vlly_W_x, df_dpth_x, lbl, clr1, clr1, mrkr1,
                                                        mrkr_sz[0], lin_wdth[1], alpha[0], 1, lctn, mrkr_scl, alpha[1],
                                                        lbl_spcng, None, None, fntsz[1], fntsz[0], lbl_pd,
                                                         'Transect width (m)', 'Average sediment thickness (m)',
                                                         None, 1, 1)  # Creates plot. Calls function.

                                        # Export data
                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.

                                        if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_vs_vlly_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) \
                                                       + '_' + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as
                                            # string.
                                        if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                            fig_name = '/D_vs_vlly_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) \
                                                       + '_' + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as
                                            # string.
                                        else:  # Conditional statement.
                                            fig_name = '/D_vs_vlly_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                                       str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.

                                        export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 8, 'pdf', None,
                                                                 None,
                                                                 'Average sediment thickness vs. valley width plot',
                                                                 None, None, None,
                                                                 0)  # Creates directory and exports
                                        # figure. Calls function.

# ======================================================================================================================
# END ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
