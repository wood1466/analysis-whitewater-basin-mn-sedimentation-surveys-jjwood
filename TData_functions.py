# ======================================================================================================================
# TRANSECT DATA USER DEFINED FUNCTIONS * -------------------------------------------------------------------------------
# PYTHON PROGRAMS * ----------------------------------------------------------------------------------------------------

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import geopandas as gpd  # Imports GeoPandas with alias. Enables geospatial functionality.
import matplotlib.pyplot as plt  # Imports Matplotlib (visualization with Python) with alias. Enables figure creation.
import numpy as np  # Imports pandas (Python data analysis library) with alias. Enables use of DataFrames.
import os  # Imports os (miscellaneous operating system interfaces). Enables operating system dependent functionality.
import pandas as pd  # Imports NumPy (the fundamental package for scientific computing with Python) with alias. Enables
# use of advanced mathematics.

# ======================================================================================================================
# PART 2: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------


def CreateFolder(path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('\033[1mCREATED FOLDER:\033[0m ' + path + '\n')  # Displays objects.


def CreateForwardRange(start, end, step, display):  # Defines function. For generating forward array between two numbers.
    end += 1  # Defines variable. Resets end of range so array includes final input value.
    EndLabel = end - 1  # Defines variable. For display.
    Range = np.arange(start, end, step)  # Defines array.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED ARRAY:\033[0m \n  Limits: ' + str(start) + ' & ' + str(EndLabel) + ' --> Array:', Range)
        # Displays objects.
    return Range  # Ends function execution.


def ConvertCsvToDataFrame(path, display):  # Defines function. For uploading .csv file and converting to a DataFrame for
    # Python manipulation.
    CsvData = pd.read_csv(path)  # Defines variable. Uploads .csv file.
    df = pd.DataFrame(CsvData)  # Defines DataFrame. Converts .csv. to DataFrame.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame display format. Displays all DataFrame columns.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mUPLOADED .CSV DATA:\033[0m ' + path + '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends function execution.


def MoveReferenceCoordinates(x, y, dataframe1, dataframe2, position, column1, column2, column3, conversion_factor,
                             display):  # Defines function. For moving transect reference coordinates if established
    # off of line.
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
        CoordinateAccuracyM = CoordinateAccuracyMList[-1]  # Redefines variable. Selects final list component for
        # value.
    else:  # Continues conditional statement. Checks inequality. Checks if estimated coordinate accuracy is a range.
        CoordinateAccuracyM = CoordinateAccuracyMList[0]  # Redefines variable. Selects first list component for
        # value.
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
        print('\033[1mMARKER SHIFT:\033[0m\n Direction: ' + str(PointOffsetDirection) + '\n Magnitude: ' + str(
            '%.2f' % PointOffsetDistanceM) + '\n Output coordinate: ' + str('%.2f' % x) + ', ' + str('%.2f' % y) + '\n')
        # Displays objects.
    return x, y  # Ends function execution.


def CalculateTransectAzimuth(x1, y1, x2, y2, display):  # Defines function. For transect azimuth calculations from reference coordinates.
    DeltaX = x2 - x1  # Defines variable. Calculates difference in x coordinates between reference points.
    DeltaY = y2 - y1  # Defines variable. Calculates difference in y coordinates between reference points.
    if DeltaX > 0:  # Begins conditional statement. Checks relation. Assigns cartesian quadrant for proper reference angle selection.
        if DeltaY >= 0:  # Begins conditional statement. Checks relation. Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 1  # Defines variable. Assigns quadrant.
        else:  # Continues conditional statement. Checks relation. Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 4  # Defines variable. Assigns quadrant.
    elif DeltaX < 0:  # Continues conditional statement. Checks relation. Assigns cartesian quadrant for proper reference angle selection.
        if DeltaY > 0:  # Begins conditional statement. Checks relation. Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 2  # Defines variable. Assigns quadrant.
        else:  # Continues conditional statement. Checks relation.  Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 3  # Defines variable. Assigns quadrant.
    else:  # Continues conditional statement. Checks relation.  Assigns cartesian quadrant for proper reference angle selection.
        if DeltaY > 0:  # Begins conditional statement. Checks relation.  Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 2  # Defines variable. Assigns quadrant.
        else:  # Continues conditional statement. Checks relation.  Assigns cartesian quadrant for proper reference angle selection.
            Quadrant = 4  # Defines variable. Assigns quadrant.
    if Quadrant == 1:  # Begins conditional statement. Checks equality. Calculates transect azimuth.
        ReferenceAngle = (1/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        Azimuth = ReferenceAngle - abs(np.arctan(DeltaX / DeltaY))  # Defines variable. Calculates transect azimuth.
    elif Quadrant == 2:  # Continues conditional statement. Checks equality.  Calculates transect azimuth.
        ReferenceAngle = (1/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        Azimuth = ReferenceAngle + abs(np.arctan(DeltaX / DeltaY))  # Defines variable. Calculates transect azimuth.
    elif Quadrant == 3:  # Continues conditional statement. Checks equality.  Calculates transect azimuth.
        ReferenceAngle = (3/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        Azimuth = ReferenceAngle - abs(np.arctan(DeltaX / DeltaY))  # Defines variable. Calculates transect azimuth.
    else:  # Continues conditional statement. Checks equality.  Calculates transect azimuth.
        ReferenceAngle = (3/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        Azimuth = ReferenceAngle + abs(np.arctan(DeltaX / DeltaY))  # Defines variable. Calculates transect azimuth.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCALCULATED TRANSECT AZIMUTH:\033[0m ' + str(Azimuth) + '\n')  # Displays objects.
    return Azimuth  # Ends function execution.


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
    dfSlice = dfSlice.loc[:, ~dfSlice.columns.str.match('Unnamed')]  # Redefines DataFrame. Searches for empty
    # columns and deletes them.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED DATAFRAME: \033[0m \n...\n', dfSlice, '\n')  # Displays objects.
    return dfSlice  # Ends function execution.