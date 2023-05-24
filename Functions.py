# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA, SEDIMENTATION SURVEY DATA ANALYSIS * ----------------------------------------------
# SECONDARY PROGRAM 1 OF 1 * -------------------------------------------------------------------------------------------
# ======================================================================================================================

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os, sys, math
# Imports "Time and access conversions". Enables time related functions.
# Imports "Miscellaneous operating system interfaces" & "System specific parameters and functions". Enables operating
# system dependent functionality.
# Imports "Mathematical functions".
import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sc, geopandas as gpd
# Imports "Python data analysis library" with alias. Enables use of DataFrames.
# Imports numerical mathematics library and a scientific mathematics library, with alias.
# Imports a plotting interface with alias.
# Imports a geographic data libray with alias. Enables spatial operations.

# SELECT INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Plot format ----------------------------------------------------------------------------------------------------------

# Set general plot format
wdth = 4.5  # Defines variable as float. Sets plot window width.
hght = wdth * 1.618  # Defines variable. Sets plot window height. Uses golden ratio.
fig_sz = (hght, wdth)  # Defines object. Sets plot window size.
fntsz = [10, 8]  # Defines list. Sets font size for axes labels and tick marks.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Set data display format
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDDD']
# Defines list. Sets Paul Tol, muted, colorblind friendly palette with hex color codes.
lin_wdth = [2, 1]  # Defines list. Sets plot line width.
lin_styl = ['solid', 'dashed', 'dotted', 'dashdot']  # Defines list. Sets line style.
mrkrs = ['h', 'v', 'P', 'o', 'X', 's', '^', 'D', '<', '>', '8', 'p', 'H', 'd', ' ']  # Defines list. Sets plot markers.
# Uses matplotlib markers.
mrkr_sz = [4, 10]  # Defines list. Sets plot marker size.
alpha = [0.5, 0.3, 1]  # Defines list. Sets object transparency for plotted data and fill.

# Set legend display format
lctn = 'best'  # Defines variable as string. Sets legend location on plot. Automatically chooses.
mrkr_scl = 2  # Defines variable as integer. Sets marker size on legend.
frm_alpha = 0.7  # Defines variable as float. Sets legend box transparency.
lbl_spcng = 0.7  # Defines variable as float. Sets legend object spacing.

# ======================================================================================================================
# PART 2: DEFINE FUNCTIONS ---------------------------------------------------------------------------------------------
# ======================================================================================================================

