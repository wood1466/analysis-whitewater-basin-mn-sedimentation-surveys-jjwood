# ======================================================================================================================
# WHITEWATER RIVER VALLEY (MN) SCS-USGS STREAM AND VALLEY SEDIMENTATION SURVEY DATA * ----------------------------------
# TRANSECT DATA COORDINATE GEOMETRY DIGITIZER * ------------------------------------------------------------------------
# PYTHON PROGRAM * -----------------------------------------------------------------------------------------------------

# ======================================================================================================================
# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START TRANSECT DATA DIGITIZATION!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from TData_functions import *   # Imports functions. Imports all functions from outside program.

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Directory
InputFolder = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.
OutputFolder = 'Output'  # Defines variable. Sets name of output folder where all data products will be exported.
GISFolder = 'GIS'  # Defines variable. Sets name of output folder where all geospatial data products will be exported.

# Data
InputFile1 = InputFolder + '/Elevation_surveys_20250127.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect data that is to be digitized.
InputFile2 = InputFolder + '/Coordinate_survey_20250127.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect monument coordinate data that is to be the coordinate reference for COGO calculations.
InputFile3 = InputFolder + '/Marker_metadata_20250120.csv'  # Defines variable. Sets file path to input file. Sets path
# to transect monument metadata to assist with COGO calculations.

# Operation limits
TransectNumberStart = 1  # Defines variable. Sets start transect number for operation loop.
TransectNumberEnd = 107  # Defines variable. Sets end transect number for operation loop.
TransectNumbers = CreateForwardRange(TransectNumberStart, TransectNumberEnd, 1, 0)  # Defines array. Calls function.
# Sets loop order by transect.

# Conversion factors
FtToM = 3.281  # Defines variable. Sets conversion factor from feet to meters.

# Geospatial
CRS = 'EPSG:26915'  # Defines variable. Sets projected coordinate reference system for output shapefiles vis EPSG code.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

CreateFolder(OutputFolder)  # Creates folder. Calls function. Creates output folder where all data products will be
# exported.
CreateFolder(OutputFolder + '/' + GISFolder)  # Creates folder. Calls function. Creates output folder where all
# geospatial data products will be exported.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

dfTransectElevations = ConvertCsvToDataFrame(InputFile1, 0)  # Defines DataFrame. Calls function. Uploads transect data.
dfTMonumentCoordinates = ConvertCsvToDataFrame(InputFile2, 0)  # Defines DataFrame. Calls function. Uploads transect
# monument coordinate data.
dfTMonumentMetadata = ConvertCsvToDataFrame(InputFile3, 0)  # Defines DataFrame. Calls function. Uploads transect
# monument metadata.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select transect data -------------------------------------------------------------------------------------------------

