# ======================================================================================================================
# WHITEWATER RIVER VALLEY, MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * --------------------------------------------
# ANALYSIS PROGRAM * ---------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

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
Plt_crdnts = 0  # Defines variable as integer. Sets binary toggle.

# Dual cross-sections analysis -----------------------------------------------------------------------------------------

Dbl = 1  # Defines variable as integer. Sets binary toggle.

# Plot dual cross-sections
Plt_dbl = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual interpolated cross-sections
Plt_intrp = 0  # Defines variable as integer. Sets binary toggle.
# Plot dual re-interpolated cross-sections
Plt_reintrp = 0  # Defines variable as integer. Sets binary toggle.

# Calculate sediment thickness from surface profiles
Dpth = 1  # Defines variable as integer. Sets binary toggle.

# Plot sediment thickness distribution
Plt_dpth_dst = 0  # Defines variable as integer. Sets binary toggle.
# Plot sediment thickness
Plt_dpth = 0  # Defines variable as integer. Sets binary toggle.
# Plot sedimentation rate
Plt_sed_rt = 0  # Defines variable as integer. Sets binary toggle.

Ststcs = 1

# SELECT INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Limits of analysis ---------------------------------------------------------------------------------------------------

rvr_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one river channel only.
rng_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one survey range only.
xtra_srvys = 0  # Defines variable as integer. Sets binary toggle. Analyzes extra survey data for range 11B (13).
rng_strt = 1  # Defines variable as integer. Sets start survey range number for analysis loop.
rng_end = 94 # Defines variable as integer. Sets end survey range number for analysis loop.
cmltv = 0  # Defines variable as integer. Sets binary toggle. Calculates cumulative sedimentation between survey
# limits.

# Conversion factors ---------------------------------------------------------------------------------------------------

deg_to_rad = math.pi / 180  # Defines variable as float. Converts between degrees and radians.
ft_m = 3.281  # Defines variable as float. Converts between international feet meters.
in_ft = 12  # Defines variable as integer. Converts between inches and feet.
mi_km = 1.609  # Defines variable as float. Converts between miles and kilometers.
cm_m = 1000  # Defines variable as integer. Converts between centimeters and meters.

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