def create_folder(level, path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')  # Displays objects.

def csv_to_DataFrame(path, display_label, display):  # Defines function. For uploading .csv file and converting to a
    # DataFrame.
    csv_data = pd.read_csv(path)  # Uploads .csv file.
    df = pd.DataFrame(csv_data)  # Defines DataFrame. Converts from .csv. For Python manipulation.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame format. Displays all DataFrame columns.
    if display == 1:  # Conditional statement. For display.
        print('\033[1m' + 'UPLOADED .CSV DATA: ' + display_label + '\033[0m', '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends function execution.

def forward_range(start, end, step, display_label, display):  # Defines function. For generating forward array
    # between two numbers.
    end = end + 1  # Defines variable. Resets end of range so array includes final input value.
    end_label = end - 1  # Defines variable. For display.
    frwd_rng = np.arange(start, end, step)  # Defines function format.
    if display == 1:  # Conditional statement. For display.
        print(display_label + '\n  Limits: ' + str(start) + ' & ' + str(end_label) + ' --> List:', frwd_rng)
        # Displays objects.
    return frwd_rng  # Ends function execution.

def slice_DataFrame_rows(search_type, dataframe, column, value, display_label, display):  # Defines function. For
    # DataFrame slicing by row value.
    if search_type == 'equals':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] == value]  # Defines function format.
    elif search_type == 'less than':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] < value]  # Defines function format.
    elif search_type == 'less than/equal':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] <= value]  # Defines function format.
    elif search_type == 'more than':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] > value]  # Defines function format.
    elif search_type == 'more than/equal':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] >= value]  # Defines function format.
    elif search_type == 'does not equal':  # Conditional statement. Sets function format.
        df_slc_r = dataframe[dataframe[column] != value]  # Defines function format.
    df_slc_r = df_slc_r.loc[:, ~df_slc_r.columns.str.match('Unnamed')]  # Redefines DataFrame. Searches for empty
    # columns and deletes them.
    if display == 1:  # Conditional statement. For display.
        print('\033[1m' + display_label + ' ' + search_type.upper() + ' ' + str(value) + '\033[0m', '\n...\n',
              df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends function execution.

def slice_DataFrame_cell(data_type, convert, conversion_factor, dataframe, position, column, display_label, display):
    # Defines function. For DataFrame slicing by row value and index.
    index = dataframe.index  # Defines object. Retrieves DataFrame index.
    slc_cl = dataframe.loc[index[position], column]  # Defines function format.
    typ = type(slc_cl)  # Defines variable. Checks data type.
    # print('This', slc_cl)
    # print(type(slc_cl))
    if slc_cl == '1850s':  # Conditional statement. Ensures desired data type retrieved by function.
        if typ == data_type:  # Conditional statement.
            pass
        else:  # Conditional statement.
            slc_cl = str(slc_cl)  # Redefines variable. Converts to string.
    else:  # Conditional statement.
        if typ == data_type:  # Conditional statement. Ensures desired data type retrieved by function.
            pass  # Pass command. Moves on to next line.
        else:  # Conditional statement.
            if data_type == 'Integer':  # Conditional statement. Enforces desired data type retrieved by function.
                slc_cl = int(slc_cl)  # Redefines variable. Converts to integer.
            elif data_type == 'Float':  # Conditional statement. Enforces desired data type retrieved by function.
                slc_cl = float(slc_cl)  # Redefines variable. Converts to float.
            else:  # Conditional statement. Enforces desired data type retrieved by function.
                slc_cl = str(slc_cl)  # Redefines variable. Converts to string.
    if convert == 1:  # Conditional statement. Also retreives converted value for number.
        slc_cl_cnvrt = slc_cl * conversion_factor  # Defines variable. Converts units.
        if display == 1:  # Conditional statement. For display.
            print(display_label + ': ' + str(slc_cl) + ' (' + str('%.2f' % slc_cl_cnvrt) + ')' + ' (' + data_type + ')'
                  + '\n')  # Displays objects.
        return slc_cl, slc_cl_cnvrt  # Ends function execution.
    else:  # Conditional statement.
        pass  # Pass command. Moves on to next line.
        if display == 1:  # Conditional statement. For display.
            print(display_label + ': ' + str(slc_cl) + ' (' + data_type + ')' + '\n')  # Displays objects.
        return slc_cl # Ends function execution.

def slice_DataFrame_columns(output, data_type, dataframe, column, check_duplicates, display_label, display):  # Defines function. For
    # DataFrame slicing by column.
    df_slc_c = dataframe[column]  # Defines function format.
    if check_duplicates == 1:  # Conditional statement.
        df_slc_c = df_slc_c.drop_duplicates(keep='first')  # Redefines DataFrame. Drops all duplicate values in
        # column.
    typ = df_slc_c.dtypes  # Defines variable. Retreives data type of column DataFrame.
    if typ == data_type:  # Conditional statement. Ensures desired data type retrieved by function.
        pass  # Pass command. Moves on to next line.
    else:  # Conditional statement.
        if data_type == 'Integer':  # Conditional statement. Enforces desired data type retrieved by function.
            df_slc_c = df_slc_c.astype(int)  # Redefines DataFrame. Converts to integer.
        elif data_type == 'Float':  # Conditional statement. Enforces desired data type retrieved by function.
            df_slc_c = df_slc_c.astype(float)  # Redefines DataFrame. Converts to float.
        else:  # Conditional statement. Enforces desired data type retrieved by function.
            df_slc_c = df_slc_c.astype(str)  # Redefines DataFrame. Converts to string.
    if output == 'DataFrame':  # Conditional statement. For output selection.
        if display == 1:  # Conditional statement. For display.
            print('\033[1m' + display_label + '\033[0m', '\n...\n', df_slc_c, '\n')  # Displays objects.
        return df_slc_c  # Ends function execution.
    else:  # Conditional statement. For display.
        slc_c_lst = df_slc_c.tolist()  # Defines list. Converts DataFrame to list.
        if display == 1:  # Conditional statement. For display.
            print('\033[1m' + display_label + '\033[0m', '\n...\n', slc_c_lst, '\n')  # Displays objects.
        return slc_c_lst  # Ends function execution.

def min_value_DataFrame(data_type, dataframe, display_label, display):  # Defines function. For retrieving minimum value from
    # DataFrame column.
    mn = dataframe.min()  # Defines function format.
    typ = type(mn)  # Defines variable. Retreives data type.
    if typ == data_type:  # Conditional statement. Ensures desired data type retrieved by function.
        pass  # Pass command. Moves on to next line.
    else:  # Conditional statement.
        if data_type == 'Integer':  # Conditional statement. Enforces desired data type retrieved by function.
            mn = int(mn)  # Redefines DataFrame. Converts to integer.
        elif data_type == 'Float':  # Conditional statement. Enforces desired data type retrieved by function.
            mn = float(mn)  # Redefines DataFrame. Converts to float.
        else:  # Conditional statement. Enforces desired data type retrieved by function.
            mn = str(mn)  # Redefines DataFrame. Converts to string.
    if display == 1:  # Conditional statement. For display.
        print('Minimum column value: ' + display_label + ' ' + str(mn))  # Displays objects.
    return mn  # Ends function execution.

def max_value_DataFrame(data_type, dataframe, display_label, display):  # Defines function. For retrieving maximum
    # value of DataFrame column.
    mx = dataframe.max()  # Defines function format.
    typ = type(mx)  # Defines variable. Retreives data type.
    if typ == data_type:  # Conditional statement. Ensures desired data type retrieved by function.
        pass  # Pass command. Moves on to next line.
    else:  # Conditional statement.
        if data_type == 'Integer':  # Conditional statement. Enforces desired data type retrieved by function.
            mx = int(mx)  # Redefines DataFrame. Converts to integer.
        elif data_type == 'Float':  # Conditional statement. Enforces desired data type retrieved by function.
            mx = float(mx)  # Redefines DataFrame. Converts to float.
        else:  # Conditional statement. Enforces desired data type retrieved by function.
            mx = str(mx)  # Redefines DataFrame. Converts to string.
    if display == 1:  # Conditional statement. For display.
        print('Maximum column value: ' + display_label + ' ' + str(mx))  # Displays objects.
    return mx  # Ends function execution.

def get_plot_feature_by_year(label, list, display_label, display):  # Defines function. For plot feature selection from
    # input list.
    label = str(label)  # Redefines variable. Converts data type to string.
    if label == '2008':  # Conditional statement.
        feature = list[0]  # Defines variable. Sets plot feature.
    elif label == '1994':  # Conditional statement.
        feature = list[3]  # Defines variable. Sets plot feature.
    elif label == '1978':  # Conditional statement.
        feature = list[2]  # Defines variable. Sets plot feature.
    elif label == '1975':  # Conditional statement.
        feature = list[4]  # Defines variable. Sets plot feature.
    elif label == '1964':  # Conditional statement.
        feature = list[5]  # Defines variable. Sets plot feature.
    elif label == '1939':  # Conditional statement.
        feature = list[6]  # Defines variable. Sets plot feature.
    else:  # Conditional statement.
        feature = list[7]  # Defines variable. Sets plot feature.
    if display == 1:  # Conditonal statement. For display.
        print('Plot feature selected: ' + display_label + str(feature))  # Displays objects.
    return feature  # Ends function execution.

def plot_lines(lines, plot_number, figure_size, x, y, label, color, marker, marker_size, line_width, line_style, alpha,
               show_legend, location, marker_scale, frame_alpha, label_spacing, invert_x, fontsize_ticks, x_label,
               fontsize_axis, label_pad, y_label, title, pause, pause_length):  # Defines function. For line plotting.
    plt.figure(plot_number, figsize=figure_size)  # Creates plot window. Sets figure size.
    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
    if lines == 1:  # Conditional statement. Plots single line.
        ax.plot(x, y, label=label, c=color, marker=marker, markersize=marker_size, linewidth=line_width,
                linestyle=line_style, alpha=alpha)  # Creates line plot. Sets display format.
        if show_legend == 1:  # Conditional statement. Shows legend if desired for single line plotting.
            ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)
            # Creates legend. Through automatic label detection.
    if lines != 1:  # Conditional statement. Plots multiple lines.
        lines = lines + 1  # Defines variable. For establishing looped plotting framework.
        line_list = range(1, lines, 1)  # Defines list. Creates range of integers for looped plotting.
        for a in line_list:  # Begins loop through list elements. Loops through line numbers.
            index = line_list.index(a)  # Defines variable. Retrieves index of element in list. For format selection.
            ax.plot(x[index], y[index], label=label[index], c=color[index], marker=marker[index],
                    markersize=marker_size, linewidth=line_width, linestyle=line_style[index], alpha=alpha)  # Creates
            # line plot. Sets display format.
        ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)
        # Creates legend. Through automatic label detection.
    plt.xticks(fontsize=fontsize_ticks)  # Sets x-axis ticks. Sets format.
    plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets format.
    plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates y-axis label. Sets format.
    plt.yticks(fontsize=fontsize_ticks)  # Sets y-axis ticks. Sets format.
    if invert_x == 1:  # Conditional statement. Inverts x-axis order.
        ax.invert_xaxis()  # Inverts x-axis.
    plt.title(title)  # Creates plot title.
    if pause == 1:  # Conditional statement. For display format.
        plt.pause(pause_length)  # Displays plot. For set interval of seconds and closes without clearing.
    elif pause == 0:  # Conditional statement. For display format.
        plt.show()  # Displays plot. Indefinite and cleared upon close.
    else:  # Conditional statement. For display format
        pass  # Pass command. Moves on to next line.

