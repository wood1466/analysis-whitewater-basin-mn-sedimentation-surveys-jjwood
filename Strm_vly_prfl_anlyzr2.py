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
from Functions import *  # Imports all functions from outside program.

# SELECT OPERATIONS ----------------------------------------------------------------------------------------------------

# Single cross-section analysis ----------------------------------------------------------------------------------------

Sngl = 1  # Defines variable as integer. Sets binary toggle.

# Plot single cross-section
Plt_sngl = 1  # Defines variable as integer. Sets binary toggle.
# Plot all cross-sections
Plt_all = 1 # Defines variable as integer. Sets binary toggle.

# Calculate coordinate geometry
Crdnts = 0  # Defines variable as integer. Sets binary toggle.

# Dual cross-sections analysis -----------------------------------------------------------------------------------------

Dbl = 0  # Defines variable as integer. Sets binary toggle.

# Plot dual cross-sections
Plt_dbl = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual interpolated cross-sections
Plt_intrp = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual re-interpolated cross-sections
Plt_reintrp = 0  # Defines variable as integer. Sets binary toggle.

# Calculate sediment thickness
Dpth = 1  # Defines variable as integer. Sets binary toggle.

# Plot sediment thickness
Plt_dpth = 1  # Defines variable as integer. Sets binary toggle.
# Plot sedimentation rate
Plt_dpth_rt = 1  # Defines variable as integer. Sets binary toggle.
# Plot sedimentation rate change
Plt_rt_chng=1  # Defines variable as integer. Sets binary toggle.

# SELECT INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Limits of analysis ---------------------------------------------------------------------------------------------------

rvr_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one river channel only.
rng_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one survey range only.
xtra_srvys = 0  # Defines variable as integer. Sets binary toggle. Analyzes extra survey data for range 11B (13).
rng_strt = 1  # Defines variable as integer. Sets start survey range number for analysis loop.
rng_end = 94  # Defines variable as integer. Sets end survey range number for analysis loop.

# Conversion factors ---------------------------------------------------------------------------------------------------

deg_to_rad = math.pi / 180  # Defines variable as float. Converts between degrees and radians.
ft_to_m = 3.281  # Defines variable as float. Converts between international feet meters.

# Plot format ----------------------------------------------------------------------------------------------------------

# Set general plot format
wdth = 4.5  # Defines variable as float. Sets plot window width.
hght = wdth * 1.618  # Defines variable. Sets plot window height. Uses golden ratio.
fig_sz = (hght, wdth)  # Defines object. Sets plot window size.
fntsz = [10, 8]  # Defines list. Sets font size for axes labels and tick marks.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Set data display format
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDDD']
# Defines list. Sets Paul Tol, muted, colorblind friendly palette with hex color codes.
lin_wdth = 2  # Defines variable as integer. Sets plot line width.
lin_styl = ['solid', 'dashed', 'dotted', 'dashdot']  # Defines list. Sets line style.
mrkrs = [' ', 'v', 'P', 'o', 'X', 's', '^', 'D', '<', '>', '8', 'p', 'h', 'H', 'd']  # Defines list. Sets plot markers.
# Uses matplotlib markers.
mrkr_sz = 4  # Defines variable as integer. Sets plot marker size.
alpha = [0.5, 0.3]  # Defines list. Sets object transparency for plotted data and fill.

# Set legend display format
lctn = 'best'  # Defines variable as string. Sets legend location on plot. Automatically chooses.
mrkr_scl = 2  # Defines variable as integer. Sets marker size on legend.
frm_alpha = 0.7  # Defines variable as float. Sets legend box transparency.
lbl_spcng = 0.7  # Defines variable as float. Sets legend object spacing.

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

# PART 2A: DATA SELECTION ----------------------------------------------------------------------------------------------

# UPLOAD DATA ----------------------------------------------------------------------------------------------------------

inpt_fl = inpt_fldr + '/Test_data.csv'  # Defines string. Sets file path to input file.

df_srvy_dt = upload_csv(inpt_fl, 'TEST DATA ', 0)  # Defines DataFrame. Calls function. Uploads survey data.

# ESTABLISH DATA SELECTION FRAMEWORK -----------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------
if rng_nly==1:
    rng_nums=[rng_strt]
    rng_end = rng_strt
elif rng_nly==0:
    rng_nums = forward_range(rng_strt, rng_end, 1, 'Range numbers', 0)  # Defines array. Calls function. Sets loop
# order by range.

# Temporal -------------------------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Range dataset --------------------------------------------------------------------------------------------------------

