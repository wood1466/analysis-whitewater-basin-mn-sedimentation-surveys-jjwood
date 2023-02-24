# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# SECONDARY PROGRAM 1 OF 2 * -------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

# print('\n\033[1m' + 'START CROSS-SECTIONAL ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os, sys  # Imports "Time and access conversions", "Miscellaneous operating system interfaces", and
# "System specific parameters and functions". Enables use of various time–related functions and operating system
# dependent functionality.
import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sc # Imports "Python data analysis library", a comprehensive
# mathematics library, and a plotting interface, with alias. Enables DataFrame array functionality.

# ======================================================================================================================
# PART 1: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------
# ======================================================================================================================
location = ['upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right', 'center', 'best']  # Defines list. Complete list of matplotlib legend placements.
ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes for ultramarine, indigo, magenta, orange, and gold.
ibm_clr_hx = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes for ultramarine, indigo, magenta, orange, and gold.
ibm_clr_rgb = [(100, 143, 255), (120, 94, 240), (220, 38, 127), (254, 97, 0), (255, 176, 0)]
# Sets muted Tol colorblind friendly palette in color hex color codes for indigo, cyan, teal, green, olive, sand, rose, wine, purple, and pale grey.
# 2008 = 0, 1994 = 3, 1978 = 2, 1975 = 4, 1964 = 5, 1939 = 6, 1850S = 7.
tol_vibrant = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', '#BBBBBB']  # Defines list. Sets
# vibrant Tol colorblind friendly palette in color hex color codes for blue, cyan, teal, orange, red, magenta, grey.
marker_mpltlib = ['.', ',', 'o', 'v', '^', '<', '>',
                          '1', '2', '3', '4', '8',
                          's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd',
                          '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ' ']  # Defines list. Complete list of matplotlib plot markers.
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDD']  # Defines list. Sets Paul Tol muted colorblind friendly palette via hex color codes.

# TEMPORARY FUNCTION HOUSING ===========================================================================================
#MOST RECENT YADA YDA RODDA RODA

def plot_lines(lines, plot_number, figure_size, x, y, label, color, marker, marker_size, line_width,
               alpha, show_legend, location, marker_scale, frame_alpha, label_spacing, fontsize_ticks, x_label,
               fontsize_axis, label_pad, y_label, title, pause,
               pause_length):  # Defines function. For cross-section plotting.
    plt.figure(plot_number, figsize=figure_size)  # Creates plot window.
    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
    if lines == 1:  # Conditional statement. Plots single line.
        ax.plot(x, y, label=label, c=color, marker=marker, markersize=marker_size, linewidth=line_width,
                alpha=alpha)  # Creates line plot of arrays from axes instance. Sets format.
        if show_legend == 1: # Conditional statement. Shows legend if desired for single line plotting.
            ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha,
                      labelspacing=label_spacing)  # Creates legend. Through automatic label detection.
    if lines != 1:  # Conditional statement. Plots multiple lines.
        lines = lines + 1  # Defines variable. For correct looping framework.
        line_list = range(1, lines, 1)  # Defines list. Creates range of integers for looped plotting.
        for i in line_list:  # Begins loop through list. For sequential plotting.
            index = line_list.index(i)  # Defines variable. Retrieves index of element in list. For format selection.
            ax.plot(x[index], y[index], label=label[index], c=color[index], marker=marker[index], markersize=marker_size,
                    linewidth=line_width,
                    alpha=alpha)  # Creates line plot of arrays from axes instance. Sets format.
        ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha,
                  labelspacing=label_spacing)  # Creates legend. Through automatic label detection.
    plt.xticks(fontsize=fontsize_ticks)  # Sets x-axis tick mark format.
    plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets format.
    plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates x-axis label. Sets format.
    plt.yticks(fontsize=fontsize_ticks)  # Sets y-axis tick mark format.
    plt.title(title)  # Creates plot title.
    if pause == 1:  # Conditional statement. For display format.
        plt.pause(pause_length)  # Displays plot. For set interval of seconds and closes without clearing.
    elif pause == 0:  # Conditional statement. For displa format.
        plt.show()  # Displays plot. Indefinite and cleared upon close.