for i in TransectNumbers:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates
    # coordinates for each transect in sequence.

    dfTransectElevationsi = SliceDataFrameRows('Equals', dfTransectElevations, 'TNum', i, 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield single transect data.

    # Select marker reference data -------------------------------------------------------------------------------------

    dfTMonumentCoordinatesi = SliceDataFrameRows('Equals', dfTMonumentCoordinates, 'TNum', i, 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield single transect monument coordinate data.

    if dfTMonumentCoordinatesi.shape[0] != 0:  # Begins conditional statement. Checks inequality. Skips transect numbers
        # for which there are no reference coordinates.

        # Coordinates
        TMonument1EMi = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 0, 'EastingM', 0)  # Defines variable.
        # Calls function. Slices DataFrame to yield Easting coordinate of start monument of present transect.
        TMonument1NMi = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 0, 'NorthingM', 0)  # Defines variable.
        # Calls function. Slices DataFrame to yield Northing coordinate of start monument of present transect.
        TMonument2EMi = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 1, 'EastingM', 0)  # Defines variable.
        # Calls function. Slices DataFrame to yield Easting coordinate of end monument of present transect.
        TMonument2NMi = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 1, 'NorthingM', 0)  # Defines variable.
        # Calls function. Slices DataFrame to yield Northing coordinate of end monument of present transect.

        # Metadata
        dfTMonumentMetadatai = SliceDataFrameRows('Equals', dfTMonumentMetadata, 'TNum', i, 0)  # Defines DataFrame.
        # Calls function. Slices DataFrame to yield single transect monument metadata.
        dfTMonumentMetadata09_14i = SliceDataFrameRows('Equals', dfTMonumentMetadatai, 'SrvEra', '2009–2014', 0)
        # Defines DataFrame. Calls function. Slices DataFrame to yield single transect, single survey, monument
        # metadata.

        TMonument1StationFti = SliceDataFrameCell('Float', dfTMonumentMetadata09_14i, 0, 'MTopSttnFt', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield transect station of start monument.

        # Check marker for off transect position -----------------------------------------------------------------------

        TMonument1OffTransecti = SliceDataFrameCell('Float', dfTMonumentMetadata09_14i, 0, 'MTOff', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield marker off transect condition.
        TMonument2OffTransecti = SliceDataFrameCell('Float', dfTMonumentMetadata09_14i, 1, 'MTOff', 0)  # Defines
        # variable. Calls function. Slices DataFrame to yield marker off transect condition.

        if TMonument1OffTransecti != 0:  # Begins conditional statement. Checks inequality. Shifts reference coordinate
            # position if marker lies off transect.
            TMonument1EMi, TMonument1NMi = MoveReferenceCoordinates(
                TMonument1EMi, TMonument1NMi, dfTMonumentMetadata09_14i, dfTMonumentCoordinatesi, 0, 'MTOffDisFt',
                'MTOffDir', 'GXYAccM', FtToM, 0)  # Redefines variables. Calls function. Shifts reference coordinate
            # position.
        if TMonument2OffTransecti != 0:  # Begins conditional statement. Checks inequality. Shifts reference coordinate
            # position if marker lies off transect.
            TMonument2EMi, TMonument2NMi = MoveReferenceCoordinates(
                TMonument2EMi, TMonument2NMi, dfTMonumentMetadata09_14i, dfTMonumentCoordinatesi, 1, 'MTOffDisFt',
                'MTOffDir', 'GXYAccM', FtToM, 0)  # Redefines variables. Calls function. Shifts reference coordinate
            # position.

        # Select transect survey data ----------------------------------------------------------------------------------

        TSurveyNumbers = SliceDataFrameColumns('Array', 'Integer', dfTransectElevationsi, 'ESrvNum', 1, 0, 0)  # Defines
        # array. Calls function. Slices DataFrame to transect survey numbers.

        for j in TSurveyNumbers:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates
            # coordinates for each survey in sequence.
            dfTransectElevationsi_j = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', j, 0)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield transect single survey data.

            # Stations
            dfTStationsFti_j = SliceDataFrameColumns('DataFrame', 'Float', dfTransectElevationsi_j, 'ESttnFt', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.

            # Metadata
            TID = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'TId24', 0)  # Defines variable. Calls
            # function.  Slices DataFrame to yield transect ID.
            TProfileYear = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'PYr', 0)  # Defines variable. Calls
            # function.  Slices DataFrame to yield transect survey profile year.

            print('\033[1mDIGITIZING:\033[0m', TID, ':', TProfileYear, '\n')  # Displays objects.

            # CALCULATE STATION COORDINATE GEOMETRY --------------------------------------------------------------------

            # Calculate station distance from marker -------------------------------------------------------------------

            dfTStationDistanceFti_j = dfTStationsFti_j - TMonument1StationFti  # Defines DataFrame. Calculates station
            # distance from start marker per station.

            # Calculate survey azimuth ---------------------------------------------------------------------------------

            TAzimuthi = CalculateTransectAzimuth(TMonument1EMi, TMonument1NMi, TMonument2EMi, TMonument2NMi, 0)
            # Defines variable. Calls function. Calculates azimuth orientation of transect.

            # Calculate station distance projections -------------------------------------------------------------------

            dfTStationDistanceEastFti_j = dfTStationDistanceFti_j * np.cos(TAzimuthi)  # Defines DataFrame. Calculates
            # station distance from start marker components projected in the East directions.
            dfTStationDistanceNorthFti_j = dfTStationDistanceFti_j * np.sin(TAzimuthi)  # Defines DataFrame. Calculates
            # station distance from start marker components projected in the North directions.

            # Calculate station coordinates ----------------------------------------------------------------------------

            dfTStationEastingsMi_j = (dfTStationDistanceEastFti_j / FtToM) + TMonument1EMi  # Defines DataFrame.
            # Calculates Easting coordinate for all stations. Converts feet to meters.
            dfTStationNorthingsMi_j = (dfTStationDistanceNorthFti_j / FtToM) + TMonument1NMi  # Defines DataFrame.
            # Calculates Northing coordinate for all stations. Converts feet to meters.

            dfTStationEastingsMi_j = dfTStationEastingsMi_j.rename('EastingM')  # Redefines DataFrame. Adds field name.
            dfTStationNorthingsMi_j = dfTStationNorthingsMi_j.rename('NorthingM')  # Redefines DataFrame. Adds field
            # name.

            # Handle exception: DC-7 1994 displaced stations -----------------------------------------------------------

            if TID == 'DC-7' and j == TSurveyNumbers[-1]:  # Begins conditional statement. Checks dual equality.
                # Performs modified digitization methodology.

                # Calculate station displacement azimuth ---------------------------------------------------------------

                TAzimuthi_j = TAzimuthi - (1/2) * np.pi  # Defines variable. Calculates a secondary azimuth that
                # stations will be displaced upon from the main transect.

                # Shift marker off transect ----------------------------------------------------------------------------

                # Reference distance projections
                TMonument1DistanceEastMi_j = (25 / FtToM) * np.cos(TAzimuthi_j)  # Defines variable. Calculates
                # reference coordinate distance to line trace of measurements shifted off line projected in the East
                # direction.
                TMonument1DistanceNorthMi_j = (25 / FtToM) * np.sin(TAzimuthi_j)  # Defines variable. Calculates
                # reference coordinate distance to line trace of measurements shifted off line projected in the North
                # direction.

                # Reference coordinates
                TMonument1EMi_j = TMonument1DistanceEastMi_j + TMonument1EMi  # Defines variable. Shifts reference
                # coordinate position.
                TMonument1NMi_j = TMonument1DistanceNorthMi_j + TMonument1NMi  # Defines variable. Shifts reference
                # coordinate position.

                # Calculate station coordinates ------------------------------------------------------------------------

                dfTStationEastingsMi_j2 = (dfTStationDistanceEastFti_j / FtToM) + TMonument1EMi_j  # Defines DataFrame.
                # Calculates Easting coordinate for all stations. Converts feet to meters.
                dfTStationNorthingsMi_j2 = (dfTStationDistanceNorthFti_j / FtToM) + TMonument1NMi_j  # Defines
                # DataFrame. Calculates Northing coordinate for all stations. Converts feet to meters.

                dfTStationEastingsMi_j2 = dfTStationEastingsMi_j2.iloc[8:16]  # Redefines DataFrame. Slices DataFrame to
                # yield displaced measurement coordinates only.
                dfTStationNorthingsMi_j2 = dfTStationNorthingsMi_j2.iloc[8:16]  # Redefines DataFrame. Slices DataFrame
                # to yield displaced measurement coordinates only.

                # Update DataFrame -------------------------------------------------------------------------------------

                dfTStationEastingsMi_j.iloc[8:16] = dfTStationEastingsMi_j2  # Redefines DataFrame. Inserts displaced
                # measurement coordinates into
                # original coordinate DataFrame.
                dfTStationNorthingsMi_j.iloc[8:16] = dfTStationNorthingsMi_j2  # Redefines DataFrame. Inserts displaced
                # measurement coordinates into
                # original coordinate DataFrame.

            # Plot
            # plt.scatter([TMonument1EMi, TMonument2EMi], [TMonument1NMi, TMonument2NMi], c='m', alpha=0.5)  # Creates
            # scatter plot. Plots monument coordinates.
            # plt.scatter(dfTStationEastingsMi_j, dfTStationNorthingsMi_j, c='c', alpha=0.1)  # Creates scatter plot.
            # Plots station coordinates.
            # plt.pause(0.5)  # Plot pause command. Enables continuous plotting on same figure at interval.

            # PREPARE DATA FOR DIGITIZATION ----------------------------------------------------------------------------

            # Compile calculations -------------------------------------------------------------------------------------

            try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
                dfTStationEastingsMAll = pd.concat([dfTStationEastingsMAll, dfTStationEastingsMi_j], axis=0)
                # Redefines DataFrame. Concatenates DataFrames if it exists. Compiles coordinate data avoiding
                # overwrite.
            except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
                # satisfied.
                dfTStationEastingsMAll = dfTStationEastingsMi_j  # Defines DataFrame. Creates new DataFrame avoiding
                # overwrite.

            try:  # Begins try-except statement. Checks object existence. Executes code when existence satisfied.
                dfTStationNorthingsMAll = pd.concat([dfTStationNorthingsMAll, dfTStationNorthingsMi_j], axis=0)
                # Redefines DataFrame. Concatenates DataFrames if it exists. Compiles coordinate data avoiding
                # overwrite.
            except NameError:  # Continues try-except statement. Checks object existence. Executes code when existence
                # satisfied.
                dfTStationNorthingsMAll = dfTStationNorthingsMi_j  # Defines DataFrame. Creates new DataFrame avoiding
                # overwrite.

            # Update input file ----------------------------------------------------------------------------------------

            if i == TransectNumberEnd - 1:  # Begins conditional statement. Checks equality. Saves coordinates to
                # DataFrame and digitizes when all COGO calculations have been completed.
                if j == TSurveyNumbers[-1]:  # Begins conditional statement. Checks equality. Saves coordinates to
                    # DataFrame and digitizes when all COGO calculations have been completed.
                    dfTransectElevations = pd.concat([
                        dfTransectElevations, dfTStationEastingsMAll, dfTStationNorthingsMAll], axis=1)  # Redefines
                    # DataFrame. Concatenates DataFrames. Append coordinates to DataFrame for digitization.

                    TProfileYears = SliceDataFrameColumns('Array', 'Integer', dfTransectElevations, 'PYr', 1, 0, 0)
                    # Defines array. Calls function. Slices DataFrame to yield survey eras of complete dataset.

                    # DIGITIZE DATA ------------------------------------------------------------------------------------

                    # Transect data
                    for k in TProfileYears:  # Begins loop. Loops through surface profile years. Digitizes transect
                        # data by surface profile year in sequence.
                        dfTransectElevationsk = SliceDataFrameRows('Equals', dfTransectElevations, 'PYr', k, 0)
                        # Defines DataFrame. Calls function. Slices DataFrame to yield single profile year data.

                        gdfTransectElevationsk = gpd.GeoDataFrame(
                            dfTransectElevationsk, geometry=gpd.points_from_xy(
                                dfTransectElevationsk.EastingM, dfTransectElevationsk.NorthingM), crs=CRS)  # Defines
                        # GeoDataFrame. Creates shapefile from DataFrame with specified coordinate reference system.

                        LayerName = str(k) + '_WW_elevations'  # Defines variable. Sets name of layer for export.

                        GPKG = '/WW_sedimentation_survey_data.gpkg'  # Defines variable. Sets name of GeoPackage where
                        # layers will be exported.

                        gdfTransectElevationsk.to_file(OutputFolder + '/' + GISFolder + GPKG, layer=LayerName,
                                                       driver='GPKG', index=True)  # Saves file to directory.

                    # Reference coordinates
                    gdfTMonumentCoordinates = gpd.GeoDataFrame(
                        dfTMonumentCoordinates, geometry=gpd.points_from_xy(
                            dfTMonumentCoordinates.EastingM, dfTMonumentCoordinates.NorthingM), crs=CRS)  # Defines
                    # GeoDataFrame. Creates shapefile from DataFrame with specified coordinate reference system.

                    LayerName = '2009_2014_WW_monuments'  # Defines variable. Sets name of layer for export.

                    gdfTMonumentCoordinates.to_file(OutputFolder + '/' + GISFolder + GPKG, layer=LayerName,
                                                    driver='GPKG', index=True)  # Saves file to directory.
else:  # Continues conditional statement. Checks inequality
    # ==================================================================================================================
    # SIGNAL END -------------------------------------------------------------------------------------------------------

    print('\n\033[1m' + 'TRANSECT DATA DIGITIZATION COMPLETE!!!' + '\033[0m', '\n...\n')  # Displays objects.