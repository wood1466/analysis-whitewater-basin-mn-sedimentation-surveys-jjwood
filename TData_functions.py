# ======================================================================================================================
# TRANSECT DATA USER DEFINED FUNCTIONS * -------------------------------------------------------------------------------
# PYTHON PROGRAMS * ----------------------------------------------------------------------------------------------------

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------

# IMPORT MODULES -------------------------------------------------------------------------------------------------------
import os  # Imports os (miscellaneous operating system interfaces). Enables operating system dependent functionality.
import numpy as np  # Imports pandas (Python data analysis library) with alias. Enables use of DataFrames.
import pandas as pd  # Imports NumPy (the fundamental package for scientific computing with Python) with alias. Enables
# use of advanced mathematics.

# ======================================================================================================================
# PART 2: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------


def ForwardRange(Start, End, Step, Display):  # Defines function. For generating forward array between two numbers.
    End += 1  # Defines variable. Resets end of range so array includes final input value.
    EndLabel = End - 1  # Defines variable. For display.
    Range = np.arange(Start, End, Step)  # Defines array.
    if Display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED ARRAY:\033[0m \n  Limits: ' + str(Start) + ' & ' + str(EndLabel) + ' --> Array:', Range)
        # Displays objects.
    return Range  # Ends function execution.


def CreateFolder(Path):  # Defines function. For generating directory paths.
    if not os.path.exists(Path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(Path)  # Creates folder if it does not exist.
        print('\033[1mCREATED FOLDER:\033[0m ' + Path + '\n')  # Displays objects.


def CsvToDataFrame(Path, Display):  # Defines function. For uploading .csv file and converting to a DataFrame for
    # Python manipulation.
    CsvData = pd.read_csv(Path)  # Defines variable. Uploads .csv file.
    df = pd.DataFrame(CsvData)  # Defines DataFrame. Converts .csv. to DataFrame.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame display format. Displays all DataFrame columns.
    if Display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mUPLOADED .CSV DATA:\033[0m ' + Path + '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends function execution.


def SliceDataFrameRows(SearchType, Dataframe, Column, Value, Display):  # Defines function. For DataFrame slicing by
    # row value.
    if SearchType == 'Equals':  # Begins conditional statement. Checks equality. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] == Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif SearchType == 'Less than':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] < Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif SearchType == 'Greater than':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] > Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif SearchType == 'Less than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] <= Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif SearchType == 'Greater than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] >= Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    else:  # Continues conditional statement. Checks inequality. Sets function format.
        dfSlice = Dataframe[Dataframe[Column] != Value]  # Defines DataFrame. Slices DataFrame by value and relation.
    dfSlice = dfSlice.loc[:, ~dfSlice.columns.str.match('Unnamed')]  # Redefines DataFrame. Searches for empty
    # columns and deletes them.
    if Display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED DATAFRAME: \033[0m \n...\n', dfSlice, '\n')  # Displays objects.
    return dfSlice  # Ends function execution.


def SliceDataFrameCell(DataType, Dataframe, Position, Column, Display):  # Defines function. For DataFrame slicing by
    # row value and index.
    Index = Dataframe.index  # Defines object. Retrieves DataFrame index.
    if Column is not None:  # Begins conditional statement. Checks inequality. Selects function format.
        CellValue = Dataframe.loc[Index[Position], Column]  # Defines variable. Slices DatFrame by row value and index.
    else:  # Continues conditional statement. Checks inequality. Selects function format.
        CellValue = Dataframe.loc[Index[Position]]  # Defines variable. Slices DatFrame by row value and index.
    Type = type(CellValue)  # Defines variable. Retrieves data type of variable.
    if Type == DataType:  # Begins conditional statement. Checks equality. Checks if data type is desired by function
        # input.
        pass  # Pass command. Moves on to next line.
    else:  # Continues conditional statement. Checks inequality. Checks if data type is desired by function input.
        if DataType == 'Integer':  # Begins conditional statement. Checks equality. Enforces desired data type.
            CellValue = int(CellValue)  # Redefines variable. Converts value to integer.
        elif DataType == 'Float':  # Continues conditional statement. Checks equality. Enforces desired data type.
            CellValue = float(CellValue)  # Redefines variable. Converts value to float.
        else:  # Continues conditional statement. Checks equality. Enforces desired data type.
            CellValue = str(CellValue)  # Redefines variable. Converts value to string.
    if Display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mRETRIEVED VALUE:\033[0m ' + str(CellValue) + '\n')  # Displays objects.
    return CellValue  # Ends function execution.
