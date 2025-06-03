# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS
# TRANSECT DATA VISUALIZER * --------------------------------------------------
import matplotlib.pyplot as plt

print('\n\033[1m' + 'START TRANSECT DATA VISUALIZATION!!!' + '\033[0m',
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
PLOT_FOLDER = 'Plots'  # Output where all visualizations will be stored.

# Define data files.
INPUT_FILE1 = INPUT_FOLDER + '/Elevation_surveys_20250129.csv'  # Data to be
# visualized.

# Define operation parameters.
TRANSECT_NUM_START = 1  # Start transect number for operation loop.
TRANSECT_NUM_END = 107  # End transect number for operation loop.

TRANSECT_NUMS = create_forward_range(
        TRANSECT_NUM_START, TRANSECT_NUM_END, 1, 0)  # Calls UDF to define
# array of transect numbers for looping visualization.

# SET UP DIRECTORY. -----------------------------------------------------------

# Create output folders.
create_folder(OUTPUT_FOLDER)  # Calls UDF.
create_folder(OUTPUT_FOLDER + '/' + PLOT_FOLDER)

# UPLOAD FILE(S). -------------------------------------------------------------

# Define DataFrames from input data.
df_transect_elevs = convert_CSV_to_dataframe(INPUT_FILE1, 0)  # Calls UDF.

# DATA OPERATIONS =============================================================

# SELECT DATA. ----------------------------------------------------------------

# Select transect data.
for i in TRANSECT_NUMS:  # Begins loop through transects to visualize data.
    df_transect_elevs_i = slice_dataframe_rows(
            'Equals', df_transect_elevs, 'TNum', i, 0)  # Calls UDF to slice
    # DataFrame and define resultant DataFrame of single transect data.

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

        df_stations_i_j = slice_dataframe_column(
                'DataFrame', 'Float', df_transect_elevs_i_j, 'ESttnFt', 0,
                0, 0)  # Transect survey stations.
        df_elevs_i_j = slice_dataframe_column(
                'DataFrame', 'Float', df_transect_elevs_i_j, 'E1Ft', 0, 0, 0)
        # Transect survey elevations.

        # Select transect and survey metadata.
        transect_ID = slice_dataframe_cell(
                'String', df_transect_elevs_i_j, 0, 'TId24', 0)
        # Transect ID.
        transect_p_year = slice_dataframe_cell(
                'String', df_transect_elevs_i_j, 0, 'PYr', 0)
        # Transect survey profile year.

        print('\033[1mVISUALIZING:\033[0m', transect_ID, ':',
              transect_p_year, '\n')  # Displays objects.

        # PLOT DATA. -----------------------------------------------------------

        plt.plot(df_stations_i_j, df_elevs_i_j)
        ax = plt.gca()
        ax.set_aspect(50)
        if j != transect_surv_nums[-1]:
            plt.pause(1)
        else:
            # plt.yticks(np.arange(min(df_elevs_i_j), max(df_elevs_i_j), 5))
            # plt.xticks(np.arange(min(df_stations_i_j), max(df_stations_i_j), 250))
            plt.pause(1)
            plt.show()
# ----------------------------------------------------------------------------79