def export_file_to_directory(export, type, directory_levels, folder_labels, output_folder, display_label1, file_name,
                             number, figure_extension, dataframe, truth_statement, display_label2, geodataframe,
                             geopackage, driver, display):  # Defines function. For exporting files.
    if export == 1:  # Conditional statement. Exports file.
        lvls = name_levels(directory_levels, folder_labels, output_folder, display_label1, display)  # Defines list.
        # Calls function. For looped folder creation.
        for a in lvls:  # Begins loop through array elements. Loops through levels.
            lvl = lvls.index(a) + 2  # Defines variable as integer. For correct display.
            create_folder(lvl, a)  # Creates folders. Calls function.
        export_file(type, number, file_name, lvls[-1], figure_extension, dataframe, truth_statement, display_label2,
                    geodataframe, geopackage, driver, display)  # Calls function. Performs file export.

def export_file(type, number, file_name, end_path, figure_extension, dataframe, truth_statement, display_label,
                geodataframe, geopackage, driver, display):  # Defines function. For file export.
    if type == 'Figure':  # Conditional statement. For figure export.
        plt.figure(number)  # Calls figure. Makes it the active plot.
        plt.savefig(end_path + file_name, format=figure_extension)  # Saves figure to directory. Sets file format.
        plt.close()  # Closes active figure.
    elif type == 'Table':  # Conditional statement. For data table export.
        dataframe.to_csv(end_path + file_name, index=truth_statement)  # Saves file to directory. Sets file format.
    elif type == 'Geospatial':  # Conditional statement. For geospatial data export.
        geodataframe.to_file(end_path + geopackage, layer=file_name, driver=driver, index=truth_statement)  # Saves
        # file to directory.
    if display == 1:  # Conditional statement. For display.
        print(display_label, ' exported')  # Display objects.

def transect_orientation(x1, x2, y1, y2, bearing_reference_direction, bearing_angle_direction, bearing_deg,
                       bearing_functional, display_label, display):  # Defines function. For transect orientation
    # check and component calculation.
    # From field data.
    if bearing_reference_direction =='N':  # Conditional statement. Converts transect bearing to azimuth.
        if bearing_angle_direction =='E':  # Conditional statement.
            if bearing_functional == 'NE':  # Conditional statement.
                qdrnt_meas = 1  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_max = 90  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_max - bearing_deg  # Defines variable. Converts bearing to azimuth.
            else:  # Conditional statement. Converts transect bearing to azimuth.
                qdrnt_meas = 3  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_max = 270  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_max - bearing_deg  # Defines variable. Converts bearing to azimuth.
        else:  # Conditional statement. Converts transect bearing to azimuth.
            if bearing_functional == 'NW':  # Conditional statement.
                qdrnt_meas = 2  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_min = 90  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_min + bearing_deg  # Defines variable. Converts bearing to azimuth.
            else:  # Conditional statement. Converts transect bearing to azimuth.
                # elif bearing_functional == 'SE':
                qdrnt_meas = 4  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_min = 270  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_min + bearing_deg  # Defines variable. Converts bearing to azimuth.
    else:  # Conditional statement. Converts transect bearing to azimuth.
        if bearing_angle_direction == 'W':  # Conditional statement.
            if bearing_functional == 'SW':  # Conditional statement.
                qdrnt_meas = 3  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_max = 270  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas= deg_max - bearing_deg  # Defines variable. Converts bearing to azimuth.
            else:  # Conditional statement. Converts transect bearing to azimuth.
                qdrnt_meas = 1  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_max = 90  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_max - bearing_deg  # Defines variable. Converts bearing to azimuth.
        else:  # Conditional statement. Converts transect bearing to azimuth.
            if bearing_functional == 'SE':  # Conditional statement.
                qdrnt_meas = 4  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_min = 270  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_min + bearing_deg  # Defines variable. Converts bearing to azimuth.
            else:  # Conditional statement. Converts transect bearing to azimuth.
                qdrnt_meas = 2  # Defines variable. Establishes azimuthal quadrant of transect bearing.
                deg_min = 90  # Defines variable. Establishes relevant azimuth limit for bearing conversion.
                azmth_deg_meas = deg_min + bearing_deg  # Defines variable. Converts bearing to azimuth.
    azmth_rad_meas = azmth_deg_meas * (np.pi / 180)  # Defines variable. Converts degrees to radians.
    # From GPS data.
    delta_x = x2 - x1  # Defines variable. Calculates change in x between coordinates.
    delta_y = y2 - y1  # Defines variable. Calculates change in y between coordinates.
    azmth_rad_clc = math.atan(delta_y / delta_x)  # Defines variable. Calculates azmiuth along line between
    # coordinates.
    azmth_deg_clc = azmth_rad_clc * (180 / np.pi)  # Defines variable. Converts radians to degrees.
    if delta_x > 1:  # Conditional statement. Transforms transect azimuth based on components.
        if delta_y > 1:  # Conditional statement.
            qdrnt_clc = 1  # Defines variable. Establishes azimuthal quadrant of transect.
            azmth_rad_cor = azmth_rad_clc  # Defines variable. Transforms azimuth.
        if delta_y < 1:  # Conditional statement.
            qdrnt_clc = 4  # Defines variable. Establishes azimuthal quadrant of transect.
            rad_max = 2 * np.pi  # Defines variable. Establishes relevant azimuth limit for transformation.
            azmth_rad_cor = rad_max + azmth_rad_clc  # Defines variable. Transforms azimuth.
    else:
        if delta_y > 1:  # Conditional statement.
            qdrnt_clc = 2  # Defines variable. Establishes azimuthal quadrant of transect.
            rad_max = np.pi  # Defines variable. Establishes relevant azimuth limit for transformation.
            azmth_rad_cor = rad_max + azmth_rad_clc  # Defines variable. Transforms azimuth.
        else:
            qdrnt_clc = 3  # Defines variable. Establishes azimuthal quadrant of transect.
            rad_min = np.pi  # Defines variable. Establishes relevant azimuth limit for transformation.
            azmth_rad_cor = rad_min + azmth_rad_clc  # Defines variable. Transforms azimuth.
    azmth_deg_cor = azmth_rad_cor * (180 / np.pi)  # Defines variable. Converts radians to degrees.
    azmth_rad_dff = azmth_rad_cor - azmth_rad_meas  # Defines variable. Calculates difference in calculated and measured
    # azimuths.
    azmth_deg_dff = azmth_rad_dff * (180 / np.pi)  # Defines variable. Converts radians to degrees.
    if qdrnt_clc != qdrnt_meas:  # Conditional statement. Sets error contingency.
        sys.exit('Quadrants misaligned - error in transformation')  # Exits code and displays string.
    sin = math.sin(azmth_rad_cor)  # Calculates sine of azimuth.
    cos = math.cos(azmth_rad_cor)  # Calculates cosine of azimuth.
    if display == 1:  # Conditional statement. For display.
        deg_sign = chr(176)  # Defines variable. Creates degree sign object.
        if abs(azmth_deg_dff) > 5:  # Conditional statement. Displays objects if threshold met.
            print('Transect orientation' + '\n Quadrant' + '\n  Measured: ' + str(qdrnt_meas) + '\n  Calculated: ' +
                  str(qdrnt_clc) + '\n Field bearing: ' + bearing_reference_direction + str(bearing_deg) + deg_sign +
                  bearing_angle_direction + '\n Azimuth' + '\n  Field: ' + str('%.2f' % azmth_rad_meas) + ' (' +
                  str('%.1f' % azmth_deg_meas) + deg_sign + ')' + '\n  Calculated: ' + str('%.2f' % azmth_rad_clc) +
                  ' (' +  str('%.1f' % azmth_deg_clc) + deg_sign + ')' + '\n   Transformed: ' +
                  str('%.2f' % azmth_rad_cor) + ' (' + str('%.1f' % azmth_deg_cor) + deg_sign + ')' +
                  '\n  Difference: ' + '\033[0;31m' + str('%.2f' % azmth_rad_dff) + ' (' + str('%.1f' % azmth_deg_dff)
                  + deg_sign + ')' + '\033[0m' + '\n Trig. components' + '\n  Sine: ' + str('%.4f'%sin) +
                  '\n  Cosine: ' + str('%.4f'%cos))  # Displays objects.
        else:  # Conditional statement. Displays objects if threshold met.
            print('Transect orientation' + '\n Quadrant' + '\n  Measured: ' + str(qdrnt_meas) + '\n  Calculated: ' +
                  str(qdrnt_clc) + '\n Field bearing: ' + bearing_reference_direction + str(bearing_deg) + deg_sign +
                  bearing_angle_direction + '\n Azimuth' + '\n  Field: ' + str('%.2f' % azmth_rad_meas) + ' (' +
                  str('%.1f' % azmth_deg_meas) + deg_sign + ')' + '\n  Calculated: ' + str('%.2f' % azmth_rad_clc) +
                  ' (' + str('%.1f' % azmth_deg_clc) + deg_sign + ')' + '\n   Transformed: ' +
                  str('%.2f' % azmth_rad_cor) + ' (' + str('%.1f' % azmth_deg_cor) + deg_sign + ')' +
                  '\n  Difference: ' + '\033[0;36m' + str('%.2f' % azmth_rad_dff) + ' (' + str('%.1f' % azmth_deg_dff)
                  + deg_sign + ')' + '\033[0m' + '\n Trig. components' + '\n  Sine: ' + str('%.4f' % sin) +
                  '\n  Cosine: ' + str('%.4f' % cos))  # Displays objects.
    return sin, cos  # Ends function execution.

