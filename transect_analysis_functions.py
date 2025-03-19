# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS
# USER DEFINED FUNCTIONS * ----------------------------------------------------

# INITIALIZATION ==============================================================

# IMPORT MODULES --------------------------------------------------------------

import geopandas as gpd  # Imports GeoPandas with alias to enable geospatial
# functionality.
import matplotlib.pyplot as plt  # Imports Matplotlib--visualization with
# Python--with alias to enable figure creation.
import numpy as np  # Imports NumPy--the fundamental package for scientific
# computing with Python--with alias to enable use of advanced mathematics.
import os  # Imports os--miscellaneous operating system interfaces--to enable
# operating system functionality.
import pandas as pd  # Imports pandas--Python data analysis library--with alias
# to enable DataFrames functionality.
import pingouin as pg  # Imports Pingouin--statistical package--to enable use
# of advanced statistics.
import scikit_posthocs as sc_p  # Imports scikit-posthocs--post hoc tests for
# pairwise multiple comparisons--with alias to enable use of advanced
# statistics.
import scipy as sc  # Imports SciPy--fundamental algorithms for scientific
# computing in Python--with alias to enable use of advanced statistics.
import statsmodels.api as sm  # Imports statsmodels--statistical models,
# hypothesis tests, and data exploration--with alias to enable use of advanced
# statistics

# DEFINE FUNCTIONS ============================================================

# User-defined functions are ordered alphabetically 


def create_folder(path):  # Defines function to generate directory paths.
    if not os.path.exists(path):  # Checks if folder exists and skips directory
        # generation if it exists.
        os.mkdir(path)  # Creates folder.
        
        print('\033[1mCREATED FOLDER:\033[0m ' + path + '\n')
        # Displays objects.


def create_forward_range(start, end, step, display):  # Defines function to
    # generate forward array between two numbers.
    end += 1  # Defines object to include end of range.
    
    range = np.arange(start, end, step)  # Defines array.
    
    if display == 1:  # Begins conditional statement for display.
        print('\033[1mCREATED ARRAY:\033[0m \n  Limits: ' + str(start) + ' & '
              + str(end - 1) + ' --> Array:', range)  # Displays objects.
        
    return range  # Ends function execution.


def convert_CSV_to_dataframe(path, display):  # Defines function to upload
    # .csv file and convert to a DataFrame for Python manipulation.
    CSV_data = pd.read_csv(path)  # Uploads .csv file.
    
    df_CSV_data = pd.DataFrame(CSV_data)  # Defines object by converting .csv
    # to DataFrame.
    
    pd.set_option('display.max_columns', None)  # Redefines object by adjusting
    # DataFrame to display all columns.
    
    if display == 1:  # Begins conditional statement for display.
        print('\033[1mUPLOADED .CSV DATA:\033[0m ' + path + '\n...\n',
              df_CSV_data, '\n')  # Displays objects.
        
    return df_CSV_data  # Ends function execution.


def calculate_transect_azimuth(x1, y1, x2, y2, display):  # Defines function to
    # calculate transect azimuth from reference coordinates.
    # Calculate the difference in x and y coordinates between reference points.
    
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Assign cartesian reference quadrant based on change in x and y coordinates
    # to enable transect azimuth calculation.
    
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
        # for correction of calculated orientation to azimuth.
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

    if display == 1:  # Begins conditional statement for display.
        print('\033[1mCALCULATED TRANSECT AZIMUTH:\033[0m ' + str(azimuth)
              + '\n')  # Displays objects.
        
    return azimuth  # Ends function execution.

