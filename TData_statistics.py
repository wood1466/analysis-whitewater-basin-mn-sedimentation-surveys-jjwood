# ======================================================================================================================
# WHITEWATER RIVER VALLEY (MN) SCS-USGS STREAM AND VALLEY SEDIMENTATION SURVEY DATA * ----------------------------------
# TRANSECT DATA SEDIMENTATION RATE STATISTICAL ANALYZER * --------------------------------------------------------------
# PYTHON PROGRAM * -----------------------------------------------------------------------------------------------------

# ======================================================================================================================
# SIGNAL RUN -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'START TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS!!!' + '\033[0m', '\n...\n')  # Displays
# objects.

# ======================================================================================================================
# PART 1: INITIALIZATION -----------------------------------------------------------------------------------------------

# IMPORT MODULES -------------------------------------------------------------------------------------------------------

from TData_functions import *   # Imports functions. Imports all functions from outside program.

# DEFINE INPUT PARAMETERS ----------------------------------------------------------------------------------------------

# Directory
InputFolder = 'Input'  # Defines variable. Sets name of input folder where all data sources will be housed.

# Data
InputFile1 = InputFolder + '/Sedimentation_rates_20250201.csv'  # Defines variable. Sets file path to input file. Sets
# path to transect data that will be used in calculations.

# Operations
Alpha = 0.05  # Defines variable. Sets statistical hypothesis testing level of significance.

# UPLOAD FILE(S) -------------------------------------------------------------------------------------------------------

dfTSedimentationRates = ConvertCsvToDataFrame(InputFile1, 0)  # Defines DataFrame. Calls function. Uploads transect
# data.

# ======================================================================================================================
# PART 2: DATA OPERATIONS ----------------------------------------------------------------------------------------------

# SELECT DATA ----------------------------------------------------------------------------------------------------------

# Select sedimentation rate data ---------------------------------------------------------------------------------------

Ary55_39 = SliceDataFrameColumns('Array', 'Float', dfTSedimentationRates, 'SR55_39CmY', 0, 1, 0)  # Defines array. Calls
# function. Slices DataFrame to yield transect sedimentation rates for interval. Creates sample group for statistical
# testing.
Ary39_65 = SliceDataFrameColumns('Array', 'Float', dfTSedimentationRates, 'SR39_65CmY', 0, 1, 0)  # Defines array. Calls
# function. Slices DataFrame to yield transect sedimentation rates for interval. Creates sample group for statistical
# testing.
Ary65_94 = SliceDataFrameColumns('Array', 'Float', dfTSedimentationRates, 'SR65_94CmY', 0, 1, 0)  # Defines array. Calls
# function. Slices DataFrame to yield transect sedimentation rates for interval. Creates sample group for statistical
# testing.

# SELECT HYPOTHESIS TESTS ----------------------------------------------------------------------------------------------

# Verify sample group normality ----------------------------------------------------------------------------------------

# Visually
LstSampleGroups = [Ary55_39, Ary39_65, Ary65_94]  # Defines list. Creates list of sample groups. For looping visual
# check.

for i in LstSampleGroups:  # Begins loop. Loops through list elements. Plots each sample group for visual normality
    # check.
    NumberOfSamplesi = len(i)  # Defines variable. Retrieves number of samples in group.

    # print(NumberOfSamplesi)  # Displays objects.

    # plt.hist(i, bins=int(np.around(np.sqrt(NumberOfSamplesi), decimals=0)))  # Plots histogram.
    # plt.show()  # Plot show command. Shows plot.
    # plt.boxplot(i, meanline=True, showmeans=True)  # Plots box plot.
    # plt.show()  # Plot show command. Shows plot.
    # sm.qqplot(i, line="45")  # Plots QQ plot.
    # plt.show()  # Plot show command. Shows plot.

    # Statistically
    KSTesti = sc.stats.kstest(i, sc.stats.norm.cdf, N=NumberOfSamplesi)  # Defines result. Performs Kolmogorov-Smirnov
    # goodness of fit test. Tests whether sample comes from a normal distribution.

    if KSTesti.pvalue < Alpha:  # Begins conditional statement. Checks relation. Checks if null hypothesis is rejected
        # or not.
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(KSTesti.pvalue) +
              '\n  Reject that distribution is normal\n')  # Displays objects.
    else:  # Continues conditional statement. Checks relation. Checks if null hypothesis is rejected or not.
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(KSTesti.pvalue) +
              '\n  Fail to reject that distribution is normal\n')  # Displays objects.

# Verify sample group homoscedasticity (variance equality) -------------------------------------------------------------

BFTest = sc.stats.levene(Ary55_39, Ary39_65, Ary65_94, center='median')  # Defines result. Performs Brown-Forsythe test.
# Tests whether sample groups have equal variance.

if BFTest.pvalue < Alpha:  # Begins conditional statement. Checks relation. Checks if null hypothesis is rejected or
    # not.
    print('Brown-Forsythe test:\n  P value: ' + str(BFTest.pvalue) +
          '\n  Reject that sample groups have equal variance\n')  # Displays objects.