def find_exp(value):  # Defines function. For retrieving exponent of value.
    bs10 = math.log10(value)  # Defines variable. Retrieves base 10 log of value.
    return math.floor(bs10)  # Defines variable. Rounds value to nearest integer.

def coordinate_error(x1, x2, y1, y2, transect_length, display):  # Defines function. For coordinate geometry error
    # analysis. Compares transect lengths from the field and calculated coordinates.
    dlta_x = x2 - x1  # Defines variable. Calculates difference in x coordinate for measurement limits of transect.
    dlta_y = y2 - y1  # Defines variable. Calculates difference in y coordinate for measurement limits of transect.
    dlta_off = math.sqrt(dlta_x ** 2 + dlta_y ** 2)  # Defines variable. Calculates line difference between
    # coordinates.
    prcnt_dff = (abs(transect_length - dlta_off)) / transect_length * 100  # Defines variable. Calculates percent
    # difference between measured and calculated transect lengths.
    exp = find_exp(prcnt_dff)  # Defines variable. Retrieves exponent of percent difference.
    if display == 1:  # Conditional statement. For display.
        print('Change in' + '\n X: ' + str('%.2f' % dlta_x) + '\n Y: ' + str('%.2f' % dlta_y) + '\n Length' +
              '\n  Measured: ' + str('%.2f' % transect_length) + '\n  Calculated: ' + str('%.2f' % dlta_off) +
              '\n  Percent difference: ' + str('%.2f' % prcnt_dff) + '%' + ' (First nonzero at ' + str(exp) +
              ' decimal place)')  # Displays objects.
    return prcnt_dff  # Ends function execution.

def plot_scatter(plot_number, figure_size, x, y, label, color, edge_color, marker, marker_size, line_width, alpha,
                show_legend, location, marker_scale, frame_alpha, label_spacing, aspect, adjustible, fontsize_ticks,
                fontsize_axis, label_pad, x_label, y_label, title, pause, pause_length):  # Defines function. For
    # scatter plotting.
    plt.figure(plot_number, figsize=figure_size)  # Creates plot window. Sets figure size.
    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
    ax.scatter(x, y, label=label, c=color, edgecolors=edge_color, marker=marker, s=marker_size, linewidth=line_width,
               alpha=alpha)  # Creates scatter plot. Sets display format.
    if show_legend == 1:  # Conditional statement. Shows legend if desired for single line plotting.
        ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)
        # Creates legend. Through automatic label detection.
    ax.set_aspect(aspect, adjustible)  # Sets aspect of axis scaling.
    plt.xticks(fontsize=fontsize_ticks)  # Sets x-axis ticks. Sets format.
    plt.xlabel(x_label, fontsize=fontsize_axis, labelpad=label_pad)  # Creates x-axis label. Sets format.
    plt.ylabel(y_label, fontsize=fontsize_axis)  # Creates y-axis label. Sets format.
    plt.yticks(fontsize=fontsize_ticks)  # Sets y-axis ticks. Sets format.
    plt.title(title)  # Creates plot title.
    if pause == 1:  # Conditional statement. For display format.
        plt.pause(pause_length)  # Displays plot. For set interval of seconds and closes without clearing.
    elif pause == 0:  # Conditional statement. For display format.
        plt.show()  # Displays plot. Indefinite and cleared upon close.
    else:  # Conditional statement. For display format
        pass  # Pass command. Moves on to next line.

