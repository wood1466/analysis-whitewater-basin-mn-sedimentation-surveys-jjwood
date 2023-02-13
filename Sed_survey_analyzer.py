# ======================================================================================================================
# WHITEWATER RIVER VALLEY MINNESOTA - SEDIMENTATION SURVEY DATA ANALYSIS * ---------------------------------------------
# PRIMARY PROGRAM * ----------------------------------------------------------------------------------------------------
# ======================================================================================================================

# SIGNAL START ---------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START SEDIMENTATION ANALYSES!!!' + '\033[0m', '\n...\n')  # Displays objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

import time, os, sys  # Imports "Time and access conversions" and "Miscellaneous operating system interfaces". Enables use
# of various time–related functions and operating system dependent functionality.
import pandas as pd, numpy as np, matplotlib.pyplot as plt  # Imports "Python data analysis library" with alias. Enables DataFrame array functionality.

# START TIMER ----------------------------------------------------------------------------------------------------------

strtTm0 = time.time()  # Starts clock. Measures program run time.

# FUNCTIONS FOR NOW
def plot_lines(lines, plot_number, figure_size, x, y, label, color, marker, marker_size,
               line_width, alpha, fontsize_ticks, x_label, fontsize_axis, label_pad, y_label,
               title, pause_length,
               pause, location, marker_scale, frame_alpha,
               label_spacing):  # Defines function. For single cross-section plotting.
    plt.figure(plot_number, figsize=figure_size)  # Creates plot window.
    ax = plt.gca()  # Defines variable. Retrieves plot axes instance.
    if lines == 1:
        ax.plot(x, y, label=label, c=color, marker=marker, markersize=marker_size,
                linewidth=line_width,
                alpha=alpha)  # Creates line plot of arrays from axes instance. Sets format.
    if lines != 1:
        lines = lines + 1
        line_list = range(1, lines, 1)
        print(*line_list)
        for i in line_list:
            index = line_list.index(i)
            ax.plot(x[index], y[index], label=label[index], c=color[index],
                    marker=marker[index], markersize=marker_size, linewidth=line_width,
                    alpha=alpha)  # Creates line plot of arrays from axes instance. Sets format.
        ax.legend(loc=location, markerscale=marker_scale, framealpha=frame_alpha,
                  labelspacing=label_spacing)  # Creates legend. Through automatic label detection.
    plt.xticks(fontsize=fontsize_ticks)  # Sets x-axis tick mark format.
    plt.xlabel(x_label, fontsize=fontsize_axis,
               labelpad=label_pad)  # Creates x-axis label. Sets format.
    plt.ylabel(y_label,
               fontsize=fontsize_axis)  # Creates x-axis label. Sets format.  # Creates y-axis label. Sets font size.
    plt.yticks(fontsize=fontsize_ticks)  # Sets y-axis tick mark format.
    plt.title(title)  # Creates plot title.

    if pause == 1:  # Conditional statement. For display.
        plt.pause(
            pause_length)  # Displays plot. For set interval of seconds and closes without clearing.
    elif pause == 0:  # Conditional statement. For display.
        plt.show()  # Displays plot. Indefinite and cleared upon close.

def create_folder(level, path):  # Defines function. For generating directory paths.
    if not os.path.exists(path):  # Checks if folder exists. Skips step if exists.
        os.mkdir(path)  # Creates folder if it does not exist.
        print('New directory level', level, '\033[0;32m' + path + '\033[0m', 'created')  # Displays objects.

def upload_csv(path, label, dsply):  # Defines function. For uploading .csv and conversion to DataFrame.
    csv_data = pd.read_csv(path)  # Uploads .csv file. Input data.
    df = pd.DataFrame(csv_data)  # Converts .csv file to DataFrame. For Python manipulation.
    pd.set_option('display.max_columns', None)  # Adjusts DataFrame format. Displays all DataFrame columns.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + 'UPLOADED .CSV DATA FOR ' + label + '\033[0m', '\n...\n', df, '\n')  # Displays objects.
    return df  # Ends execution of function.