#----------------------------------------------------------------------------79
def calculation_exclusion_checker(dataframe, column1, column2, column3, column4, position, value, display):  # Defines
    # function. For searching transect data for exclusions prior to calculations.
    dfExcCheck = SliceDataFrameRows('Equals', dataframe, column1, value, 0)  # Defines DataFrame. Calls function. Slices
    # DataFrame to yield excluded transect data.
    if dfExcCheck.shape[0] != 0:  # Begins conditional statement. Checks equality. Selects exclusion points.
        TExcStart = SliceDataFrameCell('Float', dfExcCheck, position, column2, 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield exclusion point.
        TExcEnd = SliceDataFrameCell('Float', dfExcCheck, position, column3, 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield exclusion point.
        TExcPairYear = SliceDataFrameCell('String', dfExcCheck, position, column4, 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield applicable exclusion year.
    else:  # Continues conditional statement. Checks inequality. Selects exclusion points.
        TExcStart = np.nan  # Defines variable. Sets value to NaN when no exclusion found.
        TExcEnd = np.nan  # Defines variable. Sets value to NaN when no exclusion found.
        TExcPairYear = np.nan  # Defines variable. Sets value to NaN when no exclusion found.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mRETRIEVED TRANSECT DATA DISCONTINUITY:\033[0m ' + str(TExcStart) + '-' + str(TExcEnd) + ' for ' +
              str(TExcPairYear) + '\n')  # Displays objects.
    return TExcStart, TExcEnd, TExcPairYear  # Ends function execution.


def MoveReferenceCoordinates(x, y, dataframe1, dataframe2, position, column1, column2, column3, conversion_factor,
                             display):  # Defines function. For moving transect reference coordinates if established off
    # of line.
    PointOffsetDistanceFt = SliceDataFrameCell('Float', dataframe1, position, column1, 0)  # Defines variable. Calls
    # function.  Slices DataFrame to yield marker off transect distance.
    PointOffsetDistanceM = PointOffsetDistanceFt / conversion_factor  # Defines variable. Converts feet to meters.
    PointOffsetDirection = SliceDataFrameCell('String', dataframe1, position, column2, 0)  # Defines variable. Calls
    # function.  Slices DataFrame to yield marker off transect direction.
    CoordinateAccuracyM = SliceDataFrameCell('String', dataframe2, position, column3, 0)  # Defines variable. Calls
    # function.  Slices DataFrame to yield marker coordinate estimated accuracy.
    CoordinateAccuracyMList = CoordinateAccuracyM.split('-')  # Defines list. Splits string into component parts by
    # delimiter.
    if len(CoordinateAccuracyMList) == 3:  # Begins conditional statement. Checks equality. Checks if estimated
        # coordinate accuracy is range.
        CoordinateAccuracyM = CoordinateAccuracyMList[-1]  # Redefines variable. Selects final list component for value.
    else:  # Continues conditional statement. Checks inequality. Checks if estimated coordinate accuracy is a range.
        CoordinateAccuracyM = CoordinateAccuracyMList[0]  # Redefines variable. Selects first list component for value.
    CoordinateAccuracyM = float(CoordinateAccuracyM)  # Redefines variable. Converts data type to float.
    if PointOffsetDistanceM > CoordinateAccuracyM:  # Begins conditional statement. Checks relation. Moves coordinates
        # if distance from transect is greater than estimated coordinate accuracy.
        if PointOffsetDirection == 'North':  # Begins conditional statement. Checks equality. Moves coordinates by
            # component.
            y -= PointOffsetDistanceM  # Redefines variable.
        elif PointOffsetDirection == 'South':  # Continues conditional statement. Checks equality. Moves coordinates by
            # component.
            y += PointOffsetDistanceM  # Redefines variable.
        elif PointOffsetDirection == 'East':  # Continues conditional statement. Checks equality. Moves coordinates by
            # component.
            x -= PointOffsetDistanceM  # Redefines variable.
        elif PointOffsetDirection == 'West':  # Continues conditional statement. Checks equality. Moves coordinates by
            # component.
            x += PointOffsetDistanceM  # Redefines variable.
        else:  # Continues conditional statement. Checks equality. Moves coordinates by component.
            pass  # Pass command. Moves on to next line of code.f
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mMARKER SHIFT:\033[0m\n Direction: ' + str(PointOffsetDirection) + '\n Magnitude: ' +
              str('%.2f' % PointOffsetDistanceM) + '\n Output coordinate: ' + str('%.2f' % x) + ', ' + str('%.2f' % y) +
              '\n')  # Displays objects.
    return x, y  # Ends function execution.


def SliceDataFrameCell(data_type, dataframe, position, column, display):  # Defines function. For DataFrame slicing by
    # row value and index.
    Index = dataframe.index  # Defines object. Retrieves DataFrame index.
    if column is not None:  # Begins conditional statement. Checks inequality. Selects function format.
        CellValue = dataframe.loc[Index[position], column]  # Defines variable. Slices DatFrame by row value and index.
    else:  # Continues conditional statement. Checks inequality. Selects function format.
        CellValue = dataframe.loc[Index[position]]  # Defines variable. Slices DatFrame by row value and index.
    Type = type(CellValue)  # Defines variable. Retrieves data type of variable.
    if Type == data_type:  # Begins conditional statement. Checks equality. Checks if data type is desired by function
        # input.
        pass  # Pass command. Moves on to next line.
    else:  # Continues conditional statement. Checks inequality. Checks if data type is desired by function input.
        if data_type == 'Integer':  # Begins conditional statement. Checks equality. Enforces desired data type.
            CellValue = int(CellValue)  # Redefines variable. Converts value to integer.
        elif data_type == 'Float':  # Continues conditional statement. Checks equality. Enforces desired data type.
            CellValue = float(CellValue)  # Redefines variable. Converts value to float.
        else:  # Continues conditional statement. Checks equality. Enforces desired data type.
            CellValue = str(CellValue)  # Redefines variable. Converts value to string.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mRETRIEVED VALUE:\033[0m ' + str(CellValue) + '\n')  # Displays objects.
    return CellValue  # Ends function execution.


def SliceDataFrameColumns(output, data_type, dataframe, column, check_duplicates, drop_nan, display):  # Defines
    # function. For DataFrame slicing by column.
    dfSlice = dataframe[column]  # Defines DataFrame. Slices DatFrame by column header.
    if check_duplicates == 1:  # Begins conditional statement. Checks equality. Checks if duplicate values should be
        # removed from DataFrame.
        dfSlice = dfSlice.drop_duplicates(keep='first')  # Redefines DataFrame. Drops all duplicate values.
    if drop_nan == 1:  # Begins conditional statement. Checks equality. Checks if NaN values should be removed from
        # DataFrame.
        dfSlice = dfSlice.dropna()  # Redefines DataFrame. Drops all NaN values.
    Type = dfSlice.dtypes  # Defines variable. Retrieves data type of column DataFrame.
    if Type == data_type:  # Begins conditional statement. Checks equality. Checks if data type is desired by function
        # input.
        pass  # Pass command. Moves on to next line.
    else:  # Continues conditional statement. Checks equality. Checks if data type is desired by function input.
        if data_type == 'Integer':  # Begins conditional statement. Checks equality. Enforces desired data type.
            dfSlice = dfSlice.astype(int)  # Redefines DataFrame. Converts values to integer.
        elif data_type == 'Float':  # Continues conditional statement. Checks equality. Enforces desired data type.
            dfSlice = dfSlice.astype(float)  # Redefines DataFrame. Converts values to float.
        else:  # Continues conditional statement. Checks equality. Enforces desired data type.
            dfSlice = dfSlice.astype(str)  # Redefines DataFrame. Converts value to string.
    if output == 'DataFrame':  # Begins conditional statement. Checks equality. For output type selection.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED DATAFRAME:\033[0m \n...\n', dfSlice, '\n')  # Displays objects.
        return dfSlice  # Ends function execution.
    elif output == 'List':  # Continues conditional statement. Checks equality. For output type selection.
        SliceList = dfSlice.tolist()  # Defines list. Converts DataFrame to list.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED LIST:\033[0m', SliceList, '\n')  # Displays objects.
        return SliceList  # Ends function execution.
    else:  # Continues conditional statement. Checks equality. For output type selection.
        SliceArray = dfSlice.to_numpy()  # Defines array. Converts DataFrame to array.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED ARRAY:\033[0m', SliceArray, '\n')  # Displays objects.
        return SliceArray  # Ends function execution.


def SliceDataFrameRows(search_type, dataframe, column, value, display):  # Defines function. For DataFrame slicing by
    # row value.
    if search_type == 'Equals':  # Begins conditional statement. Checks equality. Sets function format.
        dfSlice = dataframe[dataframe[column] == value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Less than':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = dataframe[dataframe[column] < value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Greater than':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = dataframe[dataframe[column] > value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Less than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = dataframe[dataframe[column] <= value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Greater than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = dataframe[dataframe[column] >= value]  # Defines DataFrame. Slices DataFrame by value and relation.
    else:  # Continues conditional statement. Checks inequality. Sets function format.
        dfSlice = dataframe[dataframe[column] != value]  # Defines DataFrame. Slices DataFrame by value and relation.
    dfSlice = dfSlice.loc[:, ~dfSlice.columns.str.match('Unnamed')]  # Redefines DataFrame. Searches for empty columns
    # and deletes them.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED DATAFRAME: \033[0m \n...\n', dfSlice, '\n')  # Displays objects.
    return dfSlice  # Ends function execution.