for i in rng_nums:  # Begins loop through array elements. Loops through range numbers.
    df_rng = slice_DataFrame_rows('equals', df_srvy_dt, 'Range_num', i, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield singular range data.
    # Retrieve metadata

    chnl_name = slice_DataFrame_cell(df_rng, 0, 'Chnl_name', 'Stream channel', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield stream channel name of present dataset.
    chnl_abrv = slice_DataFrame_cell(df_rng, 0, 'Chnl_abrv', 'Stream channel', 0)
    rng_name1 = slice_DataFrame_cell(df_rng, 0, 'Srvy_range', 'Range', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield range name of present dataset.
    strm_stat1 = slice_DataFrame_cell(df_rng, 0, 'Srvy_stat', 'Stream station', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey station of reach.
    strm_stat1_m = strm_stat1 / cnvrt_ft_t_m
    strm_stat1 = int(strm_stat1)  # Redefines variable. Converts float to integer.
    df_srvy_nums1 = slice_DataFrame_columns(df_rng, 'Srvy_num', 1, 'SURVEY NUMBERS', 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield survey numbers of present dataset.
    srvy_nums = df_srvy_nums1.tolist()
    srvy_nums = [int(x) for x in srvy_nums]
    if xtra == 1:
        pass
    elif xtra == 0:
        if i == 13:
            srvy_nums.remove(5)
            srvy_nums.remove(4)

    srvy_num_max = max_value_DataFrame(df_srvy_nums1, 'Survey', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield total number of range surveys of present dataset.
    srvy_num_max = int(srvy_num_max)

    # Survey dataset ---------------------------------------------------------------------------------------------------

    for j in srvy_nums:  # Begins loop through array elements. Loops through survey numbers.
        df_srvy1 = slice_DataFrame_rows('equals', df_rng, 'Srvy_num', j, 'SURVEY NUMBER', 0)  # Defines DataFrame.
        # Calls function. Slices DataFrame to yield singular survey data.

        # Retrieve metadata
        srvy_yr1 = slice_DataFrame_cell(df_srvy1, 0, 'Srvy_year', 'Survey year', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield survey year of present dataset.

        srvy_dt1 = slice_DataFrame_cell(df_srvy1, 0, 'Srvy_date', 'Survey date', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield survey date of present dataset.

        # Survey measurements --------------------------------------------------------------------------------------

        df_offst1 = slice_DataFrame_columns(df_srvy1, 'Offset_ft', 0, 'OFFSET', 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield survey offsets of present dataset.

        df_offst1 = df_offst1.astype(float)
        df_elvtn1 = slice_DataFrame_columns(df_srvy1, 'Elv_geo_ft', 0, 'ELEVATION', 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield survey elevations of present dataset.
        df_elvtn1 = df_elvtn1.astype(float)
        # Retrieve metadata
        offst_min1 = min_value_DataFrame(df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
        # DataFrame to yield first offset of present dataset.
        offst_max1 = max_value_DataFrame(df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
        # DataFrame to yield last offset of present dataset.
        elvtn_min1 = min_value_DataFrame(df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function. Slices
        # DataFrame to yield lowest elevation of present dataset.
        elvtn_min1 = float(elvtn_min1)
        elvtn_max1 = max_value_DataFrame(df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function. Slices
        elvtn_max1 = float(elvtn_max1)
        # DataFrame to yield highest elevation of present dataset.
        num_smpls1 = df_srvy1.shape[0]
        brng_r_dir = slice_DataFrame_cell(df_srvy1, 0, 'Brng_R_dir', 'Bearing reference direction: ', 0)
        brng_angl = slice_DataFrame_cell(df_srvy1, 0, 'Brng_A', 'Bearing angle: ', 0)
        brng_angl = float(brng_angl)
        brng_a_dir = slice_DataFrame_cell(df_srvy1, 0, 'Brng_A_dir', 'Bearing angle direction: ', 0)
        brng_fnctl = slice_DataFrame_cell(df_srvy1, 0, 'Brng_fnctl', 'Functional bearing: ', 0)

        # Calculate metadata
        rng_lngth1 = offst_max1 - offst_min1  # Defines variable. Calculates survey length.
        rng_lngth1_m = rng_lngth1 / cnvrt_ft_t_m
        srvy_rlf1 = elvtn_max1 - elvtn_min1  # Defines variable. Calculates survey relief.
        srvy_rlf1_m = srvy_rlf1 / cnvrt_ft_t_m

        # DISPLAY DATA ---------------------------------------------------------------------------------------------

        if Sngl == 1:  # Conditional statement. Executes analysis of single cross-section.
            # Metadata ---------------------------------------------------------------------------------------------

            print('==================================================')  # Displays objects.
            print('\033[1m' + 'Stream channel: ' + '\033[0m' + str(chnl_name))  # Displays
            # objects.
            print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
            # objects.
            print('\033[1m' + 'Range bearing: ' + '\033[0m' + str(brng_r_dir)+ str(brng_angl)+str(brng_a_dir) + ' ('+str(brng_fnctl)+')')  # Displays objects. Makes font# bold.
            print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1) + ' ft' + ' (' + str('%.0f' % strm_stat1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Range survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(j) + ' of ' +
                  str(srvy_num_max) + ')')  # Displays objects.
            # print('\033[1m' + 'Survey date(s): ' + '\033[0m' + str(srvy_dt1))  # Displays objects.
            print('\033[1m' + 'Survey length: ' + '\033[0m' + str('%.2f'%rng_lngth1) + ' ft' + ' (' + str('%.0f' % rng_lngth1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' ft' + ' (' + str('%.0f' % srvy_rlf1_m) + ' m)')  # Displays objects.
            print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.

            # Cross-section plot -----------------------------------------------------------------------------------

            if Plt_sngl == 1:  # Conditional statement. Plots single cross-section.
                clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                # plot color.
                mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets plot
                # marker type.

                title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')' + ' ' + str(srvy_yr1) + ' survey '  # Defines string. Sets plot
                # title.

                plot_lines(1, 1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz, lin_wdth,
                           lin_styl[0], alpha, 0, lctn, mrkr_scl, frm_alpha, lbl_spcng, 0, fntsz_tcks,
                           'Survey offset (ft)',fntsz_ax, lbl_pd, 'Surface elevation (ft)', title, 2, 1)
                # Creates plot. Calls function.

                # EXPORT FIGURE ------------------------------------------------------------------------------------

                fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Single', '/' + chnl_name]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/' + str(rng_name1) + '_s' + str(j) + '_' + str(srvy_yr1) + '.pdf'  # Defines
                # variable as strIng. Sets name of figure for export.

                export_file_to_directory(1, 'figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1,
                                         'pdf', None, None, 'Cross-sectional plot',None,None,None, 0)  # Creates directory and
                # exports figure. Calls function.

            if Plt_all == 1:
                clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                # plot color.
                mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets plot
                # marker type.
                title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')'
                plot_lines(1, 2, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz, lin_wdth,
                           lin_styl[0], alpha, 1, lctn, mrkr_scl, frm_alpha, lbl_spcng,0, fntsz_tcks,
                           'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title, 1, 1)

                # EXPORT FIGURE ------------------------------------------------------------------------------------
                if j == srvy_nums[-1]:
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/All', '/' + chnl_name]
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '.pdf'  # Defines
                    # variable as strIng. Sets name of figure for export.

                    export_file_to_directory(1, 'figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 2,
                                             'pdf', None, None, 'Cross-sectional plot',None,None,None, 0)  # Creates directory and
                    # exports figure. Calls function.

            if Crdnts == 1:
                BM1_e_std = slice_DataFrame_cell(df_srvy1, 0, 'BM1_east_m', 'Benchmark 1 Easting (m): ', 0)
                BM1_n_std = slice_DataFrame_cell(df_srvy1, 0, 'BM1_nrth_m', 'Benchmark 1 Northing (m): ', 0)
                BM2_e_std = slice_DataFrame_cell(df_srvy1, 0, 'BM2_east_m', 'Benchmark 2 Easting (m): ', 0)
                BM2_n_std = slice_DataFrame_cell(df_srvy1, 0, 'BM2_nrth_m', 'Benchmark 2 Northing (m): ', 0)
                BM1_off = slice_DataFrame_cell(df_srvy1, 0, 'BM1_off_tp', 'Benchmark 1 top offset (ft): ', 0)
                BM2_off = slice_DataFrame_cell(df_srvy1, 0, 'BM2_off_tp', 'Benchmark 2 top offset (ft): ', 0)
                rng_brng,sin,cos = coordinate_bearing(BM1_e_std, BM2_e_std, BM1_n_std, BM2_n_std, BM1_off,BM2_off, brng_r_dir, brng_a_dir,brng_angl,brng_fnctl, 'Directional data',1)
                # breakpoint()
                df_offst1_shft = df_offst1 - BM1_off
                # print(df_offst1_shft)
                df_offst1_shft_m=df_offst1_shft/cnvrt_ft_t_m
                # print(df_offst1_shft_m)
                offsets_East = cos * df_offst1_shft_m
                # print(offsets_East)
                offsets_North = sin * df_offst1_shft_m
                # print(offsets_North)
                smpl_eastings = BM1_e_std + offsets_East
                smpl_eastings = smpl_eastings.rename('Easting_m')
                # print(smpl_eastings)
                smpl_northings = BM1_n_std + offsets_North
                smpl_northings=smpl_northings.rename('Northing_m')
                # print(smpl_northings)
                # breakpoint()
                df_srvy1=pd.concat([df_srvy1,smpl_eastings,smpl_northings],axis=1)
                # print(df_srvy1)
                # breakpoint()
                plt.figure(1, figsize=(7, 7))
                ax1 = plt.gca()
                ax1.scatter(smpl_eastings, smpl_northings, s=5, label='Predicted', c='Orange', marker='o', alpha=0.5)
                ax1.scatter(BM1_e_std, BM1_n_std, s=5, label='Measured', c='Blue', marker='o', alpha=1)
                ax1.scatter(BM2_e_std, BM2_n_std, s=5, c='Blue', marker='o', alpha=1)
                ax1.set_aspect('equal', 'box')
                plt.xlabel('Easting (m)', fontsize=8)
                plt.ylabel('Northing (m)', fontsize=8)
                # plt.pause(1)
                # plt.show()
                gdf_srvy = gpd.GeoDataFrame(df_srvy1, geometry=gpd.points_from_xy(df_srvy1.Easting_m, df_srvy1.Northing_m),crs='EPSG:26915')
                fldr_lbls = ['/Cross_sectional_analysis', '/Geographic_data', '/Cross_sections', '/Points','/' + chnl_name]
                layer = 'R_' + str(rng_name1) + '_'+ str(srvy_yr1)
                geopackage = '/'+chnl_abrv+'_survey_points.gpkg'
                # gdf_srvy.to_file(opt_fldr + dig_fldrout + gis_fldr + gpkg_fl, layer=feature, driver='GPKG', index=False)
                export_file_to_directory(1, 'geo table', 5, fldr_lbls,opt_fldr,'Directiories named: ',layer,None,None,None,False,'GIS layer',gdf_srvy,geopackage,'GPKG',0)
        # Creates and exports geopackage at specified path.
        # SELECT DATA ----------------------------------------------------------------------------------------------

        if Dbl == 1:  # Conditional statement. Executes analysis of cross-sections as subsequent pairs.
            if j > 1:  # Conditional statement. Executes lines below if dataset is not second to last survey.
                index1 = srvy_nums.index(j)

                index1 = index1 + 1

                k = srvy_nums[index1]# Defines variable as integer. Allows for selection of second dataset.

                # Survey dataset -----------------------------------------------------------------------------------

                df_srvy2 = slice_DataFrame_rows('equals', df_rng, 'Srvy_num', k, 'SURVEY NUMBER', 0)  # Defines
                # DataFrame. Calls function. Slices DataFrame to yield singular survey data.

                # Retrieve metadata
                srvy_yr2 = slice_DataFrame_cell(df_srvy2, 0, 'Srvy_year', 'Survey year', 0)  # Defines variable.
                # Calls function. Slices DataFrame to yield survey year of present dataset.
                srvy_dt2 = slice_DataFrame_cell(df_srvy2, 0, 'Srvy_date', 'Survey date', 0)  # Defines variable.
                # Calls function. Slices DataFrame to yield survey date of present dataset.

                # Survey measurements ----------------------------------------------------------------------------------

                df_offst2 = slice_DataFrame_columns(df_srvy2, 'Offset_ft', 0, 'OFFSET', 0)  # Defines DataFrame.
                # Calls function. Slices DataFrame to yield survey offsets of present dataset.

                df_elvtn2 = slice_DataFrame_columns(df_srvy2, 'Elv_geo_ft', 0, 'ELEVATION',0)  # Defines
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

                num_smpls2 = df_srvy2.shape[0]
                # Defines variable. Calls function. Slices DataFrame to yield number of measurements of present
                # dataset.

                # Calculate metadata
                rng_lngth2 = offst_max2 - offst_min2  # Defines variable. Calculates survey length.
                rng_lngth2_m = rng_lngth2 / cnvrt_ft_t_m
                srvy_rlf2 = elvtn_max2 - elvtn_min2  # Defines variable. Calculates survey relief.
                srvy_rlf2_m = srvy_rlf2 / cnvrt_ft_t_m

                # DISPLAY DATA -------------------------------------------------------------------------------------

                # Metadata -----------------------------------------------------------------------------------------

                print('==================================================')  # Displays objects.
                print('\033[1m' + 'Stream channel: ' + '\033[0m' + str(chnl_name))  # Displays objects.
                print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_name1) + ' (' + str(i) + ')')  # Displays
                # objects.
                print('\033[1m' + 'Range surveys: ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' +
                      str(j) + '–' + str(k) + ' of ' + str(srvy_num_max) + ')')  # Displays objects.
                # print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))  # Displays
                # objects.
                print('\033[1m' + 'Survey lengths: ' + '\033[0m' + str('%.1f' % rng_lngth1) + ' & ' + str('%.1f' % rng_lngth2) +
                      ' ft' + ' (' + str('%.0f' % rng_lngth1_m) + ' & ' + str('%.0f' % rng_lngth2_m) + ' m)')  # Displays objects.
                print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' & ' +
                      str('%.1f' % srvy_rlf2) + ' ft' + ' (' + str('%.0f' % srvy_rlf1_m) + ' & ' + str('%.0f' % srvy_rlf2_m) + ' m)')  # Displays objects.
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

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' surveys'
                    # Defines string. Sets title of plot.  # Defines string. Sets plot title.

                    plot_lines(2, 3, fig_sz, [df_offst2, df_offst1], [df_elvtn2, df_elvtn1], [srvy_yr2, srvy_yr1],
                               [clr2, clr1], [mrkr2, mrkr1], mrkr_sz, lin_wdth, [lin_styl[0], lin_styl[0]], alpha,
                               0, lctn, mrkr_scl, frm_alpha, lbl_spcng, 0, fntsz_tcks, 'Survey offset (ft)', fntsz_ax,
                               lbl_pd, 'Surface elevation (ft)', title, 2, 1)  # Creates plot. Calls function.

                    # EXPORT FIGURE --------------------------------------------------------------------------------

                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name, '/Measured']
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                               str(srvy_yr2) + '.pdf'  # Defines variable as strIng. Sets name of figure for
                    # export.

                    export_file_to_directory(1, 'figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
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

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) +') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                            ' interpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                    # plot title.

                    plot_lines(2, 4, fig_sz, [offsts_int2, offsts_int1], [elvtns_int2, elvtns_int1],
                               [srvy_yr2, srvy_yr1], [clr2, clr1], [mrkr2, mrkr1], mrkr_sz, lin_wdth,
                               [lin_styl[0], lin_styl[0]], alpha, 0, lctn, mrkr_scl, frm_alpha, lbl_spcng,
                               0, fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title,
                               2, 1)  # Creates plot. Calls function.

                    # EXPORT FIGURE --------------------------------------------------------------------------------

                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                 '/Interpolated']  # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' \
                               + str(srvy_yr2) + '_Interp' + '.pdf'  # Defines variable as strIng. Sets name of
                    # figure for export.

                    export_file_to_directory(1, 'figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                             4, 'pdf', None, None, 'Cross-sectional plot', 0)  # Creates directory
                    # and exports figure. Calls function.

                # SELECT CALCULATION RANGE -------------------------------------------------------------------------

                start, end, srvy_lngth_shrd = select_coincident_x_range('dataframe', df_offst1, df_offst2,
                                                                        ' ft', 0)  # Defines variables. Calls
                # function. Identifies shared x values of individual datasets.b

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

                if Plt_dbl_reintrp1 == 1:  # Conditional statement. Plots reinterpolated cross-sections as
                    # subsequent pairs.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets
                    # plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 1)  # Defines variable. Calls function. Sets
                    # plot marker type.
                    clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 0)  # Defines variable. Calls function. Sets
                    # plot color.
                    mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 0)  # Defines variable. Calls function. Sets
                    # plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                            ' reinterpolated surveys'  # Defines string. Sets title of plot.

                    plot_lines(2, 5, fig_sz, [offsts_int2, offsts_int1], [elvtns_int2, elvtns_int1],
                               [srvy_yr2, srvy_yr1], [clr2, clr1], [mrkr2, mrkr1], mrkr_sz, lin_wdth,
                               [lin_styl[0], lin_styl[0]], alpha, 0, lctn, mrkr_scl, frm_alpha, lbl_spcng,
                               0,fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title,
                               2, 1)  # Creates plot. Calls function.

                    # EXPORT FIGURE --------------------------------------------------------------------------------

                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                 '/Reinterpolated']  # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) \
                               + '–' + str(srvy_yr2) + '_Reinterp' + '.pdf'  # Defines variable as strIng. Sets
                    # name of figure for export.

                    export_file_to_directory(1, 'figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
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

                        dpth1, prcs1, dpth1_rt, prcs1_rt, srvy_intrvl = sediment_thickness('depth', elvtn1_top, elvtn1_btm, srvy_yr1, srvy_yr2, None, None, 'Sedimentation over ',0)  # Defines variables. Calls
                        # function.

                        if x == index1[0]:
                            dpth1_list=[]  # Defines list. Empty for looped population.
                            dpth1_rt_list=[]

                        dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_list, 'New list appended: ', 0)  # Redefines list. Calls
                        # function.
                        dpth1_rt_list=create_appended_list(dpth1_rt,'Aggradation rate', dpth1_rt_list, 'New list appended: ', 0)

                        # Averaged over cross-section --------------------------------------------------------------

                        if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.

                            if srvy_yr2 == '1850s':

                                dpth1_list=list(filter(lambda y : y > 0, dpth1_list))



                            dpth_avg = np.sum(dpth1_list) / x  # Defines variable. Calculates average sediment
                            # thickness.

                            dpth_rt_avg = np.sum(dpth1_rt_list) / x

                            dpth_max = max(dpth1_list)  # Defines variable. Retrieves max value from list.
                            dpth_min = min(dpth1_list)  # Defines variable. Retrieves min value from list.

                        # PREPARE DATA FOR EXPORT ------------------------------------------------------------------

                        # Lists ------------------------------------------------------------------------------------

                        # # Create empty lists
                        if i == rng_strt:  # Conditional statement. Executes for first range only.
                            if j == srvy_nums[0]:  # Conditional statement. Executes for first survey only.
                                if x == index1[0]:
                                    df_sed_thck = pd.DataFrame()
                                    rng_name1_list = []  # Defines list. Empty for looped population.
                                    rng_num_list=[]
                                    srvy_yr1_list = []  # Defines list. Empty for looped population.
                                    srvy_yr2_list = []  # Defines list. Empty for looped population.
                                    srvy_intrvl_list=[]
                                    strm_stat_list = []  # Defines list. Empty for looped population.
                                    dpth_avg_list = []  # Defines list. Empty for looped population.
                                    dpth_max_list = []  # Defines list. Empty for looped population.
                                    dpth_min_list = []  # Defines list. Empty for looped population.
                                    dpth_rt_avg_list =[]

                        dtfrm_pop_lists = [rng_name1_list, rng_num_list, srvy_yr1_list, srvy_yr2_list,srvy_intrvl_list, strm_stat_list,
                                           dpth_avg_list, dpth_max_list, dpth_min_list, dpth_rt_avg_list ]  # Defines list.
                        # Nested to enable looped population.

                        # Populate lists
                        if x == index1[-1]:  # Conditional statement. Executes lines after last point calculation.
                            dtfrm_pop_values = [str(rng_name1), int(i), srvy_yr1, srvy_yr2, str(srvy_intrvl), strm_stat1, dpth_avg, dpth_max, dpth_min, dpth_rt_avg] #pulate lists.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list
                                # element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index], 'New list appended: ', 0)  # Redefines list. Calls function.

                            if k == srvy_nums[-1]:
                                dtfrm_pop_clm_lbl = ['Srvy_range', 'Range_num', 'Srvy_year1', 'Srvy_year2', 'Srvy_intvl', 'Strm_stat', 'D_avg_ft',
                                                     'D_max_ft', 'D_min_ft', 'D_avg_ft/y']  # Defines list. Sets column labels for DataFrame.
                                dtfrm_pop_lists = [rng_name1_list, rng_num_list, srvy_yr1_list, srvy_yr2_list,
                                                   srvy_intrvl_list, strm_stat_list,
                                                   dpth_avg_list, dpth_max_list, dpth_min_list,
                                                   dpth_rt_avg_list]  # Redefines list. With
                                # populated lists.
                                # DataFrame ----------------------------------------------------------------------------

                                dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array
                                # for operation.

                                dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array
                                # for DataFrame dimensional compatibility.

                                df_sed_thck_rng = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl, 'SEDIMENT THICKNESS', 0)  # Defines DataFrame. Calls function. Creates
                                # DataFrame of average sediment thickness results.

                                dtfrm_pop_values=[]
                                rng_name1_list = []  # Defines list. Empty for looped population.
                                rng_num_list = []
                                srvy_yr1_list = []  # Defines list. Empty for looped population.
                                srvy_yr2_list = []  # Defines list. Empty for looped population.
                                srvy_intrvl_list = []
                                strm_stat_list = []  # Defines list. Empty for looped population.
                                dpth_avg_list = []  # Defines list. Empty for looped population.
                                dpth_max_list = []  # Defines list. Empty for looped population.
                                dpth_min_list = []  # Defines list. Empty for looped population.
                                dpth_rt_avg_list = []
                                dpth_rt_chng_list=[]

                                index1 = df_sed_thck_rng.index
                                rt0 = slice_DataFrame_cell(df_sed_thck_rng, index1[-1], 'D_avg_ft/y', 'Average aggradation rate', 0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                rt0 = float(rt0)
                                for x in index1:
                                    rtx = slice_DataFrame_cell(df_sed_thck_rng, index1[x], 'D_avg_ft/y', 'Average aggradation rate', 0)
                                    rtx =float(rtx)
                                    rt_chngx=rtx/rt0
                                    dpth_rt_chng_list=create_appended_list(rt_chngx, 'Aggradation rate change', dpth_rt_chng_list, 'New list appended: ', 0)
                                del rt0, rtx, rt_chngx
                                dtfrm_pop_clm_lbl=['D_chng_ft/y']
                                df_sed_chng = create_DataFrame(dpth_rt_chng_list,dtfrm_pop_clm_lbl, 'AGGRADATION CHANGE', 0)
                                df_sed_thck_rng = pd.concat([df_sed_thck_rng, df_sed_chng], axis=1)
                                del df_sed_chng
                                df_sed_thck = pd.concat([df_sed_thck, df_sed_thck_rng], axis=0)

                                del df_sed_thck_rng

                            if i == rng_end:  # Conditional statement. Executes for last range only.
                                if k == srvy_nums[-1]:  # Conditional statement. Executes for last survey only.
                                    # dtfrm_pop_clm_lbl=['Srvy_range', 'Range_num', 'Srvy_year1', 'Srvy_year2','Srvy_intvl', 'Strm_stat', 'D_avg_ft',
                                    #                    'D_max_ft', 'D_min_ft', 'D_avg_ft/y']  # Defines list. Sets column labels for
                                    # # DataFrame.
                                    #
                                    # dtfrm_pop_lists = [rng_name1_list, rng_num_list, srvy_yr1_list, srvy_yr2_list,srvy_intrvl_list, strm_stat_list,
                                    #                    dpth_avg_list, dpth_max_list, dpth_min_list, dpth_rt_avg_list]  # Redefines list. With
                                    # # populated lists.
                                    #
                                    # # DataFrame ----------------------------------------------------------------------------
                                    #
                                    # dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array
                                    # # for operation.
                                    #
                                    # dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array
                                    # # for DataFrame dimensional compatibility.
                                    #
                                    # df_sed_thck = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl, 'SEDIMENT THICKNESS', 1)  # Defines DataFrame. Calls function. Creates
                                    # # DataFrame of average sediment thickness results.
                                    print(df_sed_thck)
                                    # EXPORT FILE --------------------------------------------------------------------------

                                    fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Sediment_thickness']
                                    # Defines list. Sets folder labels for directory to be made.

                                    if rng_nly==1:
                                        fl_name = '/Sediment_thickness_' + str(rng_name1) + '.csv'
                                    elif rng_nly == 0:
                                        fl_name = '/Sediment_thickness.csv'  # Defines variable as strIng. Sets name and
                                    # extension of file for export.
                                    if rvr_nly==1:
                                        fl_name = '/Sediment_thickness_' + str(chnl_name) + '.csv'
                                    elif rvr_nly==0:
                                        fl_name = '/Sediment_thickness.csv'  # Defines variable as strIng. Sets name and
                                    export_file_to_directory(1, 'table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                             fl_name, 1, None, df_sed_thck, False,
                                                             'Sediment thickness table', 0)  # Creates directory and
                                    # exports figure. Calls function.

                                    # PLOT DATA ----------------------------------------------------------------------------

                                    if Plt_dpth == 1:  # Conditional statement. Plots sediment thickness, by year, as a function of distance upstream.

                                        df_srvy_yrs = slice_DataFrame_columns(df_sed_thck, 'Srvy_year1', 1, 'Survey years', 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs = df_srvy_yrs.tolist()  # Defines list. Converts DataFrame to list.

                                        for x in srvy_yrs:  # Begins loop through list elements. Loops through survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('equals', df_sed_thck, 'Srvy_year1', x, 'SEDIMENT THICKNESS', 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_dpth_x = slice_DataFrame_columns(df_sed_thck_x, 'D_avg_ft', 0, 'SEDIMENT THICKNESS', 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_strm_stat_x = slice_DataFrame_columns(df_sed_thck_x, 'Strm_stat', 0,'STREAM STATION', 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield stream station data.
                                            df_strm_stat_x=df_strm_stat_x.iloc[::-1]
                                            df_strm_stat_x=df_strm_stat_x.astype(int)
                                            df_strm_stat_x=df_strm_stat_x.divide(1000)

                                            # strm_stat_x = df_strm_stat_x.to_numpy()
                                            # strm_stat_x=strm_stat_x.astype(int)

                                            # strm_stat_x = np.divide(strm_stat_x, 1000)

                                            df_dpth_x = df_dpth_x.astype(float)  # Redefines DataFrame. Converts values to float.
                                            df_dpth_x = df_dpth_x.iloc[::-1]
                                            srvy_yr1 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year1', 'Survey year',0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            srvy_yr2 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year2', 'Survey year', 0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            if type(srvy_yr1) == str:
                                                pass
                                            else:
                                                srvy_yr1 = srvy_yr1.values[0]
                                            if type(srvy_yr2) == str:
                                                pass
                                            else:
                                                srvy_yr2 = srvy_yr2.values[0]

                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 1)  # Defines variable. Calls function. Sets plot marker type.
                                            title = 'Average sediment thickness'  # Defines string. Sets plot title.
                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)
                                            plot_lines(1, 6, fig_sz, df_strm_stat_x, df_dpth_x, lbl, clr1, mrkr1,
                                                       mrkr_sz, lin_wdth, lin_styl[0], alpha, 1, lctn, mrkr_scl, frm_alpha,
                                                       lbl_spcng,1, fntsz_tcks, 'River station (1 x 10^3 ft)', fntsz_ax, lbl_pd,
                                                       'Average sediment thickness (ft)', title, 1, 1)  # Creates plot. Calls function.

                                        # EXPORT FIGURE --------------------------------------------------------------------

                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.
                                        df_srvy_yrs2 = slice_DataFrame_columns(df_sed_thck, 'Srvy_year2', 1, 'Survey years',
                                                                              0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs2 = df_srvy_yrs2.tolist()  # Defines list. Converts DataFrame to list.
                                        if rng_nly == 1:
                                            fig_name = '/D_' + str(rng_name1) + '_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'
                                        elif rng_nly == 0:
                                            fig_name = '/D_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                        # variable as strIng. Sets name of figure for export.
                                        if rvr_nly == 1:
                                            fig_name = '/D_' + str(chnl_name) + '_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'
                                        elif rvr_nly == 0:
                                            fig_name = '/D_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                        export_file_to_directory(1, 'figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 6, 'pdf', None, None,
                                                                 'Average sediment thickness plot', 0)  # Creates directory

                                    if Plt_dpth_rt == 1:
                                        df_srvy_yrs = slice_DataFrame_columns(df_sed_thck, 'Srvy_year1', 1,
                                                                              'Survey years',
                                                                              0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs = df_srvy_yrs.tolist()  # Defines list. Converts DataFrame to list.

                                        for x in srvy_yrs:  # Begins loop through list elements. Loops through survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('equals', df_sed_thck, 'Srvy_year1', x,
                                                                                 'SEDIMENT THICKNESS',
                                                                                 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_dpth_rt_x = slice_DataFrame_columns(df_sed_thck_x, 'D_avg_ft/y', 0,
                                                                                'SEDIMENT THICKNESS',
                                                                                0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_strm_stat_x = slice_DataFrame_columns(df_sed_thck_x, 'Strm_stat', 0,
                                                                                     'STREAM STATION',
                                                                                     0)  # Defines DataFrame. Calls function. Slices DataFrame to yield stream station data.
                                            df_strm_stat_x = df_strm_stat_x.iloc[::-1]
                                            df_strm_stat_x = df_strm_stat_x.astype(int)
                                            df_strm_stat_x = df_strm_stat_x.divide(1000)

                                            # strm_stat_x = df_strm_stat_x.to_numpy()
                                            # strm_stat_x=strm_stat_x.astype(int)

                                            # strm_stat_x = np.divide(strm_stat_x, 1000)

                                            df_dpth_rt_x = df_dpth_rt_x.astype(
                                                float)  # Redefines DataFrame. Converts values to float.
                                            df_dpth_rt_x = df_dpth_rt_x.iloc[::-1]
                                            srvy_yr1 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year1',
                                                                            'Survey year',
                                                                            0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            srvy_yr2 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year2',
                                                                            'Survey year',
                                                                            0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            if type(srvy_yr1) == str:
                                                pass
                                            else:
                                                srvy_yr1 = srvy_yr1.values[0]
                                            if type(srvy_yr2) == str:
                                                pass
                                            else:
                                                srvy_yr2 = srvy_yr2.values[0]
                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd,
                                                                            0)  # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs,
                                                                             1)  # Defines variable. Calls function. Sets plot marker type.

                                            title = 'Average aggradation rate'  # Defines string. Sets plot title.
                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)
                                            plot_lines(1, 7, fig_sz, df_strm_stat_x, df_dpth_rt_x, lbl, clr1, mrkr1,
                                                       mrkr_sz, lin_wdth, lin_styl[0], alpha, 1, lctn, mrkr_scl,
                                                       frm_alpha,
                                                       lbl_spcng, 1, fntsz_tcks, 'River station (1 x 10^3 ft)',
                                                       fntsz_ax, lbl_pd,
                                                       'Average aggradation rate (ft/y)', title, 1,
                                                       1)  # Creates plot. Calls function.

                                        # EXPORT FIGURE --------------------------------------------------------------------

                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.
                                        df_srvy_yrs2 = slice_DataFrame_columns(df_sed_thck, 'Srvy_year2', 1,
                                                                               'Survey years',
                                                                               0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs2 = df_srvy_yrs2.tolist()  # Defines list. Converts DataFrame to list.
                                        if rng_nly == 1:
                                            fig_name = '/D_rt_' + str(rng_name1) + '_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'
                                        elif rng_nly == 0:
                                            fig_name = '/D_rt_' + str(srvy_yrs2[-1]) + '–' + str(
                                            srvy_yrs[0]) + '.pdf'  # Defines
                                        # variable as strIng. Sets name of figure for export.
                                        if rvr_nly == 1:
                                            fig_name = '/D_rt_' + str(chnl_name) + '_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'
                                        elif rvr_nly == 0:
                                            fig_name = '/D_rt_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                        export_file_to_directory(1, 'figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 7, 'pdf', None, None,
                                                                 'Average sediment thickness plot',
                                                                 0)  # Creates directory
                                    if Plt_dpth_rt_chng==1:
                                        df_srvy_yrs = slice_DataFrame_columns(df_sed_thck, 'Srvy_year1', 1,'Survey years',0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs = df_srvy_yrs.tolist()  # Defines list. Converts DataFrame to list.

                                        for x in srvy_yrs:  # Begins loop through list elements. Loops through survey years.
                                            df_sed_thck_x = slice_DataFrame_rows('equals', df_sed_thck, 'Srvy_year1', x,'SEDIMENT THICKNESS',0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_dpth_rt_chng_x = slice_DataFrame_columns(df_sed_thck_x, 'D_chng_ft/y', 0,
                                                                                   'SEDIMENT THICKNESS',
                                                                                   0)  # Defines DataFrame. Calls function. Slices DataFrame to yield sediment thickness data by year.

                                            df_srvy_yr1_x = slice_DataFrame_columns(df_sed_thck_x, 'Srvy_year1', 0,
                                                                                     'STREAM STATION',
                                                                                     0)  # Defines DataFrame. Calls function. Slices DataFrame to yield stream station data.
                                            df_srvy_yr1_x=df_srvy_yr1_x.astype(int)

                                            df_dpth_rt_chng_x = df_dpth_rt_chng_x.astype(float)  # Redefines DataFrame. Converts values to float.
                                            # df_dpth_rt_chng_x = df_dpth_rt_chng_x.iloc[::-1]
                                            srvy_yr1 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year1','Survey year',0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            srvy_yr2 = slice_DataFrame_cell(df_sed_thck_x, 0, 'Srvy_year2','Survey year',0)  # Defines variable. Calls function. Slices DataFrame to yield suvey year of present dataset.
                                            if type(srvy_yr1) == str:
                                                pass
                                            else:
                                                srvy_yr1 = srvy_yr1.values[0]
                                            if type(srvy_yr2) == str:
                                                pass
                                            else:
                                                srvy_yr2 = srvy_yr2.values[0]
                                            clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd,0)  # Defines variable. Calls function. Sets plot color.
                                            mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs,1)  # Defines variable. Calls function. Sets plot marker type.

                                            title = 'Average aggradation rate'  # Defines string. Sets plot title.
                                            lbl = str(srvy_yr2) + '–' + str(srvy_yr1)
                                            plt.figure(1, figsize=fig_sz)
                                            ax = plt.gca()
                                            ax.scatter(df_srvy_yr1_x, df_dpth_rt_chng_x, c=clr1, marker=mrkr1, alpha=alpha,edgecolors=None, label=lbl)
                                            plt.xlabel('Survey year', fontsize=fntsz_ax, labelpad=lbl_pd)  # Creates x-axis label. Sets format.
                                            plt.ylabel('Aggradation rate change',fontsize=fntsz_ax)  # Creates y-axis label. Sets format.
                                            plt.yticks(fontsize=fntsz_tcks)  # Sets y-axis ticks. Sets format.
                                            plt.pause(1)
                                            # plot_lines(1, 7, fig_sz, df_srvy_yr1_x, df_dpth_rt_chng_x, lbl, clr1, mrkr1,
                                            #            mrkr_sz, lin_wdth, lin_styl[0], alpha, 1, lctn, mrkr_scl,
                                            #            frm_alpha,
                                            #            lbl_spcng, 1, fntsz_tcks, 'Survey year',
                                            #            fntsz_ax, lbl_pd,
                                            #            'Average aggradation rate change', title, 1,
                                            #            5)  # Creates plot. Calls function.

                                        # EXPORT FIGURE --------------------------------------------------------------------

                                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                                        # Defines list. Sets folder labels for directory to be made.
                                        df_srvy_yrs2 = slice_DataFrame_columns(df_sed_thck, 'Srvy_year2', 1,
                                                                               'Survey years',
                                                                               0)  # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of present dataset.
                                        srvy_yrs2 = df_srvy_yrs2.tolist()  # Defines list. Converts DataFrame to list.
                                        if rng_nly == 1:
                                            fig_name = '/D_rt_chng_' + str(rng_name1) + '_' + str(srvy_yrs2[-1]) + '–' + str(
                                                srvy_yrs[0]) + '.pdf'
                                        elif rng_nly == 0:
                                            fig_name = '/D_rt_chng_' + str(srvy_yrs2[-1]) + '–' + str(
                                                srvy_yrs[0]) + '.pdf'  # Defines
                                        # variable as strIng. Sets name of figure for export.
                                        if rvr_nly == 1:
                                            fig_name = '/D_rt_chng_' + str(chnl_name) + '_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'
                                        elif rvr_nly == 0:
                                            fig_name = '/D_rt_chng_' + str(srvy_yrs2[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines
                                        export_file_to_directory(1, 'figure', 3, fldr_lbls, opt_fldr,
                                                                 'Directories named: ', fig_name, 1, 'pdf', None, None,
                                                                 'Average sediment thickness plot',0)

