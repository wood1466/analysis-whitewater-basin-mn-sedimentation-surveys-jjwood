# ======================================================================================================================
# WHITEWATER RIVER VALLEY (MN) SCS-USGS STREAM AND VALLEY SEDIMENTATION SURVEY TRANSECTS * -----------------------------
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
InputFile1 = InputFolder + '/Elevation_surveys_20250117.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect data that is to be digitized.
InputFile2 = InputFolder + '/Coordinate_survey_20250117.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect monument coordinate data that is to be the coordinate reference for COGO calculations.
InputFile3 = InputFolder + '/Marker_metadata_20250120.csv'  # Defines variable. Sets file path to input file. Sets path
# to transect monument metadata to assist with COGO calculations.

# Operation limits
TransectNumberStart = 1  # Defines variable. Sets start transect number for operation loop.
TransectNumberEnd = 107  # Defines variable. Sets end transect number for operation loop.
TransectNumbers = ForwardRange(TransectNumberStart, TransectNumberEnd, 1, 0)  # Defines array. Calls function. Sets
# loop order by transect.

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

dfTransectElevations = CsvToDataFrame(InputFile1, 0)  # Defines DataFrame. Calls function. Uploads transect data.
dfTMonumentCoordinates = CsvToDataFrame(InputFile2, 0)  # Defines DataFrame. Calls function. Uploads transect monument
# coordinate data.
dfTMonumentMetadata = CsvToDataFrame(InputFile3, 0)  # Defines DataFrame. Calls function. Uploads transect monument
# metadata.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select transect data -------------------------------------------------------------------------------------------------

for i in TransectNumbers:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates
    # coordinates for each transect in sequence.

    dfTransectElevationsi = SliceDataFrameRows('Equals', dfTransectElevations, 'TNum', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single transect data.

    # Select reference coordinate data ---------------------------------------------------------------------------------

    dfTMonumentCoordinatesi = SliceDataFrameRows('Equals', dfTMonumentCoordinates, 'TNum', i, 0)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single transect monument coordinate data.

    if dfTMonumentCoordinatesi.shape[0] != 0:  # Begins conditional statement. Checks inequality. Skips transect numbers
        # for which there are no reference coordinates.

        # Select coordinates
        TMonument1EM = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 0, 'EastingM', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield Easting coordinate of start monument of present transect.
        TMonument1NM = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 0, 'NorthingM', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield Northing coordinate of start monument of present transect.
        TMonument2EM = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 1, 'EastingM', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield Easting coordinate of end monument of present transect.
        TMonument2NM = SliceDataFrameCell('Float', dfTMonumentCoordinatesi, 1, 'NorthingM', 0)  # Defines variable. Calls
        # function. Slices DataFrame to yield Northing coordinate of end monument of present transect.

        # Select marker metadata
        dfTMonumentMetadatai = SliceDataFrameRows('Equals', dfTMonumentMetadata, 'TNum', i, 0)  # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single transect monument metadata.
        dfTMonumentMetadatai09_14 = SliceDataFrameRows('Equals', dfTMonumentMetadatai, 'SrvEra', '2009–2014', 0)    # Defines DataFrame. Calls
        # function. Slices DataFrame to yield single transect, single survey, monument metadata.

        TMonument1StationFt = SliceDataFrameCell('Float', dfTMonumentMetadatai09_14, 0, 'MTopSttnFt', 0)  # Defines variable. Calls
        # function.  Slices DataFrame to yield transect station of start monument.

        # Check marker for off transect position
        TMonument1OffTransect = SliceDataFrameCell('Float', dfTMonumentMetadatai09_14, 0, 'MTOff', 1)  # Defines variable. Calls
        # function.  Slices DataFrame to yield marker off transect condition.
        TMonument2OffTransect = SliceDataFrameCell('Float', dfTMonumentMetadatai09_14, 1, 'MTOff', 1)  # Defines variable. Calls
        # function.  Slices DataFrame to yield marker off transect condition.

        if TMonument1OffTransect != 0:  # Begins conditional statement. Checks inequality. Shifts reference coordinate
            # position if marker lies off transect.
            TMonument1EM, TMonument1NM = MoveReferenceCoordinates(TMonument1EM, TMonument1NM, dfTMonumentMetadatai09_14,
                                                                  dfTMonumentCoordinatesi, 0, 'MTOffDisFt', 'MTOffDir',
                                                                  'GXYAccM', FtToM, 1)  # Redefines variables. Calls
            # function. Shifts reference coordinate position.
        if TMonument2OffTransect != 0:  # Begins conditional statement. Checks inequality. Shifts reference coordinate
            # position if marker lies off transect.
            TMonument2EM, TMonument2NM = MoveReferenceCoordinates(TMonument2EM, TMonument2NM, dfTMonumentMetadatai09_14,
                                                                  dfTMonumentCoordinatesi, 1, 'MTOffDisFt', 'MTOffDir',
                                                                  'GXYAccM', FtToM, 1)  # Redefines variables. Calls
            # function. Shifts reference coordinate position.

        # Select transect survey data ----------------------------------------------------------------------------------

        TSurveyNumbers = SliceDataFrameColumns('Array', 'Integer', dfTransectElevationsi, 'ESrvNum', 1, 0, 0)  # Defines
        # array. Calls function. Slices DataFrame to transect survey numbers.

        for j in TSurveyNumbers:  # Begins loop. Loops through array elements. Loops through survey numbers. Calculates
            # coordinates for each survey in sequence.
            dfTransectElevationsi_j = SliceDataFrameRows('Equals', dfTransectElevationsi, 'ESrvNum', j, 1)  # Defines
            # DataFrame. Calls function. Slices DataFrame to yield transect single survey data.

            # Stations
            dfTStationsFti_j = SliceDataFrameColumns('DataFrame', 'Float', dfTransectElevationsi_j, 'ESttnFt', 0, 0, 0)
            # Defines array. Calls function. Slices DataFrame to yield survey stations of survey dataset.

            # Metadata
            TID = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'TId24', 1)  # Defines variable. Calls
            # function.  Slices DataFrame to yield transect ID.
            TProfileYear = SliceDataFrameCell('String', dfTransectElevationsi_j, 0, 'PYr', 1)  # Defines variable. Calls
            # function.  Slices DataFrame to yield transect survey profile year.

            print('\033[1mDIGITIZING:\033[0m', TID, ':', TProfileYear, '\n')  # Displays objects.

            # CALCULATE STATION COORDINATE GEOMETRY --------------------------------------------------------------------


            x