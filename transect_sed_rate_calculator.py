# ======================================================================================================================
# WHITEWATER RIVER VALLEY (MN) SCS-USGS STREAM AND VALLEY SEDIMENTATION SURVEY DATA * ----------------------------------
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
InputFile1 = InputFolder + '/Elevation_surveys_20250129.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect data that will be used in calculations.
InputFile2 = InputFolder + '/Calculation_exceptions_20250130.csv'  # Defines variable. Sets file path to input file.
# Sets path to transect data exceptions that will be used in calculations.
OutputFile1 = '/WW_sedimentation_rates.csv'  # Defines variable. Sets name for output file.

# Operation limits
TransectNumberStart = 1  # Defines variable. Sets start transect number for operation loop.
TransectNumberEnd = 107  # Defines variable. Sets end transect number for operation loop.
AryTransectNumbers = CreateForwardRange(TransectNumberStart, TransectNumberEnd, 1, 0)  # Defines array. Calls function.
# Sets loop order by transect.

# Operations
InterpInterval = 0.1  # Defines variable. Sets interval for transect data interpolation.

# Conversion factors
FtToCm = 12 * 2.54   # Defines variable. Sets conversion factor from feet to centimeters.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

CreateFolder(OutputFolder)  # Creates folder. Calls function. Creates output folder where all data products will be
# exported.
CreateFolder(OutputFolder + '/' + CalculationFolder)  # Creates folder. Calls function. Creates output folder where all
# results will be exported.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

dfTransectElevations = ConvertCsvToDataFrame(InputFile1, 0)  # Defines DataFrame. Calls function. Uploads transect data.
dfTCalculationExceptions = ConvertCsvToDataFrame(InputFile2, 0)  # Defines DataFrame. Calls function. Uploads transect
# data exceptions.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select transect data -------------------------------------------------------------------------------------------------

