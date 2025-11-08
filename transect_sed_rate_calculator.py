# STREAM AND VALLEY SEDIMENTATION SURVEY TRANSECT DATA ANALYSIS * -------------
# WHITEWATER RIVER VALLEY, MN, US * -------------------------------------------
# TRANSECT DATA ELEVATION CHANGE RATE CALCULATOR * ----------------------------

print('\n\033[1m' + 'START TRANSECT ELEVATION CHANGE RATE CALCULATIONS!!!' 
      + '\033[0m', '\n...\n')  # Displays objects to signal run.

# INITIALIZATION ==============================================================

# IMPORT MODULES. -------------------------------------------------------------

from transect_analysis_functions import *   # Imports all functions from 
# associated program.

# DEFINE INPUT PARAMETERS. ----------------------------------------------------

# Define directory folders.
INPUT_FOLDER = 'Input'  # Input where all input data will be stored.
OUTPUT_FOLDER = 'Output'  # Output where all output data products will be
# stored.
CALC_FOLDER = 'Calculations'  # Output where all calculation results will be
# stored.

# Define data files.
INPUT_FILE1 = INPUT_FOLDER + '/WRV_MN_1855_2014_sedimentation_elevations.csv'
# Data referenced for calculations.
INPUT_FILE2 = INPUT_FOLDER + '/WRV_MN_1955_1994_sedimentation_exceptions.csv'
# Data exceptions to be excluded from calculations.
CALC_NAME = '/WRV_MN_1855_1994_sedimentation_rates.csv'  # Output file name.

DATAFRAME_COLUMNS = ['TId24', 'PYr1', 'PYr2', '1_2Ft', '1_2Cm', '1_2CmY']
# Output file column labels.

# Define operation parameters.
TRANSECT_NUM_START = 1  # Start transect number for operation loop.
TRANSECT_NUM_END = 107  # End transect number for operation loop.

TRANSECT_NUMS = create_forward_range(
        TRANSECT_NUM_START, TRANSECT_NUM_END, 1, 0)  # Calls UDF to define
# array of transect numbers for looping calculation.

FT_TO_CM = 12 * 2.54  # Conversion factor from feet to centimeters.

INTERP_INTERVAL = 0.1  # Interpolation interval in feet.

# SET UP DIRECTORY. -----------------------------------------------------------

# Create output folders.
create_folder(OUTPUT_FOLDER)  # Calls UDF.
create_folder(OUTPUT_FOLDER + '/' + CALC_FOLDER)

# UPLOAD FILE(S). -------------------------------------------------------------

# Define DataFrames from input data.
df_transect_elevs = convert_CSV_to_dataframe(INPUT_FILE1, 0)  # Calls UDF.
df_calc_exceptions = convert_CSV_to_dataframe(INPUT_FILE2, 0)
  
# DATA OPERATIONS =============================================================

# SELECT DATA. ----------------------------------------------------------------

