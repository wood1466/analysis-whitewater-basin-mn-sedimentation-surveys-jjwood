# ======================================================================================================================
# WHITEWATER RIVER VALLEY, MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * --------------------------------------------
# STATISTICS PROGRAM * -------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------
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

Plt_sed_dst = 0

# Whole basin analysis ----------------------------------------------------------------------------------------

Bsn = 0  # Defines variable as integer. Sets binary toggle.

# Calculate statistics
ANOVA = 1
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

inpt_fl1 = inpt_fldr + '/Sediment_thickness.csv'  # Defines string. Sets file path to input file.

df_sed_dt = csv_to_DataFrame(inpt_fl1, 'TEST DATA', 0)  # Defines DataFrame. Calls function. Uploads survey data.

df_sed_dt = slice_DataFrame_rows('Equals', df_sed_dt, 'Outlier', 'Statistics' , 'TEST DATA', 0)

if xtra_srvys == 1:
    inpt_fl2 = inpt_fldr + '/Sediment_thickness_11B.csv'  # Defines string. Sets file path to input file.

    df_11B_sed_dt = csv_to_DataFrame(inpt_fl2, 'TEST DATA 11B', 0)  # Defines DataFrame. Calls function. Uploads
    # transect drainage area data.

# Establish spatial selection framework
if rvr_nly == 1:
    rvr_nums = [rvr_strt]
    rvr_end = rvr_strt
elif rvr_nly == 0:
    rvr_nums = forward_range(rvr_strt, rvr_end, 1, 'Channel numbers', 0)


# retreive metadata
# Select river dataset
if Rvr == 1:
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

        for j in srvy_yrs1:
            df_rvr_j = slice_DataFrame_rows('Equals', df_rvr, 'Srvy_year1', j, 'SURVEY YEAR', 0)
            index = srvy_yrs1.index(j)
            yr1 = j
            yr2 = srvy_yrs2[index]
            sed_rts_j = slice_DataFrame_columns('List', 'Float', df_rvr_j, 'D_avg_in/y', 0, 0, 'Average sedimentation rates', 0)

            # Plots
            if Plt_sed_dst == 1:
                title = str(chnl_name) + ' ' + str(yr2) + '-' + str(yr1) + ' rates'
                plot_box(0, sed_rts_arry , True, True, None, 'Cyan', title, 1, 1)

                # Export data
                fldr_lbls = ['/Statistical_analysis', '/Plots', '/Rate_distribution', '/' + chnl_name]
                # Defines list. Sets folder labels for directory to be made.

                fig_name = '/D_rt_dst_' + str(chnl_name) + '_' + str(yr2) + '_' + str(
                    yr1) + '.pdf'  # Defines variable as string.

                export_file_to_directory(1, 'Figure', 4, fldr_lbls, opt_fldr,
                                         'Directories named: ', fig_name, 0, 'pdf', None,
                                         None, 'Sediment thickness box plot', None,
                                         None, None, 0)  # Creates directory and exports
                # figure. Calls function.

                plot_histogram(0, sed_rts_arry, 'Cyan', 'Black', title, 1, 2)

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


                plot_qq(0, sed_rts_arry, '45', title, 1, 1)

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

            if j == srvy_yrs1[0]:
                stat_smpls = []
                stat_smpls_N = []
            create_appended_list(sed_rts_j, 'Survey interval data', stat_smpls, 'New list appended: ', 0)
            create_appended_list(len(sed_rts_j), 'Survey interval sample size', stat_smpls_N, 'New list appended: ', 0)

            if j == srvy_yrs1[-1]:
                for k in stat_smpls:
                    index = stat_smpls.index(k)
                    str_name = 'smpl_' + str(index)
                    locals()[str_name] = k

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
                    if smpl_sz == 'False':
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
                    print(pvalues)
                    print(pvalues < 0.05)

# ======================================================================================================================
# END ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================