# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS
# TRANSECT DATA COORDINATE GEOMETRY DIGITIZER * -------------------------------

print('\n\033[1m' + 'START TRANSECT DATA DIGITIZATION!!!' + '\033[0m', 
      '\n...\n')  # Displays objects  to signal run.

# INITIALIZATION ==============================================================

# IMPORT MODULES. -------------------------------------------------------------

from transect_analysis_functions import *   # Imports all functions from 
# associated program.

# DEFINE INPUT PARAMETERS. ----------------------------------------------------

# Define directory folders.
INPUT_FOLDER = 'Input'  # Input where all input data will be stored.
OUTPUT_FOLDER = 'Output'  # Output where all output data products will be
# stored.
GIS_FOLDER = 'GIS'  # Output where all geospatial data products will be stored.

# Define data files.
INPUT_FILE1 = INPUT_FOLDER \
    + '/WRV_MN_1855_1994_sedimentation_elevations.csv'  # Data to be digitized.
INPUT_FILE2 = INPUT_FOLDER \
    + '/WRV_MN_2008_2014_sedimentation_coordinates.csv'  # Reference
# coordinates.
INPUT_FILE3 = INPUT_FOLDER \
    + '/WRV_MN_1939_2014_sedimentation_monuments.csv'  # Reference coordinate
#metadata.

GPKG_NAME = '/WRV_MN_1855_1994_sedimentation.gpkg'  # Output GeoPackage
# name.

LAYER_NAME1_PRE = 'WRV_MN_'  # Output layer name prefix.
LAYER_NAME1_SUF = '_elevations'  # Output layer name suffix.

LAYER_NAME2 = 'WRV_MN_2008_2014_monuments'  # Output layer name.

# Define operation parameters.
TRANSECT_NUM_START = 1  # Start transect number for operation loop.
TRANSECT_NUM_END = 107  # End transect number for operation loop.

TRANSECT_NUMS = create_forward_range(
    TRANSECT_NUM_START, TRANSECT_NUM_END, 1, 0)  # Calls UDF to define array of
# transect numbers for looping digitization.

FT_TO_M = 3.281  # Conversion factor from feet to meters.

CRS = 'EPSG:26915'  # Projected coordinate reference system EPSG code for
# output GIS files.

# SET UP DIRECTORY. -----------------------------------------------------------

# Create output folders.
create_folder(OUTPUT_FOLDER)  # Calls UDF.
create_folder(OUTPUT_FOLDER + '/' + GIS_FOLDER)

# UPLOAD FILE(S). -------------------------------------------------------------

# Define DataFrames from input data.
df_transect_elevs = convert_CSV_to_dataframe(INPUT_FILE1, 0)  # Calls UDF.
df_monument_coords = convert_CSV_to_dataframe(INPUT_FILE2, 0)
df_monument_meta = convert_CSV_to_dataframe(INPUT_FILE3, 1)

# DATA OPERATIONS =============================================================

# SELECT DATA. ----------------------------------------------------------------

