# ======================================================================================================================
# WHITEWATER RIVER VALLEY, MINNESOTA - CARTESIAN COORDINATE EXTRACTOR * ------------------------------------------------
# SECONDARY PROGRAM * --------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START COORDINATE CONVERSION!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import pandas as pd, geopandas as gpd
# Imports "Python data analysis library" with alias. Enables use of DataFrames.
# Imports a geographic data libray with alias. Enables spatial operations.
import os
# Imports "Miscellaneous operating system interfaces" & "System specific parameters and functions". Enables operating
from Functions import *  # Imports all functions from outside program.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Name folders
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Create folders
lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. To enable looped folder creation.

for i in lvl1_fldrs:  # Begins loop through elements of list. Loops through paths.
    lvl = 1  # Defines variable as integer. For function input.

    create_folder(lvl, i)  # Creates folders. Calls function.

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Input file(s) --------------------------------------------------------------------------------------------------------

inpt_fl1 = inpt_fldr + '/Survey_mons.csv'  # Defines string. Sets file path to input file.

df_bm_dt = csv_to_DataFrame(inpt_fl1, 'TEST DATA', 1)  # Defines DataFrame. Calls function. Uploads survey data.

data = gpd.read_file(inpt_fldr + '/Survey_mons.shp')  # Imports shapefile corresponding to table.
gdf_bm_dt = gpd.GeoDataFrame(data)  # Creates GeoDataFrame.

# ======================================================================================================================
# PART 2: COORDINATE EXTRACTION ----------------------------------------------------------------------------------------
# ======================================================================================================================

# RETRIEVE COORDINATES -------------------------------------------------------------------------------------------------

gs_bm_dt = gpd.GeoSeries(gdf_bm_dt['geometry'])  # Defines GeoSeries.

df_x = pd.DataFrame(gs_bm_dt.x)  # Defines DataFrame. Cartesian x coordinates.
df_y = pd.DataFrame(gs_bm_dt.y)# Defines DataFrame. Cartesian y coordinates.

# UPDATE FILE ----------------------------------------------------------------------------------------------------------

df_bm_dt = pd.concat([df_bm_dt, df_x, df_y], axis=1)  # Redefines DataFrame. Concatenates coordinates to shapefile
# DataFrame.

# EXPORT DATA ----------------------------------------------------------------------------------------------------------

# Export data
fldr_lbls = ['/Geospatial_analysis', '/Calculations', '/Coordinates']  # Defines list. Sets folder labels for directory
# to be made.

fl_name = 'BM_crdnts.csv'  # Defines variable as string.

export_file_to_directory(1, 'Table', 3, fldr_lbls, opt_fldr, 'Directories named: ', fl_name, 1, None, df_bm_dt, False,
                         'Extracted cartesian coordinates', None, None, None, 0)  # Creates directory and exports file.
# Calls function.

# ======================================================================================================================
# END! -----------------------------------------------------------------------------------------------------------------
# ======================================================================================================================