def forward_range(start, end, step, data_label, dsply):  # Defines function. For generating forward range array between two numbers.
    end = end + 1  # Defines variable. Sets end of range to include final input value.
    end_label = end - 1  # Defines variable. Sets label for display.
    frwd_rng = np.arange(start, end, step)  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label, start, '&', end_label, ':', frwd_rng)  # Displays objects.
    return frwd_rng  # Ends execution of function.

def reverse_range(start, end, step, data_label, dsply):  # Defines function. For generating forward range array between two numbers.
    end = end - 1  # Defines variable. Sets end of range to include final input value.
    end_label = end + 1  # Defines variable. Sets label for display.
    rev_rng = np.arange(start, end, step)  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label, start, '&', end_label, ':', rev_rng, '\n')  # Displays objects.
    return rev_rng  # Ends execution of function.

def slice_DataFrame_rows1(dataframe, column, row_value, label, dsply):  # Defines function. For DataFrame slicing by single row value.
    df_slc_r = dataframe[dataframe[column] == row_value]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + label + ' ' + str(row_value) + ' DATA' + '\033[0m', '\n..\n', df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends execution of function.

def slice_DataFrame_rows2(dataframe, column1, row_value1, label1, row_value2, label2,
                          dsply):  # Defines function. For DataFrame slicing by row value.
    df_slc_r = dataframe[dataframe[column1] == row_value1]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + label2 + ' ' + str(row_value2) + ' ' + label1 + ' ' + str(row_value1) + ' DATA' + '\033[0m',
              '\n..\n', df_slc_r, '\n')  # Displays objects.
    return df_slc_r  # Ends execution of function.


def slice_DataFrame_cell(dataframe, column, index, data_label,
                         dsply):  # Defines function. For DataFrame slicing by row value.
    index = dataframe.index
    df_slc_cl = dataframe.loc[index, column]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print(data_label + ':', df_slc_cl, '\n')  # Displays objects.
    return df_slc_cl  # Ends execution of function.

def slice_DataFrame_columns1(dataframe, column, data_label,
                             dsply):  # Defines function. For DataFrame slicing by row value.
    df_slc_c = dataframe[column]  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('\033[1m' + data_label + ' DATA' + '\033[0m', '\n..\n', df_slc_c, '\n')  # Displays objects.
    return df_slc_c  # Ends execution of function.

def max_value_column(dataframe, data_label, units,
                     dsply):  # Defines function. For retrieving maximum value from DataFrame column.
    max = dataframe.max()  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('Maximum column value:', max, data_label, units)  # Displays objects.
    return max  # Ends execution of function.

def min_value_column(dataframe, data_label, units,
                     dsply):  # Defines function. For retrieving minimum value from DataFrame column.
    min = dataframe.min()  # Defines function format.
    if dsply == 1:  # Conditional statement. For display.
        print('Minimum column value:', min, data_label, units)  # Displays objects.
    return min  # Ends execution of function.


def hydraulic_geometry(dataframe, column1, data_label1, data_label2, units, data_label3, data_label4, column2,
                       data_label5, data_label6, data_label7, data_label8, dsply):
    df_strm_offst = slice_DataFrame_columns1(dataframe, column1, data_label1, 0)

    offst1 = min_value_column(df_strm_offst, data_label2, units, 0)
    offst2 = max_value_column(df_strm_offst, data_label2, units, 0)

    if offst1 < offst2:
        wdth = offst2 - offst1
    elif offst1 > offst2:
        sys.exit('No stream channel detected')
    elif offst1 == offst2:
        sys.exit('No stream channel detected')

    if dsply == 1:  # Conditional statement. For display.
        print(data_label3 + units + '\n  ' + data_label4 + '%.1f' % wdth)

    df_strm_elvtn = slice_DataFrame_columns1(dataframe, column2, data_label5, 0)
    elvtn1 = min_value_column(df_strm_elvtn, data_label6, units, 0)
    elvtn2 = max_value_column(df_strm_elvtn, data_label6, units, 0)

    if elvtn1 < elvtn2:
        dpth = elvtn2 - elvtn1
    elif elvtn1 > elvtn2:
        sys.exit('No stream channel detected')
    elif elvtn1 == elvtn2:
        sys.exit('No stream channel detected')
    elif elvtn1 | elvtn2 <= 0:
        sys.exit('Negative values')

    if dsply == 1:  # Conditional statement. For display.
        print('  ' + data_label7 + '%.2f' % dpth)

    hydro_rad = (wdth * dpth) / (wdth + 2 * dpth)

    if dsply == 1:  # Conditional statement. For display.
        print('  ' + data_label8 + '%.2f' % hydro_rad)

    return wdth, dpth, hydro_rad

