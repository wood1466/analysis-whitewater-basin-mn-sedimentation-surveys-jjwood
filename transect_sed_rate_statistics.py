# WHITEWATER RIVER VALLEY, MN, US, SEDIMENTATION SURVEY DATA ANALYSIS PROGRAMS 
# TRANSECT DATA SEDIMENTATION RATE STATISTICAL ANALYZER * ---------------------

# SIGNAL RUN ==================================================================

print('\n\033[1m' + 'START TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS!!!'
      + '\033[0m', '\n...\n')  # Displays objects.

# INITIALIZATION ==============================================================

# IMPORT MODULES --------------------------------------------------------------

from transect_analysis_functions import *   # Imports all functions from 
# complimentary program.

# DEFINE INPUT PARAMETERS -----------------------------------------------------

# Directory
INPUT_FOLDER = 'Input'  # Defines object for name of input folder where all 
# input data will be stored.

# Data
INPUT_FILE = INPUT_FOLDER + '/Sedimentation_rates_20250201.csv'  # Defines 
# object for path to input file.

# Operations
# Define objects for column names of sample groups in input file.

GROUP_COLUMN_1 = 'SR55_39CmY'
GROUP_COLUMN_2 = 'SR39_65CmY'
GROUP_COLUMN_3 = 'SR65_94CmY'

ALPHA = 0.05  # Defines object for statistical hypothesis testing level of 
# significance.

# UPLOAD FILE(S) --------------------------------------------------------------

df_sed_rates = ConvertCsvToDataFrame(INPUT_FILE, 0)
# Calls UDF to define DataFrame from input data.

# =============================================================================
# PART 2: DATA OPERATIONS -----------------------------------------------------

# SELECT DATA -----------------------------------------------------------------

# Select sedimentation rate data ----------------------------------------------

# Call UDF to slice DataFrame and yield sample groups for statistical testing.

sed_rates_55_39 = SliceDataFrameColumns(
    'Array', 'Float', df_sed_rates, GROUP_COLUMN_1, 0, 1, 0)  
sed_rates_39_65 = SliceDataFrameColumns(
    'Array', 'Float', df_sed_rates, GROUP_COLUMN_2, 0, 1, 0)
sed_rates_65_94 = SliceDataFrameColumns(
    'Array', 'Float', df_sed_rates, GROUP_COLUMN_3, 0, 1, 0)

# SELECT HYPOTHESIS TESTS -----------------------------------------------------

# Verify sample group normality -----------------------------------------------

# Visually
sample_groups = [sed_rates_55_39, sed_rates_39_65, sed_rates_65_94]
# Defines list of sample groups for looping visual characterization.

for i in sample_groups:  # Begins through list elements to plot visual
    # normality check.
    N_i = len(i)  # Defines object as group sample size.

    # print(N_i)  # Displays objects.

    # plt.hist(i, bins=int(np.around(np.sqrt(N_i), decimals=0)))  
    # Plots histogram.
    # plt.show()  # Shows plot.
    # plt.boxplot(i, meanline=True, showmeans=True)  # Plots box plot.
    # plt.show()
    # sm.qqplot(i, line="45")  # Plots QQ plot.
    # plt.show()

    # Statistically
    k_s_test_i = sc.stats.kstest(i, sc.stats.norm.cdf, N=N_i)  
    # Defines result of Kolmogorov-Smirnov goodness of fit test for normalilty.

    if k_s_test_i.pvalue < ALPHA:  # Begins conditional statement to check if
        # null hypothesis is rejected or not.
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(k_s_test_i.pvalue)
              + '\n  Reject that distribution is normal\n')  
        # Displays objects.
    else:
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(k_s_test_i.pvalue)
              + '\n  Fail to reject that distribution is normal\n')

# Verify sample group homoscedasticity (variance equality) --------------------

b_f_test = sc.stats.levene(
      sed_rates_55_39, sed_rates_39_65, sed_rates_65_94, center='median')  
# Defines result of Brown-Forsythe test for variance equality.

if b_f_test.pvalue < ALPHA:  # Begins conditional statement to check if null
    # hypothesis is rejected or not.
    print('Brown-Forsythe test:\n  P value: ' + str(b_f_test.pvalue)
          + '\n  Reject that sample groups have equal variance\n')
    # Displays objects.
