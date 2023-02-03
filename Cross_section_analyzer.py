# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# SECONDARY PROGRAM 1 OF 2 * -------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

# print('\n\033[1m' + 'START CROSS-SECTIONAL ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays string. Makes font bold and
# adds new line(s).

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.
import pandas as pd, numpy as np, matplotlib.pyplot as plt  # Imports "Python data analysis library", a module for working
# with arrays, and "Visualization with Python", with aliases. Enables DataFrame array functionality, using arrays and plotting tools.

# ======================================================================================================================
# PART 1: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------
# ======================================================================================================================
# initialization general
def create_folder(level, path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')

def upload_csv(path, label):
    csv_data = pd.read_csv(path)
    df = pd.DataFrame(csv_data)
    pd.set_option('display.max_columns', None)
    print('\033[1m' + 'UPLOADED .CSV DATA FOR ' + label + '\033[0m', '\n...\n', df, '\n')  # Displays objects.
    # Makes font bold and adds new lines.
    return df


def forward_range(start, end, step):
    end = end + 1
    frwd_rng = np.arange(start, end, step)
    print(frwd_rng)
    return frwd_rng

def reverse_range(start, end, step):
    end = end - 1
    rev_rng = np.arange(start, end, step)
    print(rev_rng)
    return rev_rng

def slice_DataFrame_rows2(dataframe, column1, slice1, label1, column2, slice2, label2):
    df_slc_r2=dataframe[(dataframe[column1] ==slice1) & (dataframe[column2] ==slice2)]
    print('\033[1m'+ label1 + ' ' + str(slice1) +' '+ label2 +' '+str(slice2)+ ' DATA'+'\033[0m','\n..\n', df_slc_r2,'\n')
    return df_slc_r2

def slice_DataFrame_column1(dataframe, column1, label1):
    df_slc_c1=dataframe[column1]
    print('\033[1m'+ label1 + ' DATA'+ '\033[0m','\n..\n', df_slc_c1,'\n')
    return df_slc_c1

def plot_line(number, figure_size, x, y, label, color, marker, alpha, xlabel, fontsize_axis, ylabel, title,pause):
    plt.figure(number, figsize=figure_size)
    ax=plt.gca()
    ax.plot(x, y, label=label, c=color, marker=marker, alpha=alpha)  # Creates line
    # plot of arrays from axes instance. Sets label, color, marker type, and transparency.
    # ax.legend()  # Creates legend through automatic label detection.
    # plt.xlabel(xlabel, fontsize=fontsize_axis)  # Creates x-axis label. Sets font size.
    # plt.ylabel(ylabel, fontsize=fontsize_axis)  # Creates y-axis label. Sets font size.
    # plt.title(title)  # Creates plot title.
    if pause == 1:
        plt.pause(2)  # Displays and updates active figure before pausing for interval seconds.
    elif pause == 0:
        plt.show()