# ======================================================================================================================
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
InputFile1 = InputFolder + '/Elevation_surveys_20250117.csv'  # Defines variable. Sets file path to input file.
InputFile2 = InputFolder + '/Coordinate_survey_20250117.csv'  # Defines variable. Sets file path to input file.

# Operation limits
TransectNumberStart = 1  # Defines variable. Sets start transect number for operation loop.
TransectNumberEnd = 107  # Defines variable. Sets end transect number for operation loop.
TransectNumbers = ForwardRange(TransectNumberStart, TransectNumberEnd, 1, 1)  # Defines array. Calls function. Sets
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
dfMonumentCoordinates = CsvToDataFrame(InputFile2, 0)  # Defines DataFrame. Calls function. Uploads monument coordinate
# data.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select transect data -------------------------------------------------------------------------------------------------

for i in TransectNumbers:  # Begins loop. Loops through array elements. Loops through transect numbers. Calculates
    # coordinates for each transect in sequence.

    dfTransect = SliceDataFrameRows('Equals', dfTransectElevations, 'TNum', i, 0)  # Defines DataFrame. Calls function.
    # Slices DataFrame to yield single transect data.

    # Select reference coordinate data ---------------------------------------------------------------------------------

    dfTransectMonuments = SliceDataFrameRows('Equals', dfMonumentCoordinates, 'TNum', i, 1)  # Defines DataFrame. Calls
    # function. Slices DataFrame to yield single transect monument coordinate data.

    if dfTransectMonuments.shape[0] != 0:  # Begins conditional statement. Checks inequality. Skips transect numbers
        # for which there are no reference coordinates.

        # Select coordinates
        Monument1E = SliceDataFrameCell('Float', dfTransectMonuments, 0, 'EastingM', 1)  # Defines variable. Calls
        # function. Slices DataFrame to yield Easting coordinate of start monument of present transect.
        Monument1N = SliceDataFrameCell('Float', dfTransectMonuments, 0, 'NorthingM', 1)  # Defines variable. Calls
        # function. Slices DataFrame to yield Northing coordinate of start monument of present transect.
        Monument2E = SliceDataFrameCell('Float', dfTransectMonuments, 1, 'EastingM', 1)  # Defines variable. Calls
        # function. Slices DataFrame to yield Easting coordinate of end monument of present transect.
        Monument2N = SliceDataFrameCell('Float', dfTransectMonuments, 1, 'NorthingM', 1)  # Defines variable. Calls
        # function. Slices DataFrame to yield Northing coordinate of end monument of present transect.

        # Select station
        Monument1Station = SliceDataFrameCell('Float', dfTransectMonuments, 0, 'marker_station', 0)  # Defines variable. Calls
        # function.  Slices DataFrame to yield survey station (range position) of starting monument.
        x=1