def create_append_list(value, data_label1, new_list, chck):
    # create lists
    try:
        value
    except NameError:
        sys.exit(data_label1 + 'value undefined')
    else:
        new_list.append(value)
    if chck == 1:
        print(new_list)
    return new_list

def get_color(label):
    if label == '2008':  # Conditional statement. For display.
        color = tol_mtd[0]  # Defines variable. Sets plot color.
    elif label == '1994':  # Conditional statement. For display.
        color = tol_mtd[3]  # Defines variable. Sets plot color.
    elif label == '1978':  # Conditional statement. For display.
        color = tol_mtd[2]  # Defines variable. Sets plot color.
    elif label == '1975':  # Conditional statement. For display.
        color = tol_mtd[4]  # Defines variable. Sets plot color.
    elif label == '1964':  # Conditional statement. For display.
        color = tol_mtd[5]  # Defines variable. Sets plot color.
    elif label == '1939':  # Conditional statement. For display.
        color = tol_mtd[6]  # Defines variable. Sets plot color.
    elif label == '1850s':  # Conditional statement. For display.
        color = tol_mtd[7]  # Defines variable. Sets plot color.
    return color

def get_marker(label):
    if label == '2008':  # Conditional statement. For display.
        marker = mrkr_mpltlib[-1]  # Defines variable. Sets plot marker.
    elif label == '1994':  # Conditional statement. For display.
        marker = mrkr_mpltlib[0]  # Defines variable. Sets plot marker.
    elif label == '1978':  # Conditional statement. For display.
        marker = mrkr_mpltlib[8]  # Defines variable. Sets plot marker.
    elif label == '1975':  # Conditional statement. For display.
        label = mrkr_mpltlib[11]  # Defines variable. Sets plot marker.
    elif label == '1964':  # Conditional statement. For display.
        marker = mrkr_mpltlib[6]  # Defines variable. Sets plot marker.
    elif label == '1939':  # Conditional statement. For display.
        marker = mrkr_mpltlib[2]  # Defines variable. Sets plot marker.
    elif label == '1850s':  # Conditional statement. For display.
        marker = mrkr_mpltlib[-2]  # Defines variable. Sets plot marker.
    return marker

# SET PARAMETERS -------------------------------------------------------------------------------------------------------

# Data operations ------------------------------------------------------------------------------------------------------

# operations on single cross-section
Xsctns_1 = 1
# Calculate channel hydraulic geometry
Hydr_geom = 1  # Defines variable as integer. Sets binary toggle for operation selection.

# Analyze subsequent cross-sections
Xsctns_2 = 0
# Calculate sediment thickness
Dpth = 0  # Defines variable as integer. Sets binary toggle for operation selection.

# Plot data
Xsctn_sngl = 0  # Defines variable as integer. Sets binary toggle for operation selection—plotting a single cross-section.
Xsctn_dbl = 0
Hydr_rad = 0

#General
Exprt=1

# Data selection -------------------------------------------------------------------------------------------------------

# Field ranges
rng_strt = 70  # Defines variable as integer. Sets starting range for analysis.
rng_end = 73  # Defines variable as integer. Sets end range for analysis.

# Range surveys
srvy_strt = 5  # Defines variable as integer. Sets starting survey for analysis.
srvy_end = 2  # Defines variable as integer. Sets end survey for analysis.

# Data plotting --------------------------------------------------------------------------------------------------------

