# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.
import pandas as pd  # Imports "Python data analysis library" with alias. Enables DataFrame array functionality.
from Cross_section_analyzer import *  # Imports all functions from secondary program.

# START TIMER ----------------------------------------------------------------------------------------------------------

strtTm0 = time.time()  # Starts clock. Measures program run time.

# SET UP PARAMETERS ----------------------------------------------------------------------------------------------------

# Data operations ------------------------------------------------------------------------------------------------------

# Calculate sediment cross-sectional area
Area = 1  # Defines variable as integer. Sets binary toggle for operation selection.

# Data selection -------------------------------------------------------------------------------------------------------

# Field ranges
rng_strt = 70  # Defines variable as integer. Sets starting range for analysis.
rng_end = 71  # Defines variable as integer. Sets end range for analysis.

# Range surveys
srvy_strt = 4  # Defines variable as integer. Sets starting survey for analysis.
srvy_end = 3  # Defines variable as integer. Sets end survey for analysis.

# Plotting -------------------------------------------------------------------------------------------------------

# General
width = 4.5
height = width * 1.618
figure_size = (height, width)

# Data format
ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes.
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733', '#DDCC77', '#882255', '#DDDDD']  # Defines list.
# Sets muted Tol colorblind friendly palette in color hex color codes.
tol_vibrant = ['#0077BB', '#33BBEE', '#009988', '#999933', '#999933', '#CC6677']  # Defines list. Sets
# vibrant Tol colorblind friendly palette in color hex color codes.
marker1 = ['o', 'x', 'P', 's', 'v', 'D']  # Defines list. Selects markers.
marker_mpltlib = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x',
                   'X', 'D', 'd', '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ' ']
marker_size = 4
line_width = 2
alpha = 0.5

# Legend format
location = ['upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right', 'center', 'best']
marker_scale = 2
frame_alpha = 0.7
label_spacing = 0.7

# Axes format
fontsize_ticks = 8
fontsize_axis = 10
label_pad = 10

# SET UP DIRECTORIES ---------------------------------------------------------------------------------------------------

# Name levels ----------------------------------------------------------------------------------------------------------

# Level 1
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Level 2
xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where
# cross-sectional analysis data will be located.

xsctn_fl = '/Users/jimmywood/github/Whitewater_MN_sedimentation/PyCharm_Venv/Input/Cross_sectional_analysis/Trout_Creek_survey_data.csv'  # Defines string. Sets file path.

dgtz_fldr = '/Digitization'  # Defines variable as string. Sets name of new directory where digitization data will be
# located.

# Level 3+
clcs_fldr = '/Calculations'  # Defines variable as string. Sets name of new directory where calculations will be
# exported.
figs_fldr = '/Figures'  # Defines variable as string. Sets name of new directory where figures will be exported.

# Create folders -------------------------------------------------------------------------------------------------------

lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.
lvl2_fldrs = [xsctn_fldr, dgtz_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation
# via loop.

def create_folder(level, path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')  # Displays objects.

for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    for b in lvl2_fldrs:  # Begins loop. Loops through each element in list.
        lvl_paths = [a, a + b]  # Defines list. Inserts folder paths into list for each element combination in previous
        # lists.
        for c in lvl_paths:  # Begins loop. Loops through each element in list.
            level = lvl_paths.index(c) + 1  # Defines variable. Sets value based in list element index for display.

            create_folder(level, c)  # Creates folders. Calls function.

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

chck = 1  # Defines variable. For function display.

df_chnnl = upload_csv(xsctn_fl, 'TROUT CREEK ')  # Defines DataFrame. Calls function.

# SET DATA SELECTION LIMITS --------------------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------

def forward_range(start, end, step, data_label):  # Defines function. For generating forward range array between two numbers.
    end = end + 1  # Defines variable. Sets end of range to include final input value.
    end_label = end - 1  # Defines variable. Sets label for display.
    frwd_rng = np.arange(start, end, step)  # Defines format of function.
    if chck == 1:  # Conditional statement.
        print(data_label, start, '&', end_label, ':', frwd_rng)  # Displays objects.
    return frwd_rng  # Ends execution of function.

chck = 1  # Defines variable. For function display.
rgn_nums = forward_range(rng_strt, rng_end, 1, 'Range number limits')  # Defines array. Calls function.

# Temporal -------------------------------------------------------------------------------------------------------------

def reverse_range(start, end, step, data_label):  # Defines function. For generating forward range array between two numbers.
    end = end - 1  # Defines variable. Sets end of range to include final input value.
    end_label = end + 1  # Defines variable. Sets label for display.
    rev_rng = np.arange(start, end, step)  # Defines format of function.
    if chck == 1:  # Conditional statement.
        print(data_label, start, '&', end_label, ':', rev_rng, '\n')  # Displays objects.
    return rev_rng  # Ends execution of function.

chck = 1  # Defines variable. For function display.
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

    chck = 1  # Defines variable. For function display.

    df_rng = slice_DataFrame_rows1(df_chnnl, 'Range_num', a, 'RANGE NUMBER')

    if Area == 1:  # Conditional statement. Performs cross-sectional area analyses.

    # By range survey --------------------------------------------------------------------------------------------------

        for b in srvy_nums:  # Begins loop. Loos through range numbers.

            def slice_DataFrame_rows2(dataframe, column1, row_value1,
                                     label1, row_value2, label2):  # Defines function. For DataFrame slicing by row value.
                df_slc_r = dataframe[dataframe[column1] == row_value1]  # Defines format of function.
                if chck == 1:  # Conditional statement.
                    print('\033[1m' + label2 + ' ' + str(row_value2) + ' ' + label1 + ' ' + str(row_value1) + ' DATA' + '\033[0m',
                          '\n..\n', df_slc_r, '\n')  # Displays objects.
                return df_slc_r  # Ends execution of function.

            chck = 1  # Defines variable. For function display.

            df_srvy1 = slice_DataFrame_rows2(df_rng, 'Srvy_num', b, 'SURVEY NUMBER', a, 'RANGE NUMBER')

            # By survey measurement ------------------------------------------------------------------------------------

            def slice_DataFrame_columns1(dataframe, column, data_label):  # Defines function. For DataFrame slicing by row value.
                df_slc_c = dataframe[column]  # Defines format of function.
                if chck == 1:  # Conditional statement.
                    print('\033[1m' + data_label + ' DATA' + '\033[0m', '\n..\n', df_slc_c, '\n')  # Displays objects.
                return df_slc_c  # Ends execution of function.

            df_offst1 = slice_DataFrame_columns1(df_srvy1, 'Offset_ft', 'OFFSET')
            df_elvtn1 = slice_DataFrame_columns1(df_srvy1, 'Elv_lcl_ft', 'ELEVATION')


            def slice_DataFrame_cell(dataframe, column, data_label):  # Defines function. For DataFrame slicing by row value.
                index = dataframe.index
                df_slc_cl = dataframe.loc[index[0], column]
                if chck == 1:  # Conditional statement.
                    print(data_label + ':', df_slc_cl, '\n')  # Displays objects.
                return df_slc_cl  # Ends execution of function.

            srvy_yr1 = slice_DataFrame_cell(df_srvy1, 'Srvy_year', 'Survey year')  # Defines variable.
            rng_nm1 = slice_DataFrame_cell(df_srvy1, 'Srvy_range', 'Range')  # Defines variable.

            # PLOT CROSS-SECTIONS --------------------------------------------------------------------------------------

            def plot_lines1(number, figure_size, x, y, label1, color, marker1, marker_size, line_width, alpha,
                            fontsize_ticks, x_label, fontsize_axis, label_pad, y_label, title1, pause_length):

                plt.figure(number, figsize=figure_size)
                ax = plt.gca()
                ax.plot(x, y, label=label1, c=color, marker=marker1, markersize=marker_size, linewidth=line_width, alpha=alpha)  # Creates line
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
                plt.close()

            pause = 1

            title1 = 'Range ' + str(rng_nm1) + ' survey ' + str(srvy_yr1)
            plot_lines1(1, figure_size, df_offst1, df_elvtn1, srvy_yr1, tol_muted[b], marker1[b], marker_size, line_width,
                        alpha, fontsize_ticks, 'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)', title1, 1)
            # breakpoint()

            # select second dataset
            c = b - 1  # Defines variable. For selection of two survey datasets at once.
            chck = 1  # Defines variable. For function display.
            df_srvy2 = slice_DataFrame_rows2(df_rng, 'Srvy_num', c, 'SURVEY NUMBER', a, 'RANGE NUMBER')
            df_offst2 = slice_DataFrame_columns1(df_srvy2, 'Offset_ft', 'OFFSET')
            df_elvtn2 = slice_DataFrame_columns1(df_srvy2, 'Elv_lcl_ft', 'ELEVATION')

            srvy_yr2 = slice_DataFrame_cell(df_srvy2, 'Srvy_year', 'Survey year')  # Defines variable.
            rng_nm2 = slice_DataFrame_cell(df_srvy2, 'Srvy_range', 'Range')  # Defines variable.

            # communicate data
            print('==================================================')
            print('\033[1m' + 'Field range (number): ' + '\033[0m' + str(rng_nm1) + ' (' + str(rng_strt) + ')')
            print('\033[1m' + 'Range survey interval (numbers): ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' + str(srvy_strt) + '–' + str(srvy_end) + ')')
            chck = 0
            srvy_dt1 = slice_DataFrame_cell(df_srvy1, 'Srvy_date', 'Survey date')  # Defines variable.
            srvy_dt2 = slice_DataFrame_cell(df_srvy2, 'Srvy_date', 'Survey date')  # Defines variable.
            print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))
            print('--------------------------------------------------')

            pause = 1
            title1 = 'Range ' + str(rng_nm2) + ' survey ' + str(srvy_yr2)
            plot_lines1(2, figure_size, df_offst2, df_elvtn2, srvy_yr2, tol_muted[c], marker1[c], marker_size,
                        line_width,
                        alpha, fontsize_ticks, 'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)',
                        title1, 1)

            def plot_lines2(number, figure_size, x1, y1, label1, x2, y2, label2, color1, marker1, color2, marker2,
                            marker_size, line_width, alpha,
                            fontsize_ticks, x_label, fontsize_axis, label_pad, y_label, title1, location, marker_scale, frame_alpha, label_spacing, pause_length):

                plt.figure(number, figsize=figure_size)
                ax = plt.gca()
                ax.plot(x1, y1, label=label1, c=color1, marker=marker1, markersize=marker_size, linewidth=line_width, alpha=alpha)  # Creates line
                # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
                ax.plot(x2, y2, label=label2, c=color2, marker=marker2, markersize=marker_size, linewidth=line_width,
                        alpha=alpha)  # Creates line
                # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
                ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)  # Creates legend through automatic label detection.
                plt.xticks(fontsize=fontsize_ticks)
                plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets font size.
                plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates y-axis label. Sets font size.
                plt.yticks(fontsize=fontsize_ticks)
                plt.title(title1)  # Creates plot title.
                if pause == 1:
                    plt.pause(pause_length)  # Displays and updates active figure before pausing for interval seconds.
                elif pause == 0:
                    plt.show()
                plt.close()

            pause = 1
            title1 = 'Range ' + str(rng_nm1) + ' surveys'
            plot_lines2(3, figure_size, df_offst1, df_elvtn1, srvy_yr1, df_offst2, df_elvtn2, srvy_yr2, tol_muted[b], marker1[b], tol_muted[c], marker1[c], marker_size, line_width,
                        alpha,
                        fontsize_ticks, 'Survey offset (ft)', fontsize_axis, label_pad, 'Surface elevation (ft)', title1,
                        location[0], marker_scale, frame_alpha, label_spacing, 1)

