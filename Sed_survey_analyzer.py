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

import time, os, sys  # Imports "Time and access conversions", "Miscellaneous operating system interfaces", and
# "System specific parameters and functions". Enables use of various time–related functions and operating system
# dependent functionality.
import pandas as pd, numpy as np, matplotlib.pyplot as plt  # Imports "Python data analysis library", a comprehensive
# mathematics library, and a plotting interface, with alias. Enables DataFrame array functionality.
from Cross_section_analyzer import *

# START TIMER ----------------------------------------------------------------------------------------------------------

strtTm0 = time.time()  # Starts clock. Measures program run time.

# CHOOSE OPERATIONS ----------------------------------------------------------------------------------------------------

# Single cross-section -------------------------------------------------------------------------------------------------
# Xsctns_1 = 1  # Defines variable as integer. Sets binary toggle for operation selection.

# Plots single cross-section
Xsctn_sngl = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Calculate channel hydraulic geometry
Hydr_geom = 1  # Defines variable as integer. Sets binary toggle for operation selection.

# Plots hydraulic radius per year as a function of distance upstream
Hydr_rad = 1  # Defines variable as integer. Sets binary toggle for operation selection.

# Subsequent cross-sections --------------------------------------------------------------------------------------------
Xsctns_2 = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Plots subsequent cross-sections
Xsctn_dbl = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# SET PARAMETERS -------------------------------------------------------------------------------------------------------

# Data selection -------------------------------------------------------------------------------------------------------

# Field ranges
rng_strt = 70  # Defines variable as integer. Sets starting range for looping analysis.
rng_end = 73  # Defines variable as integer. Sets end range for looping analysis.

# Range surveys
srvy_strt = 5  # Defines variable as integer. Sets starting survey for looping analysis.
srvy_end = 2  # Defines variable as integer. Sets end survey for looping analysis.

# Data plotting --------------------------------------------------------------------------------------------------------

# General
wdth = 4.5  # Defines variable as integer. Sets plot width.
hght = wdth * 1.618  # Defines variable as integer. Sets plot height.
fig_sz = (hght, wdth)  # Defines object. Input for function. Sets plot size.

# Axes
fntsz_tcks = 8  # Defines variable as integer. Sets font size for axes tick marks.
fntsz_ax = 10  # Defines variable as integer. Sets font size for axes labels.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Display
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDD']
# Defines list. Sets Paul Tol muted colorblind friendly palette via hex color codes.
lin_wdth = 2  # Defines variable as integer. Sets plot line width.
mrkrs = [' ', 'v', 'P', 'o', 'X', 's', '^', 'D', '<', '>', '8', 'p', 'h', 'H', 'd']  # Defines list. Sets matplotlib
# plot markers.
mrkr_sz = 4  # Defines variable as integer. Sets plot marker size.
alpha = 0.5  # Defines variable as integer. Sets plotted object transparency.

# Legend
lctn = 'best'  # Defines variable as string. Sets legend location on plot automatically.
mrkr_scl = 2  # Defines variable as integer. Sets marker size.
frm_alpha = 0.7  # Defines variable as integer. Sets box transparency.
lbl_spcng = 0.7  # Defines variable as integer. Sets object spacing.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Name levels ----------------------------------------------------------------------------------------------------------

# Level 1
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Create folders -------------------------------------------------------------------------------------------------------

lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.

for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    level = 1  # Defines variable. Sets value based in list element index for display.

    create_folder(level, a)  # Creates folders. Calls function.

# ======================================================================================================================
# PART 2: DATA SELECTION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# UPLOAD DATA ----------------------------------------------------------------------------------------------------------

inpt_fl = '/Users/jimmywood/github/Whitewater_MN_sedimentation/PyCharm_Venv/Input/Trout_Creek_survey_data.csv'
# Defines string. Sets file path.

df_chnnl = upload_csv(inpt_fl, 'TROUT CREEK ', 0)  # Defines DataFrame. Calls function. Loads survey data.

# SET DATA SELECTION LIMITS --------------------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------

rgn_nums = forward_range(rng_strt, rng_end, 1, 'Range number limits', 0)  # Defines array. Calls function. Sets loop
# order by range.

# Temporal -------------------------------------------------------------------------------------------------------------

srvy_nums = reverse_range(srvy_strt, srvy_end, -1, 'Survey number limits', 0)  # Defines array. Calls function. Sets
# loop order by survey.

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# By field range -------------------------------------------------------------------------------------------------------