def create_folder(level, path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')  # Displays objects.

def upload_csv(path, label, dsply):  # Defines function. For uploading .csv and conversion to DataFrame.
    csv_data = pd.read_csv(path)  # Uploads .csv file. Input data.
    df = pd.DataFrame(csv_data)  # Converts .csv file to DataFrame. For Python manipulation.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame format. Displays all DataFrame columns.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + 'UPLOADED .CSV DATA FOR ' + label + '\033[0m', '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends execution of function.

def forward_range(start, end, step, data_label, dsply):  # Defines function. For generating forward range array between two numbers.
    end = end + 1  # Defines variable. Sets end of range to include final input value.
    end_label = end - 1  # Defines variable. Sets label for display.
    frwd_rng = np.arange(start, end, step)  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label, start, '&', end_label, ':', frwd_rng)  # Displays objects.
    return frwd_rng  # Ends execution of function.

def reverse_range(start, end, step, data_label, dsply):  # Defines function. For generating forward range array between two numbers.
    end = end - 1  # Defines variable. Sets end of range to include final input value.
    end_label = end + 1  # Defines variable. Sets label for display.
    rev_rng = np.arange(start, end, step)  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label, start, '&', end_label, ':', rev_rng, '\n')  # Displays objects.
    return rev_rng  # Ends execution of function.

def slice_DataFrame_rows1(dataframe, column, row_value, label, dsply):  # Defines function. For DataFrame slicing by single row value.
    df_slc_r = dataframe[dataframe[column] == row_value]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + label + ' ' + str(row_value) + ' DATA' + '\033[0m', '\n..\n', df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends execution of function.

def slice_DataFrame_rows2(dataframe, column1, row_value1, label1, row_value2, label2,
                          dsply):  # Defines function. For DataFrame slicing by row value.
    df_slc_r = dataframe[dataframe[column1] == row_value1]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + label2 + ' ' + str(row_value2) + ' ' + label1 + ' ' + str(row_value1) + ' DATA' + '\033[0m',
              '\n..\n', df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends execution of function.


def slice_DataFrame_cell(dataframe, value, column, data_label, dsply):  # Defines function. For DataFrame slicing by row value.
    index = dataframe.index
    df_slc_cl = dataframe.loc[index[value], column]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label + ':', df_slc_cl, '\n')  # Displays objects.
    return df_slc_cl  # Ends execution of function.

def slice_DataFrame_columns1(dataframe, column, data_label,
                             dsply):  # Defines function. For DataFrame slicing by row value.
    df_slc_c = dataframe[column]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + data_label + ' DATA' + '\033[0m', '\n..\n', df_slc_c, '\n')  # Displays objects.
    return df_slc_c  # Ends execution of function.

def max_value_column(dataframe, data_label, units,
                     dsply):  # Defines function. For retrieving maximum value from DataFrame column.
    max = dataframe.max()  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('Maximum column value:', max, data_label, units)  # Displays objects.
    return max  # Ends execution of function.

def min_value_column(dataframe, data_label, units,
                     dsply):  # Defines function. For retrieving minimum value from DataFrame column.
    min = dataframe.min()  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('Minimum column value:', min, data_label, units)  # Displays objects.
    return min  # Ends execution of function.