# General format
wdth = 4.5  # Defines variable as integer. Sets cross-sectional plot width.
hght = wdth * 1.618  # Defines variable as integer. Sets cross-sectional plot height.
fig_sz = (hght, wdth)  # Defines object. Input for function.
fntsz_tcks = 8  # Defines variable as integer. Sets font size for axes tick marks.
fntsz_ax = 10  # Defines variable as integer. Sets font size for axis labels.
lbl_pd = 10  # Defines variable as integer. Sets plot-axes label spacing.

# Data display format
tol_mtd = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499', '#DDDDD']  # Defines list.

lin_wdth = 2  # Defines variable as integer. Sets plot line width.
mrkr_mpltlib = ['o', 'v', '^', '<', '>', '8', 's', 'p', 'P', 'h', 'H', 'X', 'D', 'd', ' ']  # Defines list. Complete list of matplotlib plot markers.
mrkr_sz = 4  # Defines variable as integer. Sets plot marker size.
alpha = 0.5  # Defines variable as integer. Sets plotted object transparency.

# Legend display format
lctn = 'best'  # Defines variable as string. Sets legend location on plot.
mrkr_scl = 2  # Defines variable as integer. Sets marker size on legend.
frm_alpha = 0.7  # Defines variable as integer. Sets legend box transparency.
lbl_spcng = 0.7  # Defines variable as integer. Sets legend object spacing.

# Display
ps_lngth = 1  # Defines variable as integer. Sets pause length for display.

# SET UP DIRECTORY -----------------------------------------------------------------------------------------------------

# Name levels ----------------------------------------------------------------------------------------------------------

# Level 1
inpt_fldr = 'Input'  # Defines variable as string. Sets name of new directory where all data sources will be located.
opt_fldr = 'Output'  # Defines variable as string. Sets name of new directory where all data products will be exported.

# Create folders -------------------------------------------------------------------------------------------------------

lvl1_fldrs = [inpt_fldr, opt_fldr]  # Defines list. Inserts folder end paths into list to speed up directory creation via loop.

for a in lvl1_fldrs:  # Begins loop. Loops through each element in list.
    level = 1  # Defines variable. Sets value based in list element index for display.

    create_folder(level, a)  # Creates folders. Calls function.

# ======================================================================================================================
# PART 2: DATA SELECTION -----------------------------------------------------------------------------------------------
# ======================================================================================================================

# UPLOAD DATA ----------------------------------------------------------------------------------------------------------

inpt_fl = '/Users/jimmywood/github/Whitewater_MN_sedimentation/PyCharm_Venv/Input/Trout_Creek_survey_data.csv'  # Defines string. Sets file path.

df_chnnl = upload_csv(inpt_fl, 'TROUT CREEK ', 0)  # Defines DataFrame. Calls function.

# SET DATA SELECTION LIMITS --------------------------------------------------------------------------------------------

# Spatial --------------------------------------------------------------------------------------------------------------

rgn_nums = forward_range(rng_strt, rng_end, 1, 'Range number limits', 0)  # Defines array. Calls function.

# Temporal -------------------------------------------------------------------------------------------------------------

srvy_nums = reverse_range(srvy_strt, srvy_end, -1, 'Survey number limits', 0)  # Defines array. Calls function.

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# By field range -------------------------------------------------------------------------------------------------------

