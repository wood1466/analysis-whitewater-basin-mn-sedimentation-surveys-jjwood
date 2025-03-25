# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS
# USER DEFINED FUNCTIONS * ----------------------------------------------------

# INITIALIZATION ==============================================================

# IMPORT MODULES --------------------------------------------------------------

import geopandas as gpd  # Imports GeoPandas with alias to enable geospatial
# functionality.
import matplotlib.pyplot as plt  # Matplotlib--visualization with Python--with
# alias to enable figure creation.
import numpy as np  # NumPy--the fundamental package for scientific computing
# with Python--with alias to enable use of advanced mathematics.
import os  # os--miscellaneous operating system interfaces--to enable operating
# system functionality.
import pandas as pd  # pandas--Python data analysis library--with alias to
# enable DataFrames functionality.
import pingouin as pg  # Pingouin--statistical package--to enable use of
# advanced statistics.
import scikit_posthocs as sc_p  # scikit-posthocs--post hoc tests for pairwise
# multiple comparisons--with alias to enable use of advanced statistics.
import scipy as sc  # SciPy--fundamental algorithms for scientific computing in
# Python--with alias to enable use of advanced statistics.
import statsmodels.api as sm  # statsmodels--statistical models, hypothesis
# tests, and data exploration--with alias to enable use of advanced statistics

# DEFINE FUNCTIONS ============================================================

# UDFS are ordered alphabetically 


def create_folder(path):  # Defines function to generate directory paths.
    if not os.path.exists(path):  # Begins conditional statement to check if
        # folder exists.
        os.mkdir(path)  # Creates folder.
        
        print('\033[1mCREATED FOLDER:\033[0m ' + path + '\n')
        # Displays objects.


def create_forward_range(start, end, step, display):  # Generate forward array
    # between two numbers.
    end += 1  # Redefines object so input value is included in range.
    
    range = np.arange(start, end, step)  # Defines array for of numbers to
    # create framework for looping analysis.
    
    if display == 1:  # Begins conditional statement for display.
        print('\033[1mCREATED ARRAY:\033[0m \n  Limits: ' + str(start) + ' & '
              + str(end - 1) + ' --> Array:', range)
        
    return range  # Ends function execution.


def convert_CSV_to_dataframe(path, display):  # Upload .csv file and convert to
    # a DataFrame for Python manipulation.
    CSV_data = pd.read_csv(path)  # Defines object by uploading .csv file.
    
    df_CSV_data = pd.DataFrame(CSV_data)  # Defines DataFrame from .csv.
    
    pd.set_option('display.max_columns', None)  # Updates DataFrame display
    # format to display all columns.
    
    if display == 1:
        print('\033[1mUPLOADED .CSV DATA:\033[0m ' + path + '\n...\n',
              df_CSV_data, '\n')
        
    return df_CSV_data


def calculate_transect_azimuth(x1, y1, x2, y2, display):  # Calculate transect
    # azimuth from reference coordinates.
    # Calculate the difference in x and y coordinates between reference points.
    
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Assign transect a cartesian reference quadrant based on change in x and y
    # coordinates to enable transect azimuth calculation.
    
    if delta_x > 0:  
        if delta_y >= 0:
            ref_quadrant = 1
        else:
            ref_quadrant = 4
    elif delta_x < 0:
        if delta_y > 0:
            ref_quadrant = 2
        else:
            ref_quadrant = 3
    else:
        if delta_y > 0:
            ref_quadrant = 2
        else:
            ref_quadrant = 4

    # Select reference angle and calculate transect azimuth.
    
    if ref_quadrant == 1:
        ref_angle = (1/2) * np.pi  # Defines object by setting reference angle
        # used to correct calculated orientation to azimuth.
        azimuth = ref_angle - abs(np.arctan(delta_x / delta_y))
        # Defines object by calculating transect azimuth.
    elif ref_quadrant == 2:
        ref_angle = (1/2) * np.pi
        azimuth = ref_angle + abs(np.arctan(delta_x / delta_y))
    elif ref_quadrant == 3:
        ref_angle = (3/2) * np.pi
        azimuth = ref_angle - abs(np.arctan(delta_x / delta_y))
    else:
        ref_angle = (3/2) * np.pi
        azimuth = ref_angle + abs(np.arctan(delta_x / delta_y))

    if display == 1:
        print('\033[1mCALCULATED TRANSECT AZIMUTH:\033[0m ' + str(azimuth)
              + '\n')
        
    return azimuth