def interpolate_cross_section(type, x, y, start, end, interpolation_type, step, decimal_place, display):  # Defines
    # function. For interpolating cross-sections for comparison.
    x = np.around(x, decimals=decimal_place)  # Redefines array. Rounds decimal places for interpolation within bounds.
    y = np.around(y, decimals=decimal_place)  # Redefines array. Rounds decimal places for interpolation within bounds.
    f = sc.interpolate.interp1d(x, y, kind=interpolation_type)  # Sets interpolation format.
    if type == 'DataFrame':  # Conditional statement.
        x_lst = x.tolist()  # Defines list. Converts DataFrame to list.
        start = x_lst[0]  # Defines variable. Selects first element of list.
        end = x_lst[-1]  # Defines variable. Selects first element of list.
    elif type == 'List':  # Conditional statement.
        start = x[0]  # Defines variable. Selects first element of list.
        end = x[-1]  # Defines variable. Selects first element of list.
    elif type == 'Limits':  # Conditional statement.
        pass  # Executes nothing. Moves on to next line.
    new_end = end + step  # Defines variable. Resets end of range so array includes final input value.
    x_intrpltd = np.arange(start, new_end, step)  # Defines array. Creates x array to interpolate y values.
    if x_intrpltd[-1] > end:  # Conditional statement. Forces x to interpolate between true range.
        x_intrpltd = x_intrpltd[0:-1]  # Defines array. Slices array to include all but last element.
    if x_intrpltd[-1] == end:  # Conditional statement. Forces x to interpolate between true range.
        pass  # Pass command. Moves on to next line.
    x_intrpltd = np.around(x_intrpltd, decimals=decimal_place)  # Redefines array. Rounds values.
    y_intrpltd = f(x_intrpltd)  # Sets function format. Interpolates y based on x.
    x_rng_intrpltd = x_intrpltd[-1] - x_intrpltd[0]  # Defines variable. Calculates x range.
    nmbr_smpls = len(x_intrpltd)  # Defines variable. Calclates number of measurements.
    if display == 1:  # Conditional Statement. For Display.
        print('Interpolated datasets' + '\n  Limits: ' + str(start) + '–' + str(end) + '\n  Number of measurements: '
              + str(nmbr_smpls))  # Displays objects.
    return x_intrpltd, y_intrpltd, x_rng_intrpltd  # Ends function execution.

def get_coordinate_pairs(type, value1, value2, x_list, y1_list, y2_list, display):  # Defines function. For retrieving
    # coordinate pairs from interpolated datasets for looped calculations.
    if type == 'Depth':  # Conditional statement. Selects two coordinates on one x value.
        x1 = x_list[value1]  # Defines variable. Selects list element by index.
        y1_top = y1_list[value1]  # Defines variable. Selects list element by index.
        y1_btm = y2_list[value1]  # Defines variable. Selects list element by index.
        if display == 1:  # Conditional statement. For display.
            print('Coordinates' + '\n  Top: ' + '(' + str(x1) + ', ' + str('%.2f' % y1_top) + ')' + '\n  Bottom: ' +
                  '(' + str(x1) + ', ' + str('%.2f' % y1_btm) + ')')  # Displays objects.
        return x1, y1_top, y1_btm  # Ends function execution.
    if type == 'Area':  # Conditional statement. Selects two coordinates on two x values.
        x1 = x_list[value1]  # Defines variable. Selects list element by index.
        x2 = x_list[value2]  # Defines variable. Selects list element by index.
        y1_top = y1_list[value1]  # Defines variable. Selects list element by index.
        y1_btm = y2_list[value1]  # Defines variable. Selects list element by index.
        y2_top = y1_list[value2]  # Defines variable. Selects list element by index.
        y2_btm = y2_list[value2]  # Defines variable. Selects list element by index.
        if display == 1:  # Conditional statement. For display.
            print('Coordinates' + '\n  Top: ' + '(' + str(x1) + ', ' + str('%.2f' % y1_top) + ')' + ' & ' + '(' +
                  str(x2) + ', ' + str('%.2f' % y2_top) + ')' + '\n  Bottom: ' + '(' + str(x1) + ', ' +
                  str('%.2f' % y1_btm) + ')' + ' & ' + '(' + str(x2) + ', ' + str('%.2f' % y2_btm) + ')')  # Displays
            # objects.
        return x1, x2, y1_top, y1_btm, y2_top, y2_btm  # Ends function execution.

def sediment_thickness(y1_top, y1_btm, yr1, yr2, display_label, display):  # Defines function. For
    # calculating sediment thickness between cross-sections.
    dpth1 = y1_top - y1_btm  # Defines variable. Calculates depth at a point.
    if dpth1 > 0:  # Conditional statement. Characterizes depth measurement by surface process.
        prcs1 = 'Deposition'  # Defines variable as string. Identifies depth measurement as depositional.
        prcs_rt1 = 'Aggradation'  # Defines variable as string. Identifies depth rate measurement as aggradational.
    elif dpth1 < 0:  # Conditional statement.
        prcs1 = 'Erosion'  # Defines variable as string. Identifies depth measurement as erosional.
        prcs_rt1 = 'Denudation'  # Defines variable as string. Identifies depth rate measurement as denudational.
    else:  # Conditional statement.
        prcs1 = 'No net change'  # Defines variable as string.
        prcs_rt1 = 'No net change'  # Defines variable as string.
    if yr2 == '1850s':  # Conditional statement. Prepares calculation of time step.
        yr2 = 1854  # Defines variable.
    else:  # Conditional statement. Prepares calculation of time step.
        pass  # Pass command. Moves on to next line.
    tm_intrvl = yr1 - yr2  # Defines variable. Calculates sedimentation time step.
    dpth_rt1 = dpth1 / tm_intrvl  # Defines variable. Calculates sedimentation rate.
    if display == 1:  # Conditional statement. For display.
        print(display_label + str(tm_intrvl) + ' years' + '\n ' + prcs1 + ': ' + str('%.5f' % dpth1) + '\n ' +
              prcs_rt1 + ': ' + str('%.5f' % dpth_rt1))  # Displays objects.
    return dpth1, prcs1, dpth_rt1, prcs_rt1, tm_intrvl  # Ends function execution.

def create_appended_list(value, display_label1, new_list, display_label2, display):  # Defines function. For post
    # calculation list collection.
    try:  # Checks program for object. Takes action based off existence.
        value  # Defines object to be searched for.
    except NameError:  # Executed if object does not exist.
        sys.exit('Error: ' + display_label1 + 'value undefined')  # Exits code and displays string.
    else:  # Executed if object does exist.
        new_list.append(value)  # Appends list.
    if display == 1:  # Conditional statement. For display.
        print(display_label2 + str(new_list))  # Displays objects.
    return new_list  # Ends function execution.

