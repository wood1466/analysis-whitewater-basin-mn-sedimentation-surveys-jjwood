# ======================================================================================================================
# WHITEWATER RIVER VALLEY, MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * --------------------------------------------
# STATISTICS PROGRAM * -------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats

print('\n\033[1m' + 'START STATISTICAL ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from Functions import *  # Imports all functions from outside program.

# SELECT OPERATIONS ----------------------------------------------------------------------------------------------------

# Individual channel analysis -----------------------------------------------------------------------------------------


Rvr = 1  # Defines variable as integer. Sets binary toggle.
Plt_sed_rt_sptl = 0
Plt_sed_rt_chng = 0
Plt_sed_dst = 0
Plt_sed_dst_all = 0
Plt_sed_rt = 0

# Whole basin analysis ----------------------------------------------------------------------------------------

Bsn = 0  # Defines variable as integer. Sets binary toggle.
Plt_sed_dst_bsn = 0
Plt_sed_dst_bsn_all = 1

# Calculate statistics
Nrml_tst = 0
Shpr_Wlk = 1
Hyp_tst = 1
ANOVA = 1
Tky = 1
Krskl_Wlls = 1
Dnn = 1
# SELECT INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Limits of analysis ---------------------------------------------------------------------------------------------------

rvr_nly = 0  # Defines variable as integer. Sets binary toggle. Analyzes data for one river channel only.
xtra_srvys = 0  # Defines variable as integer. Sets binary toggle. Analyzes extra survey data for range 11B (13).
rvr_strt = 1
rvr_end = 8

# Conversion factors ---------------------------------------------------------------------------------------------------

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
# PART 2: STATISTICAL ANALYSIS - RIVER ----------------------------------------------------------------------------
# ======================================================================================================================

# ======================================================================================================================
# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Input file(s) --------------------------------------------------------------------------------------------------------

inpt_fl1 = inpt_fldr + '/Sediment_thickness_results.csv'  # Defines string. Sets file path to input file.

df_sed_dt = csv_to_DataFrame(inpt_fl1, 'TEST DATA', 0)  # Defines DataFrame. Calls function. Uploads survey data.

df_sed_dt = slice_DataFrame_rows('Equals', df_sed_dt, 'Outlier', 'Statistics' , 'TEST DATA', 0)

if xtra_srvys == 1:
    inpt_fl2 = inpt_fldr + '/Sediment_thickness_11B.csv'  # Defines string. Sets file path to input file.

    df_11B_sed_dt = csv_to_DataFrame(inpt_fl2, 'TEST DATA 11B', 0)  # Defines DataFrame. Calls function. Uploads
    # transect drainage area data.

# retreive metadata
# Select river dataset
if Rvr == 1:
    # Establish spatial selection framework
    if rvr_nly == 1:
        rvr_nums = [rvr_strt]
        rvr_end = rvr_strt
    elif rvr_nly == 0:
        rvr_nums = forward_range(rvr_strt, rvr_end, 1, 'Channel numbers', 0)

    for i in rvr_nums:
        df_rvr = slice_DataFrame_rows('Equals', df_sed_dt, 'Chnnl_num', i, 'RIVER NUMBER', 0)

        # Retrieve metadata
        chnl_name = slice_DataFrame_cell('String', 0, None, df_rvr, 0, 'Chnnl_name', 'Stream channel', 0)

        rng_names = slice_DataFrame_columns('List', 'String', df_rvr, 'Srvy_range', 1, 0, 'Transect names', 0)

        rng_strt = rng_names[0]
        rng_end = rng_names[-1]

        rng_nums = slice_DataFrame_columns('List', 'Integer', df_rvr, 'Range_num', 1, 0, 'Transect numbers', 0)

        rng_num_strt = rng_nums[0]
        rng_num_end = rng_nums[-1]

        srvy_yrs1 = slice_DataFrame_columns('List', 'Integer', df_rvr, 'Srvy_year1', 1, 0, 'Survey years', 0)
        srvy_yrs2 = slice_DataFrame_columns('List', 'Integer', df_rvr, 'Srvy_year2', 1, 0, 'Survey years', 0)

        srvy_yrs1.sort(reverse=True)
        srvy_yrs2.sort(reverse=True)

        srvy_intrvls = len(srvy_yrs1)

        num_smpls = df_rvr.shape[0]

    # DISPLAY DATA -------------------------------------------------------------------------------------------------

        # Metadata -------------------------------------------------------------------------------------------------

        print('==================================================')  # Displays objects.
        print('\033[1m' + 'Stream channel: ' + '\033[0m' + str(chnl_name))  # Displays objects.
        print('\033[1m' + 'Field transects: ' + '\033[0m' + str(rng_strt) + '—' + str(rng_end) + ' (' + str(rng_num_strt) + '—' + str(rng_num_end) + ')')  # Displays objects.
        print('\033[1m' + 'Survey intervals: ' + '\033[0m' + str(srvy_intrvls))  # Displays objects.
        for j in srvy_yrs1:
            index = srvy_yrs1.index(j)
            yr1 = j
            yr2 = srvy_yrs2[index]
            print(' ' + str(yr2) + '—' + str(yr1))  # Displays objects.
        print('\033[1m' + 'Population size: ' + '\033[0m' + str(num_smpls))  # Displays objects.
        # print('\033[1m' + 'Number of samples: ' + '\033[0m' + str(num_smpls1))  # Displays objects.
        print('--------------------------------------------------')  # Displays objects.

        if Plt_sed_rt_sptl == 1:
            rng_nums = slice_DataFrame_columns('List', 'Integer', df_rvr, 'Range_num', 1, 0, 'Transect numbers', 0)
            for j in rng_nums:
                df_rng_j = slice_DataFrame_rows('Equals', df_rvr, 'Range_num', j, 'RANGE NUMBER', 1)
                df_sed_rts_j = slice_DataFrame_columns('DataFrame', 'Float', df_rng_j, 'D_avg_in/y', 0, 0, 'Average sedimentation rates', 0)
                df_srvy_yrs1_j = slice_DataFrame_columns('DataFrame', 'Integer', df_rng_j, 'Srvy_year1', 0, 0,'Average sedimentation rates', 0)
                strm_stat = slice_DataFrame_cell('Integer', 0, None, df_rng_j, 0, 'Strm_stat', 'Stream channel', 0)
                strm_stat_arry = slice_DataFrame_columns('Array', 'Integer', df_rvr, 'Strm_stat', 0, 0,'Average sedimentation rates', 0)
                strm_stat_min = min(strm_stat_arry)
                strm_stat_max = max(strm_stat_arry)
                strm_stat_max = strm_stat_max - strm_stat_min
                strm_stat = strm_stat - strm_stat_min
                strm_stat_min = strm_stat_min - strm_stat_min
                print(strm_stat_min, strm_stat_max)
                strm_sctn_len = strm_stat_max - strm_stat_min
                prcnt_len = strm_stat / strm_sctn_len * 100
                print(prcnt_len)
                clr1, lbl1 = get_plot_feature_ramp(prcnt_len, ibm, 'Color: ', 0)
                mrkr1, lbl1 = get_plot_feature_ramp(prcnt_len, mrkrs, 'Marker: ', 0)

                title = chnl_name + ' average sedimentation rate change'  # Defines string. Sets plot title.

                # lbl = y + '–' + x  # Defines string. Sets plot
                # object labels.

                plot_lines(1, 1, fig_sz, df_srvy_yrs1_j, df_sed_rts_j, lbl1, clr1, mrkr1,
                           mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 0, lctn,
                           mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                           'Survey year', fntsz[0], lbl_pd,
                           'Average sedimentation rate (in/y)', title, 1, 1)  # Creates plot.
                # Calls function.

                if j == rng_nums[-1]:
                    plt.figure(1)
                    hndls, lbls = plt.gca().get_legend_handles_labels()
                    by_lbl = dict(zip(lbls, hndls))
                    plt.legend(by_lbl.values(), by_lbl.keys())
                    # Export data
                    fldr_lbls = ['/Statistical_analysis', '/Plots', '/Sedimentation_rate_change']
                    # Defines list. Sets folder labels for directory to be made.


                    fig_name = '/D_rt_chng_' + str(chnl_name) + '_' + str(srvy_yrs2[-1]) + '_' + str(srvy_yrs1[0]) + '.pdf'  # Defines variable as string.


                    export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1, 'pdf', None,
                                             None, 'Average sedimentation rate plot', None,
                                             None, None, 0)  # Creates directory and exports
                    # figure. Calls function.
        if Plt_sed_rt_chng == 1:
            rng_nums = slice_DataFrame_columns('List', 'Integer', df_rvr, 'Range_num', 1, 0, 'Transect numbers', 0)
            for j in rng_nums:
                df_rng_j = slice_DataFrame_rows('Equals', df_rvr, 'Range_num', j, 'RANGE NUMBER', 1)
                sed_rts_chng_j = slice_DataFrame_columns('Array', 'Float', df_rng_j, 'Rt_chng', 0, 0,
                                                       'Average sedimentation rates', 1)

                df_srvy_yrs1_j = slice_DataFrame_columns('DataFrame', 'Integer', df_rng_j, 'Srvy_year1', 0, 0,
                                                         'Average sedimentation rates', 1)
                strm_stat = slice_DataFrame_cell('Integer', 0, None, df_rng_j, 0, 'Strm_stat', 'Stream channel', 1)
                strm_stat_arry = slice_DataFrame_columns('Array', 'Integer', df_rvr, 'Strm_stat', 0, 0,
                                                         'Average sedimentation rates', 1)
                strm_stat_min = min(strm_stat_arry)
                strm_stat_max = max(strm_stat_arry)
                strm_stat_max = strm_stat_max - strm_stat_min
                strm_stat = strm_stat - strm_stat_min
                strm_stat_min = strm_stat_min - strm_stat_min
                print(strm_stat_min, strm_stat_max)
                strm_sctn_len = strm_stat_max - strm_stat_min
                prcnt_len = strm_stat / strm_sctn_len * 100
                print(prcnt_len)
                clr1, lbl1 = get_plot_feature_ramp(prcnt_len, ibm, 'Color: ', 0)
                mrkr1, lbl1 = get_plot_feature_ramp(prcnt_len, mrkrs, 'Marker: ', 0)

                title = chnl_name + ' average sedimentation rate of change'  # Defines string. Sets plot title.

                # lbl = y + '–' + x  # Defines string. Sets plot
                # object labels.

                plot_lines(1, 1, fig_sz, df_srvy_yrs1_j, sed_rts_chng_j, lbl1, clr1, mrkr1,
                           mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 0, lctn,
                           mrkr_scl, alpha[1], lbl_spcng, fntsz[1],
                           'Survey year', fntsz[0], lbl_pd,
                           'Sedimentation rate change', title, 1, 1)  # Creates plot.
                # Calls function.

                if j == rng_nums[-1]:
                    plt.figure(1)
                    hndls, lbls = plt.gca().get_legend_handles_labels()
                    by_lbl = dict(zip(lbls, hndls))
                    plt.legend(by_lbl.values(), by_lbl.keys())
                    # Export data
                    fldr_lbls = ['/Statistical_analysis', '/Plots', '/Sedimentation_rate_change']
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/D_rt_chng_nrml_' + str(chnl_name) + '_' + str(srvy_yrs2[-1]) + '_' + str(
                        srvy_yrs1[0]) + '.pdf'  # Defines variable as string.

                    export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1,
                                             'pdf', None,
                                             None, 'Average sedimentation rate plot', None,
                                             None, None, 0)  # Creates directory and exports
                    # figure. Calls function.
        for j in srvy_yrs1:
            df_rvr_j = slice_DataFrame_rows('Equals', df_rvr, 'Srvy_year1', j, 'SURVEY YEAR', 0)

            index = srvy_yrs1.index(j)
            yr1 = j
            yr2 = srvy_yrs2[index]
            sed_rts_j = slice_DataFrame_columns('List', 'Float', df_rvr_j, 'D_avg_in/y', 0, 0, 'Average sedimentation rates', 0)

            if Plt_sed_rt == 1:
                df_sed_rts_j = slice_DataFrame_columns('DataFrame', 'Float', df_rvr_j, 'D_avg_in/y', 0, 0,
                                                    'Average sedimentation rates', 1)
                df_strm_stat_j = slice_DataFrame_columns('DataFrame', 'Integer', df_rvr_j, 'Strm_stat', 0, 0, 'STREAM STATION', 0)  # Defines
                # DataFrame. Calls function. Slices DataFrame to yield stream station data.

                df_strm_stat_j = df_strm_stat_j.iloc[::-1]  # Redefines DataFrame. Inverts
                # values. For plotting sedimentation in the downstream direction.
                df_strm_stat_j = df_strm_stat_j.divide(1000)  # Redefines DataFrame.
                # Modifies values to be displayed in scientific notation.
                print(df_strm_stat_j)
                df_sed_rts_j = df_sed_rts_j.iloc[::-1]
                print(df_sed_rts_j)
                clr1 = get_plot_feature_by_year(j, tol_mtd, 'Color : ', 0)
                    # Defines variable. Calls function. Sets plot color.
                mrkr1 = get_plot_feature_by_year(j, mrkrs, 'Marker: ', 0)  # Defines
                # variable. Calls function. Sets plot marker type.

                title = 'Average sedimentation rates'  # Defines string. Sets plot title.

                lbl = str(yr2) + '–' + str(yr1)  # Defines string. Sets plot
                # object labels.

                plot_lines(1, 1, fig_sz, df_strm_stat_j, df_sed_rts_j, lbl, clr1, mrkr1, mrkr_sz[0], lin_wdth[0], lin_styl[0], alpha[0], 1, lctn,
                           mrkr_scl, alpha[1], lbl_spcng, fntsz[1], 'River station (1 x 10^3 ft)', fntsz[0], lbl_pd, 'Average sedimentation rate (in/y)', title, 1, 1)  # Creates
                # plot. Calls function.

                if j == srvy_yrs1[-1]:
                    plt.figure(1)  # Creates plot window. Sets figure size.
                    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
                    ax.invert_xaxis()  # Inverts x-axis.

                # Export data
                    fldr_lbls = ['/Statistical_analysis', '/Plots', '/Sedimentation_rate']
                    # Defines list. Sets folder labels for directory to be made.

                    if Rvr == 1:  # Conditional statement. Sets name of file for export.
                        fig_name = '/D_rt_' + str(chnl_name) + '_' + str(yr2) + '_' + str(srvy_yrs1[0]) + '.pdf'  # Defines variable as string.
                    else:  # Conditional statement.
                        fig_name = '/D_rt_Bsn' + str(yr2) + '_' + str(srvy_yrs1[0]) + '.pdf'  # Defines variable as string.

                    export_file_to_directory(1, 'Figure', 3, fldr_lbls, opt_fldr, 'Directories named: ', fig_name, 1, 'pdf', None,
                                             None, 'Average sedimentation rate plot', None,
                                             None, None, 0)  # Creates directory and exports
                    # figure. Calls function.
            # Plots
            if Plt_sed_dst == 1:
                title = str(chnl_name) + ' ' + str(yr2) + '-' + str(yr1) + ' rates'
                pstn = [index]
                plot_box(0, sed_rts_j, pstn, True, True, None, 'Cyan', title, 1, 1)

                # Export data
                fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + chnl_name]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/D_rt_dst_' + str(chnl_name) + '_' + str(yr2) + '_' + str(
                    yr1) + '.pdf'  # Defines variable as string.

                export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                         'Directories named: ', fig_name, 0, 'pdf', None,
                                         None, 'Average sedimentation rate box plot', None,
                                         None, None, 0)  # Creates directory and exports
                # figure. Calls function.

                plot_histogram(0, sed_rts_j, 'Cyan', 'Black', title, 1, 2)

                # Export data
                fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + chnl_name]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/D_rt_dst_hst_' + str(chnl_name) + '_' + str(yr2) + '_' + str(
                    yr1) + '.pdf'  # Defines variable as string.

                export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                         'Directories named: ', fig_name, 0, 'pdf', None,
                                         None, 'Sediment thickness histogram', None,
                                         None, None, 0)  # Creates directory and exports
                # figure. Calls function.


                plot_qq(0, sed_rts_j, None, title, 1, 1)

                # Export data
                fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + chnl_name]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/D_rt_dst_qq_' + str(chnl_name) + '_' + str(yr2) + '_' + str(
                    yr1) + '.pdf'  # Defines variable as string.

                export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                         'Directories named: ', fig_name, plt.gcf().number, 'pdf', None,
                                         None, 'Sediment thickness Q-Q plot', None,
                                         None, None, 0)  # Creates directory and exports
                # figure. Calls function.
            if Nrml_tst == 1:
                if Shpr_Wlk == 1:
                    H_0 = 'Average sedimentation rates come from a normal distribution'
                    H_1 = 'Average sedimentation rates do not come from a normal distribution'
                    shaprio_wilk_test(sed_rts_j, H_0, H_1, 1)

            if j == srvy_yrs1[0]:
                stat_smpls = []
                stat_smpls_N = []
            create_appended_list(sed_rts_j, 'Survey interval data', stat_smpls, 'New list appended: ', 0)
            create_appended_list(len(sed_rts_j), 'Survey interval sample size', stat_smpls_N, 'New list appended: ', 0)

            if j == srvy_yrs1[-1]:
                if Plt_sed_dst_all == 1:
                    title = str(chnl_name) + ' ' + str(yr2) + '-' + str(srvy_yrs1[0]) + ' rates'
                    for k in stat_smpls:
                        index = stat_smpls.index(k)
                        pstn = [index]
                        plot_box(0, k, pstn, True, True, None, 'Cyan', title, 1, 1)

                    # Export data
                    fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + chnl_name]
                    # Defines list. Sets folder labels for directory to be made.

                    fig_name = '/D_rt_dst_all_' + str(chnl_name) + '_' + str(yr2) + '_' + str(
                        srvy_yrs1[0]) + '.pdf'  # Defines variable as string.

                    export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                             'Directories named: ', fig_name, 0, 'pdf', None,
                                             None, 'Average sedimentation rate box plot', None,
                                             None, None, 0)  # Creates directory and exports
                # figure. Calls function.
                for k in stat_smpls:
                    index = stat_smpls.index(k)
                    str_name = 'smpl_' + str(index)
                    locals()[str_name] = k

                if Hyp_tst == 1:
                    # Stat tests
                    if ANOVA == 1:
                        H_0 = 'Average sedimentation rates are the same for all time periods'
                        H_1 = 'Average sedimentation rates are not the same for all time periods'
                        alpha = 0.05
                        if len(stat_smpls) == 4:
                            F, pvalue = sc.stats.f_oneway(smpl_0, smpl_1, smpl_2, smpl_3)
                        elif len(stat_smpls) == 3:
                            F, pvalue = sc.stats.f_oneway(smpl_0, smpl_1, smpl_2)
                        print(f'One-way ANOVA test: s = {F}, p = {pvalue}')
                        if pvalue < alpha:
                            rslt = 'Reject'
                            print(f'{rslt} H_0: {H_1}')
                        elif pvalue > alpha:
                            rslt = 'Accept'
                            print(f'{rslt} H_0: {H_0}')
                    if Tky == 1:
                        alpha = 0.05
                        for x in stat_smpls:
                            index = stat_smpls.index(x)
                            if index == 0:
                                df_tky = pd.DataFrame()
                                df_smpl = pd.DataFrame({'Rate': x, 'Group': index})
                                df_tky = pd.concat([df_tky, df_smpl])
                                del df_smpl
                            elif index > 0:
                                df_smpl = pd.DataFrame({'Rate': x, 'Group': index})
                                df_tky = pd.concat([df_tky, df_smpl])
                        # print(df_tky)
                        tky = sm.stats.multicomp.pairwise_tukeyhsd(endog=df_tky['Rate'], groups=df_tky['Group'], alpha=alpha)
                        print(tky)
                        # breakpoint()
                    if Krskl_Wlls == 1:
                        H_0 = 'Average sedimentation rates are the same for all time periods'
                        H_1 = 'Average sedimentation rates are not the same for all time periods'
                        alpha = 0.05
                        smpl_sz = all(x > 5 for x in stat_smpls_N)

                        if smpl_sz == False:
                            print('At least one sample size < 5')
                        if len(stat_smpls) == 4:
                            H, pvalue = scipy.stats.kruskal(smpl_0, smpl_1, smpl_2, smpl_3)
                        elif len(stat_smpls) == 3:
                            H, pvalue = scipy.stats.kruskal(smpl_0, smpl_1, smpl_2)
                        print(f'Kruskal_Wallis H test: s = {H}, p = {pvalue}')
                        if pvalue < alpha:
                            rslt = 'Reject'
                            print(f'{rslt} H_0: {H_1}')
                        elif pvalue > alpha:
                            rslt = 'Accept'
                            print(f'{rslt} H_0: {H_0}')

                    if Dnn == 1:
                        pvalues = sp.posthoc_dunn(stat_smpls, p_adjust='bonferroni')
                        # pvalues = np.tri(pvalues)
                        print(pvalues)
                        print(pvalues < 0.05)