for i in AryTransectNumbers:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates
    # sedimentation rates for each transect in sequence.

    dfTransectElevationsi = SliceDataFrameRows('Equals', dfTransectElevations, 'TNum', i, 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single transect data.

    # Select transect survey data --------------------------------------------------------------------------------------

    AryTSurveyNumbers = SliceDataFrameColumns('Array', 'Integer', dfTransectElevationsi, 'ESrvNum', 1, 0, 0)  # Defines
    # array. Calls function. Slices DataFrame to transect survey numbers.

    for j in AryTSurveyNumbers:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates
        # sedimentation rates for each survey in sequence.
        if j < AryTSurveyNumbers[-1]:  # Begins conditional statement. Checks relation. The most recent transect data
            # has no other dataset to compare to.
            k = j + 1  # Defines variable. Calculates survey number of earlier transect data to compare with.

            dfTransectElevationsi_j = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', j, 0)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield transect single survey data.
            dfTransectElevationsi_k = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', k, 0)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield transect single survey data.

            # Metadata
            TID = SliceDataFrameCell('String', dfTransectElevationsi, 0, 'TId24', 0)  # Defines variable. Calls
            # function.  Slices DataFrame to yield transect ID.
            TProfileYeari_j = SliceDataFrameCell('Integer', dfTransectElevationsi_j, 0, 'PYr', 0)  # Defines variable.
            # Calls function.  Slices DataFrame to yield transect survey profile year.
            TProfileTypei_j = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'PType', 0)  # Defines variable.
            # Calls function.  Slices DataFrame to yield transect survey profile type.
            TProfileYeari_k = SliceDataFrameCell('Integer', dfTransectElevationsi_k, 0, 'PYr', 0)  # Defines variable.
            # Calls function.  Slices DataFrame to yield transect survey profile year.
            TProfileTypei_k = SliceDataFrameCell('String', dfTransectElevationsi_k, 0, 'PType', 0)  # Defines variable.
            # Calls function.  Slices DataFrame to yield transect survey profile type.

            print('\033[1mCALCULATING:\033[0m', TID, ': ' + str(TProfileYeari_j) + ' (' + str(TProfileTypei_j) + ') – '
                  + str(TProfileYeari_k) + ' (' + str(TProfileTypei_k) + ') \n')  # Displays objects.

            # Stations
            AryTStationsFti_j = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_j, 'ESttnFt', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.
            AryTStationsFti_k = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_k, 'ESttnFt', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.

            # Elevations
            AryTElevationsFti_j = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_j, 'E1Ft', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield absolute elevations of survey dataset.
            AryTElevationsFti_k = SliceDataFrameColumns('Array', 'Float', dfTransectElevationsi_k, 'E1Ft', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield absolute elevations of survey dataset.

            # INTERPOLATE DATA -----------------------------------------------------------------------------------------

            # Select interpolation range -------------------------------------------------------------------------------

            TStationStartFti_j = np.min(AryTStationsFti_j)  # Defines variable. Selects min element of array. For
            # choosing interpolation start.
            TStationEndFti_j = np.max(AryTStationsFti_j)  # Defines variable. Selects max element of array. For choosing
            # interpolation end.
            TStationStartFti_k = np.min(AryTStationsFti_k)  # Defines variable. Selects min element of array. For
            # choosing interpolation start.
            TStationEndFti_k = np.max(AryTStationsFti_k)  # Defines variable. Selects max element of array. For choosing
            # interpolation end.

            AryTStationStartFti_jk = np.array([TStationStartFti_j, TStationStartFti_k])  # Defines array. Creates array
            # of survey station starts.  For choosing interpolation start.
            AryTStationEndFti_jk = np.array([TStationEndFti_j, TStationEndFti_k])  # Defines array. Creates array of
            # survey station ends. For choosing interpolation end.

            TInterpStationStartFti_jk = np.max(AryTStationStartFti_jk)  # Defines variable. Selects max element of
            # array. Selects first shared station. Selects interpolation start.
            TInterpStationEndFti_jk = np.min(AryTStationEndFti_jk)  # Defines variable. Selects min element of array.
            # Selects last shared station. Selects interpolation start.

            AryTInterpStationsFti_jk = np.arange(TInterpStationStartFti_jk, TInterpStationEndFti_jk + InterpInterval,
                                                 InterpInterval)  # Defines array. Creates interpolation framework.

            AryTInterpStationsFti_jk = np.around(AryTInterpStationsFti_jk, decimals=1)  # Redefines array. Rounds
            # values.

            # Interpolate data -----------------------------------------------------------------------------------------

            AryTInterpElevationsFti_j = np.interp(AryTInterpStationsFti_jk, AryTStationsFti_j, AryTElevationsFti_j)
            # Defines array. Interpolates data.
            AryTInterpElevationsFti_k = np.interp(AryTInterpStationsFti_jk, AryTStationsFti_k, AryTElevationsFti_k)
            # Defines array. Interpolates data.

            # Plot
            # plt.plot(AryTInterpStationsFti_jk, AryTInterpElevationsFti_j, c='Magenta', marker='o', alpha=0.9)
            # Creates line plot. Plots interpolated transect data.
            # plt.plot(AryTStationsFti_j, AryTElevationsFti_j, c='Cyan', marker='o', alpha=0.9)  # Creates line plot.
            # Plots surveyed transect data.
            # plt.plot(AryTInterpStationsFti_jk, AryTInterpElevationsFti_k, c='Green', marker='o', alpha=0.9)
            # Creates line plot. Plots interpolated transect data.
            # plt.plot(AryTStationsFti_k, AryTElevationsFti_k, c='Yellow', marker='o', alpha=0.9)  # Creates line plot.
            # Plots surveyed transect data.
            # plt.show()  # Plot show command. Shows plot.

            # CALCULATE SEDIMENTATION RATES ----------------------------------------------------------------------------

            # Check for calculation exception --------------------------------------------------------------------------

            dfTExcChecki = SliceDataFrameRows('Equals', dfTCalculationExceptions, 'TId24', TID, 0)  # Defines DataFrame.
            # Calls function. Slices DataFrame to yield calculation exceptions.

            TSurveyExcStart1i_j, TSurveyExcEnd1i_j, TSurveyExcPairYear1i_j = CalculationExclusionChecker(
                dfTExcChecki, 'PYr', 'ESttnFt1', 'ESttnFt2', 'ExcPYr', 0, TProfileYeari_j, 0)  # Defines array. Calls
            # function. Creates array of exception zone if it exists.
            TSurveyExcStart1i_k, TSurveyExcEnd1i_k, TSurveyExcPairYear1i_k = CalculationExclusionChecker(
                dfTExcChecki, 'PYr', 'ESttnFt1', 'ESttnFt2', 'ExcPYr', 0, TProfileYeari_k, 0)  # Defines array. Calls
            # function. Creates array of exception zone if it exists.

            if TProfileYeari_k == 1939 and TProfileTypei_k == 'Extrapolated' and TSurveyExcPairYear1i_k == '1965':
                # Begin conditional statement. Checks equalities. Creates empty array of exception zone for 1939
                # extrapolated exception type. To ignore 1939 extrapolated exception if not paired with 1965 data.
                TSurveyExcStart1i_k = np.nan  # Defines value. Assigns NaN to value for 1939 extrapolated exception
                # type.
                TSurveyExcEnd1i_k = np.nan  # Defines value. Assigns NaN to value 1939 extrapolated for exception type.

            AryTSurveyExc1i_jk = np.array([TSurveyExcStart1i_j, TSurveyExcEnd1i_j, TSurveyExcStart1i_k,
                                           TSurveyExcEnd1i_k])  # Defines array. Creates array of transect exception
            # points. For general exceptions enacted during calculations.
            AryTSurveyExc1i_jk = np.delete(AryTSurveyExc1i_jk, np.isnan(AryTSurveyExc1i_jk))  # Redefines array. Deletes
            # NaN values.
            AryTSurveyExc1i_jk = np.around(AryTSurveyExc1i_jk, decimals=1)  # Redefines array. Rounds values.

            AryTSurveyExc2_1i_jk = np.empty(0)  # Defines array. Creates empty array. When 1939 extrapolated exception
            # does not exist or to ignore it if not paired with 1965 data.
            AryTSurveyExc2_2i_jk = np.empty(0)  # Defines array. Creates empty array. When 1939 extrapolated exception
            # does not exist or to ignore it if not paired with 1965 data.

            if TProfileYeari_j == 1939 and TProfileTypei_j == 'Extrapolated' and TProfileYeari_k == 1965:  # Begins
                # conditional statement. Checks equalities. Creates array of transect exception points. To enact 1939
                # extrapolation exceptions after calculations if paired with 1965 data.
                AryTSurveyExc2_1i_jk = np.array([TSurveyExcStart1i_j, TSurveyExcEnd1i_j])  # Defines array. Creates
                # array of transect exception points.
                AryTSurveyExc2_1i_jk = np.delete(AryTSurveyExc2_1i_jk, np.isnan(AryTSurveyExc2_1i_jk))  # Redefines
                # array. Deletes NaN values.
                AryTSurveyExc2_1i_jk = np.around(AryTSurveyExc2_1i_jk, decimals=1)  # Redefines array. Rounds values.

                dfTExcChecki_j = SliceDataFrameRows('Equals', dfTExcChecki, 'PYr', 1939, 0)  # Defines DataFrame. Calls
                # function. Slices DataFrame to yield calculation exceptions. For selection of second exception zone if
                # it exists.

                if any(dfTExcChecki_j.duplicated('PYr')):  # Begins conditional statement. Checks boolean. Checks if
                    # second exception zone exists.
                    TSurveyExcStart2i_j, TSurveyExcEnd2i_j, TSurveyExcPairYear2i_j = CalculationExclusionChecker(
                        dfTExcChecki, 'PYr', 'ESttnFt1', 'ESttnFt2', 'ExcPYr', 1, TProfileYeari_j, 0)  # Defines array.
                    # Calls function. Creates array of exception zone if it exists.

                    AryTSurveyExc2_2i_jk = np.array([TSurveyExcStart2i_j, TSurveyExcEnd2i_j])  # Defines array. Creates
                    # array of transect exclusion points.
                    AryTSurveyExc2_2i_jk = np.delete(AryTSurveyExc2_2i_jk, np.isnan(AryTSurveyExc2_2i_jk))  # Redefines
                    # array. Deletes NaN values.
                    AryTSurveyExc2_2i_jk = np.around(AryTSurveyExc2_2i_jk, decimals=1)  # Redefines array. Rounds
                    # values.

            if TProfileYeari_j == 1939 and TProfileTypei_j == 'Extrapolated' and TProfileYeari_k == 1965:  # Begins
                # conditional statement. Checks equalities. Creates empty array of exception zone for 1939 extrapolated
                # exception type. To enact 1939 extrapolated exception after calculations if paired with 1965 data.
                AryTSurveyExc1i_jk = np.empty(0)  # Defines array. Creates empty array. When 1939 extrapolated exception
                # exists and is paired with 1965 data.

            # Select interpolation pairs for calculation ---------------------------------------------------------------

            AryInterpIndices = np.arange(0, len(AryTInterpStationsFti_jk), 1)  # Defines array. Creates array of indices
            # for looping transect calculation.

            for x in AryInterpIndices:  # Begins loop. Loops through array elements. Loops through interpolated point
                # indices. Calculates sedimentation rate for each interpolation point in sequence.
                TInterpStationFti_jk_x = AryTInterpStationsFti_jk[x]  # Defines variable. Selects interpolation point.

                # Check if interpolation point is within exclusion bounds ----------------------------------------------

                if len(AryTSurveyExc1i_jk) != 0 and AryTSurveyExc1i_jk[0] < TInterpStationFti_jk_x < \
                        AryTSurveyExc1i_jk[-1]:  # Begins conditional statement. Checks inequality and relation. Checks
                    # if interpolation point is within exception bounds.
                    try:  # Begins try-except statement. Checks object existence. Compiles exception point indices for
                        # exception handling.
                        AryTElevChangeExcIndicesi_jk = np.append(AryTElevChangeExcIndicesi_jk,
                                                                 np.where(AryTInterpStationsFti_jk ==
                                                                          TInterpStationFti_jk_x)[0])  # Redefines
                        # array. Appends to array if it exists. Compiles exception point indices avoiding overwrite.
                    except NameError:  # Continues try-except statement. Checks object existence. Compiles exception
                        # point indices for exception handling.
                        AryTElevChangeExcIndicesi_jk = np.where(AryTInterpStationsFti_jk == TInterpStationFti_jk_x)[0]
                        # Defines array. Creates array of indices where condition satisfied. Compiles exception point
                        # indices avoiding overwrite.
                else:  # Continues conditional statement. Checks equality and relation. Checks if interpolation point
                    # is within exception bounds.
                    TInterpElevationFti_j_x = AryTInterpElevationsFti_j[x]  # Defines variable. Selects elevation at
                    # interpolation point.
                    TInterpElevationFti_k_x = AryTInterpElevationsFti_k[x]  # Defines variable. Selects elevation at
                    # interpolation point.

                    # Calculate interpolation point elevation change ---------------------------------------------------

                    TElevChangeFti_jk_x = TInterpElevationFti_k_x - TInterpElevationFti_j_x  # Defines variable.
                    # Subtracts elevations.

                    # Compile calculations -----------------------------------------------------------------------------

                    try:  # Begins try-except statement. Checks object existence. Compiles interpolation point
                        # calculations for mean calculation.
                        AryTElevChangeFti_jk = np.append(AryTElevChangeFti_jk, np.array([TElevChangeFti_jk_x],
                                                                                        dtype=float))  # Redefines
                        # array. Appends to array if it exists. Compiles calculations avoiding overwrite.
                    except NameError:  # Continues try-except statement. Checks object existence. Compiles
                        # interpolation point calculations for mean calculation.
                        AryTElevChangeFti_jk = np.array([TElevChangeFti_jk_x], dtype=float)  # Defines array. Creates
                        # empty array.

            # Handle exceptions ----------------------------------------------------------------------------------------

            # Exclude negative results: 1855–Any year ------------------------------------------------------------------

            if TProfileYeari_j == 1855:  # Begins conditional statement. Checks equality. Removes negative values from
                # array.
                AryTElevChangeFti_jk[AryTElevChangeFti_jk < 0] = -100  # Redefines array. Replaces all negative elements
                # with -100.

                AryTElevChangeFti_jk = np.delete(AryTElevChangeFti_jk, np.where(AryTElevChangeFti_jk == -100)[0])
                # Redefines array. Deletes all elements equal to -100.

            # Exclude negative or channel crossing results: 1939 extrapolated-1965 -------------------------------------

            elif TProfileYeari_j == 1939:  # Continues conditional statement. Checks equality. Removes results from
                # array.
                if TID == 'SF-16' or TID == 'SF-17' or TID == 'SF-23':  # Begins conditional statement. Checks
                    # equalities. Removes negative values from array for specific transects.
                    AryTElevChangeFti_jk[AryTElevChangeFti_jk < 0] = -100  # Redefines array. Replaces all negative
                    # elements with -100.

                    AryTElevChangeFti_jk = np.delete(AryTElevChangeFti_jk, np.where(AryTElevChangeFti_jk == -100)[0])
                    # Redefines array. Deletes all elements equal to -100.

                elif TProfileTypei_j == 'Extrapolated' and TProfileYeari_k == 1965:  # Begins conditional statement.
                    # Checks equalities. Removes negative values or values calculated where 1939 extrapolated data is
                    # effectively discontinuous.
                    if len(AryTSurveyExc2_1i_jk) != 0:  # Begins conditional statement. Checks equality. Enacts
                        # exception 1.
                        if TID == 'MF-26B':  # Begins conditional statement. Checks equality. Modifies exception for
                            # specific transect.
                            AryTSurveyExcIndicesi_jk = np.where(
                                np.logical_and(AryTElevChangeFti_jk < 0,
                                               np.logical_and(AryTInterpStationsFti_jk > AryTSurveyExc2_1i_jk[0],
                                                              AryTInterpStationsFti_jk < 156.5)))  # Defines array.
                            # Creates array of indices where condition satisfied. Creates array of exception point
                            # indices.
                        elif TID == 'DC-7':  # Continues conditional statement. Checks equality. Modifies exception for
                            # specific transect.
                            AryTSurveyExcIndicesi_jk = np.where(
                                np.logical_and(AryTElevChangeFti_jk < 0,
                                               np.logical_and(AryTInterpStationsFti_jk > 345.1,
                                                              AryTInterpStationsFti_jk < AryTSurveyExc2_1i_jk[-1])))
                            # Defines array. Creates array of indices where condition satisfied. Creates array of
                            # exception point indices.
                        else:  # Continues conditional statement. Checks equality. Enacts standard exception.
                            AryTSurveyExcIndicesi_jk = np.where(
                                np.logical_and(AryTElevChangeFti_jk < 0,
                                               np.logical_and(AryTInterpStationsFti_jk > AryTSurveyExc2_1i_jk[0],
                                                              AryTInterpStationsFti_jk < AryTSurveyExc2_1i_jk[-1])))
                            # Defines array. Creates array of indices where condition satisfied. Creates array of
                            # exception point indices.

                        AryTElevChangeFti_jk = np.delete(AryTElevChangeFti_jk, AryTSurveyExcIndicesi_jk)  # Redefines
                        # array. Deletes all elements with exception point indices.
                        AryTInterpStationsFti_jk = np.delete(AryTInterpStationsFti_jk, AryTSurveyExcIndicesi_jk)
                        # Redefines array. Deletes all elements with exception point indices.

                        del AryTSurveyExcIndicesi_jk  # Delete command. Deletes objects.
                    if len(AryTSurveyExc2_2i_jk) != 0:  # Begins conditional statement. Checks equality. Enacts
                        # exception 2.
                        AryTSurveyExcIndicesi_jk = np.where(
                            np.logical_and(AryTElevChangeFti_jk < 0,
                                           np.logical_and(AryTInterpStationsFti_jk > AryTSurveyExc2_2i_jk[0],
                                                          AryTInterpStationsFti_jk < AryTSurveyExc2_2i_jk[-1])))
                        # Defines array. Creates array of indices where condition satisfied. Creates array of exception
                        # point indices.

                        AryTElevChangeFti_jk = np.delete(AryTElevChangeFti_jk, AryTSurveyExcIndicesi_jk)  # Redefines
                        # array. Deletes all elements with exception point indices.

                        del AryTSurveyExcIndicesi_jk  # Delete command. Deletes objects.
            else:  # Continues conditional statement. Checks inequality.
                pass  # Pass command. Moves on to next line.

            # Calculate mean transect sedimentation rate ---------------------------------------------------------------

            TMeanElevChangeFti_jk = np.mean(AryTElevChangeFti_jk)  # Defines value. Calculates mean of array.

            TMeanElevChangeCmi_jk = TMeanElevChangeFti_jk * FtToCm  # Defines value. Converts value from feet to cm.

            TMeanElevChangeRatesCmYi_jk = TMeanElevChangeCmi_jk / (TProfileYeari_k - TProfileYeari_j)  # Defines value.
            # Calculates rate.

            # EXPORT RESULTS -------------------------------------------------------------------------------------------

            # Compile calculations -------------------------------------------------------------------------------------

            dfTMeanElevChangesi_jk = pd.DataFrame(
                np.array([[TID, TProfileYeari_j, TProfileYeari_k, TMeanElevChangeFti_jk, TMeanElevChangeCmi_jk,
                           TMeanElevChangeRatesCmYi_jk]]))  # Defines DataFrame. Creates new DataFrame to save results.

            try:  # Begins try-except statement. Checks object existence. Compiles mean calculations.
                dfTMeanElevChangesAll = pd.concat([dfTMeanElevChangesAll, dfTMeanElevChangesi_jk], axis=0)  # Redefines
                # DataFrame. Concatenates DataFrames if it exists. Compiles calculations avoiding overwrite.
            except NameError:  # Continues try-except statement. Checks object existence. Compiles mean calculations.
                dfTMeanElevChangesAll = dfTMeanElevChangesi_jk  # Defines DataFrame. Creates new DataFrame avoiding
                # overwrite.

            del AryTElevChangeFti_jk, TMeanElevChangeFti_jk, TMeanElevChangeCmi_jk, TMeanElevChangeRatesCmYi_jk, \
                dfTMeanElevChangesi_jk  # Deletes objects. For manual overwrite.

DataFrameColumns = ['TId24', 'PYr1', 'PYr2', '1_2Ft', '1_2Cm', '1_2CmY']  # Defines list. Sets DataFrame column labels.

dfTMeanElevChangesAll.columns = DataFrameColumns  # Redefines DataFrame. Sets column labels.

# Export
dfTMeanElevChangesAll.to_csv(OutputFolder + '/' + CalculationFolder + OutputFile1, header=True, index=False)  # Exports
# DataFrame to .csv.

# ======================================================================================================================
# SIGNAL END -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'SEDIMENTATION RATES CALCULATED!!!' + '\033[0m', dfTMeanElevChangesAll, '\n...\n')  # Displays
# objects.
