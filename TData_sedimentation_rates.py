# ======================================================================================================================
# WHITEWATER RIVER VALLEY (MN) SCS-USGS STREAM AND VALLEY SEDIMENTATION SURVEY TRANSECTS * -----------------------------
# TRANSECT DATA SEDIMENTATION RATE CALCULATOR * ------------------------------------------------------------------------
# PYTHON PROGRAM * -----------------------------------------------------------------------------------------------------

# ======================================================================================================================
# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START TRANSECT SEDIMENTATION RATE CALCULATIONS!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from TData_functions import *   # Imports functions. Imports all functions from outside program.

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Directory
InputFolder = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.
OutputFolder = 'Output'  # Defines variable. Sets name of output folder where all data products will be exported.
CalculationFolder = 'Calculations'  # Defines variable. Sets name of output folder where all results will be exported.

# Data
InputFile1 = InputFolder + '/Elevation_surveys_20250127.csv'  # Defines variable. Sets file path to input file. Sets path to transect data that will be used in calculations.
InputFile2 = InputFolder + '/Boring_surveys_20250127.csv'  # Defines variable. Sets file path to input file. Sets path to transect data that will be used in calculations.
InputFile3 = InputFolder + '/Discontinuous_elevation_surveys_20250127.csv'  # Defines variable. Sets file path to input file. Sets path to transect data exceptions that will be used in calculations.

# Operation limits
TransectNumberStart = 1  # Defines variable. Sets start transect number for operation loop.
TransectNumberEnd = 13  # Defines variable. Sets end transect number for operation loop.
TransectNumbers = CreateForwardRange(TransectNumberStart, TransectNumberEnd, 1, 0)  # Defines array. Calls function. Sets loop order by transect.

# Conversion factors
FtToM = 3.281  # Defines variable. Sets conversion factor from feet to meters.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

CreateFolder(OutputFolder)  # Creates folder. Calls function. Creates output folder where all data products will be exported.
CreateFolder(OutputFolder + '/' + CalculationFolder)  # Creates folder. Calls function. Creates output folder where all results will be exported.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

dfTransectElevations = ConvertCsvToDataFrame(InputFile1, 0)  # Defines DataFrame. Calls function. Uploads transect data.
dfTransectBorings = ConvertCsvToDataFrame(InputFile2, 0)  # Defines DataFrame. Calls function. Uploads transect data.
dfTDiscontinuousElevations = ConvertCsvToDataFrame(InputFile3, 0)  # Defines DataFrame. Calls function. Uploads transect data exceptions.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select transect data -------------------------------------------------------------------------------------------------

for i in TransectNumbers:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates sedimentation rates for each transect in sequence.

    dfTransectElevationsi = SliceDataFrameRows('Equals', dfTransectElevations, 'TNum', i, 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield single transect data.

    # Select transect survey data --------------------------------------------------------------------------------------

    TSurveyNumbers = SliceDataFrameColumns('Array', 'Integer', dfTransectElevationsi, 'ESrvNum', 1, 0, 0)  # Defines array. Calls function. Slices DataFrame to transect survey numbers.

    for j in TSurveyNumbers:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates sedimentation rates for each survey in sequence.
        if j < TSurveyNumbers[-1]:  # Begins conditional statement. Checks relation. The most recent transect data has no other dataset to compare to.
            k = j + 1  # Defines variable. Calculates survey number of earlier transect data to compare with.

            dfTransectElevationsi_j = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', j, 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield transect single survey data.
            dfTransectElevationsi_k = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', k, 0)  # Defines DataFrame. Calls function. Slices DataFrame to yield transect single survey data.

            # Stations
            AryTStationsFti_j = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_j, 'ESttnFt', 0, 0, 0)  # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.
            AryTStationsFti_k = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_k, 'ESttnFt', 0, 0, 0)  # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.

            # Elevations

            # Check survey uncertainties -------------------------------------------------------------------------------

            TPropagatedErrori_j = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'PrpClsErFt', 0)  # Defines variable. Calls function. Slices DataFrame to yield propagated survey error value. For selecting to use local or absolute elevation data.
            TPropagatedErrori_k = SliceDataFrameCell('String', dfTransectElevationsi_k, 0, 'PrpClsErFt', 0)  # Defines variable. Calls function. Slices DataFrame to yield propagated survey error value. For selecting to use local or absolute elevation data.

            if TPropagatedErrori_j == 'nan':  # Begins conditional statement. Checks equality. Selects local or absolute elevation data.
                AryTElevationsFti_j = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_j, 'E1Ft', 0, 0, 0)  # Defines array. Calls function. Slices DataFrame to yield absolute elevations of survey dataset.
            else:  # Continues conditional statement. Checks inequality. Selects local or absolute elevation data.
                TSurveyErrori_j = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'SrvClsErFt', 0)  # Defines variable. Calls function. Slices DataFrame to yield propagated survey error value. For selecting to use local or absolute elevation data.
                break  # Break command. Exits loop.
            if TPropagatedErrori_k == 'nan':  # Begins conditional statement. Checks equality. Selects local or absolute elevation data.
                AryTElevationsFti_k = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_k, 'E1Ft', 0, 0, 0)  # Defines array. Calls function. Slices DataFrame to yield absolute elevations of survey dataset.
            else:  # Continues conditional statement. Checks inequality. Selects local or absolute elevation data.
                TSurveyErrori_k = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'SrvClsErFt', 0)  # Defines variable. Calls function. Slices DataFrame to yield propagated survey error value. For selecting to use local or absolute elevation data.
                break  # Break command. Exits loop.

            # INTERPOLATE DATA -----------------------------------------------------------------------------------------

            # Select interpolation bounds ------------------------------------------------------------------------------

            TStationStartFti_j = np.min(AryTStationsFti_j)  # Defines variable. Selects min element of array.
            TStationEndFti_j = np.max(AryTStationsFti_j)  # Defines variable. Selects max element of array.
            TStationStartFti_k = np.min(AryTStationsFti_k)  # Defines variable. Selects min element of array.
            TStationEndFti_k = np.max(AryTStationsFti_k)  # Defines variable. Selects max element of array.

            print(TStationStartFti_j, TStationEndFti_j, TStationStartFti_k, TStationEndFti_k)

            AryTStationStartFti_jk = np.array([TStationStartFti_j,TStationStartFti_k])  # Defines array. Creates array of survey station starts. For selecting shared station for interpolation.
            AryTStationEndFti_jk = np.array([TStationEndFti_j, TStationEndFti_k])  # Defines array. Creates array of survey station ends. For selecting shared station for interpolation.

            print(AryTStationStartFti_jk, AryTStationEndFti_jk)

            TInterpStationStartFti_jk = np.max(AryTStationStartFti_jk)  # Defines variable. Selects max element of array. Selects first shared station.
            TInterpStationEndFti_jk = np.min(AryTStationEndFti_jk)  # Defines variable. Selects min element of array. Selects last shared station.

            print(TInterpStationStartFti_jk, TInterpStationEndFti_jk)

            # Interpolate data -----------------------------------------------------------------------------------------
            f = sc.interpolate.interp1d(AryTStationsFti_j, AryTElevationsFti_j, kind='linear')  # Sets interpolation format.
            breakpoint()