def create_DataFrame(array1, array2, display_label, display):  # Defines function. For creating DataFrame from arrays
    # or lists.
    df_new = pd.DataFrame(data=array1, columns=array2)  # Defines function format.
    if display == 1:  # Conditional statement. For display.
        print('\033[1m' + display_label + ' DATA' + '\033[0m', '\n...\n', df_new, '\n')  # Displays objects.
    return df_new  # Ends function execution.

# ======================================================================================================================
# END ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

# if abs(offst_dff) >= 1:
        #     print(' Coordinate offset' + '\n  X: ' + str('%.2f'%delta_x) + '\n  Y: ' + str('%.2f'%delta_y) +'\n  Measured: ' + str('%.1f' % offst_meas) + '\n  Calculated: ' + str('%.1f' % offst_clc) + '\n  Difference: ' + '\033[0;31m' + str('%.1f' % offst_dff) + '\033[0m')
        # else:
        #     print(' Coordinate offset' +'\n  X: ' + str('%.2f'%delta_x) + '\n  Y: ' + str('%.2f'%delta_y) +'\n  Measured: ' + str('%.1f' % offst_meas) + '\n  Calculated: ' + str('%.1f' % offst_clc) + '\n  Difference: ' + '\033[0;36m' + str('%.1f' % offst_dff) + '\033[0m')
# offst_dff = offst_clc - offst_meas  # Defines variable. Calculates difference in calculated and measured transect
    # lengths.
# offst_meas = c2 - c1  # Defines variable. Calculates transect offset between benchmark positions.
    # offst_meas = offst_meas * 1 / 3.281  # Redefines variable. Converts to meters.

# location = ['upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right', 'center', 'best']  # Defines list. Complete list of matplotlib legend placements.
# ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes for ultramarine, indigo, magenta, orange, and gold.
# ibm_clr_hx = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']  # Defines list. Sets IBM colorblind friendly palette in color hex color codes for ultramarine, indigo, magenta, orange, and gold.
# ibm_clr_rgb = [(100, 143, 255), (120, 94, 240), (220, 38, 127), (254, 97, 0), (255, 176, 0)]
# Sets muted Tol colorblind friendly palette in color hex color codes for indigo, cyan, teal, green, olive, sand, rose, wine, purple, and pale grey.
# 2008 = 0, 1994 = 3, 1978 = 2, 1975 = 4, 1964 = 5, 1939 = 6, 1850S = 7.
# tol_vibrant = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', '#BBBBBB']  # Defines list. Sets
# vibrant Tol colorblind friendly palette in color hex color codes for blue, cyan, teal, orange, red, magenta, grey.
# marker_mpltlib = ['.', ',', 'o', 'v', '^', '<', '>',
#                           '1', '2', '3', '4', '8',
#                           's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd',
#                           '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ' ']  # Defines list. Complete list of matplotlib plot markers.
# tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDD']  # Defines list. Sets Paul Tol muted colorblind friendly palette via hex color codes.
# lin_styls = ['solid', 'dotted', 'dashed', 'dashdot']
# TEMPORARY FUNCTION HOUSING ===========================================================================================

def sedimentation(type, y1_top, y1_btm, yr1, yr2, y2_top, y2_btm, display_label, display):  # Defines function. For calculating sediment thickness between cross-sections.
    if type == 'Depth':  # Conditional statement. Calculates 1D sedimentation.
        dpth1 = y1_top - y1_btm  # Defines variable. Calculates depth at a point.
        if dpth1 > 0:  # Conditional statement. Characterizes depth measurement by surface process.
            prcs1 = 'Deposition'  # Defines variable as string. Identifies depth measurement as depositional.
            prcs_rt1 = 'Aggradation'  # Defines variable as string. Identifies depth rate measurement as aggradational.
        elif dpth1 < 0:  # Conditional statement.
            prcs1 = 'Erosion'  # Defines variable as string. Identifies depth measurement as erosional.
            prcs_rt1 = 'Denudation'  # Defines variable as string. Identifies depth rate measurement as denudational.
        else:  # Conditional statement.
            prcs1 = 'No net change'  # Defines variable as string.
            prcs_rt1 = 'No net change'  # Defines variable as string.
        if survey_year2 == '1850s':  # Conditional statement. Prepares calculation of time step.
            yr2 = 1854  # Defines variable.
        else:  # Conditional statement. Prepares calculation of time step.
            pass  # Pass command. Moves on to next line.
        tm_intrvl = yr1 - yr2  # Defines variable. Calculates sedimentation time step.
        dpth_rt1 = dpth1 / tm_intrvl  # Defines variable. Calculates sedimentation rate.
        if display == 1:  # Conditional statement. For display.
            print(display_label + str(srvy_intrvl) + ' years' + '\n ' + prcs1 + ': ' + str('%.5f' % dpth1) + '\n ' +
                  prcs_rt1 + ': ' + str('%.5f' % dpth_rt1))  # Displays objects.
        return dpth1, prcs1, dpth_rt1, prcs_rt1, tm_intrvl  # Ends function execution.
    if type == 'Area':  # Conditional statement.
        dpth1 = y1_top - y1_btm  # Defines variable. Calculates depth at a point.
        if dpth1 > 0:  # Conditional statement. Characterizes depth measurement by surface process.
            prcs1 = 'Deposition'  # Defines variable as string. Identifies depth measurement as depositional.
        elif dpth1 < 0:  # Conditional statement.
            prcs1 = 'Erosion'  # Defines variable as string.
        elif dpth1 == 0:  # Conditional statement.
            prcs1 = 'No net change'  # Defines variable as string.
        dpth2 = y2_top - y2_btm  # Defines variable. Calculates depth at a point.
        if dpth2 > 0:  # Conditional statement.
            prcs2 = 'Deposition'  # Defines variable as string.
        elif dpth2 < 0:  # Conditional statement.
            prcs2 = 'Erosion'  # Defines variable as string.
        elif dpth2 == 0:  # Conditional statement.
            prcs2 = 'No net change'  # Defines variable as string.
        if display == 1:  # Conditional Statement. For display.
            print(display_label1 + '\n  x1: ' + str('%.5f' % dpth1) + ' (' + prcs1 + ')' + '\n  x2: ' + str('%.5f' % dpth2) + ' (' + prcs2 + ')')  # Displays objects.
        return dpth1, dpth2, prcs1, prcs2  # Ends function execution.



