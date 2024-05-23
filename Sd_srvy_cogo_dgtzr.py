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
inpt_fl1 = inpt_fldr + '/QC3_surface_profiles_5_22.csv'  # Defines variable. Sets file path to input file.
inpt_fl2 = inpt_fldr + '/Monument metadata 5 22.csv'  # Defines variable. Sets file path to input file.
inpt_fl3 = inpt_fldr + '/Monument coordinates 5 22.csv'  # Defines variable. Sets file path to input file.

# Limits of analysis
rng_strt = 1  # Defines variable. Sets start survey range number for operation loop.
rng_end = 106  # Defines variable. Sets end survey range number for operation loop.

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
df_mnt_mtdt = csv_to_DataFrame(inpt_fl2, 0)  # Defines DataFrame. Calls function. Uploads monument metadata.
df_crdnt_dt = csv_to_DataFrame(inpt_fl3, 0)  # Defines DataFrame. Calls function. Uploads monument coordinate data.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------
# ======================================================================================================================

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Establish spatial selection framework --------------------------------------------------------------------------------

rng_nmbrs = forward_range(rng_strt, rng_end, 1, 0)  # Defines array. Calls function. Sets loop order by transect.

# Select transect data -------------------------------------------------------------------------------------------------

for i in rng_nmbrs:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates coordinates
    # for each range in sequence.

    df_rng_dt = slice_DataFrame_rows('Equals', df_srvy_dt, 'range_number', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single range data.

    # Metadata
    df_rng_mtdt = slice_DataFrame_rows('Equals', df_mnt_mtdt, 'range_number', i, 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single range metadata.

    # Select monument data ---------------------------------------------------------------------------------------------

    df_mnt_crdnts = slice_DataFrame_rows('Equals', df_crdnt_dt, 'range_number', i, 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single range monument coordinate data.

    if df_mnt_crdnts.shape[0] != 0:  # Begins conditional statement. Checks
    # inequality. Skips range numbers for which there are no surface profiles.
        # Coordinates
        mnt1_e = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'easting_m', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield Easting coordinate of starting monument of present dataset.
        mnt1_n = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'northing_m', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield Northing coordinate of starting monument of present dataset.
        mnt2_e = slice_DataFrame_cell('Float', df_mnt_crdnts, 1, 'easting_m', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield Easting coordinate of ending monument of present dataset.
        mnt2_n = slice_DataFrame_cell('Float', df_mnt_crdnts, 1, 'northing_m', 0)  # Defines variable. Calls function.
        # Slices DataFrame to yield Northing coordinate of ending monument of present dataset.

        # Reference station
        mnt1_stn = slice_DataFrame_cell('Float', df_mnt_crdnts, 0, 'marker_station', 0)  # Defines variable. Calls
        # function.  Slices DataFrame to yield survey station (range position) of starting monument.

        # Check for monument displacement from range line --------------------------------------------------------------

        mnt1_e, mnt1_n = check_marker_displacement(mnt1_e, mnt1_n, df_mnt_crdnts, 0, ft_to_m, 0)  # Redefines variables.
        # Calls function. Checks if coordinates need shifted to account for monument offset from range line.
        mnt2_e, mnt2_n = check_marker_displacement(mnt2_e, mnt2_n, df_mnt_crdnts, 1, ft_to_m, 0)  # Redefines variables.
        # Calls function. Checks if coordinates need shifted to account for monument offset from range line.

    # Select survey data -----------------------------------------------------------------------------------------------

    prfl_nmbrs = slice_DataFrame_columns('Array', 'Integer', df_rng_dt, 'profile_number', 1, 0, 0)  # Defines array.
    # Calls function. Slices DataFrame to yield survey numbers of range dataset.

    for j in prfl_nmbrs:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates
        # coordinates for each survey in sequence.
        df_rng_srvy_dt = slice_DataFrame_rows('Equals', df_rng_dt, 'profile_number', j, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single range single survey data.

        # Metadata
        df_rng_srvy_mtdt = slice_DataFrame_rows('Equals', df_rng_mtdt, 'profile_number', j, 0)  # Defines DataFrame.
        # Calls function. Slices DataFrame to yield single range survey metadata.

        rng_id = retrieve_metadata(df_rng_srvy_mtdt, 1)  # Calls function. Displays and retrieves metadata.

        # Survey data
        df_stns = slice_DataFrame_columns('DataFrame', 'Float', df_rng_srvy_dt, 'station', 0, 0, 0)  # Defines array.
        # Calls function. Slices DataFrame to yield survey stations of survey dataset.
        df_elvtns = slice_DataFrame_columns('DataFrame', 'Float', df_rng_srvy_dt, 'elevation_1', 0, 0, 0)  # Defines
        # array. Calls function. Slices DataFrame to yield survey elevations of survey dataset.

        # CALCULATE STATION COORDINATE GEOMETRY ------------------------------------------------------------------------

        if df_mnt_crdnts.shape[0] != 0:  # Begins conditional statement. Checks inequality.
            # Digitizes all data that has elevation records. Ignores soil bore depth only data.
            # Station separations down range
            df_dlt_r = df_stns - mnt1_stn  # Defines DataFrame. Calculates station separation between survey points and
            # reference monument.

            # Survey azimuth
            azmth = range_orientation_calculator(mnt1_e, mnt2_e, mnt1_n, mnt2_n, 0)  # Defines variable. Calls
            # function. Calculates azimuth angle of range.

            # Station separations projected East and North
            df_dlt_e = df_dlt_r * np.cos(azmth)  # Defines DataFrame. Calculates station separation components projected
            # in the East directions.
            df_dlt_n = df_dlt_r * np.sin(azmth)  # Defines DataFrame. Calculates station separation components projected
            # in the North directions.

            # Station coordinates
            df_e = (df_dlt_e / ft_to_m) + mnt1_e  # Defines DataFrame. Calculates Easting coordinate for all stations.
            df_n = (df_dlt_n / ft_to_m) + mnt1_n  # Defines DataFrame. Calculates Northing coordinate for all stations.

            df_e = df_e.rename('easting_m')  # Redefines DataFrame. Renames column.
            df_n = df_n.rename('northing_m')  # Redefines DataFrame. Renames column.

            # Handle exception: DC-7 1994 partially displaced survey ---------------------------------------------------

            if rng_id == 'DC-7' and j == prfl_nmbrs[0]:  # Begins conditional statement. Checks dual equality. Performs
                # alternate digitization methodology.
                # Survey displacement azimuth
                azmth_2 = azmth - (1/2) * np.pi  # Defines variable. Calculates the azimuth that survey measurements
                # will be displaced upon from the main range.

                # Monument coordinate displacements projected East and North
                mnt1_dlt_e = (25 / ft_to_m) * np.cos(azmth_2)  # Defines variable. Calculates displacement to coordinate
                # of synthetic monument.
                mnt1_dlt_n = (25 / ft_to_m) * np.sin(azmth_2)  # Defines variable. Calculates displacement to coordinate
                # of synthetic monument.

                # Monument coordinate
                mnt1_e2 = mnt1_dlt_e + mnt1_e  # Defines variable. Calculates synthetic coordinate.
                mnt1_n2 = mnt1_dlt_n + mnt1_n  # Defines variable. Calculates synthetic coordinate.

                # Station coordinates
                df_e2 = (df_dlt_e / ft_to_m) + mnt1_e2  # Defines DataFrame. Calculates Easting coordinate for all
                # stations from synthetic monument.
                df_n2 = (df_dlt_n / ft_to_m) + mnt1_n2  # Defines DataFrame. Calculates Northing coordinate for all
                # stations from synthetic monument.

                df_e2 = df_e2.iloc[8:16]  # Redefines DataFrame. Slices DataFrame to yield displaced survey measurement
                # coordinates only.
                df_n2 = df_n2.iloc[8:16]  # Redefines DataFrame. Slices DataFrame to yield displaced survey measurement
                # coordinates only.

                df_e.iloc[8:16] = df_e2  # Redefines DataFrame. Inserts displaced survey measurement coordinates into
                # original coordinate DataFrame.
                df_n.iloc[8:16] = df_n2  # Redefines DataFrame. Inserts displaced survey measurement coordinates into
                # original coordinate DataFrame.

            # Plot
            #plt.scatter([mnt1_e, mnt2_e], [mnt1_n, mnt2_n], c='m', alpha=0.1)  # Creates scatter plot. Plots monument
            # coordinates. Enable for check.
            #plt.scatter(df_e, df_n, c='c', alpha=0.1)  # Creates scatter plot. Plots station coordinates. Enable for
            # check.
            #plt.pause(1)  # Plot pause command. Enables continuous plotting on same figure at interval.

            # PREPARE DATA FOR DIGITIZATION ----------------------------------------------------------------------------

            # Compile calculations -------------------------------------------------------------------------------------

            try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
                df_e_all = pd.concat([df_e_all, df_e], axis=0)  # Redefines DataFrame. Concatenates DataFrames if it
                # exists. Compiles coordinate data avoiding overwrite.
            except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
                # satisfied.
                df_e_all = df_e  # Defines DataFrame. Creates new DataFrame avoiding overwrite.

            try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
                df_n_all = pd.concat([df_n_all, df_n], axis=0)  # Redefines DataFrame. Concatenates DataFrames if it
                # exists. Compiles coordinate data avoiding overwrite.
            except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
                # satisfied.
                df_n_all = df_n  # Defines DataFrame. Creates new DataFrame avoiding overwrite.

        # Update data file ---------------------------------------------------------------------------------------------

        if i == rng_end:  # Begins conditional statement. Checks equality. Executes code when condition satisfied.
            # Save coordinates to DataFrame and digitizes DataFrame when all surveys have been completed.
            if j == prfl_nmbrs[-1]:  # Begins conditional statement. Checks equality. Executes code when condition
                # satisfied.
                df_srvy_dt = pd.concat([df_srvy_dt, df_e_all, df_n_all], axis=1)  # Redefines DataFrame.
                # Concatenates DataFrames. Append coordinates to DataFrame for digitization.

                prfl_yrs = slice_DataFrame_columns('Array', 'Integer', df_srvy_dt, 'profile_year', 1, 0, 0)  # Defines
                # array. Calls function. Slices DataFrame to yield survey eras of complete dataset.

                for k in prfl_yrs:  # Begins loop. Loops through survey era years. Digitizes data for each survey
                    # era in sequence.
                    df_prfl_yr_k = slice_DataFrame_rows('Equals', df_srvy_dt, 'profile_year', k, 0)  # Defines
                    # DataFrame. Calls function. Slices DataFrame to yield single survey era data.

                    gdf_prfl_yr_k = gpd.GeoDataFrame(df_prfl_yr_k,
                                                      geometry=gpd.points_from_xy(df_prfl_yr_k.easting_m,
                                                                                  df_prfl_yr_k.northing_m),
                                                      crs=crdnt_rf_sys)  # Defines GeoDataFrame. Creates shapefile
                    # from DataFrame and coordinate geometry.

                    lyr_nm = str(k) + '_ww_surface_profiles'  # Defines variable. Sets name of layer for export.

                    gpkg = '/WW_sedimentation_surveys.gpkg'  # Defines variable. Sets name of GeoPackage where
                    # layers will be exported.

                    gdf_prfl_yr_k.to_file(otpt_fldr + '/' + gis_fldr + gpkg, layer=lyr_nm, driver='GPKG', index=True)
                    # Saves file to directory.

# ======================================================================================================================
# * --------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================