def calculation_exclusion_checker(
            dataframe, column1, column2, column3, column4, position, value, 
            display):  # Search transect data for calculation exclusion
            # zones/exceptions.  
    df_exclusion = slice_dataframe_rows('Equals', dataframe, column1, value, 0)
    # Calls UDF to slice DataFrame for excluded transect data and define
    # resultant DataFrame.
              
    if df_exclusion.shape[0] != 0:  # Begins conditional statement to select
        # exclusion limits.
        excl_start = slice_dataframe_cell(
                'Float', df_exclusion, position, column2, 0)  # Calls UDF to 
        # slice DataFrame for exclusion lower limit and define resultant
        # object.
        excl_end = slice_dataframe_cell(
                'Float', df_exclusion, position, column3, 0)  # Exclusion upper
        # limit.
        excl_year_pair = slice_dataframe_cell(
                'String', df_exclusion, position, column4, 0)  # Year pair for
        # which exclusion applies.
    else:
        # Defines object as NaN when no exclusion found.
        
        excl_start = np.nan
        excl_end = np.nan
        excl_year_pair = np.nan
    
    if display == 1:
        print('\033[1mRETRIEVED TRANSECT DATA DISCONTINUITY:\033[0m '
              + str(excl_start) + '-' + str(excl_end) + ' for '
              + str(excl_year_pair) + '\n')
        
    return excl_start, excl_end, excl_year_pair

  
def move_reference_coordinates(
            x, y, dataframe1, dataframe2, position, column1, column2, column3,
            conversion_factor, display):  # Move transect reference coordinates
            # if reference point established off of transect.
    off_distance_ft = slice_dataframe_cell(
            'Float', dataframe1, position, column1, 0)  # Reference point's
    # distance off of transect.
            
    off_distance_m = off_distance_ft / conversion_factor  # Converts feet to
    # meters.

    off_direction = slice_dataframe_cell(
            'String', dataframe1, position, column2, 0)  # Reference point's
    # offset direction from transect.
            
    GNSS_accuracy = slice_dataframe_cell(
            'String', dataframe2, position, column3, 0)  # Reference point's
    # coordinate accuracy.
                       
    # Check if coordinate accuracy is a range and select value.

    GNSS_accuracy_split = GNSS_accuracy.split('-')  # Defines list of
    # coordinate accuracy split by delimiter to check if value is a range.
            
    if len(GNSS_accuracy_split) == 3:
        GNSS_accuracy = GNSS_accuracy_split[-1]  # Defines object as largest
        # value from coordinate accuracy range.
    else:
        GNSS_accuracy = GNSS_accuracy_split[0]  # Defines object as single
        # value.
    GNSS_accuracy = float(GNSS_accuracy)  # Defines object for coordinate
    # accuracy.

    # Check if coordinate distance off of transect exceeds coordinate accuracy
    # and moves coordinate accordingly.
            
    if off_distance_m > GNSS_accuracy:
        if off_direction == 'North':
            y -= off_distance_m  # Redefines object.
        elif off_direction == 'South':
            y += off_distance_m
        elif off_direction == 'East':
            x -= off_distance_m
        elif off_direction == 'West':
            x += off_distance_m
        else:
            pass  # Pass command.

    if display == 1:
        print('\033[1mMARKER SHIFT:\033[0m\n Direction: '
              + str(off_direction) + '\n Magnitude: '
              + str('%.2f' % off_distance_m) + '\n Output coordinate: '
              + str('%.2f' % x) + ', ' + str('%.2f' % y) + '\n')
        
    return x, y


