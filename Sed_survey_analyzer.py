# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * ---------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os, sys  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.
import pandas as pd  # Imports "Python data analysis library" with alias. Enables DataFrame array functionality.
from Cross_section_analyzer import *  # Imports all functions from program.

# START TIMER ----------------------------------------------------------------------------------------------------------

strtTm0 = time.time()  # Starts clock. Measures program run time.

# SET PARAMETERS -------------------------------------------------------------------------------------------------------

# Data operations ------------------------------------------------------------------------------------------------------

# Calculate sediment thickness
Hydr_geom = 1
Dpth = 1  # Defines variable as integer. Sets binary toggle for operation selection.
Plot = 1
# Digitize survey data
Dgtz = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Data selection -------------------------------------------------------------------------------------------------------

# Field ranges
rng_strt = 70  # Defines variable as integer. Sets starting range for analysis.
rng_end = 73  # Defines variable as integer. Sets end range for analysis.

# Range surveys
srvy_strt = 4  # Defines variable as integer. Sets starting survey for analysis.
srvy_end = 2  # Defines variable as integer. Sets end survey for analysis.

# Data plotting --------------------------------------------------------------------------------------------------------

# General format
width = 4.5  # Defines variable as integer. Sets cross-sectional plot width.
height = width * 1.618  # Defines variable as integer. Sets cross-sectional plot height.
figure_size = (height, width)  # Defines object. Input for function.
fontsize_ticks = 8  # Defines variable as integer. Sets font size for axes tick marks.
fontsize_axis = 10  # Defines variable as integer. Sets font size for axis labels.
label_pad = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Data display format
ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes for ultramarine, indigo, magenta, orange, and gold.
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDD']  # Defines list.
# Sets muted Tol colorblind friendly palette in color hex color codes for indigo, cyan, teal, green, olive, sand, rose, wine, purple, and pale grey.
# 2008 = 0, 1994 = 3, 1978 = 2, 1975 = 4, 1964 = 5, 1939 = 6, 1850S = 7.
tol_vibrant = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', '#BBBBBB']  # Defines list. Sets
# vibrant Tol colorblind friendly palette in color hex color codes for blue, cyan, teal, orange, red, magenta, grey.
marker_mpltlib = ['.', ',', 'o', 'v', '^', '<', '>',
                          '1', '2', '3', '4', '8',
                          's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd',
                          '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ' ']  # Defines list. Complete list of matplotlib plot markers.
marker_mpltlib = ['o', 'v', '^', '<', '>', '8', 's', 'p', 'P', 'h', 'H', 'X', 'D', 'd', ' ']  # Defines list. Complete list of matplotlib plot markers.

marker_size = 4  # Defines variable as integer. Sets plot marker size.
line_width = 2  # Defines variable as integer. Sets plot line width.
alpha = 0.5  # Defines variable as integer. Sets plotted object transparency.

# Legend display format
location = ['upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right', 'center', 'best']  # Defines list. Complete list of matplotlib legend placements.
location = 'best'
marker_scale = 2  # Defines variable as integer. Sets marker size on legend.
frame_alpha = 0.7  # Defines variable as integer. Sets legend box transparency.
label_spacing = 0.7  # Defines variable as integer. Sets legend object spacing.

pause_length = 1

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Name levels ----------------------------------------------------------------------------------------------------------

# Level 1
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Create folders -------------------------------------------------------------------------------------------------------

lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.

def create_folder(level, path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')  # Displays objects.

for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    level = 1  # Defines variable. Sets value based in list element index for display.

    create_folder(level, a)  # Creates folders. Calls function.

# ======================================================================================================================
# PART 2: DATA SELECTION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# UPLOAD DATA ----------------------------------------------------------------------------------------------------------

def upload_csv(path, label):  # Defines function. For uploading .csv and conversion to DataFrame.
    csv_data = pd.read_csv(path)  # Uploads .csv file.
    df = pd.DataFrame(csv_data)  # Converts .csv file to DataFrame.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame format. Displays all DataFrame columns.
    if chck == 1:  # Conditional statement.
        print('\033[1m' + 'UPLOADED .CSV DATA FOR ' + label + '\033[0m', '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends execution of function.

inpt_fl = '/Users/jimmywood/github/Whitewater_MN_sedimentation/PyCharm_Venv/Input/Trout_Creek_survey_data.csv'  # Defines string. Sets file path.
chck = 0  # Defines variable. For function display.
df_chnnl = upload_csv(inpt_fl, 'TROUT CREEK ')  # Defines DataFrame. Calls function.

# SET DATA SELECTION LIMITS --------------------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------

def forward_range(start, end, step, data_label):  # Defines function. For generating forward range array between two numbers.
    end = end + 1  # Defines variable. Sets end of range to include final input value.
    end_label = end - 1  # Defines variable. Sets label for display.
    frwd_rng = np.arange(start, end, step)  # Defines format of function.
    if chck == 1:  # Conditional statement.
        print(data_label, start, '&', end_label, ':', frwd_rng)  # Displays objects.
    return frwd_rng  # Ends execution of function.

chck = 0  # Defines variable. For function display.
rgn_nums = forward_range(rng_strt, rng_end, 1, 'Range number limits')  # Defines array. Calls function.

# Temporal -------------------------------------------------------------------------------------------------------------

def reverse_range(start, end, step, data_label):  # Defines function. For generating forward range array between two numbers.
    end = end - 1  # Defines variable. Sets end of range to include final input value.
    end_label = end + 1  # Defines variable. Sets label for display.
    rev_rng = np.arange(start, end, step)  # Defines format of function.
    if chck == 1:  # Conditional statement.
        print(data_label, start, '&', end_label, ':', rev_rng, '\n')  # Displays objects.
    return rev_rng  # Ends execution of function.

chck = 0  # Defines variable. For function display.
srvy_nums = reverse_range(srvy_strt, srvy_end, -1, 'Survey number limits')  # Defines array. Calls function.

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# By field range -------------------------------------------------------------------------------------------------------

for a in rgn_nums:  # Begins loop. Loops through range numbers.

    def slice_DataFrame_rows1(dataframe, column, row_value,
                             label):  # Defines function. For DataFrame slicing by row value.
        df_slc_r = dataframe[dataframe[column] == row_value]  # Defines format of function.
        if chck == 1:  # Conditional statement.
            print('\033[1m' + label + ' ' + str(row_value) + ' DATA' + '\033[0m',
                  '\n..\n', df_slc_r, '\n')  # Displays objects.
        return df_slc_r  # Ends execution of function.

    chck = 0  # Defines variable. For function display.

    df_rng = slice_DataFrame_rows1(df_chnnl, 'Range_num', a, 'RANGE NUMBER')

    # By range survey --------------------------------------------------------------------------------------------------

    for b in srvy_nums:  # Begins loop. Loos through range numbers.
        def slice_DataFrame_rows2(dataframe, column1, row_value1,
                                 label1, row_value2, label2):  # Defines function. For DataFrame slicing by row value.
            df_slc_r = dataframe[dataframe[column1] == row_value1]  # Defines format of function.
            if chck == 1:  # Conditional statement.
                print('\033[1m' + label2 + ' ' + str(row_value2) + ' ' + label1 + ' ' + str(row_value1) + ' DATA' + '\033[0m',
                      '\n..\n', df_slc_r, '\n')  # Displays objects.
            return df_slc_r  # Ends execution of function.

        chck = 0  # Defines variable. For function display.
        df_srvy1 = slice_DataFrame_rows2(df_rng, 'Srvy_num', b, 'SURVEY NUMBER', a, 'RANGE NUMBER')
        # df_srvy2 = slice_DataFrame_rows2(df_rng, 'Srvy_num', c, 'SURVEY NUMBER', a, 'RANGE NUMBER')

        #meta
        def slice_DataFrame_cell(dataframe, column, index,
                                 data_label):  # Defines function. For DataFrame slicing by row value.
            df_slc_cl = dataframe.loc[index, column]
            if chck == 1:  # Conditional statement.
                print(data_label + ':', df_slc_cl, '\n')  # Displays objects.
            return df_slc_cl  # Ends execution of function.

        chck = 0
        index = df_srvy1.index
        srvy_yr1 = slice_DataFrame_cell(df_srvy1, 'Srvy_year', index[0], 'Survey year')  # Defines variable.
        rng_nm1 = slice_DataFrame_cell(df_srvy1, 'Srvy_range', index[0], 'Range')  # Defines variable.
        # srvy_yr2 = slice_DataFrame_cell(df_srvy2, 'Srvy_year', 'Survey year')  # Defines variable.
        # rng_nm2 = slice_DataFrame_cell(df_srvy2, 'Srvy_range', 'Range')  # Defines variable.

        # DISPLAY DATASET ------------------------------------------------------------------------------------------

        # print('==================================================')
        # print('\033[1m' + 'Field range (number): ' + '\033[0m' + str(rng_nm1) + ' (' + str(rng_strt) + ')')
        # print('\033[1m' + 'Range survey interval (numbers): ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' + str(srvy_strt) + '–' + str(srvy_end) + ')')
        # chck = 0
        # srvy_dt1 = slice_DataFrame_cell(df_srvy1, 'Srvy_date', 'Survey date')  # Defines variable.
        # srvy_dt2 = slice_DataFrame_cell(df_srvy2, 'Srvy_date', 'Survey date')  # Defines variable.
        # print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))
        # print('--------------------------------------------------')
        #
        def slice_DataFrame_columns1(dataframe, column, data_label):  # Defines function. For DataFrame slicing by row value.
            df_slc_c = dataframe[column]  # Defines format of function.
            if chck == 1:  # Conditional statement.
                print('\033[1m' + data_label + ' DATA' + '\033[0m', '\n..\n', df_slc_c, '\n')  # Displays objects.
            return df_slc_c  # Ends execution of function.

        print('==================================================')
        print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_nm1) + ' (' + str(a) + ')')
        df_srvy_yrs = slice_DataFrame_columns1(df_rng, 'Srvy_num', 'Survey numbers')
        df_srvy_yrs = df_srvy_yrs.drop_duplicates(keep='first')
        srvy_yrs = df_srvy_yrs.to_numpy()
        num_srvys = max(srvy_yrs)
        print('\033[1m' + 'Range survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(b) + ' of ' + str(num_srvys) + ')')
        chck = 0
        index = df_srvy1.index
        srvy_dt1 = slice_DataFrame_cell(df_srvy1, 'Srvy_date', index[0], 'Survey date')  # Defines variable.
        # srvy_dt2 = slice_DataFrame_cell(df_srvy2, 'Srvy_date', 'Survey date')  # Defines variable.
        print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1))
        print('--------------------------------------------------')

        # Plot

        # By survey measurement ------------------------------------------------------------------------------------

        df_offst1 = slice_DataFrame_columns1(df_srvy1, 'Offset_ft', 'OFFSET')
        df_elvtn1 = slice_DataFrame_columns1(df_srvy1, 'Elv_lcl_ft', 'ELEVATION')

        # PLOT CROSS-SECTIONS --------------------------------------------------------------------------------------

        def plot_lines1(number, figure_size, x, y, label1, color1, marker1, marker_size, line_width, alpha,
                        fontsize_ticks, x_label, fontsize_axis, label_pad, y_label, title1, pause_length):

            plt.figure(number, figsize=figure_size)
            ax = plt.gca()
            ax.plot(x, y, label=label1, c=color1, marker=marker1, markersize=marker_size, linewidth=line_width, alpha=alpha)  # Creates line
            # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
            # ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)  # Creates legend through automatic label detection.
            plt.xticks(fontsize=fontsize_ticks)
            plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets font size.
            plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates y-axis label. Sets font size.
            plt.yticks(fontsize=fontsize_ticks)
            plt.title(title1)  # Creates plot title.
            if pause == 1:
                plt.pause(pause_length)  # Displays and updates active figure before pausing for interval seconds.
            elif pause == 0:
                plt.show()

        pause = 1

        if srvy_yr1 == '2008':
            color = tol_muted[0]
            marker = marker_mpltlib[-1]
        elif srvy_yr1 == '1994':
            color = tol_muted[3]
            marker = marker_mpltlib[0]
        elif srvy_yr1 == '1978':
            color = tol_muted[2]
            marker = marker_mpltlib[8]
        elif srvy_yr1 == '1975':
            color = tol_muted[4]
            marker = marker_mpltlib[11]
        elif srvy_yr1 == '1964':
            color = tol_muted[5]
            marker = marker_mpltlib[6]
        elif srvy_yr1 == '1939':
            color = tol_muted[6]
            marker = marker_mpltlib[2]
        elif srvy_yr1 == '1850s':
            color = tol_muted[7]
            marker = marker_mpltlib[-2]


        title1 = 'Range ' + str(rng_nm1) + ' survey ' + str(srvy_yr1)
        plot_lines1(1, figure_size, df_offst1, df_elvtn1, srvy_yr1, color, marker, marker_size, line_width,
                    alpha, fontsize_ticks, 'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)', title1, pause_length)

        # export
        # create folder
        #level2
        xsctn_fldr = '/Cross_sectional_analysis'
        lvl2 = opt_fldr + xsctn_fldr
        plts_fldr = '/Plots'
        lvl3 = lvl2 + plts_fldr
        xsctn_plts_fldr = '/Cross_sections'
        lvl4 = lvl3 + xsctn_plts_fldr
        xsctn_plts_fldr1 = '/Single'
        lvl5 = lvl4 + xsctn_plts_fldr1
        lvls = [lvl2, lvl3, lvl4, lvl5]

        for i in lvls:
            level = lvls.index(i)
            create_folder(level, i)

        # Export
        plt.figure(1)  # Calls figure making it the active plot.

        fig_name = '/' + str(rng_nm1) + '_s' +str(b) + '_' + str(srvy_yr1) + '.pdf'  # Sets name of
        # exported figure.

        plt.savefig(lvl5 + fig_name,
                    format='pdf')  # Saves figure to directory. Sets file format.

        plt.close()  # Closes active figure.

        if Hydr_geom == 1:
            chck = 0
            df_strm = slice_DataFrame_rows1(df_srvy1, 'Gmrph_dsc', 'Stream channel', 'RANGE ' + str(a))

            # df_strm_offsts = slice_DataFrame_columns1(df_strm, 'Offset_ft', 'RANGE ' + str(a) + ' STREAM CHANNEL OFFSETS')
            # df_strm_elvtns = slice_DataFrame_columns1(df_strm, 'Elv_lcl_ft', 'RANGE ' + str(a) + ' STREAM CHANNEL ELEVATIONS')

            def hydraulic_geometry(dataframe, column1, data_label1, column2, data_label2, chck):
                chck=chck
                df_slc_wdth = slice_DataFrame_columns1(dataframe, column1, data_label1)
                offst1 = df_slc_wdth.min()
                offst2 = df_slc_wdth.max()

                if offst1 < offst2:
                    width = offst2 - offst1
                elif offst1 > offst2:
                    sys.exit('No stream channel detected')
                elif offst1 == offst2:
                    sys.exit('No stream channel detected')
                chck=1
                if chck == 1:
                    print(offst1, offst2, width)

                chck=chck
                df_slc_dpth = slice_DataFrame_columns1(dataframe, column2, data_label2)
                elvtn1 = df_slc_dpth.min()
                elvtn2 = df_slc_dpth.max()

                if elvtn1 < elvtn2:
                    depth = elvtn2 - elvtn1
                elif elvtn1 > elvtn2:
                    sys.exit('No stream channel detected')
                elif elvtn1 == elvtn2:
                    sys.exit('No stream channel detected')

                chck=1
                if chck ==1:
                    print(elvtn1, elvtn2, depth)


            hydraulic_geometry(df_strm, 'Offset_ft', 'RANGE ' + str(a) + ' STREAM CHANNEL OFFSET', 'Elv_lcl_ft',  'RANGE ' + str(a) + ' STREAM CHANNEL ELEVATION', 0)


