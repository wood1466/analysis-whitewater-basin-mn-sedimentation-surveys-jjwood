# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS 
# TRANSECT DATA SEDIMENTATION RATE STATISTICAL ANALYZER * ---------------------

print('\n\033[1m' + 'START TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS!!!'
      + '\033[0m', '\n...\n')  # Displays objects to signal run.

# INITIALIZATION ==============================================================

# IMPORT MODULES. -------------------------------------------------------------

from transect_analysis_functions import *   # Imports all functions from 
# associated program.

# DEFINE INPUT PARAMETERS. ----------------------------------------------------

INPUT_FOLDER = 'Input'  # Input folder where all input data will be stored.

INPUT_FILE = INPUT_FOLDER + '/Sedimentation_rates_20250201.csv'  # Input file
# with data to be analyzed.

# Define operation parameters.
ALPHA = 0.05  # Statistical hypothesis testing level of significance.

# Define column names for test sample groups in input file. 

GROUP_COLUMN_1 = 'SR55_39CmY'  # Sample group 1.
GROUP_COLUMN_2 = 'SR39_65CmY'  # Sample group 2.
GROUP_COLUMN_3 = 'SR65_94CmY'  # Sample group 3.

# UPLOAD FILE(S). -------------------------------------------------------------

df_sed_rates = convert_CSV_to_dataframe(INPUT_FILE, 0)  # Calls UDF to define
# DataFrame from input data.

# DATA OPERATIONS =============================================================

# SELECT DATA. ----------------------------------------------------------------

# Select sample group sedimentation rate data.

sed_rates_55_39 = slice_dataframe_column(
        'Array', 'Float', df_sed_rates, GROUP_COLUMN_1, 0, 1, 0)  # Calls UDF
# to slice DataFrame and yield array.  
sed_rates_39_65 = slice_dataframe_column(
        'Array', 'Float', df_sed_rates, GROUP_COLUMN_2, 0, 1, 0)
sed_rates_65_94 = slice_dataframe_column(
        'Array', 'Float', df_sed_rates, GROUP_COLUMN_3, 0, 1, 0)

# SELECT HYPOTHESIS TESTS. ----------------------------------------------------

# Verify sample group normality. ----------------------------------------------

# Visually verify.
sample_groups = [sed_rates_55_39, sed_rates_39_65, sed_rates_65_94]
# Defines list of sample groups for looping visual characterization.

for i in sample_groups:  # Begins through list elements to plot visual
    # normality check.
    N_i = len(i)  # Sets group sample size.

    # print(N_i)

    # plt.hist(i, bins=int(np.around(np.sqrt(N_i), decimals=0)))  
    # Plots histogram.
    # plt.show()  # Shows plot.
    # plt.boxplot(i, meanline=True, showmeans=True)  # Plots box plot.
    # plt.show()
    # sm.qqplot(i, line="45")  # Plots QQ plot.
    # plt.show()

    # Statistically verify.
    k_s_test_i = sc.stats.kstest(i, sc.stats.norm.cdf, N=N_i)  
    # Defines result of Kolmogorov-Smirnov goodness of fit test for normality.

    if k_s_test_i.pvalue < ALPHA:  # Begins conditional statement to check if
        # null hypothesis is rejected or not.
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(k_s_test_i.pvalue)
              + '\n  Reject that distribution is normal\n')
    else:
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(k_s_test_i.pvalue)
              + '\n  Fail to reject that distribution is normal\n')

# Verify sample group homoscedasticity (variance equality). -------------------

b_f_test = sc.stats.levene(
          sed_rates_55_39, sed_rates_39_65, sed_rates_65_94, center='median')  
# Defines result of Brown-Forsythe test for variance equality.

if b_f_test.pvalue < ALPHA:
    print('Brown-Forsythe test:\n  P value: ' + str(b_f_test.pvalue)
          + '\n  Reject that sample groups have equal variance\n')
else:
    print('Brown-Forsythe test:\n  P value: ' + str(b_f_test.pvalue)
          + '\n  Fail to reject that sample groups have equal variance\n')

# PERFORM SAMPLE GROUP COMPARISONS. -------------------------------------------

# Perform nonparametric tests. ------------------------------------------------

# Perform omnibus comparison.
k_w_ANOVA_test = sc.stats.kruskal(
          sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result
# of Kruskal-Wallis H-test for median equality.

if k_w_ANOVA_test.pvalue < ALPHA:
    print('Kruskal-Wallis test:\n  P value: ' + str(k_w_ANOVA_test.pvalue)
          + '\n  Reject that sample groups have equal median\n')
else:
    print('Kruskal-Wallis test:\n  P value: ' + str(k_w_ANOVA_test.pvalue)
          + '\n  Fail to reject that sample groups have equal median\n')  

# Perform post-hoc pairwise comparisons.
d_test = sc_p.posthoc_dunn(sample_groups, p_adjust='bonferroni')  # Defines
# result of Dunn's test for median equality.

print("Dunn's test:\n" + str(d_test) + '\n')

# Perform parametric tests. ---------------------------------------------------

# Assume normality and equal variance. ----------------------------------------

# Perform omnibus comparison.
ANOVA_test = sc.stats.f_oneway(
        sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result of
# one-way ANOVA test for mean equality.

if ANOVA_test.pvalue < ALPHA:
    print('One-way ANOVA test:\n  P value: ' + str(ANOVA_test.pvalue)
          + '\n  Reject that sample groups have equal mean\n')
else:
    print('One-way ANOVA test:\n  P value: ' + str(ANOVA_test.pvalue)
          + '\n  Fail to reject that sample groups have equal mean\n')  

# Perform post-hoc pairwise comparisons.
t_HSD_test = sc.stats.tukey_hsd(
        sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result of
# Tukey's HSD test for mean equality.

print("Tukey's test:\n" + str(t_HSD_test) + '\n')

# Assume normality and unequal variance. --------------------------------------

# Compile samples. ------------------------------------------------------------

# Define DataFrame of sample group.

df_sed_rates_55_39 = pd.DataFrame({'Samples': sed_rates_55_39, 'Group': 1})
df_sed_rates_39_65 = pd.DataFrame({'Samples': sed_rates_39_65, 'Group': 2})
df_sed_rates_65_94 = pd.DataFrame({'Samples': sed_rates_65_94, 'Group': 3})

df_sample_groups = pd.concat([
        df_sed_rates_55_39, df_sed_rates_39_65, df_sed_rates_65_94])
# Defines DataFrame through concatenation.

# Perform omnibus comparison.
w_ANOVA_test = pg.welch_anova(
        data=df_sample_groups, dv='Samples', between='Group')  # Defines result
# of One-way Welch's ANOVA test for mean equality.

if w_ANOVA_test.iloc[0, 4] < ALPHA:
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(w_ANOVA_test.iloc[0, 4])
          + '\n  Reject that sample groups have equal mean\n')
else:
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(w_ANOVA_test.iloc[0, 4])
          + '\n  Fail to reject that sample groups have equal mean\n')

# Perform post-hoc pairwise comparisons.
g_h_test = pg.pairwise_gameshowell(
        data=df_sample_groups, dv='Samples', between='Group')  # Defines result
# of Games-Howell (nonparametric) test for mean equality.

print('Games-Howell test:\n' + str(g_h_test) + '\n')

print('\n\033[1m'
      + 'TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS COMPLETED!!!'
      + '\033[0m', '\n...\n')  # Signals end.