def hydraulic_geometry(dataframe, column1, data_label1, data_label2, units, data_label3, data_label4,
                       column2, data_label5, data_label6, data_label7, data_label8, dsply):  # Defines
    # function. For hydraulic geometry calculation.

    # Calculate channel width
    df_strm_offst = slice_DataFrame_columns1(dataframe, column1, data_label1, 0)  # Defines DataFrame.
    # Slices DataFrame to contain stream channel survey offsets only.
    offst1 = min_value_column(df_strm_offst, data_label2, units, 0)  # Defines variable. Slices DataFrame
    # to yield smallest offset for stream channel.
    offst2 = max_value_column(df_strm_offst, data_label2, units, 0)  # Defines variable. Slices DataFrame
    # to yield largest offset for stream channel.
    if offst1 < offst2:  # Conditional statement. Sets order of operations for channel width calculation.
        wdth = offst2 - offst1  # Defines variable. Sets calculation framework.
    elif offst1 > offst2:  # Conditional statement. Sets error contingency.
        sys.exit('No stream channel detected')  # Exits code and displays string.
    elif offst1 == offst2:  # Conditional statement. Sets error contingency.
        sys.exit('No stream channel detected')  # Exits code and displays string.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label3 + units + '\n  ' + data_label4 + '%.1f' % wdth)  # Displays objects.

    # Calculate channel depth
    df_strm_elvtn = slice_DataFrame_columns1(dataframe, column2, data_label5, 0)  # Defines DataFrame.
    # Slices DataFrame to contain stream channel survey offsets only.
    elvtn1 = min_value_column(df_strm_elvtn, data_label6, units, 0)  # Defines variable. Slices DataFrame
    # to yield smallest elevation for stream channel.
    elvtn2 = max_value_column(df_strm_elvtn, data_label6, units, 0)  # Defines variable. Slices DataFrame
    # to yield largest elevation for stream channel.
    if elvtn1 < elvtn2:  # Conditional statement. Sets order of operations for channel depth calculation.
        dpth = elvtn2 - elvtn1  # Defines variable. Sets calculation framework.
    elif elvtn1 > elvtn2:  # Conditional statement. Sets error contingency.
        sys.exit('No stream channel detected')  # Exits code and displays string.
    elif elvtn1 == elvtn2:  # Conditional statement. Sets error contingency.
        sys.exit('No stream channel detected')  # Exits code and displays string.
    elif elvtn1 | elvtn2 <= 0:  # Conditional statement. Sets error contingency.
        sys.exit('No stream channel detected')  # Exits code and displays string.
    if dsply == 1:  # Conditional statement. For display.
        print('  ' + data_label7 + '%.2f' % dpth)  # Displays objects.

    # Calculate hydraulic radius
    hydro_rad = (wdth * dpth) / (wdth + 2 * dpth)  # Defines variable. Sets calculation framework.
    if dsply == 1:  # Conditional statement. For display.
        print('  ' + data_label8 + '%.2f' % hydro_rad)  # Displays objects.

    return wdth, dpth, hydro_rad  # Ends execution of function.


def create_appended_list(value, data_label1, new_list, data_label2,
                         dsply):  # Defines function. For post calculation list collection.

    try:  # Checks program for object. Takes action based off existence.
        value  # Defines object to be searched for.
    except NameError:  # Executed if object does not exist.
        sys.exit(data_label1 + 'value undefined')
    else:  # Executed if object does exist.
        new_list.append(value)  # Appends list.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label2, new_list)  # Displays objects.
    return new_list  # Ends execution of function.


def get_plot_format_by_year(label, list, alternate):  # Defines function. For plot color selection.
    if label == '2008':  # Conditional statement.
        quality = list[0]  # Defines variable. Sets plot color.
        if alternate == 1:  # Conditional statement.
            quality = list[-3]  # Defines variable. Sets plot color.
    elif label == '1994':  # Conditional statement.
        quality = list[3]  # Defines variable. Sets plot color.
    elif label == '1978':  # Conditional statement.
        quality = list[2]  # Defines variable. Sets plot color.
    elif label == '1975':  # Conditional statement.
        quality = list[4]  # Defines variable. Sets plot color.
    elif label == '1964':  # Conditional statement.
        quality = list[5]  # Defines variable. Sets plot color.
    elif label == '1939':  # Conditional statement.
        quality = list[6]  # Defines variable. Sets plot color.
    elif label == '1850s':  # Conditional statement.
        quality = list[7]  # Defines variable. Sets plot color.
    elif label == 'Shaded area':  # Conditional statement.
        quality = list[-1]  # Defines variable. Sets plot color.
    return quality  # Ends execution of function.

def create_DataFrame_frm_arry(array1, array2, data_label1,
                              dsply):  # Defines function. For creating DataFrame from arrays or lists.
    df_new = pd.DataFrame(data=array1, columns=array2)  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + data_label1 + ' DATA' + '\033[0m', '\n..\n', df_new, '\n')  # Displays objects.
    return df_new  # Ends execution of function.


#================================newer nother day
def export_file(type, number, name, end_path, figure_extension, dataframe, data_label1, truth_statement, display):
    if type == 'figure':
        plt.figure(number)  # Calls figure. Makes it the active plot.
        figure_name = name  # Defines variable as strong. Names figure for export.
        plt.savefig(end_path + figure_name,
                    format=figure_extension)  # Saves figure to directory. Sets file format.
        plt.close()  # Closes active figure.
    elif type == 'table':
        file_name = name
        dataframe.to_csv(end_path + file_name, index=truth_statement)
    if display == 1:
        print(data_label1, 'exported')  # Display objects.


def name_levels(directory_levels, folder_labels, output_folder, data_label1, dsply):
    index = np.arange(0, directory_levels, 1)

    for i in index:
        # Name levels ------------------------------------------------------------------------------------------

        folder_name = folder_labels[i]

        if i == 0:
            level_i = output_folder + folder_name
            levels = [level_i]
        elif i != 0:
            level_i = level_i + folder_name
            levels.append(level_i)
        if dsply == 1:
            print(data_label1, levels)
    return levels