if Bsn == 1:
    srvy_yrs1 = slice_DataFrame_columns('List', 'Integer', df_sed_dt, 'Srvy_year1', 1, 0, 'Survey years', 0)
    srvy_yrs2 = slice_DataFrame_columns('List', 'Integer', df_sed_dt, 'Srvy_year2', 1, 0, 'Survey years', 0)
    srvy_yrs1.sort(reverse=True)
    srvy_yrs2.sort(reverse=True)
    for i in srvy_yrs1:
        index = srvy_yrs1.index(i)
        yr1 = i
        yr2 = srvy_yrs2[index]
        df_srvy_yr = slice_DataFrame_rows('Equals', df_sed_dt, 'Srvy_year1', i, 'RIVER NUMBER', 0)
        sed_rts = slice_DataFrame_columns('List', 'Float', df_srvy_yr, 'D_avg_in/y', 0, 0, 'Average sedimentation rates', 0)

        if Plt_sed_dst_bsn == 1:
            bsn = 'Whitewater'
            title = bsn + ' ' + str(yr2) + '-' + str(yr1) + ' rates'
            pstn = [index]
            plot_box(0, sed_rts, pstn, True, True, None, 'Cyan', title, 1, 1)

            # Export data
            fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + bsn]
            # Defines list. Sets folder labels for directory to be made.

            fig_name = '/D_rt_dst' + '_' + str(yr2) + '_' + str(
                yr1) + '.pdf'  # Defines variable as string.

            export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                     'Directories named: ', fig_name, 0, 'pdf', None,
                                     None, 'Average sedimentation rate box plot', None,
                                     None, None, 0)  # Creates directory and exports
            # figure. Calls function.

            plot_histogram(0, sed_rts, 'Cyan', 'Black', title, 1, 2)

            # Export data
            fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + bsn]
            # Defines list. Sets folder labels for directory to be made.

            fig_name = '/D_rt_dst_hst' + '_' + str(yr2) + '_' + str(
                yr1) + '.pdf'  # Defines variable as string.

            export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                     'Directories named: ', fig_name, 0, 'pdf', None,
                                     None, 'Sediment thickness histogram', None,
                                     None, None, 0)  # Creates directory and exports
            # figure. Calls function.


            plot_qq(0, sed_rts, '45', title, 1, 1)

            # Export data
            fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + bsn]
            # Defines list. Sets folder labels for directory to be made.

            fig_name = '/D_rt_dst_qq'  + '_' + str(yr2) + '_' + str(
                yr1) + '.pdf'  # Defines variable as string.

            export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                     'Directories named: ', fig_name, plt.gcf().number, 'pdf', None,
                                     None, 'Sediment thickness Q-Q plot', None,
                                     None, None, 0)  # Creates directory and exports
            # figure. Calls function.
        if i == srvy_yrs1[0]:
            stat_smpls = []
            stat_smpls_N = []
        create_appended_list(sed_rts, 'Survey interval data', stat_smpls, 'New list appended: ', 0)
        create_appended_list(len(sed_rts), 'Survey interval sample size', stat_smpls_N, 'New list appended: ', 0)
        if i == srvy_yrs1[-1]:
            if Plt_sed_dst_bsn_all == 1:
                bsn = 'Whitewater'
                title = bsn + ' ' + str(yr2) + '-' + str(srvy_yrs1[0]) + ' rates'
                for j in stat_smpls:
                    index = stat_smpls.index(j)
                    pstn = [index]
                    plot_box(0, j, pstn, True, True, None, 'Cyan', title, 1, 1)

                # Export data
                fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + bsn]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/D_rt_dst_all' + '_' + str(yr2) + '_' + str(
                    srvy_yrs1[0]) + '.pdf'  # Defines variable as string.

                export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                         'Directories named: ', fig_name, 0, 'pdf', None,
                                         None, 'Average sedimentation rate box plot', None,
                                         None, None, 0)  # Creates directory and exports
                # figure. Calls function.
            for j in stat_smpls:
                index = stat_smpls.index(j)
                str_name = 'smpl_' + str(index)
                locals()[str_name] = j
            if Hyp_tst == 1:
                # Stat tests
                if ANOVA == 1:
                    H_0 = 'Average sedimentation rates are the same for all time periods'
                    H_1 = 'Average sedimentation rates are not the same for all time periods'
                    alpha = 0.05
                    if len(stat_smpls) == 4:
                        F, pvalue = sc.stats.f_oneway(smpl_0, smpl_1, smpl_2, smpl_3)
                    elif len(stat_smpls) == 3:
                        F, pvalue = sc.stats.f_oneway(smpl_0, smpl_1, smpl_2)
                    print(f'One-way ANOVA test: s = {F}, p = {pvalue}')
                    if pvalue < alpha:
                        rslt = 'Reject'
                        print(f'{rslt} H_0: {H_1}')
                    elif pvalue > alpha:
                        rslt = 'Accept'
                        print(f'{rslt} H_0: {H_0}')

                if Krskl_Wlls == 1:
                    H_0 = 'Average sedimentation rates are the same for all time periods'
                    H_1 = 'Average sedimentation rates are not the same for all time periods'
                    alpha = 0.05
                    smpl_sz = all(x > 5 for x in stat_smpls_N)

                    if smpl_sz == False:
                        print('At least one sample size < 5')
                    if len(stat_smpls) == 4:
                        H, pvalue = scipy.stats.kruskal(smpl_0, smpl_1, smpl_2, smpl_3)
                    elif len(stat_smpls) == 3:
                        H, pvalue = scipy.stats.kruskal(smpl_0, smpl_1, smpl_2)
                    print(f'Kruskal_Wallis H test: s = {H}, p = {pvalue}')
                    if pvalue < alpha:
                        rslt = 'Reject'
                        print(f'{rslt} H_0: {H_1}')
                    elif pvalue > alpha:
                        rslt = 'Accept'
                        print(f'{rslt} H_0: {H_0}')

                if Dnn == 1:
                    pvalues = sp.posthoc_dunn(stat_smpls, p_adjust='bonferroni')
                    # pvalues = np.tri(pvalues)
                    print(pvalues)
                    print(pvalues < 0.05)



# ======================================================================================================================
# END ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================