#             chck = 0  # Defines variable. For function display.
#
#             df_offst2 = slice_DataFrame_columns1(df_srvy2, 'Offset_ft', 'OFFSET')
#             df_elvtn2 = slice_DataFrame_columns1(df_srvy2, 'Elv_lcl_ft', 'ELEVATION')
#
#             pause = 1
#             title1 = 'Range ' + str(rng_nm2) + ' survey ' + str(srvy_yr2)
#             plot_lines1(2, figure_size, df_offst2, df_elvtn2, srvy_yr2, tol_muted[c], marker1, marker_size,
#                         line_width,
#                         alpha, fontsize_ticks, 'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)',
#                         title1, 5)
#
#
#             def plot_lines2(number, figure_size, x1, y1, label1, x2, y2, label2, color1, marker1, color2, marker2,
#                             marker_size, line_width, alpha,
#                             fontsize_ticks, x_label, fontsize_axis, label_pad, y_label, title1, location, marker_scale, frame_alpha, label_spacing, pause_length):
#
#                 plt.figure(number, figsize=figure_size)
#                 ax = plt.gca()
#                 ax.plot(x1, y1, label=label1, c=color1, marker=marker1, markersize=marker_size, linewidth=line_width, alpha=alpha)  # Creates line
#                 # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
#                 ax.plot(x2, y2, label=label2, c=color2, marker=marker2, markersize=marker_size, linewidth=line_width,
#                         alpha=alpha)  # Creates line
#                 # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
#                 ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)  # Creates legend through automatic label detection.
#                 plt.xticks(fontsize=fontsize_ticks)
#                 plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets font size.
#                 plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates y-axis label. Sets font size.
#                 plt.yticks(fontsize=fontsize_ticks)
#                 plt.title(title1)  # Creates plot title.
#                 if pause == 1:
#                     plt.pause(pause_length)  # Displays and updates active figure before pausing for interval seconds.
#                 elif pause == 0:
#                     plt.show()
#                 plt.close()
#
#             pause = 1
#             title1 = 'Range ' + str(rng_nm1) + ' surveys'
#             plot_lines2(3, figure_size, df_offst1, df_elvtn1, srvy_yr1, df_offst2, df_elvtn2, srvy_yr2, tol_muted[b],
#                         marker1, tol_muted[c], marker1, marker_size, line_width, alpha, fontsize_ticks,
#                         'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)', title1, location,
#                         marker_scale, frame_alpha, label_spacing, 5)
#
#
#
# # if Dgtz == 1:
# #     dgtz_fldr = '/Digitization'  # Defines variable as string. Sets name of new directory where digitization data will be
#     # located.