# Select transect data.
for i in TRANSECT_NUMS:  # Begins loop through transects to calculate
    # elevation change rates.
    df_transect_elevs_i = slice_dataframe_rows(
            'Equals', df_transect_elevs, 'TNum', i, 0)  # Calls UDF to slice
    # DataFrame and define resultant DataFrame of single transect data.

    # Select survey pair data.
    transect_surv_nums = slice_dataframe_column(
            'Array', 'Integer', df_transect_elevs_i, 'ESrvNum', 1, 0, 0)
    # Calls UDF to slice DataFrame and define resultant array as survey
    # numbers associated with present transect.

    for j in transect_surv_nums:  # Begins loop through transect survey pairs
        # to calculate elevation change rates between.
        if j < transect_surv_nums[-1]:  # Begins conditional statement to omit
            # selection of the most recent survey as it has no later data to
            # compare to.
            k = j + 1  # Sets survey number of next earliest survey to enable
              # its selection for calculation.
            
            df_transect_elevs_i_j = slice_dataframe_rows(
                    'Equals', df_transect_elevs_i, 'ESrvNum', j, 0)
            # Earlier survey.
            df_transect_elevs_i_k = slice_dataframe_rows(
                    'Equals', df_transect_elevs_i, 'ESrvNum', k, 0)
            # Later survey.

            # Select transect and survey metadata.
            transect_ID = slice_dataframe_cell(
                    'String', df_transect_elevs_i, 0, 'TId24', 0)  # Calls UDF
            # to slice DataFrame and define resultant value as transect ID of
            # present transect.
            
            transect_p_year_i_j = slice_dataframe_cell(
                    'Integer', df_transect_elevs_i_j, 0, 'PYr', 0)
            # Earlier survey profile year.
            transect_p_type_i_j = slice_dataframe_cell(
                    'String', df_transect_elevs_i_j, 0, 'PSource', 0)
            # Earlier survey profile type.
            transect_p_year_i_k = slice_dataframe_cell(
                    'Integer', df_transect_elevs_i_k, 0, 'PYr', 0)
            # Later survey profile year.
            transect_p_type_i_k = slice_dataframe_cell(
                    'String', df_transect_elevs_i_k, 0, 'PSource', 0)
            # Later survey profile type.

            print('\033[1mCALCULATING:\033[0m', transect_ID, ': ' 
                  + str(transect_p_year_i_j) + ' (' + str(transect_p_type_i_j) 
                  + ') – ' + str(transect_p_year_i_k) + ' (' 
                  + str(transect_p_type_i_k) + ') \n')

            # Select survey measurement stations.
            stations_i_j = slice_dataframe_column(
                    'Array', 'Float', df_transect_elevs_i_j, 'ESttnFt', 0, 0, 
                    0)
            stations_i_k = slice_dataframe_column(
                    'Array', 'Float', df_transect_elevs_i_k, 'ESttnFt', 0, 0, 
                    0)

            # Select survey elevations.
            elevs_i_j = slice_dataframe_column(
                    'Array', 'Float', df_transect_elevs_i_j, 'E1Ft', 0, 0, 0)
            elevs_i_k = slice_dataframe_column(
                    'Array', 'Float', df_transect_elevs_i_k, 'E1Ft', 0, 0, 0)

            # INTERPOLATE DATA. -----------------------------------------------

            # Establish interpolation range. ----------------------------------
            
            # Select survey station limits.
            station_start_i_j = np.min(stations_i_j)
            station_end_i_j = np.max(stations_i_j)
            station_start_i_k = np.min(stations_i_k)
            station_end_i_k = np.max(stations_i_k)

            station_starts_i_jk = np.array(
                    [station_start_i_j, station_start_i_k])
            station_ends_i_jk = np.array(
                    [station_end_i_j, station_end_i_k])
            
            # Select min and max shared stations.
            interp_station_start_i_jk = np.max(station_starts_i_jk)
            interp_station_end_i_jk = np.min(station_ends_i_jk)

            interp_stations_i_jk = np.arange(
                    interp_station_start_i_jk, 
                    interp_station_end_i_jk + INTERP_INTERVAL, INTERP_INTERVAL)
            # Define interpolation range.

            interp_stations_i_jk = np.around(interp_stations_i_jk, decimals=1)
            # Rounds values to tenths place.

            # Interpolate data. -----------------------------------------------

            interp_elevs_i_j = np.interp(
                    interp_stations_i_jk, stations_i_j, elevs_i_j)
            interp_elevs_i_k = np.interp(
                    interp_stations_i_jk, stations_i_k, elevs_i_k)

            # Plot
            # plt.plot(
            #        interp_stations_i_jk, interp_elevs_i_j, c='Magenta', 
            #        marker='o', alpha=0.9)  # Plots interpolated survey data. 
            # plt.plot(stations_i_j, elevs_i_j, c='Cyan', marker='o', alpha=0.9)
            # # Plots field survey data.
            # plt.plot(
            #        interp_stations_i_jk, interp_elevs_i_k, c='Green', 
            #        marker='o', alpha=0.9)
            # plt.plot(stations_i_k, elevs_i_k, c='Yellow', marker='o', alpha=0.9)
            # plt.show()  # Shows plot.

            # CALCULATE ELEVATION CHANGE RATES. -------------------------------

            # Check data for calculation exclusion zones/exceptions. ----------

            transect_exc_check_i = slice_dataframe_rows(
                    'Equals', df_calc_exceptions, 'TId24', transect_ID, 0)
            # Transect calculation exceptions.

            # Select measurement station limits of calculation exclusion 
            # zones for individual surveys.

            exc_station_start_i_j, exc_station_end_i_j, exc_pair_year_i_j = \
                 calculation_exclusion_checker(
                         transect_exc_check_i, 'PYr', 'ESttn1Ft', 'ESttn2Ft', 
                         'ExcPrYr', 0, transect_p_year_i_j, 0)  # Calls UDF.
            exc_station_start_i_k, exc_station_end_i_k, exc_pair_year_i_k = \
                calculation_exclusion_checker(
                        transect_exc_check_i, 'PYr', 'ESttn1Ft', 'ESttn2Ft', 
                        'ExcPrYr', 0, transect_p_year_i_k, 0)

            # Handle exception: 1939–1965 survey pair exclusion zones.
            if (transect_p_year_i_k == 1939 
                    and transect_p_type_i_k == 'Borings' 
                    and exc_pair_year_i_k == '1965'):
                # Reset station limits of calculation exclusion zone for
                # 1939–1965 survey pair to NaN to ignore it when 1939 data is
                # not paired with 1965.
                exc_station_start_i_k = np.nan
                exc_station_end_i_k = np.nan

            # Establish station limits for shared calculation exclusion zone.
            exc_stations1_i_jk = np.array(
                    [exc_station_start_i_j, exc_station_end_i_j, 
                     exc_station_start_i_k, exc_station_end_i_k])
            # Compiles both surveys' exclusion zone station limits.

            exc_stations1_i_jk = np.delete(exc_stations1_i_jk, 
                                           np.isnan(exc_stations1_i_jk))
            # Deletes NaN values to ignore NaN stations from surveys without
            # calculation exclusion zones.
            
            exc_stations1_i_jk = np.around(exc_stations1_i_jk, decimals=1)
            # Rounds values to tenths place so calculation exclusion zone is
            # recognized among interpolated stations.

            # Handle exception: 1939–1965 survey pair exclusion zones. --------
            
            # Establish exclusion zone arrays solely for 1939–1965 survey pair
            # exception handling.
            #
            # Initially establish arrays as empty to populate when operating on
            # 1939–1965 survey pair.
            exc_stations2_1_i_jk = np.empty(0)  # Primary exclusion zone.
            exc_stations2_2_i_jk = np.empty(0)  # Secondary exclusion zone.

            # Establish station limits for shared calculation exclusion zone.
            if (transect_p_year_i_j == 1939 
                    and transect_p_type_i_j == 'Borings' 
                    and transect_p_year_i_k == 1965):
                exc_stations2_1_i_jk = np.array([exc_station_start_i_j, 
                                                 exc_station_end_i_j])
              
                exc_stations2_1_i_jk = np.delete(
                        exc_stations2_1_i_jk, np.isnan(exc_stations2_1_i_jk))
                
                exc_stations2_1_i_jk = np.around(exc_stations2_1_i_jk, 
                                                 decimals=1)
  
                # Check data for second calculation exclusion zones/exceptions.
                transect_exc_check_i_j = slice_dataframe_rows(
                        'Equals', transect_exc_check_i, 'PYr', 1939, 0)

                if any(transect_exc_check_i_j.duplicated('PYr')):
                    exc_station_start2_i_j, exc_station_end2_i_j, \
                         exc_pair_year2_i_j = calculation_exclusion_checker(
                                 transect_exc_check_i, 'PYr', 'ESttnFt1', 
                                 'ESttnFt2', 'ExcPrYr', 1, transect_p_year_i_j, 0)

                    # Establish station limits for shared calculation exclusion
                    # zone.
                    exc_stations2_2_i_jk = np.array([exc_station_start2_i_j, 
                                                     exc_station_end2_i_j])
                    
                    exc_stations2_2_i_jk = np.delete(
                            exc_stations2_2_i_jk, np.isnan(exc_stations2_2_i_jk))
                    
                    exc_stations2_2_i_jk = np.around(exc_stations2_2_i_jk, 
                                                     decimals=1)

            if (transect_p_year_i_j == 1939 
                    and transect_p_type_i_j == 'Borings' 
                    and transect_p_year_i_k == 1965):
                exc_stations1_i_jk = np.empty(0)  # Redefines exclusion zone
                # array as empty so that 1939–1965 survey pair operations only
                # reference the 1939–1965 specific arrays.

            # Select interpolation point pairs for calculation. ---------------

            interp_indices = np.arange(0, len(interp_stations_i_jk), 1)
            # Defines array of indices for looping survey pair calculation.

            for x in interp_indices:  # Begins loop through interpolation point
                # indices to calculates elevation change rates per point.
                interp_station_i_jk_x = interp_stations_i_jk[x]
                # Interpolation point station.

                # Check if interpolation point is within calculation exclusion
                # zone limits. ------------------------------------------------

                # Exception 1: Skip interpolation point calculation if point is
                # within limits of calculation exclusion zone.
                if (len(exc_stations1_i_jk) != 0 
                        and exc_stations1_i_jk[0] < interp_station_i_jk_x 
                        < exc_stations1_i_jk[-1]):
                    pass  # Moves on to next line.
                    # try:  # Begins try-except statement to compile exception
                    #     # point indices for exception handling.
                    #     exc_interp_indices_i_jk = np.append(
                    #             exc_interp_indices_i_jk, 
                    #             np.where(interp_stations_i_jk == 
                    #                      interp_station_i_jk_x)[0])  # Redefines
                    #     # array of exception point indices via append.
                    # except NameError:
                    #     exc_interp_indices_i_jk = np.where(
                    #             interp_stations_i_jk == interp_station_i_jk_x)[0]
                    #     # Defines array of exception point indices.
                else:
                    # Select survey elevations at interpolation point.
                    interp_elevs_i_j_x = interp_elevs_i_j[x]
                    interp_elevs_i_k_x = interp_elevs_i_k[x]

                    # Calculate interpolation point elevation change between
                    # surveys. ------------------------------------------------

                    elev_change_i_jk_x = (interp_elevs_i_k_x 
                                          - interp_elevs_i_j_x)
                    # Calculates elevation change.

                    # Compile preliminary calculations. -----------------------

                    try:
                        elev_change_i_jk = np.append(
                                elev_change_i_jk, np.array(
                                        [elev_change_i_jk_x], 
                                        dtype=float))
                    except NameError:
                        elev_change_i_jk = np.array([elev_change_i_jk_x], 
                                                    dtype=float)

            # Handle special calculation exceptions. --------------------------

            # Exception 2: Exclude negative results for all 1855–Any year
            # survey pairs. ---------------------------------------------------

            if transect_p_year_i_j == 1855:
                elev_change_i_jk[elev_change_i_jk < 0] = -100  # Replaces all
                # negative elements with -100.

                elev_change_i_jk = np.delete(
                        elev_change_i_jk, 
                        np.where(elev_change_i_jk == -100)[0])
                # Deletes all elements equal to -100.

            # Exception 3: Exclude negative results for 1939–1965 survey pairs
            # for SF-16, -17, & -23. ------------------------------------------

            elif transect_p_year_i_j == 1939:
                if (transect_ID == 'SF-16' or transect_ID == 'SF-17' 
                        or transect_ID == 'SF-23'):
                    elev_change_i_jk[elev_change_i_jk < 0] = -100

                    elev_change_i_jk = np.delete(
                            elev_change_i_jk, 
                            np.where(elev_change_i_jk == -100)[0])
            
                # Exception 4: Exclude channel crossing results from 
                # 1939 (borings)–1965 survey pairs. ---------------------------
            
                # Select exclusion point indices.
                elif (transect_p_type_i_j == 'Borings' 
                      and transect_p_year_i_k == 1965):
                    if len(exc_stations2_1_i_jk) != 0:  # Checks if array is
                        # non-empty to enact exception.
                        if transect_ID == 'MF-26B':
                            exc_indices_i_jk = np.where(
                                    np.logical_and(
                                        elev_change_i_jk < 0, 
                                        np.logical_and(
                                            interp_stations_i_jk 
                                            > exc_stations2_1_i_jk[0], 
                                            interp_stations_i_jk < 156.5)))
                        elif transect_ID == 'DC-7':
                            exc_indices_i_jk = np.where(
                                    np.logical_and(
                                        elev_change_i_jk < 0, 
                                        np.logical_and(
                                            interp_stations_i_jk > 345.1, 
                                            interp_stations_i_jk 
                                            < exc_stations2_1_i_jk[-1])))
                        else:
                            exc_indices_i_jk = np.where(
                                    np.logical_and(
                                        elev_change_i_jk < 0, 
                                        np.logical_and(
                                            interp_stations_i_jk 
                                            > exc_stations2_1_i_jk[0], 
                                            interp_stations_i_jk 
                                            < exc_stations2_1_i_jk[-1])))

                        # Delete exclusion points from calculations.
                        elev_change_i_jk = np.delete(elev_change_i_jk, 
                                                     exc_indices_i_jk)
                        interp_stations_i_jk = np.delete(interp_stations_i_jk, 
                                                         exc_indices_i_jk)
                 
                        del exc_indices_i_jk  # Delete objects.
                               
                    if len(exc_stations2_2_i_jk) != 0:
                        exc_indices_i_jk = np.where(
                                np.logical_and(
                                    elev_change_i_jk < 0, 
                                    np.logical_and(
                                        interp_stations_i_jk 
                                        > exc_stations2_2_i_jk[0], 
                                        interp_stations_i_jk 
                                        < exc_stations2_2_i_jk[-1])))
                        
                        # Delete exclusion points from calculations.
                        elev_change_i_jk = np.delete(elev_change_i_jk, 
                                                     exc_indices_i_jk)

                        del exc_indices_i_jk
            else:
                pass

            # Calculate mean transect elevation change rate. ---------------------

            mean_elev_change_i_jk = np.mean(elev_change_i_jk) * FT_TO_CM
            # Calculates mean elevation change.

            mean_elev_change_rate_i_jk = (mean_elev_change_i_jk / 
                                          (transect_p_year_i_k 
                                           - transect_p_year_i_j))
            # Calculates mean elevation change rate.

            # EXPORT RESULTS. --------------------------------------------------
 
            # Compile final calculations. -------------------------------------

            df_mean_elev_change_i_jk = pd.DataFrame(
                    np.array(
                        [[transect_ID, transect_p_year_i_j, 
                          transect_p_year_i_k, mean_elev_change_i_jk, 
                          mean_elev_change_i_jk, mean_elev_change_rate_i_jk]]))
            # Creates new DataFrame to save results.

            try:
                df_mean_elev_change_all = pd.concat(
                        [df_mean_elev_change_all, df_mean_elev_change_i_jk], 
                        axis=0)
            except NameError:
                df_mean_elev_change_all = df_mean_elev_change_i_jk

            del elev_change_i_jk, mean_elev_change_i_jk, mean_elev_change_rate_i_jk, \
                df_mean_elev_change_i_jk

df_mean_elev_change_all.columns = DATAFRAME_COLUMNS  # Sets column labels.

# Export data.
df_mean_elev_change_all.to_csv(
        OUTPUT_FOLDER + '/' + CALC_FOLDER + CALC_NAME, header=True, 
        index=False)

print('\n\033[1m' + 'ELEVATION CHANGE RATES CALCULATED!!!' + '\033[0m', 
      df_mean_elev_change_all, '\n...\n')  # Signals end.