for a in rgn_nums:  # Begins loop for array. Loops through range numbers.

    df_rng = slice_DataFrame_rows1(df_chnnl, 'Range_num', a, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.

    # By range survey --------------------------------------------------------------------------------------------------

    for b in srvy_nums:  # Begins loop. Loos through range numbers.

        df_srvy1 = slice_DataFrame_rows2(df_rng, 'Srvy_num', b, 'SURVEY NUMBER', a, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.

        # Survey metadata --------------------------------------------------------------------------------------------------

        srvy_yr1 = slice_DataFrame_cell(df_srvy1, 'Srvy_year', index[0], 'Survey year', 0)  # Defines variable. Calls function.
        rng_nm1 = slice_DataFrame_cell(df_srvy1, 'Srvy_range', index[0], 'Range', 0)  # Defines variable. Calls function.

        df_srvy_nums = slice_DataFrame_columns1(df_rng, 'Srvy_num', 'Survey numbers', 0)  # Defines DataFrame. Calls function.
        df_srvy_nums = df_srvy_nums.drop_duplicates(keep='first')  # Modifies DataFrame. Drops all duplicate values in column.

        num_srvys = max_value_column(df_srvy_nums, '', '', 0)  # Defines variable. Calls function.

        srvy_dt1 = slice_DataFrame_cell(df_srvy1, 'Srvy_date', index[0], 'Survey date', 0)  # Defines variable. Calls function.
        strm_stat1 = slice_DataFrame_cell(df_srvy1, 'Srvy_stat', index[0], 'Stream station', 0)

        # Byr survey ------------------------------------------------------------------------------------------

        df_offst1 = slice_DataFrame_columns1(df_srvy1, 'Offset_ft', 'OFFSET', 0)  # Defines DataFrame. Calls function.
        df_elvtn1 = slice_DataFrame_columns1(df_srvy1, 'Elv_geo_ft', 'ELEVATION', 0)  # Defines DataFrame. Calls function.

        # DISPLAY DATASET ------------------------------------------------------------------------------------------

        if Xsctns_1 == 1:
            # Metadata ------------------------------------------------------------------------------------------
            print('==================================================')  # Displays objects.
            print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_nm1) + ' (' + str(a) + ')')  # Displays objects.
            print('\033[1m' + 'Stream station: ' + '\033[0m' + str(strm_stat1))  # Displays objects.
            print('\033[1m' + 'Range survey: ' + '\033[0m' + str(srvy_yr1) + ' (' + str(b) + ' of ' + str(num_srvys) + ')')  # Displays objects.
            print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.

            # Plot data ------------------------------------------------------------------------------------------

            if srvy_yr1 == '2008':  # Conditional statement. For display.
                color = tol_mtd[0]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[-1]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1994':  # Conditional statement. For display.
                color = tol_mtd[3]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[0]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1978':  # Conditional statement. For display.
                color = tol_mtd[2]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[8]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1975':  # Conditional statement. For display.
                color = tol_mtd[4]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[11]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1964':  # Conditional statement. For display.
                color = tol_mtd[5]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[6]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1939':  # Conditional statement. For display.
                color = tol_mtd[6]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[2]  # Defines variable. Sets plot marker.
            elif srvy_yr1 == '1850s':  # Conditional statement. For display.
                color = tol_mtd[7]  # Defines variable. Sets plot color.
                marker = mrkr_mpltlib[-2]  # Defines variable. Sets plot marker.

            if Xsctn_sngl == 1:  # Conditional statement. Plots single cross-section.

                title1 = 'Range ' + str(rng_nm1) + ' ' + str(srvy_yr1) + ' survey '  # Defines string. Sets title of plot.
                plot_lines(1,1, fig_sz, df_offst1, df_elvtn1, srvy_yr1, color, marker, mrkr_sz, lin_wdth, alpha,
                            fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title1,
                            ps_lngth, 1,lctn,mrkr_scl,frm_alpha,lbl_spcng)  # Creates plot. Calls function.

            # Export figure
            # Name folders
            # Level 2
            xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
            lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file path.

            # Level 3
            plts_fldr = '/Plots'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
            lvl3 = lvl2 + plts_fldr  # Defines variable as string. Concatenates strings to create file path.

            # Level 4
            xsctn_plts_fldr = '/Cross_sections'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
            lvl4 = lvl3 + xsctn_plts_fldr  # Defines variable as string. Concatenates strings to create file path.

            # Level 5
            xsctn_plts_fldr1 = '/Single'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
            lvl5 = lvl4 + xsctn_plts_fldr1  # Defines variable as string. Concatenates strings to create file path.

            # Create folders
            lvls = [lvl2, lvl3, lvl4, lvl5]  # Defines list. For looping through and conventient folder creation.

            for i in lvls:  # Begins loop. Loops through each element in list.  #
                level = lvls.index(i)  # Defines variable. Sets value based in list element index for display.
                create_folder(level, i)  # Creates folder. Calls function.

            # Export
            if Exprt==1:
                plt.figure(1)  # Calls figure. Makes it the active plot.

                fig_name = '/' + str(rng_nm1) + '_s' +str(b) + '_' + str(srvy_yr1) + '.pdf' # Defines variable as strong. Names figure for export.

                plt.savefig(lvl5 + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

                plt.close()  # Closes active figure.

            # ======================================================================================================================
            # PART 3: DATA ANALYSIS -----------------------------------------------------------------------------------------------
            # ======================================================================================================================

            # Calculated hydro geom -----------------------------------------------------------------------------------------------


            if Hydr_geom == 1: # Conditional statement. Calculates hydraulic geometry.
                df_strm = slice_DataFrame_rows1(df_srvy1, 'Gmrph_dsc', 'Stream channel', 'RANGE ' + str(a), 0)  # Defines DataFrame. Calls function.

                wdth, dpth, hydro_rad = hydraulic_geometry(df_strm, 'Offset_ft', 'RANGE ' + str(a) + ' SURVEY ' + str(b) + ' STREAM CHANNEL OFFSET',
                                   'Offset', ' (ft)', 'Channel dimensions', 'Width: ', 'Elv_geo_ft', 'RANGE ' + str(a) +
                                   ' SURVEY ' + str(b) + ' STREAM CHANNEL ELEVATION', 'Elevation', 'Depth: ',
                                   'Bankfull hydraulic radius: ', 1)

                # collect results

                if a==rng_strt:
                    if b==srvy_strt:
                        rng_nm1_list=[]
                        srvy_yr1_list=[]
                        strm_stat_list=[]
                        hydro_rad_list=[]
                        wdth_list=[]
                        dpth_list=[]
                        hydro_geom_lists=[rng_nm1_list,srvy_yr1_list,strm_stat_list,wdth_list,dpth_list,hydro_rad_list]
                        # df_hydro_geom=pd.DataFrame()

                hydro_geom_list=[rng_nm1, srvy_yr1, strm_stat1, wdth,dpth,hydro_rad]
                hydro_geom_dt_lbl=['Range name', 'Survey year', 'Stream station', 'Width','Depth','Hydraulic radius']
                hydro_geom_clm_lbl=['Srvy_range', 'Srvy_year', 'Strm_stat', 'Chnl_wdth_ft', 'Chnl_dpth_ft', 'Hydro_rad_ft']

                for i in hydro_geom_lists:
                    index=hydro_geom_lists.index(i)
                    i =create_append_list(hydro_geom_list[index], hydro_geom_dt_lbl[index], i, 1)

                hydro_geom_lists = [rng_nm1_list, srvy_yr1_list, strm_stat_list, wdth_list, dpth_list, hydro_rad_list]

                _tmp = np.array(hydro_geom_lists)
                _tmp = _tmp.transpose()

                if a == rng_end:
                    if b == srvy_end:
                        df_hydro_geom = pd.DataFrame(data=_tmp, columns=hydro_geom_clm_lbl)
                        print(df_hydro_geom)

                        # export frame
                        if Exprt==1:
                            # Export figure
                            # Name folders
                            # Level 2
                            xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.

                            # Level 3
                            clcs_fldr = '/Calculations'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                            lvl3 = lvl2 + clcs_fldr  # Defines variable as string. Concatenates strings to create file path.

                            # Level 4
                            h_geom_clcs_fldr = '/Hydraulic_geometry'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                            lvl4 = lvl3 + h_geom_clcs_fldr  # Defines variable as string. Concatenates strings to create file path.

                            # Create folders
                            lvls = [lvl2, lvl3, lvl4]  # Defines list. For looping through and conventient folder creation.

                            for i in lvls:  # Begins loop. Loops through each element in list.  #
                                level = lvls.index(
                                    i)  # Defines variable. Sets value based in list element index for display.
                                create_folder(level, i)  # Creates folder. Calls function.

                            fl_name = '/Hydraulic_geometry.csv'
                            df_hydro_geom.to_csv(lvl4+fl_name, index=False)

                        # df_srvy_yrs = slice_DataFrame_columns1(df_rng, 'Srvy_year', 'Survey years',
                        #                                         1)  # Defines DataFrame. Calls function.
                        # df_srvy_yrs = df_srvy_yrs.drop_duplicates(keep='first')  # Modifies DataFrame. Drops all duplicate values in column.
                        #
                        # srvy_yrs=df_srvy_yrs.tolist()
                        #
                        # del srvy_yrs[-1]

                        df_chnl_geom_08 = slice_DataFrame_rows1(df_hydro_geom, 'Srvy_year', '2008', 'HYDRAULIC GEOMETRY',0)
                        df_chnl_geom_94 = slice_DataFrame_rows1(df_hydro_geom, 'Srvy_year', '1994', 'HYDRAULIC GEOMETRY', 0)
                        df_chnl_geom_64 = slice_DataFrame_rows1(df_hydro_geom, 'Srvy_year', '1964', 'HYDRAULIC GEOMETRY', 0)
                        df_chnl_geom_39 = slice_DataFrame_rows1(df_hydro_geom, 'Srvy_year', '1939', 'HYDRAULIC GEOMETRY', 1)

                        df_h_rad_08=slice_DataFrame_columns1(df_chnl_geom_08, 'Hydro_rad_ft', 'HYDRAULIC RADIUS',0)
                        df_h_rad_08 = df_h_rad_08.astype(float)
                        df_strm_stat_08 = slice_DataFrame_columns1(df_chnl_geom_08, 'Strm_stat', 'STREAM STATION',0)

                        df_h_rad_94 = slice_DataFrame_columns1(df_chnl_geom_94, 'Hydro_rad_ft', 'HYDRAULIC RADIUS',0)
                        df_h_rad_94 = df_h_rad_94.astype(float)
                        df_strm_stat_94 = slice_DataFrame_columns1(df_chnl_geom_94, 'Strm_stat', 'STREAM STATION', 0)

                        df_h_rad_64 = slice_DataFrame_columns1(df_chnl_geom_64, 'Hydro_rad_ft', 'HYDRAULIC RADIUS',0)
                        df_h_rad_64 = df_h_rad_64.astype(float)
                        df_strm_stat_64 = slice_DataFrame_columns1(df_chnl_geom_64, 'Strm_stat', 'STREAM STATION', 0)

                        df_h_rad_39 = slice_DataFrame_columns1(df_chnl_geom_39, 'Hydro_rad_ft', 'HYDRAULIC RADIUS',1)
                        df_h_rad_39=df_h_rad_39.astype(float)
                        df_strm_stat_39 = slice_DataFrame_columns1(df_chnl_geom_39, 'Strm_stat', 'STREAM STATION', 1)

                        x=[df_strm_stat_08,df_strm_stat_94,df_strm_stat_64,df_strm_stat_39]
                        y=[df_h_rad_08,df_h_rad_94,df_h_rad_64,df_h_rad_39]
                        label=['2008','1994','1964','1939']
                        color=[tol_mtd[0],tol_mtd[3],tol_mtd[5],tol_mtd[6]]
                        marker=[mrkr_mpltlib[-1],mrkr_mpltlib[0],mrkr_mpltlib[6],mrkr_mpltlib[2]]
                        title= 'Hydraulic radius along Trout Creek, 1939–2008'
                        plot_lines(4, 2, fig_sz,x,y,label,color,marker,mrkr_sz,lin_wdth,alpha,fntsz_tcks,'Distance upstream ( )',fntsz_ax,lbl_pd,'Bankfull hydraulic radius (ft)',
                                   title, 1,0,lctn,mrkr_scl,frm_alpha,lbl_spcng)

        # Calculate sediment thickness
        if Xsctns_2 == 1:

            # Create second dataset
            c=b-1  # Defines variable. Allows for selection of two datasets for change detection.

            #survey
            df_srvy2 = slice_DataFrame_rows2(df_rng, 'Srvy_num', c, 'SURVEY NUMBER', a, 'RANGE NUMBER', 0)  # Defines DataFrame. Calls function.

            #metadata
            index = df_srvy2.index  # Defines variable. Retrieves index of DataFrame.
            srvy_yr2 = slice_DataFrame_cell(df_srvy2, 'Srvy_year', index[0], 'Survey year', 0)  # Defines variable. Calls function.
            srvy_dt2 = slice_DataFrame_cell(df_srvy2, 'Srvy_date', index[0], 'Survey date', 0)  # Defines variable. Calls function.

            # Measurements
            df_offst2 = slice_DataFrame_columns1(df_srvy2, 'Offset_ft', 'OFFSET', 0)  # Defines DataFrame. Calls function.
            df_elvtn2 = slice_DataFrame_columns1(df_srvy2, 'Elv_geo_ft', 'ELEVATION', 0)  # Defines DataFrame. Calls function.

            # DISPLAY DATASET ------------------------------------------------------------------------------------------

            # Metadata ------------------------------------------------------------------------------------------
            print('==================================================')  # Displays objects.
            print('\033[1m' + 'Field range: ' + '\033[0m' + str(rng_nm1) + ' (' + str(a) + ')')  # Displays objects.
            print('\033[1m' + 'Range surveys: ' + '\033[0m' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' (' + str(b) + '–' + str(c) + ' of ' + str(num_srvys) + ')')  # Displays objects.
            print('\033[1m' + 'Survey dates: ' + '\033[0m' + str(srvy_dt1) + ' & ' + str(srvy_dt2))  # Displays objects.
            print('--------------------------------------------------')  # Displays objects.

            # Plot data ------------------------------------------------------------------------------------------

            if Xsctn_dbl == 1:  # Conditional statement. Plots single cross-section.
                clr1 = get_color(srvy_yr1)
                mrkr1 = get_marker(srvy_yr1)
                clr2 = get_color(srvy_yr2)
                mrkr2 = get_marker(srvy_yr2)

                title1 = 'Range ' + str(rng_nm1) + ' ' + str(srvy_yr1) + '–' + str(srvy_yr2) + ' surveys'  # Defines string. Sets title of plot.

                plot_lines(2, 2, fig_sz, [df_offst1, df_offst2], [df_elvtn1,df_elvtn2], [srvy_yr1,srvy_yr2], [clr1,clr2], [mrkr1, mrkr2], mrkr_sz, lin_wdth, alpha, fntsz_tcks, 'Survey offset (ft)', fntsz_ax, lbl_pd, 'Surface elevation (ft)', title1, ps_lngth, 1,lctn, mrkr_scl, frm_alpha, lbl_spcng)  # Creates plot. Calls function.

                # Export figure
                # Name folders
                # Level 2
                xsctn_fldr = '/Cross_sectional_analysis'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl2 = opt_fldr + xsctn_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 3
                plts_fldr = '/Plots'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl3 = lvl2 + plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 4
                xsctn_plts_fldr = '/Cross_sections'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl4 = lvl3 + xsctn_plts_fldr  # Defines variable as string. Concatenates strings to create file path.

                # Level 5
                xsctn_plts_fldr1 = '/Double'  # Defines variable as string. Sets name of new directory where all cross-section data will be exported.
                lvl5 = lvl4 + xsctn_plts_fldr1  # Defines variable as string. Concatenates strings to create file path.

                # Create folders
                lvls = [lvl2, lvl3, lvl4, lvl5]  # Defines list. For looping through and conventient folder creation.

                for i in lvls:  # Begins loop. Loops through each element in list.  #
                    level = lvls.index(i)  # Defines variable. Sets value based in list element index for display.
                    create_folder(level, i)  # Creates folder. Calls function.

                # Export
                if Exprt==1:
                    plt.figure(2)  # Calls figure. Makes it the active plot.

                    fig_name = '/' + str(rng_nm1) + '_s' + str(b) + '–' + str(c) + '_' + str(srvy_yr1) + '–' + str(srvy_yr2) + '.pdf' # Defines variable as strong. Names figure for export.

                    plt.savefig(lvl5 + fig_name, format='pdf')  # Saves figure to directory. Sets file format.

                    plt.close()  # Closes active figure.