def reverse_range(start, end, step, display_label, display):  # Defines function. For generating reverse array between two numbers.
    end = end - 1  # Defines variable. Resets end of range so array includes final input value.
    end_label = end + 1  # Defines variable. For display.
    rev_rng = np.arange(start, end, step)  # Defines function format.
    if display == 1:  # Conditional statement. For display.
        print(display_label + '\n  Limits: ' + str(start) + ' & ' + str(end_label) + ' --> List:', rev_rng)  # Displays objects.
    return rev_rng  # Ends function execution.












def name_levels(directory_levels, folder_labels, output_folder, display_label,
                display):  # Defines function. For defining list of directory levels for looped creation.
    index = np.arange(0, directory_levels, 1)  # Defines array. Index values for looped naming.
    for a in index:  # Begins loop through array elements. Loops through indices.
        folder_name = folder_labels[a]  # Defines variable as array element. Selects name of folder.
        if a == 0:  # Conditional statement. Executes lines if element is first.
            level_a = output_folder + folder_name  # Defines string. Builds path directory from folder name.
            levels = [level_a]  # Defines list.
        elif a != 0:  # Conditional statement. Executes lines if element is not first.
            level_a = level_a + folder_name  # Defines string. Builds path directory from folder name.
            levels.append(level_a)  # Redefines list. Appends with new element.
        if display == 1:  # Conditional statement. For display.
            print(display_label, levels)  # Display objects.
    return levels  # Ends function execution.







def hydraulic_geometry(dataframe, column1, display_label1, display_label2, display_label3, units,
                       display_label4, column2, display_label5, display_label6, display_label7,
                       display_label8, display):  # Defines function. For hydraulic geometry calculation.
    # Channel width
    df_strm_offst = slice_DataFrame_columns(dataframe, column1, 0, display_label1, 0)  # Defines DataFrame.
    # Calls function. Slices DataFrame to yield stream channel survey offsets.
    offst1 = min_value_DataFrame(df_strm_offst, display_label2, 0)  # Defines variable. Slices DataFrame
    # to yield first offset for stream channel.
    offst2 = max_value_DataFrame(df_strm_offst, display_label2, 0)  # Defines variable. Slices DataFrame
    # to yield last offset for stream channel.
    if offst1 < offst2:  # Conditional statement. Sets order of channel width calculation.
        wdth = offst2 - offst1  # Defines variable. Calculates channel width.
    elif offst1 > offst2:  # Conditional statement. Sets error contingency.
        sys.exit('Error: No stream channel detected')  # Exits code and displays string.
    elif offst1 == offst2:  # Conditional statement. Sets error contingency.
        sys.exit('Error: No stream channel detected')  # Exits code and displays string.
    if display == 1:  # Conditional statement. For display.
        print(display_label3 + units + '\n  ' + display_label4 + '%.1f' % wdth)  # Displays objects.
    # Channel depth
    df_strm_elvtn = slice_DataFrame_columns(dataframe, column2, 0, display_label5, 0)  # Defines DataFrame.
    # Slices DataFrame to yield stream channel survey elevations.
    elvtn1 = min_value_DataFrame(df_strm_elvtn, display_label6, 0)  # Defines variable. Slices DataFrame
    # to yield lowest elevation for stream channel.
    elvtn2 = max_value_DataFrame(df_strm_elvtn, display_label6, 0)  # Defines variable. Slices DataFrame
    # to yield highest elevation for stream channel.
    if elvtn1 < elvtn2:  # Conditional statement. Sets order of channel depth calculation.
        dpth = elvtn2 - elvtn1  # Defines variable. Calculates channel depth.
    elif elvtn1 > elvtn2:  # Conditional statement. Sets error contingency.
        sys.exit('Error: No stream channel detected')  # Exits code and displays string.
    elif elvtn1 == elvtn2:  # Conditional statement. Sets error contingency.
        sys.exit('Error: No stream channel detected')  # Exits code and displays string.
    elif elvtn1 | elvtn2 <= 0:  # Conditional statement. Sets error contingency.
        sys.exit('Error: No stream channel detected')  # Exits code and displays string.
    if display == 1:  # Conditional statement. For display.
        print('  ' + display_label7 + '%.2f' % dpth)  # Displays objects.
    # Hydraulic radius
    hydro_rad = (wdth * dpth) / (wdth + 2 * dpth)  # Defines variable. Calculated hydraulic radius.
    if display == 1:  # Conditional statement. For display.
        print('  ' + display_label8 + '%.2f' % hydro_rad)  # Displays objects.
    return wdth, dpth, hydro_rad  # Ends function execution.

def select_coincident_x_range(type, x1, x2, units,
                              display):  # Defines function. For selecting coincident x values for reinpterpolation.
    if type == 'dataframe':  # Conditional statement. Executes lines below when input object is DataFrame.
        x1_list = x1.tolist()  # Defines list. Converts DataFrame to list.
        x2_list = x2.tolist()  # Defines list. Converts DataFrame to list.
    elif type == 'list':  # Conditional statement. Executes lines below when input object is list.
        x1_list = x1  # Defines list.
        x2_list = x2  # Defines list.
    x_min1 = x1_list[0]  # Defines variable. Selects lowest x value in list.
    x_max1 = x1_list[-1]  # Defines variable. Selects largest x value in list.
    x_min2 = x2_list[0]  # Defines variable. Selects lowest x value in list.
    x_max2 = x2_list[-1]  # Defines variable. Selects largest x value in list.
    if x_min1 == x_min2:  # Conditional statement. Selects limits shared between datasets.
        start = x_min1  # Defines variable. Sets first shared x value.
        if x_max1 == x_max2 or x_max1 < x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max1  # Defines variable. Sets last shared x value.
        elif x_max1 > x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max2  # Defines variable. Sets last shared x value.
    elif x_min1 < x_min2:  # Conditional statement.  Selects limits shared between datasets.
        start = x_min2  # Defines variable. Sets first shared x value.
        if x_max1 == x_max2 or x_max1 < x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max1  # Defines variable. Sets last shared x value.
        elif x_max1 > x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max2  # Defines variable. Sets last shared x value.
    elif x_min1 > x_min2:  # Conditional statement.  Selects limits shared between datasets.
        start = x_min1  # Defines variable. Sets first shared x value.
        if x_max1 == x_max2 or x_max1 < x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max1  # Defines variable. Sets last shared x value.
        elif x_max1 > x_max2:  # Conditional statement.  Selects limits shared between datasets.
            end = x_max2  # Defines variable. Sets last shared x value.
    coincident_range = end - start  # Defines variable. Calculates coincident range between datasets.
    if display == 1:  # Conditional statement. For display.
        print('Coincident x values ' + '\n  X min: ' + str(x_min1) + ' & ' + str(x_min2) +
              '\n  X max: ' + str(x_max1) + ' & ' + str(x_max2) + '\n  Range: ' + str(
            start) + '–' + str(end) + ' (' + str('%.2f' % coincident_range) + units + ')')  # Displays objects.
    return start, end, coincident_range  # Ends function execution.