def interpolate_cross_section(type, x, y, start, end, interpolation_type, step, decimal_place):
    f = sc.interpolate.interp1d(x, y, kind=interpolation_type)

    if type == 'dataframe':
        x_list = x.tolist()
        start = x_list[0]
        # print(start)
        end = x_list[-1]
        # print(end)
    elif type == 'list':
        x_list = x
        start = x_list[0]
        # print(start)
        end = x_list[-1]
        # print(end)
    elif type == 'limits':
        pass

    new_end = end + step

    x_interpolated = np.arange(start, new_end, step)
    x_interpolated = np.around(x_interpolated, decimals=decimal_place)
    # print(x_interpolated)

    y_interpolated = f(x_interpolated)
    x_range_interpolated = x_interpolated[-1] - x_interpolated[0]
    sample_numbers = len(x_interpolated)
    return x_interpolated, y_interpolated, x_range_interpolated, sample_numbers

def select_coincident_x_range(type, x1, x2, units, display):
    if type == 'dataframe':
        x1_list = x1.tolist()
        x2_list = x2.tolist()
    elif type == 'list':
        x1_list = x1
        x2_list = x2

    x_min1 = x1_list[0]
    x_max1 = x1_list[-1]
    x_min2 = x2_list[0]
    x_max2 = x2_list[-1]

    if x_min1 == x_min2:
        start = x_min1
        if x_max1 == x_max2 or x_max1 < x_max2:
            end = x_max1
        elif x_max1 > x_max2:
            end = x_max2
    elif x_min1 < x_min2:
        start = x_min2
        if x_max1 == x_max2 or x_max1 < x_max2:
            end = x_max1
        elif x_max1 > x_max2:
            end = x_max2
    elif x_min1 > x_min2:
        start = x_min1
        if x_max1 == x_max2 or x_max1 < x_max2:
            end = x_max1
        elif x_max1 > x_max2:
            end = x_max2
    coincident_range = end - start
    if display == 1:
        print('Coincident range ' + '\n  X min: ' + str(x_min1) + ' & ' + str(x_min2) +
              '\n  X max: ' + str(x_max1) + ' & ' + str(x_max2) + '\n  Range: ' + str(start) + '–' + str(end) + ' (' + str('%.2f' % coincident_range) + units + ')')
    return start, end, coincident_range


def get_coordinate_pairs(type, value1, value2, x_list, data_label1, y1_list, y2_list, data_label2, display):
    if type == 'depth':
        # x
        x1 = x_list[value1]
        if display == 1:
            print(data_label1, x1)

        # y
        y1_top = y1_list[value1]
        y1_btm = y2_list[value1]
        if display == 1:
            print(data_label2 + str(y1_top) + ' & ' + str(y1_btm))
        return x1, y1_top, y1_btm

    if type == 'area':
        x1 = x_list[value1]
        x2 = x_list[value2]
        if display == 1:
            print(data_label1 + str(x1) + '–' + str(x2))

        # y
        y1_top = y1_list[value1]
        y1_btm = y2_list[value1]
        y2_top = y1_list[value2]
        y2_btm = y2_list[value2]
        if display == 1:
            print(data_labe2 + str(y1_top) + ' & ' + str(y1_btm) + str(y2_top) + ' & ' + str(y2_btm))
        return x1, x2, y1_top, y1_btm, y2_top, y2_btm


def sediment_thickness(type, y1_top, y1_btm, y2_top, y2_btm, data_label1, display):
    if type == 'depth':
        depth1 = y1_top - y1_btm
        if depth1 > 0:
            process1 = 'Deposition'
        elif depth1 < 0:
            process1 = 'Erosion'
        elif depth1 == 0:
            process1 = 'No net change'
        return depth1, process1
    if type == 'area':
        depth2 = y2_top - y2_btm
        if depth2 > 0:
            process2 = 'Deposition'
        elif depth2 < 0:
            process2 = 'Erosion'
        elif depth2 == 0:
            process2 = 'No net change'
        return depth1, depth2, process2
    if display == 1:
        try:
            depth2
        except NameError:
            print(data_label1, depth1, process1)
        else:
            print(data_label1 + str(depth1) + ' & ' + str(depth2), process1, process2)






#================================newer nother day