def slice_dataframe_cell(
        data_type, dataframe, position, column, display):  # Slice DataFrame
    # for individual cell value.
    indx = dataframe.index  # Retrieves DataFrame index.
    
    if column is not None:  # Begins conditional statement to select function
    # format based off of input DataFrame.
        cell = dataframe.loc[indx[position], column]  # Defines object from
        # DataFrame slice.
    else:
        cell = dataframe.loc[indx[position]]
                        
    # Enforce desired output data type.

    typ = type(cell)  # Retrieves object data type.
        
    if typ == data_type:
        pass  # Pass command.
    else:
        if data_type == 'Integer':
            cell = int(cell)  # Redefines object to integer.
        elif data_type == 'Float':
            cell = float(cell)  # Redefines object to float.
        else:
            cell = str(cell)  # Redefines object to string.
            
    if display == 1:
        print('\033[1mRETRIEVED VALUE:\033[0m ' + str(cell) + '\n')
        
    return cell

# DEFINE FUNCTIONS ===========================================================5
def slice_dataframe_column(
        output, data_type, dataframe, column, check_duplicates, drop_nan, 
        display):  # Slice DataFrame for individual column.
    
    df_column = dataframe[column]  # Defines DataFrame from DataFrame slice.

    if check_duplicates == 1:  # Begins conditional statement to check if
        # duplicate values are desired in DataFrame.
        df_column = df_column.drop_duplicates(keep='first')
        # Redefines DataFrame.
    else:
        pass  # Pass command.

    if drop_nan == 1:  # Begins conditional statement to check if NaN values
        # are desired in DataFrame.
        df_column = df_column.dropna()  # Redefines DataFrame.
    else:
        pass
                
    # Enforce desired output data type.
            
    typ = df_column.dtypes  # Retrieves object data type.
            
    if typ == data_type:
        pass
    else:
        if data_type == 'Integer':
            df_column = df_column.astype(int)  # Redefines DataFrame values to
            # integer.
        elif data_type == 'Float':
            df_column = df_column.astype(float)  # Redefines DataFrame values
            # to float.
        else:
            df_column = df_column.astype(str)  # Redefines DataFrame value to
            # string.
  
    # Enforce desired output type.        
            
    if output == 'DataFrame':
        if display == 1:
            print('\033[1mCREATED DATAFRAME:\033[0m \n...\n', df_column, '\n')
        
        return df_column
        
    elif output == 'List':
        list_column = df_column.tolist()  # Redefines DataFrame as list.
        
        if display == 1:
            print('\033[1mCREATED LIST:\033[0m', list_column, '\n')
            
        return list_column
        
    else:
        array_column = df_column.to_numpy()  # Redefines DataFrame as array.
        
        if display == 1:
            print('\033[1mCREATED ARRAY:\033[0m', array_column, '\n')
            
        return array_column


def slice_dataframe_rows(search_type, dataframe, column, value, display):
    # Slice DataFrame for rows.
    # Slice DataFrame based off of search parameter.
    
    if search_type == 'Equals':
        df_rows = dataframe[dataframe[column] == value]  # Defines DataFrame
        # from DataFrame slice.
    elif search_type == 'Less than':
        df_rows = dataframe[dataframe[column] < value]
    elif search_type == 'Greater than':
        df_rows = dataframe[dataframe[column] > value]
    elif search_type == 'Less than/Equal':
        df_rows = dataframe[dataframe[column] <= value]
    elif search_type == 'Greater than/Equal':
        df_rows = dataframe[dataframe[column] >= value]
    else:
        df_rows = dataframe[dataframe[column] != value]
        
    df_rows = df_rows.loc[:, ~df_rows.columns.str.match('Unnamed')]
    # Redefines DataFrame by deleting empty columns.
    
    if display == 1:
        print('\033[1mCREATED DATAFRAME: \033[0m \n...\n', df_rows, '\n')
    
    return df_rows