else:
    print('Brown-Forsythe test:\n  P value: ' + str(b_f_test.pvalue)
          + '\n  Fail to reject that sample groups have equal variance\n')

# PERFORM SAMPLE GROUP COMPARISONS --------------------------------------------

# Perform nonparametric tests -------------------------------------------------

# Omnibus comparison
k_w_ANOVA_test = sc.stats.kruskal(
      sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result of
# Kruskal-Wallis H-test for median equality.

if k_w_ANOVA_test.pvalue < ALPHA:  # Begins conditional statement to check if
    # null hypothesis is rejected or not.
    print('Kruskal-Wallis test:\n  P value: ' + str(k_w_ANOVA_test.pvalue)
          + '\n  Reject that sample groups have equal median\n')
    # Displays objects.
else:
    print('Kruskal-Wallis test:\n  P value: ' + str(k_w_ANOVA_test.pvalue)
          + '\n  Fail to reject that sample groups have equal median\n')  

# Post-hoc pairwise comparisons
d_test = sc_p.posthoc_dunn(sample_groups, p_adjust='bonferroni')  # Defines
# result of Dunn's test for median equality.

print("Dunn's test:\n" + str(d_test) + '\n')  # Displays objects.

# Perform parametric tests ----------------------------------------------------

# Assume normality and equal variance -----------------------------------------

# Omnibus comparison
ANOVA_test = sc.stats.f_oneway(
    sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result of
# one-way ANOVA test for mean equality.

if ANOVA_test.pvalue < ALPHA:  # Begins conditional statement to check if null
    # hypothesis is rejected or not.
    print('One-way ANOVA test:\n  P value: ' + str(ANOVA_test.pvalue)
          + '\n  Reject that sample groups have equal mean\n')
    # Displays objects.
else:
    print('One-way ANOVA test:\n  P value: ' + str(ANOVA_test.pvalue)
          + '\n  Fail to reject that sample groups have equal mean\n')  

# Post-hoc pairwise comparisons
t_HSD_test = sc.stats.tukey_hsd(
    sed_rates_55_39, sed_rates_39_65, sed_rates_65_94)  # Defines result of
# Tukey's HSD test for mean equality.

print("Tukey's test:\n" + str(t_HSD_test) + '\n')  # Displays objects.

# Assume normality and unequal variance ---------------------------------------

# Compile samples -------------------------------------------------------------

# Define DataFrame of sample group.

df_sed_rates_55_39 = pd.DataFrame({'Samples': sed_rates_55_39, 'Group': 1})
df_sed_rates_39_65 = pd.DataFrame({'Samples': sed_rates_39_65, 'Group': 2})
df_sed_rates_65_94 = pd.DataFrame({'Samples': sed_rates_65_94, 'Group': 3})

df_sample_groups = pd.concat([
    df_sed_rates_55_39, df_sed_rates_39_65, df_sed_rates_65_94])
# Defines DataFrame through concatenation.

# Omnibus comparison
w_ANOVA_test = pg.welch_anova(
    data=df_sample_groups, dv='Samples', between='Group')  # Defines result of
# One-way Welch's ANOVA test for mean equality.

if w_ANOVA_test.iloc[0, 4] < ALPHA:  # Begins conditional statement to check if
    # null hypothesis is rejected or not.
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(w_ANOVA_test.iloc[0, 4])
          + '\n  Reject that sample groups have equal mean\n')
    # Displays objects.
else:
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(w_ANOVA_test.iloc[0, 4])
          + '\n  Fail to reject that sample groups have equal mean\n')

# Post-hoc pairwise comparisons
g_h_test = pg.pairwise_gameshowell(
    data=df_sample_groups, dv='Samples', between='Group')  # Defines result of
# Games-Howell (nonparametric) test for mean equality.

print('Games-Howell test:\n' + str(g_h_test) + '\n')  # Displays objects.

# SIGNAL END ==================================================================

print('\n\033[1m'
      + 'TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS COMPLETED!!!'
      + '\033[0m', '\n...\n')  # Displays objects.