def plot_fill(number, zones, x, y1, y2, label, face_color, alpha, location, marker_scale, frame_alpha, label_spacing, pause, pause_length):
    plt.figure(number)  # Calls figure. Makes it the active plot.
    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
    if zones == 1:  # Conditional statement. For shading 1 area.
        ax.fill_between(x, y1, y2, label=label, facecolor=face_color, alpha=alpha)  # Fills area over x range between y values.
        ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)  # Creates legend. Through automatic label detection.
    if zones != 1:  # Conditional statement. For shading multiple areas.
        zones = zones + 1  # Defines variable. For establishing looped plotting framework.
        zone_list = range(1, zones, 1)  # Defines list. Creates range of integers for looped plotting.
        for a in zone_list:  # Begins loop through list elements. Loops through line numbers.
            index = zone_list.index(a)  # Defines variable. Retrieves index of element in list. For format selection.
            ax.fill_between(x, y1[index], y2[index], label=label[index], facecolor=face_color[index], alpha=alpha)  # Fills area over x range between y values.
            ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha, labelspacing=label_spacing)  # Creates legend. Through automatic label detection.
    if pause == 1:  # Conditional statement. For display format.
        plt.pause(pause_length)  # Displays plot. For set interval of seconds and closes without clearing.
    elif pause == 0:  # Conditional statement. For display format.
        plt.show()  # Displays plot. Indefinite and cleared upon close.

#*****************************************************************************************************************************


def sediment_area_trpz(x1, x2, height_R, height_L, display_label, display):
    if x1 > x2:
        x_R = x1
        x_L = x2
    elif x1 < x2:
        x_L = x1
        x_R = x2
    delta_x = x_R - x_L
    trpz_area = ((height_R + height_L) / 2) * delta_x
    if trpz_area > 0:
        prcs = 'Deposition'
    if trpz_area < 0:
        prcs = 'Erosion'
    if trpz_area == 0:
        prcs = 'No net change'
    if display == 1:
        print(display_label + '%.10f' % trpz_area + ' (' + prcs + ')')
    return trpz_area, prcs

#$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%nother day
def check_for_empties(dataframe, display):
    result = dataframe.empty
    if display == 1:
        print('Empty = ', result)
    return result


def mean_plus_stdv(array, display_label1, display):
    avg = np.mean(array)
    stdv = np.std(array)
    strt = avg - stdv
    end = avg + stdv
    if display == 1:
        print(display_label1 + '\n  Mean: ' + str('%.2f' % avg) + '\n  Standard deviation: ' + str(
            '%.4f' % stdv) + '\n  Range: ' + str('%.2f' % strt) + '–' + str('%.2f' % end))
    return avg, stdv, strt, end

#^^^^^^^^^^^^^^^^^^^^^^^^^nother day
def find_intersection(x1, x2, y1_1, y1_2, y2_1, y2_2, display):
    slpe1 = (y1_2 - y1_1) / (x2 - x1)
    b1_a = y1_1 - slpe1 * x1
    b1_b = y1_2 - slpe1 * x2
    b1_a = round(b1_a, 5)
    b1_b = round(b1_b, 5)
    if bool(b1_a == b1_b) == True:
        b1 = b1_a
    elif bool(b1_a == b1_b) == False:
        sys.exit('Error: Intercepts do not coincide')
    slpe2 = (y2_2 - y2_1) / (x2 - x1)
    b2_a = y2_1 - slpe2 * x1
    b2_b = y2_2 - slpe2 * x2
    b2_a = round(b2_a, 5)
    b2_b = round(b2_b, 5)
    if bool(b2_a == b2_b) == True:
        b2 = b2_a
    elif bool(b2_a == b2_b) == False:
        print('\n', b2_a, b2_b)
        sys.exit('Error: Intercepts do not coincide')
    x_test = (b1 - b2) / (slpe2 - slpe1)
    if x1 <= x_test <= x2:
        y1_test = slpe1 * x_test + b1
        y2_test = slpe2 * x_test + b2
        y1_test = round(y1_test, 5)
        y2_test = round(y2_test, 5)
        if bool(y1_test == y2_test) == True:
            y_test = y1_test
            intrsctn = 'Exists'
            if display == 1:
                print('Intersection found' + '\n  Between: ' + str(x1) + '–' + str(x2) + '\n  At: ' + '(' + str(x_test) + ', ' + str(y_test) + ')')
        elif bool(y1_test == y2_test) == False:
            sys.exit('Error: No intersection found at shared point')
    elif x1 > x_test or x2 < x_test:
        # print('No intersection between ' + str(x1) + '–' + str(x2))
        x_test = None
        y_test = None
        intrsctn = None
    return x_test, y_test, intrsctn
#^^^^^^^^^^^^^^^^^^^^^***********nother day
def sediment_volume(type, area1, area2, area_prime, area_quad, separation, width1, width2, display_label, display):
    if type == 'Average end area':
        # average end area
        V = (area1 + area2) / 2 * separation
    elif type == 'Prismoidal':
        # prismoidal
        V = (area_prime / 3) * ((area1 + area2) / (width1 + width2)) + (area_quad / 3) * ((area1 / width1) + (area2 / width2))
    if V < 0:
        prcs = 'Erosion'
    elif V > 0:
        prcs = 'Deposition'
    elif V == 0:
        prcs = 'No net change'
    if display == 1:
        print(display_label + str('%.2f' % V) + ' (' + prcs + ')')
    return V, prcs
#%%%%%%%%%%%%%%

# ibm = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']
#
# # convert hex to rgb
#
# x = np.arange(0, np.pi, 0.1)
# y = np.arange(0, 2 * np.pi, 0.1)
# X, Y = np.meshgrid(x, y)
# Z = np.cos(X) * np.sin(Y) * 10
#
# clr1=matplotlib.colors.to_rgb('#648FFF')
# clr1=matplotlib.colors.to_rgb('#785EF0')
# clr2=matplotlib.colors.to_rgb('#FFB000')
# colors=[clr1,clr2]
# n_bins = [3, 6, 10, 100]
# cmap_name = 'my_list'
# fig, axs = plt.subplots(2, 2, figsize=(6, 9))
# fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.05)
# for n_bin, ax in zip(n_bins, axs.ravel()):
#
#     cm = LinearSegmentedColormap.from_list(
#         cmap_name, colors, N=n_bin)
#     im = ax.imshow(Z, interpolation='nearest', origin='lower', cmap=cm)
#     ax.set_title("N bins: %s" % n_bin)
#     fig.colorbar(im, ax=ax)