inpt_fl1 = inpt_fldr + '/Test_data_transformed.csv'  # Defines string. Sets file path to input file.

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

    strm_stat1, strm_stat1_m = slice_DataFrame_cell('Integer', 1, 1/ft_m,  df_rng, 0, 'Srvy_stat', 'Stream station',
                                                    0)  # Defines variable. Calls function. Slices DataFrame to yield
    # survey station of transect on reach.

    wshd_A, wshd_A_mi = slice_DataFrame_cell('Float', 1, (1/mi_km)**2, df_wshd_A, 0, 'Wshd_A_sqkm',
                                             'Transect drainage area', 0)  # Defines variable. Calls function. Slices
    # DataFrame to yield drainage area of transect on reach.

    srvy_nums1 = slice_DataFrame_columns('List', 'Integer', df_rng, 'Srvy_num', 1, 0, 'SURVEY NUMBERS', 0)  # Defines
    # list. Calls function. Slices DataFrame to yield survey numbers of present dataset.

    if cmltv == 1:  # Conditional statement. Analyzes cumulative sedimentation instead of step.
        if len(srvy_nums1) > 2:  # Conditional statement. Slices if condition satisfied.
            del srvy_nums1[1:-1]  # Redefines list. Removes all but first and last elements. Takes all but first and
            # last surveys out of analysis.
    else:  # Conditional statement.
        if xtra_srvys == 1:  # Conditional statement. Modifies survey years under analysis. For transect 11B (13) with
            # extra survey years compared to all other ranges.
            pass  # Pass command. Moves on to next line.
        elif xtra_srvys == 0:  # Conditional statement. Modifies survey years under analysis.
            if i == 13:  # Conditional statement.
                srvy_nums1.remove(5)  # Redefines list. Removes survey inconsistent survey year.
                srvy_nums1.remove(4)  # Redefines list. Removes survey inconsistent survey year.

    srvy_nums_max = len(srvy_nums1)  # Defines variable. Selects maximum survey number.

    # Select survey dataset
    for j in srvy_nums1:  # Establishes loop through array elements. Loops through survey numbers.
        df_srvy1 = slice_DataFrame_rows('Equals', df_rng, 'Srvy_num', j, 'SURVEY NUMBER', 0)  # Defines DataFrame.
        # Calls function. Slices DataFrame to yield singular survey data.
        df_splt_cls_strt1 = slice_DataFrame_rows('Equals', df_srvy1, 'Rng_splt', 'Split', 'SPLIT POINT', 0)
        # Defines DataFrame. # Calls function. Slices DataFrame to yield starting split point.
        df_splt_cls_end1 = slice_DataFrame_rows('Equals', df_srvy1, 'Rng_splt', 'Zip', 'ZIP POINT', 0)
        # Defines DataFrame. # Calls function. Slices DataFrame to yield end split point.

        # Retrieve metadata
        srvy_yr1 = slice_DataFrame_cell('Integer', 0, None, df_srvy1, 0, 'Srvy_year', 'Survey year', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey year of present dataset.
        srvy_dt1 = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Srvy_date', 'Survey date', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey date of present dataset.
        srvy_typ1 = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Srvy_type', 'Survey type', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield survey type of present dataset.
        # Select survey measurements
        if j > 0:
            df_offst1 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy1, 'Offset_ft', 0, 0, 'OFFSET', 0)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield survey offsets of present dataset.
            df_elvtn1 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy1, 'Elv_geo_ft', 0, 0, 'ELEVATION', 0)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield survey elevations of present dataset.
        else:
            brng_in_arry1 = slice_DataFrame_columns('Array', 'Float', df_srvy1, 'Brhl_fl_in', 0, 1,
                                                   'Borehole depths (in)', 0)  # Defines array. Calls function. Slices DataFrame to yield borehole fill depths in inches of present dataset.
            brng_ft_arry1 = slice_DataFrame_columns('Array', 'Float', df_srvy1, 'Brhl_fl_ft', 0, 1, 'Borehole depths (ft)', 0)

            if np.any(brng_in_arry1) == False:  # Conditional statement. Selects non-empty set of borings for calculations.
                del brng_in_arry1  # Deletes array.
                brng_arry1 = brng_ft_arry1  # Defines array. Selects non-empty array.
                unts1 = 'Feet'  # Defines variable. For unit conversion.
            if np.any(brng_ft_arry1) == False:  # Conditional statement. Selects non-empty set of borings for calculations.
                del brng_ft_arry1  # Deletes array.
                brng_arry1 = brng_in_arry1  # Defines array. Selects non-empty array.
                unts1 = 'Inches'  # Defines variable. For unit conversion.

        # Retrieve metadata
        if j > 0:
            offst_min1 = min_value_DataFrame('Float', df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield first offset of present dataset.
            offst_max1 = max_value_DataFrame('Float', df_offst1, 'Offset', 0)  # Defines variable. Calls function. Slices
            # DataFrame to yield last offset of present dataset.
            elvtn_min1 = min_value_DataFrame('Float', df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function.
            # Slices DataFrame to yield lowest elevation of present dataset.
            elvtn_max1 = max_value_DataFrame('Float', df_elvtn1, 'Elevation', 0)  # Defines variable. Calls function.
            # Slices DataFrame to yield highest elevation of present dataset.
            num_smpls1 = df_srvy1.shape[0]  # Defines variable. Returns dimensionality of DataFrame.
        else:
            num_smpls1 = len(brng_arry1)

        brng_r_dir = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_R_dir',
                                          'Bearing reference direction: ', 0)   # Defines variable. Calls function.
        # Slices DataFrame to yield bearing reference direction of present dataset.
        brng_angl = slice_DataFrame_cell('Float', 0, None, df_srvy1, 0, 'Brng_A', 'Bearing angle: ', 0)   # Defines
        # variable. Calls function. Slices DataFrame to yield bearing angle of present dataset.
        brng_a_dir = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_A_dir', 'Bearing angle direction: ', 0)
        # Defines variable. Calls function. Slices DataFrame to yield bearing angle direction of present dataset.
        brng_fnctl = slice_DataFrame_cell('String', 0, None, df_srvy1, 0, 'Brng_fnctl', 'Functional bearing: ', 0)
        # Defines variable. Calls function. Slices DataFrame to yield functional bearing directions of present dataset.

        if df_splt_cls_strt1.empty and df_splt_cls_end1.empty == True:  # Conditional statement. Executes lines if split clause exists.
            splt_pnt1 = None  # Defines variable. Sets to null. For later selection.
            splt_pnt1_m = None  # Defines variable. Sets to null. For later selection.
            zip_pnt1 = None  # Defines variable. Sets to null. For later selection.
            zip_pnt1_m = None  # Defines variable. Sets to null. For later selection.
        else:  # Conditional statement.
            splt_pnt1 = slice_DataFrame_cell('Float', 0, None, df_splt_cls_strt1, 0, 'Offset_ft', 'Transect split point: ', 0)  # Defines variable. Calls function. Retrieves position of split point.
            splt_pnt1_m = splt_pnt1 / ft_m  # Defines variable. Converts feet to meters.
            zip_pnt1 = slice_DataFrame_cell('Float', 0, None, df_splt_cls_end1, 0, 'Offset_ft', 'Transect zip point: ', 0)  # Defines variable. Calls function. Retrieves position of zip point.
            # Defines variable. Calls function. Slices DataFrame to yield split clause.
            zip_pnt1_m = zip_pnt1 / ft_m  # Defines variable. Converts feet to meters.

        rng_lngth1 = offst_max1 - offst_min1  # Defines variable. Calculates survey length.
        rng_lngth1_m = rng_lngth1 / ft_m  # Defines variable. Converts to meters.
        srvy_rlf1 = elvtn_max1 - elvtn_min1  # Defines variable. Calculates survey relief.
        srvy_rlf1_m = srvy_rlf1 / ft_m  # Defines variable. Converts to meters.

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
            if j > 0:
                print('\033[1m' + 'Survey length: ' + '\033[0m' + str('%.2f' % rng_lngth1) + ' ft' +
                      ' (' + str('%.0f' % rng_lngth1_m) + ' m)')  # Displays objects.
                print('\033[1m' + 'Survey relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' ft' +
                      ' (' + str('%.0f' % srvy_rlf1_m) + ' m)')  # Displays objects.
            try:  # Conditional statement. Executes lines based on existence of object.
                splt_pnt1  # Defines object.
                if splt_pnt1 != None:  # Conditional statement. Executes lines if object exits and is not null.
                    print('\033[1m' + 'Split points: ' + '\033[0m' + str('%.2f' % splt_pnt1) + ' & ' +
                          str('%.2f' % zip_pnt1) + ' ft ' + '(' + str('%.2f' % splt_pnt1_m) + ' & ' +
                          str('%.2f' % zip_pnt1_m) + ' m)')  # Displays objects.
            except NameError:  # Conditional statement. Executes lines if object does not exist.
                pass  # Pass command. Moves on to next line.
            print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.

            if j > 0:  # Conditional statement. Executes lines for surface profiles only.
                # Cross-section --------------------------------------------------------------------------------------------
                if Plt_sngl == 1:  # Conditional statement. Plots single cross-section.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')' + ' ' + str(srvy_yr1) + ' survey '
                    # Defines string. Sets plot title.

                    plot_lines(1, 1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz[0], lin_wdth[0],
                               lin_styl[0], alpha[0], 0, lctn, mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                               'Survey offset (ft)', fntsz[0], lbl_pd, 'Surface elevation (ft)', title, 1, 1)
                    # Creates plot. Calls function.

                    # Export data
                    fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Single', '/' + chnl_name]
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/' + str(rng_name1) + '_s' + str(j) + '_' + str(srvy_yr1) + '.pdf'  # Defines variable
                    # as strIng. Sets name of figure for export.

                    export_file_to_directory(1, 'Figure', 5, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1,
                                             'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)  # Creates
                    # directory and exports figure. Calls function.

                # All cross-sections -----------------------------------------------------------------------------------

                if Plt_all == 1:  # Conditional statement. Plots all cross-sections on transect.
                    clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color ', 0)  # Defines variable. Calls
                    # function. Sets plot color.
                    mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker ', 0)  # Defines variable. Calls
                    # function. Sets plot marker type.

                    title = 'Range ' + str(rng_name1) + ' (' + str(i) + ')'  # Defines string. Sets plot title.

                    plot_lines(1, 2, fig_sz, df_offst1, df_elvtn1, srvy_yr1, clr1, mrkr1, mrkr_sz[0], lin_wdth[0],
                               lin_styl[0], alpha[0], 1, lctn, mrkr_scl, frm_alpha, lbl_spcng, fntsz[-1],
                               'Survey offset (ft)', fntsz[0], lbl_pd, 'Surface elevation (ft)', title, 1, 0.5)
                    # Creates plot. Calls function.

                    # Export data
                    if j == 1:  # Conditional statement. Exports only when final cross-section has been
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
                    if srvy_typ1 == 'Lidar':  # Conditional statement. Performs calculations for lidar data only.
                        srvy_typ_prv = srvy_typ1  # Defines variable.

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

                        azmth_deg_meas, azmth_deg_cor, azmth_deg_dff, sin, cos = transect_orientation(BM1_e, BM2_e,
                                                                                                      BM1_n, BM2_n,
                                                                                                      brng_r_dir,
                                                                                                      brng_a_dir,
                                                                                                      brng_angl,
                                                                                                      brng_fnctl, 0)
                        # Defines variables. Calls function. Calculates trigonometric components of transect from GPS
                        # points.

                        # TRANSFORM MEASUREMENT OFFSETS --------------------------------------------------------------------

                        if BM1_off == BM1_crd_off:  # Conditonal statement. Selects standard to transform offsets.
                            df_offst1_shft = df_offst1 - BM1_off  # Defines DataFrame. Shifts measurement offsets by
                            # benchmark position.
                        else:  # Conditional statement.
                            df_offst1_shft = df_offst1 - BM1_crd_off  # Defines DataFrame. Shifts measurement offsets by
                            # benchmark position.
                        df_offst1_shft_m = df_offst1_shft / ft_m  # Defines DataFrame. Converts feet to meters.

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

                        crd1_e = slice_DataFrame_cell('Float', 0, None, df_e, 0, None, 'Measurement 1 Easting (m): ', 0)
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

                        lgnth_prcnt_dff = coordinate_error(crd1_e, crd2_e, crd1_n, crd2_n, rng_lngth1_m, 0)  # Defines
                        # variable. Calculates percent difference between field measured and GPS calculated transect
                        # lengths.

                        rng_end_shft, rng_10_shft = orientation_error(rng_lngth1, azmth_deg_dff, 0)  # Defines
                        # variable. Calculates lateral shift along transect due to measured and calculated azimuth
                        # difference.

                        # UPDATE FILE --------------------------------------------------------------------------------------

                        df_srvy1 = pd.concat([df_srvy1, df_e, df_n], axis=1)  # Redefines DataFrame. Concatenates
                        # coordinates to survey DataFrame.

                        # Save data
                        if i == rng_strt:  # Conditional statement. Executes for first range only.
                            try:  # Checks for existence of object.
                                srvy_typ_prv  # Defines object to be searched for.

                                chnl_name_lst = []  # Defines list. Empty for looped population.
                                chnl_abrv_lst = []  # Defines list. Empty for looped population.
                                rng_name1_lst = []  # Defines list. Empty for looped population.
                                rng_num_lst = []  # Defines list. Empty for looped population.
                                srvy_yr1_lst = []  # Defines list. Empty for looped population.
                                brng_lst = []  # Defines list. Empty for looped population.
                                azmth_deg_meas_lst = []  # Defines list. Empty for looped population.
                                azmth_deg_cor_lst = []  # Defines list. Empty for looped population.
                                azmth_deg_dff_list = []  # Defines list. Empty for looped population.
                                rng_end_shft_lst = []  # Defines list. Empty for looped population.
                                rng_10_shft_lst = []  # Defines list. Empty for looped population.

                                del srvy_typ_prv  # Deletes object if exists.

                            except NameError:  # Executes lines below if object does not exist.
                                if j == srvy_nums1[0]:  # Conditional
                                    # statement. Executes for first survey only if no lidar data exists for transect or
                                    # for second survey if it does.
                                    df_rng_orntn = pd.DataFrame()  # Defines DataFrame. Creates new DataFrame.
                                    chnl_name_lst = []  # Defines list. Empty for looped population.
                                    chnl_abrv_lst = []  # Defines list. Empty for looped population.
                                    rng_name1_lst = []  # Defines list. Empty for looped population.
                                    rng_num_lst = []  # Defines list. Empty for looped population.
                                    srvy_yr1_lst = []  # Defines list. Empty for looped population.
                                    brng_lst = []  # Defines list. Empty for looped population.
                                    azmth_deg_meas_lst = []  # Defines list. Empty for looped population.
                                    azmth_deg_cor_lst = []  # Defines list. Empty for looped population.
                                    azmth_deg_dff_list = []  # Defines list. Empty for looped population.
                                    rng_end_shft_lst = []  # Defines list. Empty for looped population.
                                    rng_10_shft_lst = []  # Defines list. Empty for looped population.

                        dtfrm_pop_lists = [chnl_name_lst, chnl_abrv_lst, rng_name1_lst, rng_num_lst, srvy_yr1_lst,
                                           brng_lst, azmth_deg_meas_lst, azmth_deg_cor_lst, azmth_deg_dff_list,
                                           rng_end_shft_lst, rng_10_shft_lst]  # Defines list. Nested to enable looped
                        # population.

                        dtfrm_pop_values = [chnl_name, chnl_abrv, rng_name1, i, srvy_yr1,
                                            brng_r_dir + str(brng_angl) + brng_a_dir, azmth_deg_meas, azmth_deg_cor,
                                            azmth_deg_dff, rng_end_shft, rng_10_shft]  # Defines list. Values
                        # to populate lists for export.

                        for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                            # lists.
                            index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                            y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                     'New list appended: ', 0)  # Redefines list. Calls function.

                        if i == rng_end:  # Conditional statement. Executes for first range only.
                            if j == 1:  # Conditional statement. Executes for first survey only.
                                dtfrm_pop_clm_lbl = ['Chnnl_name', 'Chnnl_abrv', 'Srvy_range', 'Range_num',
                                                     'Srvy_year', 'Brng', 'Azmth_meas', 'Azmth_cor', 'Azmth_dff',
                                                     'Rng_end_shft', 'Rng_10_shft']  # Defines list. Sets column labels
                                # for DataFrame.

                                dtfrm_pop_lists = [chnl_name_lst, chnl_abrv_lst, rng_name1_lst, rng_num_lst,
                                                   srvy_yr1_lst, brng_lst, azmth_deg_meas_lst, azmth_deg_cor_lst,
                                                   azmth_deg_dff_list, rng_end_shft_lst, rng_10_shft_lst]  # Redefines
                                # list. With populated lists.

                                dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array for
                                # operation.

                                dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array for
                                # DataFrame dimensional compatibility.

                                df_rng_orntn = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl,
                                                                   'TRANSECT ORIENTATION', 1)  # Defines DataFrame.
                                # Calls function. Creates DataFrame of sediment thickness results for single transect.

                                # Export data
                                fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Digitzer_error']
                                # Defines list. Sets folder labels for directory to be made.

                                if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                    fl_name = '/Digitizer_error' + str(chnl_name) + '.csv'  # Defines variable
                                    # as string.
                                else:  # Conditional statement.
                                    fl_name = '/Digitizer_error.csv'  # Defines variable as string.
                                if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                    fl_name = '/Digitizer_error_' + str(rng_name1) + '.csv'  # Defines variable
                                    # as string.

                                export_file_to_directory(1, 'Table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                         fl_name, 1, None, df_rng_orntn, False,
                                                         'Transect digitizer error', None, None, None, 0)  # Creates
                                # directory and exports file. Calls function.

                        # DISPLAY DATA -------------------------------------------------------------------------------------

                        if Plt_crdnts == 1:  # Conditional statement. Plots all measurement coordinates on transect.
                            plot_scatter(3, fig_sz, df_e, df_n, 'Predicted', tol_mtd[6], tol_mtd[6], mrkrs[3], mrkr_sz[0],
                                         lin_wdth[1], alpha[0], 0, lctn, mrkr_scl, alpha[1], lbl_spcng, 'equal', 'box',
                                         fntsz[1], fntsz[0], lbl_pd, 'Easting (m)', 'Northing (m)', 'Coordinates', 1, 1)
                            # Creates plot. Calls function.

                            if j == srvy_nums1[-1]:  # Conditional statement. Plots benchmark GPS coordinates.
                                plot_scatter(3, fig_sz, BM1_e, BM1_n, None, tol_mtd[1], tol_mtd[0], mrkrs[3], mrkr_sz[0],
                                             lin_wdth[1], alpha[2], 0, lctn, mrkr_scl, alpha[1], lbl_spcng, 'equal', 'box',
                                             fntsz[1], fntsz[0], lbl_pd, 'Easting (m)', 'Northing (m)', 'Coordinates', 1,
                                             1)  # Creates plot. Calls function.
                                plot_scatter(3, fig_sz, BM2_e, BM2_n, 'Original gps', tol_mtd[1], tol_mtd[0], mrkrs[3],
                                             mrkr_sz[0], lin_wdth[1], alpha[2], 1, lctn, mrkr_scl, alpha[1], lbl_spcng,
                                             'equal', 'box', fntsz[1], fntsz[0], lbl_pd, 'Easting (m)', 'Northing (m)',
                                             'Coordinates', 1, 1)  # Creates plot. Calls function.

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

                        export_file_to_directory(0, 'Geospatial', 5, fldr_lbls, opt_fldr, 'Directiories named: ', lyr_name,
                                                 None, None, None, False, 'GIS layer', gdf_srvy, gpckg, 'GPKG', 0)
                        # Creates directory and exports figure. Calls function.

        # ==============================================================================================================
        # PART 3: CROSS-SECTIONAL ANALYSIS - DOUBLE --------------------------------------------------------------------
        # ==============================================================================================================

        # SELECT DATA --------------------------------------------------------------------------------------------------

        if Dbl == 1:  # Conditional statement. Executes analysis of cross-sections as pairs.
            if j > srvy_nums1[-1]:  # Conditional statement. Performs operations for all but the last survey.
                if j == 1:
                    pass
                else:
                    index1 = srvy_nums1.index(j)  # Defines variable. Retrieves index of survey number from list. Enables
                    # selection of second survey.

                    index1 = index1 + 1  # Redefines variable. Retrieves index for second dataset selection.

                    k = srvy_nums1[index1]  # Defines variable as integer. Allows for selection of second dataset.

                    # Select second survey dataset
                    df_srvy2 = slice_DataFrame_rows('Equals', df_rng, 'Srvy_num', k, 'SURVEY NUMBER', 0)  # Defines
                    # DataFrame. Calls function. Slices DataFrame to yield singular survey data.
                    df_splt_cls_strt2 = slice_DataFrame_rows('Equals', df_srvy2, 'Rng_splt', 'Split', 'SPLIT POINT', 0)
                    # Defines DataFrame. # Calls function. Slices DataFrame to yield starting split point.
                    df_splt_cls_end2 = slice_DataFrame_rows('Equals', df_srvy2, 'Rng_splt', 'Zip', 'ZIP POINT', 0)
                    # Defines DataFrame. # Calls function. Slices DataFrame to yield end split point.

                    # Retrieve metadata
                    srvy_yr2 = slice_DataFrame_cell('Integer', 0, None, df_srvy2, 0, 'Srvy_year', 'Survey year', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield survey year of present dataset.
                    srvy_dt2 = slice_DataFrame_cell('String', 0, None, df_srvy2, 0, 'Srvy_date', 'Survey date', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield survey date of present dataset.
                    srvy_typ2 = slice_DataFrame_cell('String', 0, None, df_srvy2, 0, 'Srvy_type', 'Survey type', 0)
                    # Defines variable. Calls function. Slices DataFrame to yield survey type of present dataset.
                    # Select survey measurements
                    if j > 0:
                        df_offst2 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy2, 'Offset_ft', 0, 0, 'OFFSET', 0)
                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey offsets of present dataset.
                        df_elvtn2 = slice_DataFrame_columns('DataFrame', 'Float', df_srvy2, 'Elv_geo_ft', 0, 0, 'ELEVATION', 0)
                        # Defines DataFrame. Calls function. Slices DataFrame to yield survey elevations of present dataset.
                        # Retrieve metadata
                    else:
                        brng_in_arry2 = slice_DataFrame_columns('Array', 'Float', df_srvy2, 'Brhl_fl_in', 0, 1,
                                                               'Borehole depths (in)',
                                                               0)  # Defines array. Calls function. Slices DataFrame to yield borehole fill depths in inches of present dataset.
                        brng_ft_arry2 = slice_DataFrame_columns('Array', 'Float', df_srvy2, 'Brhl_fl_ft', 0, 1,
                                                               'Borehole depths (ft)', 0)

                        if np.any(brng_in_arry2) == False:  # Conditional statement. Selects non-empty set of borings for calculations.
                            del brng_in_arry2  # Deletes array.
                            brng_arry2 = brng_ft_arry2  # Defines array. Selects non-empty array.
                            unts2 = 'Feet'  # Defines variable. For unit conversion.
                        if np.any(brng_ft_arry2) == False:  # Conditional statement. Selects non-empty set of borings for calculations.
                            del brng_ft_arry2  # Deletes array.
                            brng_arry2 = brng_in_arry2  # Defines array. Selects non-empty array.
                            unts2 = 'Inches'  # Defines variable. For unit conversion.

                    if j > 0:
                        offst_min2 = min_value_DataFrame('Float', df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                        # Slices DataFrame to yield first offset of present dataset.
                        offst_max2 = max_value_DataFrame('Float', df_offst2, 'Offset', 0)  # Defines variable. Calls function.
                        # Slices DataFrame to yield last offset of present dataset.
                        elvtn_min2 = min_value_DataFrame('Float', df_elvtn2, 'Elevation', 0)  # Defines variable. Calls
                        # function. Slices DataFrame to yield lowest elevation of present dataset.
                        elvtn_max2 = max_value_DataFrame('Float', df_elvtn2, 'Elevation', 0)  # Defines variable. Calls
                        # function. Slices DataFrame to yield highest elevation of present dataset.
                        num_smpls2 = df_srvy2.shape[0]  # Defines variable. Returns dimensionality of DataFrame.
                    else:
                        num_smpls2 = len(brng_arry2)

                    if df_splt_cls_strt2.empty and df_splt_cls_end2.empty == True:  # Conditional statement. Executes lines if split clause exists.
                        splt_pnt2 = None  # Defines variable. Sets to null. For later selection.
                        splt_pnt2_m = None  # Defines variable. Sets to null. For later selection.
                        zip_pnt2 = None  # Defines variable. Sets to null. For later selection.
                        zip_pnt2_m = None  # Defines variable. Sets to null. For later selection.
                    else:  # Conditional statement.
                        splt_pnt2 = slice_DataFrame_cell('Float', 0, None, df_splt_cls_strt2, 0, 'Offset_ft',
                                                         'Transect split point: ',
                                                         0)  # Defines variable. Calls function. Retrieves position of split point.
                        splt_pnt2_m = splt_pnt2 / ft_m  # Defines variable. Converts feet to meters.
                        zip_pnt2 = slice_DataFrame_cell('Float', 0, None, df_splt_cls_end2, 0, 'Offset_ft',
                                                        'Transect zip point: ',
                                                        0)  # Defines variable. Calls function. Retrieves position of zip point.
                        # Defines variable. Calls function. Slices DataFrame to yield split clause.
                        zip_pnt2_m = zip_pnt2 / ft_m  # Defines variable. Converts feet to meters.

                    rng_lngth2 = offst_max2 - offst_min2  # Defines variable. Calculates survey length.
                    rng_lngth2_m = rng_lngth2 / ft_m  # Defines variable. Converts to meters.
                    srvy_rlf2 = elvtn_max2 - elvtn_min2  # Defines variable. Calculates survey relief.
                    srvy_rlf2_m = srvy_rlf2 / ft_m  # Defines variable. Converts to meters.

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
                    if j > 0:
                        print('\033[1m' + 'Survey lengths: ' + '\033[0m' + str('%.1f' % rng_lngth1) + ' & ' + str(
                            '%.1f' % rng_lngth2) +
                              ' ft' + ' (' + str('%.0f' % rng_lngth1_m) + ' & ' + str(
                            '%.0f' % rng_lngth2_m) + ' m)')  # Displays objects.
                        print('\033[1m' + 'Range relief: ' + '\033[0m' + str('%.1f' % srvy_rlf1) + ' & ' +
                              str('%.1f' % srvy_rlf2) + ' ft' + ' (' + str('%.0f' % srvy_rlf1_m) + ' & ' + str(
                            '%.0f' % srvy_rlf2_m) + ' m)')  # Displays objects.
                    try:  # Conditional statement. Executes lines based on existence of object.
                        splt_pnt1  # Defines object.
                        if splt_pnt1 != None:  # Conditional statement. Executes lines if object exits and is not null.
                            print('\033[1m' + 'Split points: ' + '\033[0m' + str('%.2f' % splt_pnt1) + ' & ' +
                                  str('%.2f' % zip_pnt1) + ' ft ' + '(' + str('%.2f' % splt_pnt1_m) + ' & ' +
                                  str('%.2f' % zip_pnt1_m) + ' m)')  # Displays objects.
                    except NameError:  # Conditional statement. Executes lines if object does not exist.
                        pass  # Pass command. Moves on to next line.
                    try:  # Conditional statement. Executes lines based on existence of object.
                        splt_pnt2  # Conditional statement. Executes lines if object exits and is not null.
                        if splt_pnt2 != None:  # Conditional statement. Executes lines if object exits and is not null.
                            print('\033[1m' + 'Split points: ' + '\033[0m' + str('%.2f' % splt_pnt2) + ' & ' +
                                  str('%.2f' % zip_pnt2) + ' ft ' + '(' + str('%.2f' % splt_pnt2_m) + ' & ' +
                                  str('%.2f' % zip_pnt2_m) + ' m)')  # Displays objects.
                    except NameError:  # Conditional statement. Executes lines if object does not exist.
                        pass  # Pass command. Moves on to next line.
                    print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1) + ' & ' + str(num_smpls2))
                    # Displays objects.
                    print('--------------------------------------------------')  # Displays objects.

                # Two cross-sections -------------------------------------------------------------------------------
                if j > 1:
                    if Plt_dbl == 1:  # Conditional statement. Plots cross-sections as dual pairs.
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.

                        title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                ' surveys'  # Defines string. Sets title of plot.

                        plot_lines(2, 4, fig_sz, [df_offst2, df_offst1], [df_elvtn2, df_elvtn1], [srvy_yr2, srvy_yr1],
                                   [clr2, clr1], [mrkr2, mrkr1], mrkr_sz[0], lin_wdth[0], [lin_styl[0], lin_styl[0]],
                                   alpha[0], 1, lctn, mrkr_scl, alpha[1], lbl_spcng, fntsz[-1], 'Survey offset (ft)',
                                   fntsz[0], lbl_pd, 'Surface elevation (ft)', title, 2, 1)  # Creates plot. Calls
                        # function.

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                     '/Measured']  # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                                   str(srvy_yr2) + '.pdf'  # Defines variable as strIng. Sets name of figure for export.

                        export_file_to_directory(1, 'Figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 4, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
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
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.

                        title = 'Range ' + str(rng_name1) + ' (' + str(i) +') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                ' interpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                        # plot title.

                        plot_lines(2, 5, fig_sz, [df_off_i2, df_off_i1], [df_elv_i2, df_elv_i1], [srvy_yr2, srvy_yr1],
                                   [clr2, clr1], [mrkr2, mrkr1], mrkr_sz[0], lin_wdth[0], [lin_styl[0], lin_styl[0]],
                                   alpha[0], 0, lctn, mrkr_scl, alpha[1], lbl_spcng, fntsz[1], 'Survey offset (ft)',
                                   fntsz[0], lbl_pd, 'Surface elevation (ft)', title, 2, 1)
                        # Creates plot. Calls function.

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                     '/Interpolated']  # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                                   str(srvy_yr2) + '_Interp' + '.pdf'  # Defines variable as strIng. Sets name of figure
                        # for export.

                        export_file_to_directory(1, 'Figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 5, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                        # Creates directory and exports figure. Calls function.

                    # SELECT CALCULATION RANGE -----------------------------------------------------------------------------

                    start, end, shrd_rng = select_coincident_x_range('dataframe', df_offst1, df_offst2, ' ft', 0)
                    # Defines variables. Calls function. Identifies shared x values of individual datasets.

                    shrd_rng_m = shrd_rng / ft_m  # Defines variable. Converts feet to meters.

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
                        clr1 = get_plot_feature_by_year(srvy_yr1, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr1 = get_plot_feature_by_year(srvy_yr1, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.
                        clr2 = get_plot_feature_by_year(srvy_yr2, tol_mtd, 'Color : ', 0)  # Defines variable. Calls
                        # function. Sets plot color.
                        mrkr2 = get_plot_feature_by_year(srvy_yr2, mrkrs, 'Marker: ', 0)  # Defines variable. Calls
                        # function. Sets plot marker type.

                        title = 'Range ' + str(rng_name1) + ' (' + str(i) + ') ' + str(srvy_yr1) + '–' + str(srvy_yr2) + \
                                ' reinterpolated surveys'  # Defines string. Sets title of plot.  # Defines string. Sets
                        # plot title.

                        plot_lines(2, 6, fig_sz, [df_off_i2, df_off_i1], [df_elv_i2, df_elv_i1], [srvy_yr2, srvy_yr1],
                                   [clr2, clr1], [mrkr2, mrkr1], mrkr_sz[0], lin_wdth[0],
                                   [lin_styl[0], lin_styl[0]], alpha[0], 0, lctn, mrkr_scl, alpha[1],
                                   lbl_spcng, fntsz[1], 'Survey offset (ft)', fntsz[0], lbl_pd,
                                   'Surface elevation (ft)', title, 2, 2)  # Creates plot. Calls function.

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Cross_sections', '/Double', '/' + chnl_name,
                                     '/Reinterpolated']  # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/' + str(rng_name1) + '_s' + str(j) + '–' + str(k) + '_' + str(srvy_yr1) + '–' + \
                                   str(srvy_yr2) + '_Reinterp' + '.pdf'  # Defines variable as strIng. Sets name of  figure
                        # for export.

                        export_file_to_directory(0, 'Figure', 6, fldr_lbls, opt_fldr, 'Directories named: ', fig_name,
                                                 6, 'pdf', None, None, 'Cross-sectional plot', None, None, None, 0)
                        # Creates directory and exports figure. Calls function.

            # ======================================================================================================
            # CALCULATE SEDIMENTATION ------------------------------------------------------------------------------

            if Dpth == 1:  # Conditional statement. Calculates sediment thickness between cross-sections.
                if j > 1:
                    # SELECT COORDINATE PAIRS --------------------------------------------------------------------------

                    # Check for split
                    splt_pnt, zip_pnt = check_for_multipart(splt_pnt1, splt_pnt2, zip_pnt1, zip_pnt2, 0)  # Defines
                    # variables. Calls function. Selects split and zip points for multipart transects.

                    index1 = np.arange(0, len(df_off_i1), 1, dtype=int)  # Defines array. Creates array of index values
                    # for coordinate pair selection.

                    for x in index1:  # Begins loop through array. Loops through coordinate indices.
                        # Select survey measurements
                        off1, elv1_top, elv1_btm = get_coordinate_pairs('Depth', x, None, df_off_i1, df_elv_i1,
                                                                        df_elv_i2, 0)  # Defines variables. Calls
                        # function.

                        # CALCULATE SEDIMENT THICKNESS -----------------------------------------------------------------

                        if splt_pnt == None:  # Conditional statement. Transect is single part and calculation will not be interrupted.
                            # At a point -----------------------------------------------------------------------------------

                            dpth1, prcs1, sed_rt1, prcs_rt1, tm_intrvl = sediment_thickness(elv1_top, elv1_btm,
                                                                                             srvy_yr1,
                                                                                             srvy_yr2,
                                                                                             'Sedimentation over ',
                                                                                             0)
                            # Defines variables. Calls function.

                            # Save data
                            if x == index1[0]:  # Conditional statement. Executes on first calculation only.
                                dpth1_lst = []  # Defines list. Empty for looped population.
                                sed_rt1_lst = []  # Defines list. Empty for looped population.

                            dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_lst,
                                                              'New list appended: ',
                                                              0)  # Redefines list. Calls function.
                            # Populates list.
                            sed_rt1_lst = create_appended_list(sed_rt1, 'Aggradation rate', sed_rt1_lst,
                                                                'New list appended: ',
                                                                0)  # Redefines list. Calls function.
                            # Populates list.
                        else:  # Conditional statement. Transect is multipart and calculation will not be interrupted outside of split point.
                            if off1 <= splt_pnt or off1 >= zip_pnt:  # Conditional statement.
                                # At a point -----------------------------------------------------------------------------------

                                dpth1, prcs1, sed_rt1, prcs_rt1, tm_intrvl = sediment_thickness(elv1_top, elv1_btm,
                                                                                                 srvy_yr1,
                                                                                                 srvy_yr2,
                                                                                                 'Sedimentation over ',
                                                                                                 0)
                                # Defines variables. Calls function.

                                # Save data
                                # Save data
                                if x == index1[0]:  # Conditional statement. Executes on first calculation only.
                                    dpth1_lst = []  # Defines list. Empty for looped population.
                                    sed_rt1_lst = []  # Defines list. Empty for looped population.

                                dpth1_list = create_appended_list(dpth1, 'Sediment thickness', dpth1_lst,
                                                                  'New list appended: ',
                                                                  0)  # Redefines list. Calls function.
                                # Populates list.
                                sed_rt1_lst = create_appended_list(sed_rt1, 'Aggradation rate', sed_rt1_lst,
                                                                    'New list appended: ',
                                                                    0)  # Redefines list. Calls function.
                                # Populates list.
                            elif splt_pnt < off1 < zip_pnt:  # Conditional statement. Does not calculate between
                            # multiparts.
                                pass  # Pass command. Moves on to next line.

                        # Save data
                        if i == rng_strt:  # Conditional statement. Executes for first range only.
                            if j == srvy_nums1[0]:  # Conditional statement. Executes for first survey only.
                                if x == index1[0]:  # Conditional statement. Executes for first calculation only.
                                    df_sed_thck = pd.DataFrame()  # Defines DataFrame. Creates new DataFrame.
                        if j == srvy_nums1[0]:  # Conditional statement. Executes for first survey only.
                            if x == index1[0]:  # Conditional statement. Executes for first calculation only.
                                chnl_name_lst = []  # Defines list. Empty for looped population.
                                rng_name_lst = []  # Defines list. Empty for looped population.
                                rng_num_lst = []  # Defines list. Empty for looped population.
                                srvy_yr1_lst = []  # Defines list. Empty for looped population.
                                srvy_yr2_lst = []  # Defines list. Empty for looped population.
                                tm_intrvl_lst = []  # Defines list. Empty for looped population.
                                strm_stat_lst = []  # Defines list. Empty for looped population.
                                dpth_avg1_lst = []  # Defines list. Empty for looped population.
                                dpth_mdn1_lst = []  # Defines list. Empty for looped population.
                                dpth_stdv1_lst = []  # Defines list. Empty for looped population.
                                dpth_max1_lst = []  # Defines list. Empty for looped population.
                                dpth_min1_lst = []  # Defines list. Empty for looped population.
                                sed_rt_avg1_lst = []
                                wshd_A_lst = []  # Defines list. Empty for looped population.
                                vlly_W_lst = []  # Defines list. Empty for looped population.

                                dtfrm_pop_lists = [chnl_name_lst, rng_name_lst, rng_num_lst, srvy_yr1_lst, srvy_yr2_lst,
                                           tm_intrvl_lst,
                                           strm_stat_lst, dpth_avg1_lst, dpth_mdn1_lst, dpth_stdv1_lst, dpth_max1_lst,
                                           dpth_min1_lst,
                                           sed_rt_avg1_lst, wshd_A_lst, vlly_W_lst]  # Defines list.
                        # Nested to enable looped population.

                        # Over cross-section ---------------------------------------------------------------------------

                        if x == index1[-1]:  # Conditional statement. Executes on last calculation only.
                            if srvy_yr2 == 1855:  # Conditional statement. Corrects values in list.
                                dpth1_lst = list(filter(lambda y : y > 0, dpth1_lst))  # Redefines list. Removes
                                # erroneous erosion values from list.
                                sed_rt1_lst = list(filter(lambda y: y > 0, sed_rt1_lst))  # Redefines list. Removes
                                # erroneous erosion values from list.

                            dpth_avg1 = np.mean(dpth1_lst)  # Defines variable. Calculates average sediment
                            # thickness on transect.

                            # dpth_avg_m = dpth_avg / ft_m  # Defines variable. Converts units to meters.

                            dpth_mdn1 = np.median(dpth1_lst)  # Defines variable. Calculates median sediment thickness
                            # of transect.

                            dpth_stdv1 = np.std(dpth1_lst)  # Defines variable. Calculations standard deviation of sediment thickness of transect.

                            sed_rt_avg1 = np.mean(sed_rt1_lst)  # Defines variable. Calculates average
                            # sedimentation rate on transect.

                            sed_rt_avg1 = sed_rt_avg1 * in_ft  # Defines variable. Converts units to inches.

                            dpth_max1 = max(dpth1_lst)  # Defines variable. Retrieves max value from list.
                            dpth_min1 = min(dpth1_lst)  # Defines variable. Retrieves min value from list.


                            dtfrm_pop_values = [chnl_name, str(rng_name1), int(i), str(srvy_yr1), str(srvy_yr2),
                                                str(tm_intrvl), strm_stat1,
                                                float(dpth_avg1), str(dpth_mdn1), dpth_stdv1, dpth_max1, dpth_min1, str(sed_rt_avg1),
                                                wshd_A, shrd_rng_m]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ',
                                                         0)  # Redefines list. Calls function.

                elif j < 1:
                    if j == 0:
                        if srvy_nums1[-1] == -1:
                            # overlapp"" range
                            dpth_avg_br1 = np.mean(brng_arry1)  # Defines variable. Calculates mean of array values.

                            if unts1 == 'Inches':  # Conditional statement. Converts units to feet.
                                dpth_avg_br1 = dpth_avg_br1 / in_ft  # Redefines variable.

                            dpth_avg_br2 = np.mean(brng_arry2)  # Defines variable. Calculates mean of array values.

                            if unts2 == 'Inches':  # Conditional statement. Converts units to feet.
                                dpth_avg_br2 = dpth_avg_br2 / in_ft  # Redefines variable.

                            dpth_avg_br_dff = dpth_avg_br1 - dpth_avg_br2

                            # CALCULATE SEDIMENTATION RATE ---------------------------------------------------------------------
                            yr1 = 1964
                            yr2 = 1939
                            tm_intrvl_dff = yr1 - yr2

                            sed_rt_avg_br_dff = dpth_avg_br_dff / tm_intrvl_dff
                            sed_rt_avg_br_dff = sed_rt_avg_br_dff * in_ft

                            dtfrm_pop_values = [chnl_name, str(rng_name1), int(i), str(yr1), str(yr2),
                                                str(tm_intrvl_dff), strm_stat1,
                                                float(dpth_avg_br_dff), None, 'Nan', 'N/A', 'n/a', str(sed_rt_avg_br_dff),
                                                wshd_A, str(None)]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ',
                                                         0)  # Redefines list. Calls function.

                            # other interval
                            if unts2 == 'Inches':
                                brng_arry2 = brng_arry2 / in_ft

                            dpth_avg_br2 = np.mean(brng_arry2)
                            dpth_mdn_br2 = np.median(brng_arry2)
                            dpth_stdv_br2 = np.std(brng_arry2)
                            dpth_max_br2 = max(brng_arry2)
                            dpth_min_br2 = min(brng_arry2)

                            yr1 = 1939
                            yr2 = 1855
                            tm_intrvl2 = yr1 - yr2

                            sed_rt_arry2 = brng_arry2 / tm_intrvl2
                            # print(brng_arry2)
                            sed_rt_avg_br2 = np.mean(sed_rt_arry2)

                            sed_rt_avg_br2 = sed_rt_avg_br2 * in_ft

                            dtfrm_pop_values = [chnl_name, str(rng_name1), int(i), str(yr1), str(yr2),
                                                str(tm_intrvl2), strm_stat1,
                                                float(dpth_avg_br2), str(dpth_mdn_br2), dpth_stdv_br2, dpth_max_br2, float(dpth_min_br2), str(sed_rt_avg_br2),
                                                wshd_A, str(None)]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ',
                                                         0)  # Redefines list. Calls function.
                            # overlapped interval
                            if unts1 == 'Inches':
                                brng_arry1 = brng_arry1 / in_ft

                            dpth_avg_br1 = np.mean(brng_arry1)
                            dpth_mdn_br1 = np.median(brng_arry1)
                            dpth_stdv_br1 = np.std(brng_arry1)
                            dpth_max_br1 = max(brng_arry1)
                            dpth_min_br1 = min(brng_arry1)

                            yr1 = 1964
                            yr2 = 1855
                            tm_intrvl1 = yr1 - yr2

                            sed_rt_arry1 = brng_arry1 / tm_intrvl1

                            sed_rt_avg_br1 = np.mean(sed_rt_arry1)

                            sed_rt_avg_br1 = sed_rt_avg_br1 * in_ft

                            dtfrm_pop_values = [chnl_name, str(rng_name1), int(i), str(yr1), str(yr2),
                                                str(tm_intrvl1), strm_stat1,
                                                float(dpth_avg_br1), str(dpth_mdn_br1), dpth_stdv_br1, dpth_max_br1,
                                                str(dpth_min_br1), str(sed_rt_avg_br1),
                                                wshd_A, str(None)]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(
                                    y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ',
                                                         0)  # Redefines list. Calls function.
                        elif srvy_nums1[-1] == 0:
                            if unts1 == 'Inches':
                                brng_arry1 = brng_arry1 / in_ft

                            dpth_avg_br1 = np.mean(brng_arry1)
                            dpth_mdn_br1 = np.median(brng_arry1)
                            dpth_stdv_br1 = np.std(brng_arry1)
                            dpth_max_br1 = max(brng_arry1)
                            dpth_min_br1 = min(brng_arry1)

                            if i == 56:
                                yr1 = 1939
                            else:
                                yr1 = 1964
                            yr2 = 1855
                            tm_intrvl1 = yr1 - yr2
                            sed_rt_arry1 = brng_arry1 / tm_intrvl1
                            sed_rt_avg_br1 = np.mean(sed_rt_arry1)

                            sed_rt_avg_br1 = sed_rt_avg_br1 * in_ft

                            dtfrm_pop_values = [chnl_name, str(rng_name1), int(i), str(yr1), str(yr2),
                                                str(tm_intrvl1), strm_stat1,
                                                float(dpth_avg_br1), str(dpth_mdn_br1), dpth_stdv_br1, dpth_max_br1, str(dpth_min_br1),
                                                str(sed_rt_avg_br1), wshd_A, str(None)]  # Defines list. Values to populate lists for
                            # export.

                            for y in dtfrm_pop_values:  # Begins loop through list. Loops through values to populate
                                # lists.
                                index = dtfrm_pop_values.index(y)  # Defines variable. Retrieves index of list element.

                                y = create_appended_list(y, 'Populated values', dtfrm_pop_lists[index],
                                                         'New list appended: ',
                                                         0)  # Redefines list. Calls function.

                dtfrm_pop_lists = [chnl_name_lst, rng_name_lst, rng_num_lst, srvy_yr1_lst, srvy_yr2_lst,
                                   tm_intrvl_lst,
                                   strm_stat_lst, dpth_avg1_lst, dpth_mdn1_lst, dpth_stdv1_lst, dpth_max1_lst,
                                   dpth_min1_lst,
                                   sed_rt_avg1_lst, wshd_A_lst, vlly_W_lst]  # Defines list.
                # Nested to enable looped population.

                dtfrm_pop_arry = np.array(dtfrm_pop_lists)  # Defines array. Converts list to array for
                # operation.

                dtfrm_pop_arry = dtfrm_pop_arry.transpose()  # Redefines array. Transposes array for
                # DataFrame dimensional compatibility.
                dtfrm_pop_clm_lbl = ['Chnnl_name', 'Srvy_range', 'Range_num', 'Srvy_year1', 'Srvy_year2',
                                     'Tm_intvl', 'Strm_stat', 'D_avg_ft', 'D_mdn_ft', 'D_std_ft', 'D_max_ft',
                                     'D_min_ft', 'D_avg_in/y', 'Wshd_A_sqkm', 'Vlly_W_m']  # Defines
                        # list. Sets column labels for DataFrame.

                df_sed_thck_rng = create_DataFrame(dtfrm_pop_arry, dtfrm_pop_clm_lbl,
                                                   'SEDIMENT THICKNESS', 0)  # Defines DataFrame. Calls
                # function. Creates DataFrame of sediment thickness results for single transect.

                if j > 1 or j < 1:
                    if Plt_dpth_dst == 1:
                        if j > 1:
                            y = sed_rt1_lst
                            yr1 = srvy_yr1
                            yr2 = srvy_yr2
                        elif j < 1:
                            if srvy_nums1[-1] == -1:
                                yr2 = 1855
                                if j == 0:
                                    y = brng_arry1
                                    yr1 = 1964
                                elif j == -1:
                                    y = sed_rt_arry2
                                    yr1 = 1939
                            elif srvy_nums1[-1] == 0:
                                y = sed_rt_arry1

                        title = str(rng_name1) + ' ' + str(yr2) + '-' + str(yr1)
                        plot_box(0, y, True, True, None, 'Cyan', title, 2, 1)

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Thickness_distribution', '/' + chnl_name]
                        # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/D_dst_' + str(rng_name1) + '_' + str(yr2) + '_' + str(yr1) + '.pdf'  # Defines variable as string.

                        export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                                 'Directories named: ', fig_name, 0, 'pdf', None,
                                                 None, 'Sediment thickness box plot', None,
                                                 None, None, 0)  # Creates directory and exports
                        # figure. Calls function.

                        title = str(rng_name1) + ' ' + str(yr2) + '-' + str(yr1)
                        plot_histogram(0, y, 'Cyan', 'Black', title, 2, 2)

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Thickness_distribution', '/' + chnl_name]
                        # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/D_dst_hst_' + str(rng_name1) + '_' + str(yr2) + '_' + str(
                            yr1) + '.pdf'  # Defines variable as string.

                        export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                                 'Directories named: ', fig_name, 0, 'pdf', None,
                                                 None, 'Sediment thickness histogram', None,
                                                 None, None, 0)  # Creates directory and exports
                        # figure. Calls function.

                        title = str(rng_name1) + ' ' + str(yr2) + '-' + str(yr1)
                        plot_qq(0, y, '45', title, 2, 1)

                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Thickness_distribution', '/' + chnl_name]
                        # Defines list. Sets folder labels for directory to be made.

                        fig_name = '/D_dst_qq_' + str(rng_name1) + '_' + str(yr2) + '_' + str(
                            yr1) + '.pdf'  # Defines variable as string.

                        export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                                 'Directories named: ', fig_name, plt.gcf().number, 'pdf', None,
                                                 None, 'Sediment thickness Q-Q plot', None,
                                                 None, None, 0)  # Creates directory and exports
                        # figure. Calls function.

                # coordinates to survey DataFrame.
                if j == srvy_nums1[-1]:
                    df_sed_thck = pd.concat([df_sed_thck, df_sed_thck_rng], axis=0)  # Redefines DataFrame. Concatenates

                    del df_sed_thck_rng
                if i == rng_end:
                    if j == srvy_nums1[-1]:
                        print(df_sed_thck)
                        # Export data
                        fldr_lbls = ['/Cross_sectional_analysis', '/Calculations', '/Sediment_thickness']
                        # Defines list. Sets folder labels for directory to be made.

                        if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                            fl_name = 'Sediment_thickness_' + str(chnl_name) + '.csv'  # Defines variable
                            # as string.
                            if cmltv == 1:  # Conditional statement.
                                fl_name = 'Sediment_thickness_cmltv' + str(chnl_name) + '.csv'
                                # Defines variable as string.
                        else:  # Conditional statement.
                            fl_name = 'Sediment_thickness.csv'  # Defines variable as string.
                        if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                            fl_name = 'Sediment_thickness_' + str(rng_name1) + '.csv'  # Defines variable
                            # as string.
                        if cmltv == 1:  # Conditional statement.
                            fl_name = '/cmltv_' + fl_name  # Redefines string.
                        else:  # Conditional statement.
                            fl_name = '/' + fl_name  # Redefines string.

                        export_file_to_directory(1, 'Table', 3, fldr_lbls, opt_fldr, 'Directories named: ',
                                                 fl_name, 1, None, df_sed_thck, False, '1D sedimentation table', None, None, None, 0)  # Creates
                        # directory and exports file. Calls function.

                        # DISPLAY DATA ---------------------------------------------------------------------

                        # Sediment thickness ---------------------------------------------------------------

                        if Plt_dpth == 1:  # Conditional statement. Plots sediment thickness by time
                            # interval against of distance upstream.

                            srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                  'Srvy_year1', 1, 1, 'Survey years', 0)
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

                                    srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck_x,
                                                                            'Srvy_year2', 1, 0, 'Survey years',
                                                                            0)
                                    # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                    # present dataset.

                                    for y in srvy_yrs2_lst:
                                        df_sed_thck_y = slice_DataFrame_rows('Equals', df_sed_thck_x,
                                                                             'Srvy_year2',
                                                                             y, 'SEDIMENT THICKNESS',
                                                                             0)  # Defines
                                        # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                        # data by first survey year.

                                        df_dpth_y = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_y,
                                                                            'D_avg_ft', 0, 0, 'SEDIMENT THICKNESS', 0)
                                        # Defines DataFrame. Calls function. Slices DataFrame to yield sediment
                                        # thickness data.

                                        df_strm_stat_y = slice_DataFrame_columns('DataFrame', 'Integer',
                                                                                 df_sed_thck_y, 'Strm_stat', 0,
                                                                                 0, 'STREAM STATION', 0)  # Defines
                                        # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                                        df_strm_stat_y = df_strm_stat_y.divide(1000)  # Redefines DataFrame.
                                        # Modifies values to be displayed in scientific notation.

                                        if x == '1964':
                                            if y == '1855':
                                                clr1 = get_plot_feature_by_year('Bores', tol_mtd, 'Color : ', 0)
                                                # Defines variable. Calls function. Sets plot color.
                                            else:
                                                clr1 = get_plot_feature_by_year(x, tol_mtd, 'Color : ', 0)
                                                # Defines variable. Calls function. Sets plot color.
                                        else:
                                            clr1 = get_plot_feature_by_year(x, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                        mrkr1 = get_plot_feature_by_year(x, mrkrs, 'Marker: ', 0)  # Defines
                                        # variable. Calls function. Sets plot marker type.

                                        title = 'Average sediment thickness'  # Defines string. Sets plot title.

                                        lbl = y + '–' + x  # Defines string. Sets plot
                                        # object labels.

                                        plot_lines(1, 7, fig_sz, df_strm_stat_y, df_dpth_y, lbl, clr1, mrkr1,
                                                   mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 1, lctn,
                                                   mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                                                   'River station (1 x 10^3 ft)', fntsz[0], lbl_pd,
                                                   'Average sediment thickness (ft)', title, 1, 1)  # Creates plot.
                                        # Calls function.

                            plt.figure(7)  # Creates plot window. Sets figure size.
                            ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
                            ax.invert_xaxis()  # Inverts x-axis.

                            # Export data
                            fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sediment_thickness']
                            # Defines list. Sets folder labels for directory to be made.

                            if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                fig_name = 'D_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                           str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                            else:  # Conditional statement.
                                fig_name = 'D_' + str(srvy_yrs2_lst[-1]) + '_' + str(srvy_yrs_lst[0]) \
                                           + '.pdf'  # Defines variable as string.
                            if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                fig_name = 'D_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) + '_' + \
                                           str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                            if cmltv == 1:  # Conditional statement.
                                fig_name = 'cmltv_' + fig_name  # Redefines string.
                            else:  # Conditional statement.
                                fig_name = '/' + fig_name  # Redefines string.
                            export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                     'Directories named: ', fig_name, 7, 'pdf', None,
                                                     None, 'Average sediment thickness plot', None,
                                                     None, None, 0)  # Creates directory and exports
                            # figure. Calls function.

                        # Sedimentation rate ---------------------------------------------------------------

                        if Plt_sed_rt == 1:  # Conditional statement. Plots sedimentation rate by time
                            # interval against of distance upstream.
                            srvy_yrs_lst = slice_DataFrame_columns('List', 'String', df_sed_thck,
                                                                   'Srvy_year1', 1, 0, 'Survey years', 0)
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

                                srvy_yrs2_lst = slice_DataFrame_columns('List', 'String', df_sed_thck_x,
                                                                        'Srvy_year2', 1, 0, 'Survey years', 0)
                                # Defines DataFrame. Calls function. Slices DataFrame to yield survey years of
                                # present dataset.

                                for y in srvy_yrs2_lst:
                                    df_sed_thck_y = slice_DataFrame_rows('Equals', df_sed_thck_x,
                                                                         'Srvy_year2',
                                                                         y, 'SEDIMENT THICKNESS',
                                                                         0)  # Defines
                                    # DataFrame. Calls function. Slices DataFrame to yield sediment thickness
                                    # data by first survey year.

                                    df_sed_rt_y = slice_DataFrame_columns('DataFrame', 'Float', df_sed_thck_y,
                                                                        'D_avg_in/y', 0, 0, 'SEDIMENT THICKNESS',
                                                                           0)  # Defines DataFrame. Calls
                                    # function. Slices DataFrame to yield sediment thickness data.

                                    df_strm_stat_y = slice_DataFrame_columns('DataFrame', 'Integer',
                                                                             df_sed_thck_y, 'Strm_stat', 0,
                                                                             0, 'STREAM STATION', 0)  # Defines
                                    # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                                    df_strm_stat_y = df_strm_stat_y.iloc[::-1]  # Redefines DataFrame. Inverts
                                    # values. For plotting sedimentation in the downstream direction.
                                    df_strm_stat_y = df_strm_stat_y.divide(1000)  # Redefines DataFrame.
                                    # Modifies values to be displayed in scientific notation.

                                    df_sed_rt_y = df_sed_rt_y.iloc[::-1]  # Redefines DataFrame. Inverts
                                    # values.  For plotting sedimentation in the downstream direction.

                                    if x == '1964':
                                        if y == '1855':
                                            clr1 = get_plot_feature_by_year('Bores', tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                        else:
                                            clr1 = get_plot_feature_by_year(x, tol_mtd, 'Color : ', 0)
                                            # Defines variable. Calls function. Sets plot color.
                                    else:
                                        clr1 = get_plot_feature_by_year(x, tol_mtd, 'Color : ', 0)
                                        # Defines variable. Calls function. Sets plot color.
                                    mrkr1 = get_plot_feature_by_year(x, mrkrs, 'Marker: ', 0)  # Defines
                                    # variable. Calls function. Sets plot marker type.

                                    title = 'Average sedimentation rate'  # Defines string. Sets plot title.

                                    lbl = y + '–' + x  # Defines string. Sets plot
                                    # object labels.

                                    plot_lines(1, 8, fig_sz, df_strm_stat_y, df_sed_rt_y, lbl, clr1, mrkr1,
                                               mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 1, lctn,
                                               mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                                               'River station (1 x 10^3 ft)', fntsz[0], lbl_pd,
                                               'Average sedimentation rate (in/y)', title, 1, 1)  # Creates
                                    # plot. Calls function.

                            plt.figure(8)  # Creates plot window. Sets figure size.
                            ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
                            ax.invert_xaxis()  # Inverts x-axis.

                            # Export data
                            fldr_lbls = ['/Cross_sectional_analysis', '/Plots', '/Sedimentation_rate']
                            # Defines list. Sets folder labels for directory to be made.

                            if rvr_nly == 1:  # Conditional statement. Sets name of file for export.
                                fig_name = 'D_rt_' + str(chnl_name) + '_' + str(srvy_yrs2_lst[-1]) + '_' \
                                           + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                            else:  # Conditional statement.
                                fig_name = 'D_rt_' + str(srvy_yrs2_lst[-1]) + '_' + str(srvy_yrs_lst[0]) \
                                           + '.pdf'  # Defines variable as string.
                            if rng_nly == 1:  # Conditional statement. Sets name of file for export.
                                fig_name = 'D_rt_' + str(rng_name1) + '_' + str(srvy_yrs2_lst[-1]) + '_' \
                                           + str(srvy_yrs_lst[0]) + '.pdf'  # Defines variable as string.
                            if cmltv == 1:  # Conditional statement.
                                fig_name = 'cmltv_' + fig_name  # Redefines string.
                            else:  # Conditional statement.
                                fig_name = '/' + fig_name  # Redefines string.

                            export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr,
                                                     'Directories named: ', fig_name, 8, 'pdf', None,
                                                     None, 'Average sediment thickness plot', None,
                                                     None, None, 0)  # Creates directory and exports
                            # figure. Calls function.

                        sed_rts_arry = slice_DataFrame_columns('Array', 'Float', df_sed_thck, 'D_avg_in/y', 0, 0, None, 0)
                        dpth_arry = slice_DataFrame_columns('Array', 'Float', df_sed_thck, 'D_avg_ft', 0, 0, None, 0)

# ======================================================================================================================
# END ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================