for a in rgn_nums:  # Begins loop for array. Loops through range numbers.

    df_rng = slice_DataFrame_rows1(df_chnnl, 'Range_num', a, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to contain singular range data only.

    # Range metadata
    rng_name1 = slice_DataFrame_cell(df_rng, 'Srvy_range', 'Range', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield range number of present dataset.

    df_srvy_nums = slice_DataFrame_columns1(df_rng, 'Srvy_num', 'Survey numbers', 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to contain all survey numbers of present dataset.
    df_srvy_nums = df_srvy_nums.drop_duplicates(keep='first')  # Modifies DataFrame. Drops all duplicate values in
    # column.
    num_srvys = max_value_column(df_srvy_nums, '', '', 0)  # Defines variable. Calls function. Slices DataFrame to
    # yield total number of range surveys.

    strm_stat1 = slice_DataFrame_cell(df_rng, 'Srvy_stat', 'Stream station', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey station of river segment.

    # By range survey --------------------------------------------------------------------------------------------------

    for b in srvy_nums:  # Begins loop. Loos through survey numbers.

        df_srvy1 = slice_DataFrame_rows2(df_rng, 'Srvy_num', b, 'SURVEY NUMBER', a, 'RANGE NUMBER', 0)  # Defines
        # DataFrame. Calls function. Slices DataFrame to contain singular range survey data only.

        # Survey metadata
        srvy_yr1 = slice_DataFrame_cell(df_srvy1, 'Srvy_year', 'Survey year', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield survey year of present dataset.

        srvy_dt1 = slice_DataFrame_cell(df_srvy1, 'Srvy_date', 'Survey date', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield survey date of present dataset.

        # Survey data --------------------------------------------------------------------------------------------------

        df_offst1 = slice_DataFrame_columns1(df_srvy1, 'Offset_ft', 'OFFSET', 0)  # Defines DataFrame. Calls function.
        # Slices DataFrame to contain survey offsets only.
        df_elvtn1 = slice_DataFrame_columns1(df_srvy1, 'Elv_geo_ft', 'ELEVATION', 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to contain survey elevations only.

        # DISPLAY DATASET ----------------------------------------------------------------------------------------------

        # if Xsctns_1 == 1:  # Conditional statement. Carries out single cross-section analysis.

        # Dataset metadata ---------------------------------------------------------------------------------------------

        print('==================================================')  # Displays objects. Communicates present dataset
        # undergoing analysis to programmer.
        print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_name1) + ' (' + str(a) + ')')  # Displays objects.
        print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1))  # Displays objects.
        print('\033[1m' + 'Range survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(b) + ' of ' + str(num_srvys) + ')')
        # Displays objects.
        print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1))  # Displays objects.
        print('--------------------------------------------------')  # Displays objects.

        # Plot dataset -------------------------------------------------------------------------------------------------

        if Xsctn_sngl == 1:  # Conditional statement. Plots single cross-section.

            clr1 = get_plot_format_by_year(srvy_yr1, tol_mtd, 0)  # Defines variable. Calls function. Sets plot color.
            mrkr1 = get_plot_format_by_year(srvy_yr1, mrkrs, 0)  # Defines variable. Calls function. Sets plot marker
            # type.
            title1 = 'Range ' + str(rng_name1) + ' ' + str(srvy_yr1) + ' survey '  # Defines string. Sets title of
            # plot.

            plot_lines(1, 1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz, lin_wdth, alpha, 0, lctn,
                       mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd,
                       'Surface elevation (ft)', title1, 1, 1)  # Creates plot. Calls function.

            # EXPORT DATA ----------------------------------------------------------------------------------------------

            exprt = 1  # Defines variable. Local export binary toggle.

            if exprt == 1:  # Conditional statement. Exports figure.

                # Name levels ------------------------------------------------------------------------------------------

                # Level 2
                xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory
                # where all cross-section data will be exported.
                lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 3
                plts_fldr = '/Plots'  # Defines variable as string. Sets name of new directory where all cross-section
                # data will be exported.
                lvl3 = lvl2 + plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 4
                xsctn_plts_fldr = '/Cross_sections'  # Defines variable as string. Sets name of new directory where all
                # cross-section data will be exported.
                lvl4 = lvl3 + xsctn_plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 5
                xsctn_plts_fldr1 = '/Single'  # Defines variable as string. Sets name of new directory where all
                # cross-section data will be exported.
                lvl5 = lvl4 + xsctn_plts_fldr1  # Defines variable as string. Concatenates strings to create file path.

                # Create folders ---------------------------------------------------------------------------------------

                lvls = [lvl2, lvl3, lvl4, lvl5]  # Defines list. For looping through and conventient folder creation.

                for i in lvls:  # Begins loop. Loops through each element in list.
                    level = lvls.index(i)  # Defines variable. Sets value based in list element index for display.

                    create_folder(level, i)  # Creates folder. Calls function.

                # Export figure ----------------------------------------------------------------------------------------

                plt.figure(1)  # Calls figure. Makes it the active plot.

                fig_name = '/' + str(rng_name1) + '_s' +str(b) + '_' + str(srvy_yr1) + '.pdf' # Defines variable as
                # strong. Names figure for export.

                plt.savefig(lvl5 + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

                plt.close()  # Closes active figure.

        # ==============================================================================================================
        # PART 3: DATA ANALYSIS ----------------------------------------------------------------------------------------
        # ==============================================================================================================

        # CALCULATE HYDRAULC GEOMETRY ==================================================================================

        if Hydr_geom == 1: # Conditional statement. Calculates hydraulic geometry.

            df_strm = slice_DataFrame_rows1(df_srvy1, 'Gmrph_dsc', 'Stream channel', 'RANGE ' + str(a), 0)  # Defines
            # DataFrame. Calls function.

            wdth, dpth, hydro_rad = hydraulic_geometry(df_strm, 'Offset_ft', 'RANGE ' + str(a) + ' SURVEY ' + str(b) +
                                                       ' STREAM CHANNEL OFFSET', 'Offset', ' (ft)',
                                                       'Channel dimensions', 'Width: ', 'Elv_geo_ft', 'RANGE ' + str(a)
                                                       + ' SURVEY ' + str(b) + ' STREAM CHANNEL ELEVATION',
                                                       'Elevation', 'Depth: ', 'Bankfull hydraulic radius: ', 1)

            # EXPORT DATA ----------------------------------------------------------------------------------------------

            # Compile data to lists ------------------------------------------------------------------------------------

            # Create lists for population
            if a == rng_strt:  # Conditional statement. Executes on first range only.
                if b == srvy_strt:  # Conditional statement. Executes on first survey only of first range.
                    rng_name1_list = []  # Defines list. Empty for later population.
                    srvy_yr1_list = []  # Defines list. Empty for later population.
                    strm_stat_list = []  # Defines list. Empty for later population.
                    hydro_rad_list = []  # Defines list. Empty for later population.
                    wdth_list = []  # Defines list. Empty for later population.
                    dpth_list = []  # Defines list. Empty for later population.
                    dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, strm_stat_list, wdth_list, dpth_list,
                                       hydro_rad_list]  # Defines list. Nested to enabling looping population.

            dtfrm_pop_values=[rng_name1, srvy_yr1, strm_stat1, wdth, dpth, hydro_rad]   # Defines list. Sets values to
            # populate lists.
            dtfrm_pop_dt_lbl=['Range name', 'Survey year', 'Stream station', 'Width', 'Depth', 'Hydraulic radius']
            # Defines list. Sets labels for display.
            dtfrm_pop_clm_lbl=['Srvy_range', 'Srvy_year', 'Strm_stat', 'Chnl_wdth_ft', 'Chnl_dpth_ft', 'Hydro_rad_ft']
            # Defines list. Sets column labels for DataFrame.

            # Populate lists
            for i in dtfrm_pop_lists:  # Begins loop. Through empty lists.
                index = dtfrm_pop_lists.index(i)  # Defines variable. Retrieves index of list element for appropriate
                # selection.
                i = create_appended_list(dtfrm_pop_values[index], dtfrm_pop_dt_lbl[index], i, 'New list appended: ', 0)
                # Calls function. Populates empty list with corresponding value.

            if a == rng_end:  # Conditional statement. Executes on last range only.
                if b == srvy_end:  # Conditional statement. Executes on first survey only of last range.

                    dtfrm_pop_lists = [rng_name1_list, srvy_yr1_list, strm_stat_list, wdth_list, dpth_list,
                                       hydro_rad_list]  # Defines list. Redefines with populated lists.

                    # Compile lists in DataFrame -----------------------------------------------------------------------

                    dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array for operation.
                    dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Defines array. Transposes array for DataFrame
                    # dimensional compatibility.

                    # Create DataFrame from lists ----------------------------------------------------------------------
                    df_hydro_geom = create_DataFrame_frm_arry(dtfrm_pop_arry, dtfrm_pop_clm_lbl, 'HYDRAULIC GEOMETRY',
                                                              1)  # Defines DataFrame. Calls function.

                    exprt = 0  # Defines variable. Local export binary toggle.

                    if exprt == 1:  # Conditional statement. Exports figure.

                        # Name levels ----------------------------------------------------------------------------------

                        # Level 2
                        xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new
                        # directory where all cross-section data will be exported.
                        lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file
                        # path.

                        # Level 3
                        clcs_fldr = '/Calculations'  # Defines variable as string. Sets name of new directory where all
                        # cross-section data will be exported.
                        lvl3 = lvl2 + clcs_fldr  # Defines variable as string. Concatenates strings to create file path.

                        # Level 4
                        h_geom_clcs_fldr = '/Hydraulic_geometry'  # Defines variable as string. Sets name of new
                        # directory where all cross-section data will be exported.
                        lvl4 = lvl3 + h_geom_clcs_fldr  # Defines variable as string. Concatenates strings to create
                        # file path.

                        # Create folders -------------------------------------------------------------------------------

                        lvls = [lvl2, lvl3, lvl4]  # Defines list. For looping through and conventient folder creation.

                        for i in lvls:  # Begins loop. Loops through each element in list.
                            level = lvls.index(i)  # Defines variable. Sets value based in list element index for
                            # display.

                            create_folder(level, i)  # Creates folder. Calls function.

                        # Export table ---------------------------------------------------------------------------------

                        fl_name = '/Hydraulic_geometry.csv'  # Defines variable as string. Names and sets extension for
                        # table for export.

                        df_hydro_geom.to_csv(lvl4 + fl_name, index=False)  # Saves table to directory.

                    # PLOT DATA ----------------------------------------------------------------------------------------

                    if Hydr_rad == 1:  # Conditional statement. Plots hydraulic radius by year as a function of distance upstream.

                        # select years for selection
                        df_srvy_yrs = slice_DataFrame_columns1(df_hydro_geom, 'Srvy_year', 'Survey years', 0)
                        df_srvy_yrs = df_srvy_yrs.drop_duplicates(keep='first')
                        srvy_yrs = df_srvy_yrs.tolist()
                        print(df_srvy_yrs)

                        for i in srvy_yrs:
                            df_chnl_geom_i = slice_DataFrame_rows1(df_hydro_geom, 'Srvy_year', i, 'HYDRAULIC GEOMETRY', 1)
                            df_h_rad_i = slice_DataFrame_columns1(df_chnl_geom_i, 'Hydro_rad_ft', 'HYDRAULIC RADIUS', 1)
                            df_h_rad_i = df_h_rad_i.astype(float)
                            df_strm_stat_i = slice_DataFrame_columns1(df_chnl_geom_i, 'Strm_stat', 'STREAM STATION', 1)
                            srvy_yr = slice_DataFrame_cell(df_chnl_geom_i, 'Srvy_year', 'Survey year', 1)

                            clr1 = get_plot_format_by_year(srvy_yr, tol_mtd, 0)  # Defines variable. Calls function. Sets plot color.
                            mrkr1 = get_plot_format_by_year(srvy_yr, mrkrs, 1)  # Defines variable. Calls function. Sets plot marker type.

                            title1 = 'Hydraulic radius evolution: Trout Creek'  # Defines string. Sets title of plot.

                            plot_lines(1, 2, fig_sz, df_strm_stat_i, df_h_rad_i, srvy_yr, clr1, mrkr1, mrkr_sz,
                                       lin_wdth, alpha, 1, lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz_tcks,
                                       'River station', fntsz_ax, lbl_pd, 'Hydraulic radius (ft)', title1, 1,
                                       1)  # Defines function. For cross-section plotting.

                        # EXPORT DATA ----------------------------------------------------------------------------------------------

                        exprt = 1  # Defines variable. Local export binary toggle.

                        if exprt == 1:  # Conditional statement. Exports figure.

                            # Name levels ------------------------------------------------------------------------------------------

                            # Level 2
                            xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory
                            # where all cross-section data will be exported.
                            lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file path.

                            # Level 3
                            plts_fldr = '/Plots'  # Defines variable as string. Sets name of new directory where all cross-section
                            # data will be exported.
                            lvl3 = lvl2 + plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                            # Level 4
                            xsctn_plts_fldr = '/Hydraulic_radius'  # Defines variable as string. Sets name of new directory where all
                            # cross-section data will be exported.
                            lvl4 = lvl3 + xsctn_plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                            # Create folders ---------------------------------------------------------------------------------------

                            lvls = [lvl2, lvl3, lvl4]  # Defines list. For looping through and conventient folder creation.

                            for i in lvls:  # Begins loop. Loops through each element in list.
                                level = lvls.index(i)  # Defines variable. Sets value based in list element index for display.

                                create_folder(level, i)  # Creates folder. Calls function.

                            # Export figure ----------------------------------------------------------------------------------------

                            plt.figure(2)  # Calls figure. Makes it the active plot.

                            fig_name = '/R_h_' + str(srvy_yrs[-1]) + '–' + str(srvy_yrs[0]) + '.pdf'  # Defines variable as
                            # strong. Names figure for export.

                            plt.savefig(lvl4 + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

                            plt.close()  # Closes active figure.

        # Calculate sediment thickness
        if Xsctns_2 == 1:

            # Create second dataset
            c=b-1  # Defines variable. Allows for selection of two datasets for change detection.

            #survey
            df_srvy2 = slice_DataFrame_rows2(df_rng, 'Srvy_num', c, 'SURVEY NUMBER', a, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.

            #metadata
            index = df_srvy2.index  # Defines variable. Retrieves index of DataFrame.
            srvy_yr2 = slice_DataFrame_cell(df_srvy2, 'Srvy_year', index[0], 'Survey year', 0)  # Defines variable. Calls function.
            srvy_dt2 = slice_DataFrame_cell(df_srvy2, 'Srvy_date', index[0], 'Survey date', 0)  # Defines variable. Calls function.

            # Measurements
            df_offst2 = slice_DataFrame_columns1(df_srvy2, 'Offset_ft', 'OFFSET', 0)  # Defines DataFrame. Calls function.
            df_elvtn2 = slice_DataFrame_columns1(df_srvy2, 'Elv_geo_ft', 'ELEVATION', 0)  # Defines DataFrame. Calls function.

            # DISPLAY DATASET ------------------------------------------------------------------------------------------

            # Metadata ------------------------------------------------------------------------------------------
            print('==================================================')  # Displays objects.
            print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_nm1) + ' (' + str(a) + ')')  # Displays objects.
            print('\033[1m' + 'Range surveys: ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' + str(b) + '–' + str(c) + ' of ' + str(num_srvys) + ')')  # Displays objects.
            print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.

            # Plot data ------------------------------------------------------------------------------------------

            if Xsctn_dbl == 1:  # Conditional statement. Plots single cross-section.
                clr1 = get_color(srvy_yr1)
                mrkr1 = get_marker(srvy_yr1)
                clr2 = get_color(srvy_yr2)
                mrkr2 = get_marker(srvy_yr2)

                title1 = 'Range ' + str(rng_nm1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' surveys'  # Defines string. Sets title of plot.

                plot_lines(2, 2, fig_sz, [df_offst1, df_offst2], [df_elvtn1,df_elvtn2], [srvy_yr1,srvy_yr2], [clr1,clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title1, ps_lngth, 1,lctn, mrkr_scl, frm_alpha, lbl_spcng)  # Creates plot. Calls function.

                # Export figure
                # Name folders
                # Level 2
                xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 3
                plts_fldr = '/Plots'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl3 = lvl2 + plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 4
                xsctn_plts_fldr = '/Cross_sections'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl4 = lvl3 + xsctn_plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 5
                xsctn_plts_fldr1 = '/Double'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl5 = lvl4 + xsctn_plts_fldr1  # Defines variable as string. Concatenates strings to create file path.

                # Create folders
                lvls = [lvl2, lvl3, lvl4, lvl5]  # Defines list. For looping through and conventient folder creation.

                for i in lvls:  # Begins loop. Loops through each element in list.  #
                    level = lvls.index(i)  # Defines variable. Sets value based in list element index for display.
                    create_folder(level, i)  # Creates folder. Calls function.

                # Export
                if Exprt==1:
                    plt.figure(2)  # Calls figure. Makes it the active plot.

                    fig_name = '/' + str(rng_nm1) + '_s' + str(b) + '–' + str(c) + '_' + str(srvy_yr1) + '–' + str(srvy_yr2) + '.pdf' # Defines variable as strong. Names figure for export.

                    plt.savefig(lvl5 + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

                    plt.close()  # Closes active figure.