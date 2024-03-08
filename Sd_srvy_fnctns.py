# ======================================================================================================================
# WHITEWATER RIVER VALLEY SEDIMENTATION SURVEYS * ----------------------------------------------------------------------
# SURVEY DATA ANALYSIS, DIGITIZATION, AND VISUALIZATION FUNCTIONS * ----------------------------------------------------
# PYTHON SCRIPTS * -----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import os # Imports os (miscellaneous operating system interfaces). Enables operating system dependent functionality.

import pandas as pd, numpy as np, matplotlib.pyplot as plt, geopandas as gpd

# Imports pandas (Python data analysis library) with alias. Enables use of DataFrames.
# Imports NumPy (the fundamental package for scientific computing with Python) with alias. Enables use of advanced
# mathematics.
# Imports Matplotlib (visualization with Python) with alias. Enables figure creation.
# Imports GeoPandas with alias. Enables geospatial functionality.

# ======================================================================================================================
# PART 2: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------
# ======================================================================================================================

def create_folder(path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('\033[1mCREATED FOLDER:\033[0m ' + path + '\n')  # Displays objects.

def csv_to_DataFrame(path, display):  # Defines function. For uploading .csv file and converting to a DataFrame for
    # Python manipulation.
    csv_data = pd.read_csv(path)  # Defines variable. Uploads .csv file.
    df = pd.DataFrame(csv_data)  # Defines DataFrame. Converts .csv. to DataFrame.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame display format. Displays all DataFrame columns.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mUPLOADED .CSV DATA:\033[0m ' + path + '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends function execution.

def forward_range(start, end, step, display):  # Defines function. For generating forward array between two numbers.
    end += 1  # Defines variable. Resets end of range so array includes final input value.
    end_lbl = end - 1  # Defines variable. For display.
    frwd_rng = np.arange(start, end, step)  # Defines array.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED ARRAY:\033[0m \n  Limits: ' + str(start) + ' & ' + str(end_lbl) + ' --> Array:', frwd_rng)
        # Displays objects.
    return frwd_rng  # Ends function execution.

def slice_DataFrame_rows(search_type, dataframe, column, value, display):  # Defines function. For DataFrame slicing by
    # row value.
    if search_type == 'Equals':  # Begins conditional statement. Checks equality. Sets function format.
        df_slc_r = dataframe[dataframe[column] == value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Less than':  # Continues conditional statement. Checks relation. Sets function format.
        df_slc_r = dataframe[dataframe[column] < value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'Less than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        df_slc_r = dataframe[dataframe[column] <= value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'More than':  # Continues conditional statement. Checks relation. Sets function format.
        df_slc_r = dataframe[dataframe[column] > value]  # Defines DataFrame. Slices DataFrame by value and relation.
    elif search_type == 'More than/Equal':  # Continues conditional statement. Checks relation. Sets function format.
        df_slc_r = dataframe[dataframe[column] >= value]  # Defines DataFrame. Slices DataFrame by value and relation.
    else:  # Continues conditional statement. Checks inequality. Sets function format.
        df_slc_r = dataframe[dataframe[column] != value]  # Defines DataFrame. Slices DataFrame by value and relation.
    df_slc_r = df_slc_r.loc[:, ~df_slc_r.columns.str.match('Unnamed')]  # Redefines DataFrame. Searches for empty
    # columns and deletes them.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCREATED DATAFRAME: \033[0m \n...\n', df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends function execution.

def slice_DataFrame_columns(output, data_type, dataframe, column, check_duplicates, drop_nan, display):  # Defines
    # function. For DataFrame slicing by column.
    df_slc_c = dataframe[column]  # Defines DataFrame. Slices DatFrame by column header.
    if check_duplicates == 1:  # Begins conditional statement. Checks equality. Checks if duplicate values should be
        # removed from DataFrame.
        df_slc_c = df_slc_c.drop_duplicates(keep='first')  # Redefines DataFrame. Drops all duplicate values.
    if drop_nan == 1:  # Begins conditional statement. Checks equality. Checks if NaN values should be removed from
        # DataFrame.
        df_slc_c = df_slc_c.dropna()  # Redefines DataFrame. Drops all NaN values.
    typ = df_slc_c.dtypes  # Defines variable. Retrieves data type of column DataFrame.
    if typ == data_type:  # Begins conditional statement. Checks equality. Checks if data type is desired by function
        # input.
        pass  # Pass command. Moves on to next line.
    else:  # Continues conditional statement. Checks equality. Checks if data type is desired by function input.
        if data_type == 'Integer':  # Begins conditional statement. Checks equality. Enforces desired data type.
            df_slc_c = df_slc_c.astype(int)  # Redefines DataFrame. Converts values to integer.
        elif data_type == 'Float':  # Continues conditional statement. Checks equality. Enforces desired data type.
            df_slc_c = df_slc_c.astype(float)  # Redefines DataFrame. Converts values to float.
        else:  # Continues conditional statement. Checks equality. Enforces desired data type.
            df_slc_c = df_slc_c.astype(str)  # Redefines DataFrame. Converts values to string.
    if output == 'DataFrame':  # Begins conditional statement. Checks equality. For output type selection.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED DATAFRAME:\033[0m \n...\n', df_slc_c, '\n')  # Displays objects.
        return df_slc_c  # Ends function execution.
    elif output == 'List':  # Continues conditional statement. Checks equality. For output type selection.
        slc_c_lst = df_slc_c.tolist()  # Defines list. Converts DataFrame to list.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED LIST:\033[0m', slc_c_lst, '\n')  # Displays objects.
        return slc_c_lst  # Ends function execution.
    else:  # Continues conditional statement. Checks equality. For output type selection.
        slc_c_arr = df_slc_c.to_numpy()  # Defines array. Converts DataFrame to array.
        if display == 1:  # Begins conditional statement. Checks equality. For display.
            print('\033[1mCREATED ARRAY:\033[0m', slc_c_arr, '\n')  # Displays objects.
        return slc_c_arr  # Ends function execution.

def slice_DataFrame_cell(data_type, dataframe, position, column, display):  # Defines function. For DataFrame slicing by
    # row value and index.
    index = dataframe.index  # Defines object. Retrieves DataFrame index.
    if column != None:  # Begins conditional statement. Checks inequality. Selects function format.
        slc_cl = dataframe.loc[index[position], column]  # Defines variable. Slices DatFrame by row value and index.
    else:  # Continues conditional statement. Checks inequality. Selects function format.
        slc_cl = dataframe.loc[index[position]]  # Defines variable. Slices DatFrame by row value and index.
    typ = type(slc_cl)  # Defines variable. Retrieves data type of variable.
    if typ == data_type:  # Begins conditional statement. Checks equality. Checks if data type is desired by function
        # input.
        pass  # Pass command. Moves on to next line.
    else:  # Continues conditional statement. Checks equality. Checks if data type is desired by function input.
        if data_type == 'Integer':  # Begins conditional statement. Checks equality. Enforces desired data type.
            slc_cl = int(slc_cl)  # Redefines variable. Converts value to integer.
        elif data_type == 'Float':  # Continues conditional statement. Checks equality. Enforces desired data type.
            slc_cl = float(slc_cl)  # Redefines variable. Converts value to float.
        else:  # Continues conditional statement. Checks equality. Enforces desired data type.
            slc_cl = str(slc_cl)  # Redefines variable. Converts value to string.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mRETRIEVED VALUE:\033[0m ' + str(slc_cl) + '\n')  # Displays objects.
    return slc_cl # Ends function execution.

def retrieve_metadata(dataframe, display):  # Defines function. For metadata retrieval for display and data slicing.
    chnl_nm = slice_DataFrame_cell('String', dataframe, 0, 'Chnl_name', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield stream channel name of present dataset.
    rng_nm = slice_DataFrame_cell('String', dataframe, 0, 'Srvy_range', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield transect name of present dataset.
    srvy_era = slice_DataFrame_cell('Integer', dataframe, 0, 'Srvy_year', 0)  # Defines variable. Calls
    # function. Slices DataFrame to yield survey era of present dataset.
    srvy_yr = slice_DataFrame_cell('String', dataframe, 0, 'Year', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey year of present dataset.
    srvy_mnth = slice_DataFrame_cell('String', dataframe, 0, 'Month', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey month of present dataset.
    srvy_dy = slice_DataFrame_cell('String', dataframe, 0, 'Day', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield survey day(s) of present dataset.
    brng_r_dr = slice_DataFrame_cell('String', dataframe, 0, 'Brng_R_dir', 0)  # Defines variable. Calls
    # function. Slices DataFrame to yield bearing reference direction of present dataset.
    brng_angl = slice_DataFrame_cell('Float', dataframe, 0, 'Brng_A', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield bearing angle of present dataset.
    brng_a_dr = slice_DataFrame_cell('String', dataframe, 0, 'Brng_A_dir', 0)  # Defines variable. Calls
    # function. Slices DataFrame to yield bearing angle direction of present dataset.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('==================================================')  # Displays objects.
        print('\033[1mChannel:\033[0m ' + str(chnl_nm))  # Displays objects.
        print('\033[1mTransect:\033[0m ' + str(rng_nm))  # Displays objects.
        print('\033[1mSurvey:\033[0m ' + str(srvy_era))  # Displays objects.
        print('\033[1mDate:\033[0m ' + str(srvy_mnth) + '/' + str(srvy_dy) + '/' + str(srvy_yr))  # Displays objects.
        print('\033[1mBearing:\033[0m ' + str(brng_r_dr) + str(brng_angl) + str(brng_a_dr))  # Displays objects.
        print('--------------------------------------------------')  # Displays objects.

def range_orientation_calculator(x1, x2, y1, y2, display):  # Defines function. For range azimuth calculation from
    # cartesian coordinates for coordinate geometry digitization.
    dlt_x = x2 - x1  # Defines variable. Calculates difference in x monument coordinates.
    dlt_y = y2 - y1  # Defines variable. Calculates difference in y monument coordinates.
    if dlt_x > 0:  # Begins conditional statement. Checks relation. Executes code when condition satisfied. Assigns
        # cartesian quadrant for proper reference azimuth selection.
        if dlt_y >= 0:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 1  # Defines variable. Assigns quadrant.
        else:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 4  # Defines variable. Assigns quadrant.
    elif dlt_x < 0:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
        if dlt_y > 0:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 2  # Defines variable. Assigns quadrant.
        else:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 3  # Defines variable. Assigns quadrant.
    else:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
        if dlt_y > 0:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 2  # Defines variable. Assigns quadrant.
        else:  # Begins conditional statement. Checks relation. Executes code when condition satisfied.
            qdrnt = 4  # Defines variable. Assigns quadrant.
    if qdrnt == 1:  # Begins conditional statement. Checks equality. Executes code when condition satisfied.
        angl = abs(np.arctan(dlt_x / dlt_y))  # Defines variable. Calculates range azimuth.
        trg = 1  # Defines variable. Sets binary toggle. For selection of correct trigonometric operation for
        # change in x: 1 = cosine, 0 = sine.
    elif qdrnt == 2:  # Begins conditional statement. Checks equality. Executes code when condition satisfied.
        rf_angl = 2 * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        angl = rf_angl - abs(np.arctan(dlt_x / dlt_y))  # Defines variable. Calculates range azimuth.
        trg = 0  # Defines variable. Sets binary toggle. For selection of correct trigonometric operation for
        # change in x: 1 = cosine, 0 = sine.
    elif qdrnt == 3:  # Begins conditional statement. Checks equality. Executes code when condition satisfied.
        rf_angl = (3/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        angl = rf_angl - abs(np.arctan(dlt_x / dlt_y))  # Defines variable. Calculates range azimuth.
        trg = 1  # Defines variable. Sets binary toggle. For selection of correct trigonometric operation for
        # change in x: 1 = cosine, 0 = sine.
    else:  # Begins conditional statement. Checks equality. Executes code when condition satisfied.
        rf_angl = (3/2) * np.pi  # Defines variable. Sets reference angle for correction of calculated orientation to
        # azimuth.
        angl = rf_angl + abs(np.arctan(dlt_x / dlt_y))  # Defines variable. Calculates range azimuth.
        trg = 0  # Defines variable. Sets binary toggle. For selection of correct trigonometric operation for
        # change in x: 1 = cosine, 0 = sine.
    if display == 1:  # Begins conditional statement. Checks equality. For display.
        print('\033[1mCALCULATED RANGE ORIENTATION:\033[0m ' + str(angl) + '\n')  # Displays objects.
    return angl, trg  # Ends function execution.

# ======================================================================================================================
# * --------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================