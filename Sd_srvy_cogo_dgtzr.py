# ======================================================================================================================
# WHITEWATER RIVER VALLEY SEDIMENTATION SURVEYS * ----------------------------------------------------------------------
# SURVEY DATA COORDINATE GEOMETRY DIGITIZER * --------------------------------------------------------------------------
# PYTHON SCRIPTS * -----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION DATA DIGITIZATION!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from Sd_srvy_fnctns import *  # Imports all functions from outside program.

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Directory
inpt_fldr = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.
otpt_fldr = 'Output'  # Defines variable. Sets name of output folder where all data products will be exported.
gis_fldr = 'GIS'  # Defines variable. Sets name of output folder where all geospatial data products will be exported.

# Data
inpt_fl1 = inpt_fldr + '/Survey data new MS.csv'  # Defines variable. Sets file path to input file.
inpt_fl2 = inpt_fldr + '/Monument metadata original.csv'  # Defines variable. Sets file path to input file.

# Limits of analysis
rng_strt = 1  # Defines variable. Sets start survey range number for operation loop.
rng_end = 13  # Defines variable. Sets end survey range number for operation loop.

# Data slicing criteria
crdnt_srvy_yr = 2011  # Defines variable. Sets survey year of field coordinate survey.

# Conversion factors
ft_to_m = 3.281  # Defines variable. Sets conversion factor from feet to meters.

# Geospatial
crdnt_rf_sys = 'EPSG:26915'  # Defines variable. Sets projected coordinate reference system for output shapefiles.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

create_folder(otpt_fldr)  # Creates folder. Calls function. Creates output folder where all data products will be
# exported.
create_folder(otpt_fldr + '/' + gis_fldr)  # Creates folder. Calls function. Creates output folder where all geospatial
# data products will be exported.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

df_srvy_dt = csv_to_DataFrame(inpt_fl1, 0)  # Defines DataFrame. Calls function. Uploads survey data.
df_mnt_dt = csv_to_DataFrame(inpt_fl2, 0)  # Defines DataFrame. Calls function. Uploads monument metadata.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Establish spatial selection framework --------------------------------------------------------------------------------

rng_nmbrs = forward_range(rng_strt, rng_end, 1, 0)  # Defines array. Calls function. Sets loop order by transect.

# Select transect data -------------------------------------------------------------------------------------------------