# Select transect data.
for i in TRANSECT_NUMS:  # Begins loop through transects to calculate their
    # coordinate geometry.
    df_transect_elevs_i = slice_dataframe_rows(
            'Equals', df_transect_elevs, 'TNum', i, 0)  # Calls UDF to slice
    # DataFrame and define resultant DataFrame of single transect data.

    # Select marker data.
    df_monument_coords_i = slice_dataframe_rows(
            'Equals', df_monument_coords, 'TNum', i, 0)  # Slices DataFrame and
    # defines resultant DataFrame of single transect monument coordinate data.

    if df_monument_coords_i.shape[0] != 0:  # Begins conditional statement to
        # skip transects without reference coordinates.
        #
        # Define marker coordinates.
        monument1_east_i = slice_dataframe_cell(
                'Float', df_monument_coords_i, 0, 'EastingM', 0)  # Calls UDF
        # to slice DataFrame and define resultant value as Easting coordinate
        # of start monument of present transect.
        monument1_north_i = slice_dataframe_cell(
                'Float', df_monument_coords_i, 0, 'NorthingM', 0)
        # Northing coordinate of start monument of present transect.
        monument2_east_i = slice_dataframe_cell(
                'Float', df_monument_coords_i, 1, 'EastingM', 0)
        # Easting coordinate of end monument of present transect.
        monument2_north_i = slice_dataframe_cell(
                'Float', df_monument_coords_i, 1, 'NorthingM', 0)
        # Northing coordinate of end monument of present transect.

        # Retrieve marker (meta)data.
        df_monument_meta_i = slice_dataframe_rows(
                'Equals', df_monument_meta, 'TNum', i, 0)  # Slice DataFrame
        # and define resultant DataFrame of single transect monument metadata.
        df_monument_meta08_14_i = slice_dataframe_rows(
                'Equals', df_monument_meta_i, 'SrvEra', '2008–2014', 0)
        # Single transect monument metadata from the 2009–2014 survey.

        monument_stat_i = slice_dataframe_cell(
                'Float', df_monument_meta08_14_i, 0, 'MTopSttnFt', 0)
        # Transect station of start monument

        # Check if marker is off transect.
        #
        # Retrieve monument off transect condition.
        monument1_off_i = slice_dataframe_cell(
                'Float', df_monument_meta08_14_i, 0, 'MOffT', 0)
        # Start monument off of transect condition.
        monument2_off_i = slice_dataframe_cell(
                'Float', df_monument_meta08_14_i, 1, 'MOffT', 0)
        # End monument off of transect condition.

        # Check off transect condition and shift reference coordinate to the
        # transect where applicable. 
        if monument1_off_i != 0:  # Begins conditional statement to check
            # start monument off transect condition.
            monument1_east_i, monument1_north_i = move_reference_coordinates(
                    monument1_east_i, monument1_north_i, 
                    df_monument_meta08_14_i, df_monument_coords_i, 0,
                    'MOffTDisFt', 'MOffTDir', 'GXYAccM', FT_TO_M, 0)
            # Calls UDF to redefine objects by shifting reference coordinate
            # position.
        if monument2_off_i != 0:  # Check end monument off transect condition.
            monument2_east_i, monument2_north_i = move_reference_coordinates(
                    monument2_east_i, monument2_north_i, 
                    df_monument_meta08_14_i, df_monument_coords_i, 1,
                    'MOffTDisFt', 'MOffTDir', 'GXYAccM', FT_TO_M, 0)

        # Select survey data.
        transect_surv_nums = slice_dataframe_column(
                'Array', 'Integer', df_transect_elevs_i, 'ESrvNum', 1, 0, 0)
        # Calls UDF to slice DataFrame and define resultant array as survey
        # numbers associated with present transect.

        for j in transect_surv_nums:  # Begins loop through transect surveys to
            # calculate their coordinate geometry
            df_transect_elevs_i_j = slice_dataframe_rows(
                    'Equals', df_transect_elevs_i, 'ESrvNum', j, 0)
            # Single transect single survey data.

            # Select measurement stations.
            df_stations_i_j = slice_dataframe_column(
                    'DataFrame', 'Float', df_transect_elevs_i_j, 'ESttnFt', 0, 
                    0, 0)  # Transect survey stations.

            # Select transect and survey metadata.
            transect_ID = slice_dataframe_cell(
                    'String', df_transect_elevs_i_j, 0, 'TId24', 0)
            # Transect ID.
            transect_p_year = slice_dataframe_cell(
                    'String', df_transect_elevs_i_j, 0, 'PYr', 0)
            # Transect survey profile year.

            print('\033[1mDIGITIZING:\033[0m', transect_ID, ':', 
                  transect_p_year, '\n')  # Displays objects.

            # CALCULATE STATION COORDINATE GEOMETRY. --------------------------

            # Calculate station distance from marker.
            df_station_dist_i_j = df_stations_i_j - monument_stat_i
            # Defines DataFrame of measurement distance from start marker
            # station.

            # Calculate survey azimuth.
            transect_azi_i = calculate_transect_azimuth(
                    monument1_east_i, monument1_north_i, monument2_east_i, 
                    monument2_north_i, 0)  # Calls UDF to define object for
            # transect azimuth from reference coordinates. 

            # Calculate station distance projections east and north.
            df_station_dist_east_i_j = (df_station_dist_i_j 
                                        * np.cos(transect_azi_i))  
            # Defines DataFrame of measurement distance from start marker
            # station components projected in the East direction.
            df_station_dist_north_i_j = (df_station_dist_i_j 
                                         * np.sin(transect_azi_i))
            # North direction.

            # Calculate station coordinates.
            df_station_east_i_j = ((df_station_dist_east_i_j / FT_TO_M) 
                                   + monument1_east_i)  # Defines DataFrame of
            # Easting coordinate for all measurement stations.
            df_station_north_i_j = ((df_station_dist_north_i_j / FT_TO_M) 
                                    + monument1_north_i)  # Northing coordinate
            # for all measurement stations.

            # Add field names to new DataFrame columns.
            df_station_east_i_j = df_station_east_i_j.rename('EastingM')
            df_station_north_i_j = df_station_north_i_j.rename('NorthingM')

            # Handle exception: DC-7 1994 mid-transect displaced stations.
            if transect_ID == 'DC-7' and j == transect_surv_nums[-1]:
                # Begins conditional statement to check if standard COGO
                # methods need modified.

                # Calculate station displacement azimuth.
                transect_azi_i_j = transect_azi_i - (1/2) * np.pi
                # Defines object for secondary, orthogonal azimuth that
                # stations will be displaced upon from the main transect.

                # Shift marker off transect.
                #
                # Calculate reference distance projections east and north.
                monument1_dist_east_i_j = ((25 / FT_TO_M) 
                                           * np.cos(transect_azi_i_j))
                # Defines object for reference coordinate distance in the East
                # direction to a synthetic transect where displaced
                # measurements are located.

                monument1_dist_north_i_j = ((25 / FT_TO_M) 
                                            * np.sin(transect_azi_i_j))
                # North direction.

                # Calculate reference coordinates.
                monument1_east_i_j = monument1_dist_east_i_j + monument1_east_i
                # Defines object for shifted reference coordinate component.
                monument1_north_i_j = (monument1_dist_north_i_j 
                                       + monument1_north_i)

                # Calculate station coordinates.
                df_station_east_i_j2 = ((df_station_dist_east_i_j / FT_TO_M) 
                                        + monument1_east_i_j)
                # Easting coordinate for all measurement stations.
                df_station_north_i_j2 = ((df_station_dist_north_i_j / FT_TO_M) 
                                         + monument1_north_i_j)
                # Northing coordinate for all measurement stations.
                
                # Update DataFrame.
                #
                # Delete measurement coordinates that were not displaced by the
                # standard method.
                df_station_east_i_j2 = df_station_east_i_j2.iloc[8:16]
                # Easting coordinates.
                df_station_north_i_j2 = df_station_north_i_j2.iloc[8:16]
                # Northing coordinates.

                # Add measurement coordinates that were displaced by the
                # modified method.
                df_station_east_i_j.iloc[8:16] = df_station_east_i_j2
                df_station_north_i_j.iloc[8:16] = df_station_north_i_j2

            # Plot
            # plt.scatter(
            #     [monument1_east_i, monument2_east_i], 
            #     [monument1_north_i, monument2_north_i], c='m', alpha=0.5)
            # Plots monument coordinates.
            # plt.scatter(
            #     df_station_east_i_j, df_station_north_i_j, c='c', alpha=0.1)
            # Plots station coordinates.
            # plt.pause(0.5)  # Shows plot.

            # PREPARE DATA FOR DIGITIZATION. ----------------------------------

            # Compile calculations.
            try:  # Begins try-except statement to select calculation
                # compilation method.
                df_station_east_all = pd.concat(
                        [df_station_east_all, df_station_east_i_j], axis=0)
                # Redefines DataFrame of measurement coordinates through
                # concatenation.
            except NameError:
                df_station_east_all = df_station_east_i_j  # Defines DataFrame
                # of measurement coordinates.
            try:
                df_station_north_all = pd.concat(
                        [df_station_north_all, df_station_north_i_j], axis=0)
            except NameError:
                df_station_north_all = df_station_north_i_j

            # Update input file.
            if i == TRANSECT_NUM_END - 1:  # Begins conditional statement to
                # save coordinates and digitizes when all COGO calculations
                # have been completed.
                if j == transect_surv_nums[-1]:
                    df_transect_elevs = pd.concat(
                            [df_transect_elevs, df_station_east_all, 
                             df_station_north_all], axis=1)
                    # Redefines DataFrame through concatenation.

                    # DIGITIZE DATA. ------------------------------------------
                    
                    transect_p_years = slice_dataframe_column(
                            'Array', 'Integer', df_transect_elevs, 'PYr', 1, 0, 
                            0)  # Survey years of complete entire.

                    # Digitize transect data.
                    for k in transect_p_years:  # Begins loop through surface
                        # profile years tod digitize transect data by surface
                        # profile year in sequence.
                        df_transect_elevs_k = slice_dataframe_rows(
                                'Equals', df_transect_elevs, 'PYr', k, 0)
                        # Single profile year data.

                        gdf_transect_elevs_k = gpd.GeoDataFrame(
                                df_transect_elevs_k, 
                                geometry=gpd.points_from_xy(
                                        df_transect_elevs_k.EastingM, 
                                        df_transect_elevs_k.NorthingM), 
                                crs=CRS)  # Defines GeoDataFrame from DataFrame
                        # with specified coordinate reference system.

                        layer_name_k = LAYER_NAME1_PRE + str(k) + LAYER_NAME1_SUF
                        # Defines object for name of layer for export.

                        gdf_transect_elevs_k.to_file(OUTPUT_FOLDER + '/' 
                                                     + GIS_FOLDER + 
                                                     GPKG_NAME, 
                                                     layer=layer_name_k, 
                                                     driver='GPKG', 
                                                     index=True)
                        # Saves file to directory.
else:
    print('\n\033[1m' + 'TRANSECT DATA DIGITIZATION COMPLETE!!!' + '\033[0m', 
          '\n...\n')  # Signals end.
