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
import pandas as pd, numpy as np  # Imports "Python data analysis library" with alias. Enables DataFrame array functionality.

# ======================================================================================================================
# PART 1: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------
# ======================================================================================================================
# initialization general
def create_folder(level, path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')

def upload_csv(path,stream_channel):
    csv_data = pd.read_csv(path)
    df = pd.DataFrame(csv_data)
    pd.set_option('display.max_columns', None)
    print('\033[1m' + 'UPLOADED .CSV DATA FOR ' + stream_channel + '\033[0m', '\n...\n', df, '\n')  # Displays objects. Makes
    # font bold and adds new lines.
    return df

def forward_range(array_label, start, end, step):
    end = end + 1
    array_label = np.arange(start, end, step)
    print(array_label)

def reverse_range(array_label, start, end, step):
    end = end - 1
    array_label = np.arange(start, end, step)
    print(array_label)

def slice_DataFrame_2x(slice_label, frame_label, column1, slice1, column2, slice2):
    slice_label=frame_label[(frame_label[column1] ==slice1) & (frame_label[column2] ==slice2)]
    print('\033[1m'+ column1 + str(slice1) +column2+str(slice2)+ 'data'+'\033[0m','\n..\n',slice_label,'\n')