else:  # Continues conditional statement. Checks relation. Checks if null hypothesis is rejected or not.
    print('Brown-Forsythe test:\n  P value: ' + str(BFTest.pvalue) +
          '\n  Fail to reject that sample groups have equal variance\n')  # Displays objects.

# PERFORM SAMPLE GROUP COMPARISONS -------------------------------------------------------------------------------------

# Perform nonparametric tests ------------------------------------------------------------------------------------------

# Omnibus comparison
KWTest = sc.stats.kruskal(Ary55_39, Ary39_65, Ary65_94)  # Defines result. Performs Kruskal-Wallis H-test. Tests whether
# sample groups have an equal median.

if KWTest.pvalue < Alpha:  # Begins conditional statement. Checks relation. Checks if null hypothesis is rejected or
    # not.
    print('Kruskal-Wallis test:\n  P value: ' + str(KWTest.pvalue) +
          '\n  Reject that sample groups have equal median\n')  # Displays objects.
else:  # Continues conditional statement. Checks relation. Checks if null hypothesis is rejected or not.
    print('Kruskal-Wallis test:\n  P value: ' + str(KWTest.pvalue) +
          '\n  Fail to reject that sample groups have equal median\n')  # Displays objects.

# Post-hoc pairwise comparisons
DnTest = sc_p.posthoc_dunn(LstSampleGroups, p_adjust='bonferroni')  # Defines result. Performs Dunn's test. Tests
# whether sample group pairs have an equal median.

print("Dunn's test:\n" + str(DnTest) + '\n')  # Displays objects.

# Perform parametric tests ---------------------------------------------------------------------------------------------

# Assume normality and equal variance ----------------------------------------------------------------------------------

# Omnibus comparison
ANOVATest = sc.stats.f_oneway(Ary55_39, Ary39_65, Ary65_94)  # Defines result. Performs one-way ANOVA test. Tests
# whether sample groups have an equal mean.

if ANOVATest.pvalue < Alpha:  # Begins conditional statement. Checks relation. Checks if null hypothesis is rejected or
    # not.
    print('One-way ANOVA test:\n  P value: ' + str(ANOVATest.pvalue) +
          '\n  Reject that sample groups have equal mean\n')  # Displays objects.
else:  # Continues conditional statement. Checks relation. Checks if null hypothesis is rejected or not.
    print('One-way ANOVA test:\n  P value: ' + str(ANOVATest.pvalue) +
          '\n  Fail to reject that sample groups have equal mean\n')  # Displays objects.

# Post-hoc pairwise comparisons
TkTest = sc.stats.tukey_hsd(Ary55_39, Ary39_65, Ary65_94)  # Defines result. Performs Tukey's HSD test. Tests whether
# sample group pairs have an equal mean.

print("Tukey's test:\n" + str(TkTest) + '\n')  # Displays objects.

# Assume normality and unequal variance --------------------------------------------------------------------------------

# Compile samples ------------------------------------------------------------------------------------------------------

df55_39 = pd.DataFrame({'Samples': Ary55_39, 'Group': 1})  # Defines DataFrame. Creates DataFrame for sample group.
df39_65 = pd.DataFrame({'Samples': Ary39_65, 'Group': 2})  # Defines DataFrame. Creates DataFrame for sample group.
df65_94 = pd.DataFrame({'Samples': Ary65_94, 'Group': 3})  # Defines DataFrame. Creates DataFrame for sample group.
dfSampleGroups = pd.concat([df55_39, df39_65, df65_94])  # Defines DataFrame. Concatenates DataFrames.

# Omnibus comparison
WlANOVATest = pg.welch_anova(data=dfSampleGroups, dv='Samples', between='Group')  # Defines result. Performs One-way
# Welch's ANOVA test. Tests whether sample groups have an equal mean.

if WlANOVATest.iloc[0, 4] < Alpha:  # Begins conditional statement. Checks relation. Checks if null hypothesis is
    # rejected or not.
    print("One-way Welch's ANOVA test:\n  P value: " + str(WlANOVATest.iloc[0, 4]) +
          '\n  Reject that sample groups have equal mean\n')  # Displays objects.
else:  # Continues conditional statement. Checks relation. Checks if null hypothesis is rejected or not.
    print("One-way Welch's ANOVA test:\n  P value: " + str(WlANOVATest.iloc[0, 4]) +
          '\n  Fail to reject that sample groups have equal mean\n')  # Displays objects.

# Post-hoc pairwise comparisons
GHTest = pg.pairwise_gameshowell(data=dfSampleGroups, dv='Samples', between='Group')  # Defines result. Performs
# Games-Howell (nonparametric) test. Tests whether sample group pairs have an equal mean.

print('Games-Howell test:\n' + str(GHTest) + '\n')  # Displays objects.

# ======================================================================================================================
# SIGNAL END -----------------------------------------------------------------------------------------------------------

print('\n\033[1m' + 'TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS COMPLETED!!!' + '\033[0m', '\n...\n')  # Displays
# objects.