for i in rng_nmbrs:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates coordinates
    # for each range in sequence.

    df_rng_dt = slice_DataFrame_rows('Equals', df_srvy_dt, 'Range_num', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single range data.

    # Metadata
    df_rng_mtdt = slice_DataFrame_rows('Equals', df_mnt_dt, 'Range_num', str(i), 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single range metadata.

    # Select monument data ---------------------------------------------------------------------------------------------

    df_mnt_crdnts = slice_DataFrame_rows('Equals', df_rng_mtdt, 'Srvy_year', crdnt_srvy_yr, 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield single range monument coordinate data.

    # Coordinates
    mnt1_e = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'Easting', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield Easting coordinate of starting monument of present dataset.
    mnt1_n = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'Northing', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield Northing coordinate of starting monument of present dataset.
    mnt2_e = slice_DataFrame_cell('Float', df_mnt_crdnts, 1, 'Easting', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield Easting coordinate of ending monument of present dataset.
    mnt2_n = slice_DataFrame_cell('Float', df_mnt_crdnts, 1, 'Northing', 0)  # Defines variable. Calls function.
    # Slices DataFrame to yield Northing coordinate of ending monument of present dataset.

    # Reference station
    mnt1_stn = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'BM_off_tp', 0)

    # Select survey data -----------------------------------------------------------------------------------------------

    srvy_nmbrs = slice_DataFrame_columns('Array', 'Integer', df_rng_dt, 'Srvy_num', 1, 0, 0)  # Defines array. Calls
    # function. Slices DataFrame to yield survey numbers of range dataset.

    for j in srvy_nmbrs:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates
        # coordinates for each survey in sequence.
        df_rng_srvy_dt = slice_DataFrame_rows('Equals', df_rng_dt, 'Srvy_num', j, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range single survey data.

        # Metadata
        df_rng_srvy_mtdt = slice_DataFrame_rows('Equals', df_rng_mtdt, 'Srvy_num', j, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range survey metadata.

        retrieve_metadata(df_rng_srvy_mtdt, 1)  # Calls function. Displays and retrieves metadata.

        # Survey stations
        df_stns = slice_DataFrame_columns('DataFrame', 'Float', df_rng_srvy_dt, 'Offset_ft', 0, 0, 0)  # Defines array.
        # Calls function. Slices DataFrame to yield survey stations of survey dataset.

        # CALCULATE STATION COORDINATE GEOMETRY ------------------------------------------------------------------------

        # Station separations down range
        df_dlt_r = df_stns - mnt1_stn  # Defines DataFrame. Calculates station separation between survey points and
        # reference monument.

        # Survey azimuth
        thta, trg_slctr = range_orientation_calculator(mnt1_e, mnt2_e, mnt1_n, mnt2_n, 0)  # Defines variable. Calls
        # function. Calculates azimuth angle of range.

        # Station separations projected East and North
        if trg_slctr == 1:  # Begins conditional statement. Checks equality. Eecutes code when condition satisfied.
            df_dlt_e = df_dlt_r * np.cos(thta)  # Defines DataFrame. Calculates station separation components projected
            # in the East directions.
            df_dlt_n = df_dlt_r * np.sin(thta)  # Defines DataFrame. Calculates station separation components projected
            # in the North directions.
        else:  # Begins conditional statement. Checks equality. Eecutes code when condition satisfied.
            df_dlt_e = df_dlt_r * np.sin(thta)  # Defines DataFrame. Calculates station separation components projected
            # in the East directions.
            df_dlt_n = df_dlt_r * np.cos(thta)  # Defines DataFrame. Calculates station separation components projected
            # in the North directions.

        # Station coordinates
        df_e = (df_dlt_e / ft_to_m) + mnt1_e  # Defines DataFrame. Calculates Easting coordinate for all stations.
        df_n = (df_dlt_n / ft_to_m) + mnt1_n  # Defines DataFrame. Calculates Northing coordinate for all stations.

        df_e = df_e.rename('Easting')  # Redefines DataFrame. Renames column.
        df_n = df_n.rename('Northing')  # Redefines DataFrame. Renames column.

        # Plot
        plt.scatter(df_e, df_n, c='Cyan', alpha=0.1)  # Creates scatter plot. Plots station coordinates. Enable for
        # check.
        plt.scatter([mnt1_e, mnt2_e], [mnt1_n, mnt2_n], c='Orange')  # Creates scatter plot. Plots monument coordinates.
        # Enable for check.
        plt.pause(1)  # Plot pause command. Enables continuous plotting on same figure at interval of 1 second.

        # PREPARE DATA FOR DIGITIZATION --------------------------------------------------------------------------------

        # Compile calculations -----------------------------------------------------------------------------------------

        try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
            df_e_all = pd.concat([df_e_all, df_e], axis=0)  # Redefines DataFrame. Concatenates DataFrames if it exists.
            # Compiles coordinate data avoiding overwrite.
        except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
            # satisfied.
            df_e_all = df_e  # Defines DataFrame. Creates new DataFrame avoiding overwrite.

        try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
            df_n_all = pd.concat([df_n_all, df_n], axis=0)  # Redefines DataFrame. Concatenates DataFrames if it exists.
            # Compiles coordinate data avoiding overwrite.
        except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
            # satisfied.
            df_n_all = df_n  # Defines DataFrame. Creates new DataFrame avoiding overwrite.

        # Update data file ---------------------------------------------------------------------------------------------

        if i == rng_end:  # Begins conditional statement. Checks equality. Executes code when condition satisfied. Saves
            # coordinates to DataFrame and digitizes DataFrame when all surveys have been completed.
            if j == srvy_nmbrs[-1]:  # Begins conditional statement. Checks equality. Executes code when condition
                # satisfied.
                df_srvy_dt = pd.concat([df_srvy_dt, df_e_all, df_n_all], axis=1)  # Redefines DataFrame. Concatenates
                # DataFrames. Appends coordinates to DataFrame for digitization.

                srvy_eras = slice_DataFrame_columns('Array', 'Integer', df_srvy_dt, 'Srvy_year', 1, 0, 0)  # Defines
                # array. Calls function. Slices DataFrame to yield survey eras of complete dataset.

                for k in srvy_eras:  # Begins loop. Loops through survey era years. Digitizes data for each survey era
                    # in sequence.
                    df_srvy_era_k = slice_DataFrame_rows('Equals', df_srvy_dt, 'Srvy_year', k, 0)  # Defines DataFrame.
                    # Calls function. Slices DataFrame to yield single survey era data.

                    gdf_srvy_era_k = gpd.GeoDataFrame(df_srvy_era_k, geometry=gpd.points_from_xy(df_srvy_era_k.Easting,
                                                                                                 df_srvy_era_k.Northing)
                                                      , crs=crdnt_rf_sys)  # Defines GeoDataFrame. Creates shapefile
                    # from DataFrame and coordinate geometry.

                    lyr_nm = str(k) + '_ww_survey_data'  # Defines variable. Sets name of layer for export.

                    gpkg = '/WW_sedimentation_surveys.gpkg'  # Defines variable. Sets name of GeoPackage where layers
                    # will be exported.

                    gdf_srvy_era_k.to_file(otpt_fldr + '/' + gis_fldr + gpkg, layer=lyr_nm, driver='GPKG', index=True)
                    # Saves file to directory.

# ======================================================================================================================
# * --------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================