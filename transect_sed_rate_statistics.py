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
InputFolder = 'Input'  # Defines object for name of input folder where all 
# input data will be stored.

# Data
InputFile1 = InputFolder + '/Sedimentation_rates_20250201.csv'  # Defines 
# object for path to input file.

# Operations
Alpha = 0.05  # Defines object for statistical hypothesis testing level of 
# significance.

# UPLOAD FILE(S) --------------------------------------------------------------

dfTSedimentationRates = ConvertCsvToDataFrame(InputFile1, 0)
# Calls user-defined function (UDF) to define  DataFrame from input data.

# =============================================================================
# PART 2: DATA OPERATIONS -----------------------------------------------------

# SELECT DATA -----------------------------------------------------------------

# Select sedimentation rate data ----------------------------------------------

# Calls UDF to slice DataFrame and define resultant array to serve as sample
# group for statistical testing.

Ary55_39 = SliceDataFrameColumns(
    'Array', 'Float', dfTSedimentationRates, 'SR55_39CmY', 0, 1, 0)  
Ary39_65 = SliceDataFrameColumns(
    'Array', 'Float', dfTSedimentationRates, 'SR39_65CmY', 0, 1, 0)
Ary65_94 = SliceDataFrameColumns(
    'Array', 'Float', dfTSedimentationRates, 'SR65_94CmY', 0, 1, 0)

# SELECT HYPOTHESIS TESTS -----------------------------------------------------

# Verify sample group normality -----------------------------------------------

# Visually
LstSampleGroups = [Ary55_39, Ary39_65, Ary65_94]  # Defines list of sample
# groups for looping visual characterization.

for i in LstSampleGroups:  # Begins through list elements to plot visual
    # normality check.
    NumberOfSamplesi = len(i)  # Defines object as group sample size.

    # print(NumberOfSamplesi)  # Displays objects.

    # plt.hist(i, bins=int(np.around(np.sqrt(NumberOfSamplesi), decimals=0)))  
    # Plots histogram.
    # plt.show()  # Shows plot.
    # plt.boxplot(i, meanline=True, showmeans=True)  # Plots box plot.
    # plt.show()
    # sm.qqplot(i, line="45")  # Plots QQ plot.
    # plt.show()

    # Statistically
    KSTesti = sc.stats.kstest(i, sc.stats.norm.cdf, N=NumberOfSamplesi)  
    # Defines result of Kolmogorov-Smirnov goodness of fit test for normalilty.

    if KSTesti.pvalue < Alpha:  # Begins conditional statement to check if null
        # hypothesis is rejected or not.
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(KSTesti.pvalue)
              + '\n  Reject that distribution is normal\n')  
        # Displays objects.
    else:
        print('Kolmogorov-Smirnov test:\n  P value: ' + str(KSTesti.pvalue)
              + '\n  Fail to reject that distribution is normal\n')

# Verify sample group homoscedasticity (variance equality) --------------------

BFTest = sc.stats.levene(Ary55_39, Ary39_65, Ary65_94, center='median')  
# Defines result of Brown-Forsythe test for variance equality.

if BFTest.pvalue < Alpha:  # Begins conditional statement to check if null
    # hypothesis is rejected or not.
    print('Brown-Forsythe test:\n  P value: ' + str(BFTest.pvalue)
          + '\n  Reject that sample groups have equal variance\n')
    # Displays objects.
else:
    print('Brown-Forsythe test:\n  P value: ' + str(BFTest.pvalue)
          + '\n  Fail to reject that sample groups have equal variance\n')

# PERFORM SAMPLE GROUP COMPARISONS --------------------------------------------

# Perform nonparametric tests -------------------------------------------------

# Omnibus comparison
KWTest = sc.stats.kruskal(Ary55_39, Ary39_65, Ary65_94)  # Defines result of
# Kruskal-Wallis H-test for median equality.

if KWTest.pvalue < Alpha:  # Begins conditional statement to check if null
    # hypothesis is rejected or not.
    print('Kruskal-Wallis test:\n  P value: ' + str(KWTest.pvalue)
          + '\n  Reject that sample groups have equal median\n')
    # Displays objects.
else:
    print('Kruskal-Wallis test:\n  P value: ' + str(KWTest.pvalue)
          + '\n  Fail to reject that sample groups have equal median\n')  

# Post-hoc pairwise comparisons
DnTest = sc_p.posthoc_dunn(LstSampleGroups, p_adjust='bonferroni')  # Defines
# result of Dunn's test for median equality.

print("Dunn's test:\n" + str(DnTest) + '\n')  # Displays objects.

# Perform parametric tests ----------------------------------------------------

# Assume normality and equal variance -----------------------------------------

# Omnibus comparison
ANOVATest = sc.stats.f_oneway(Ary55_39, Ary39_65, Ary65_94)  # Defines result
# of one-way ANOVA test for mean equality.

if ANOVATest.pvalue < Alpha:  # Begins conditional statement to check if null
    # hypothesis is rejected or not.
    print('One-way ANOVA test:\n  P value: ' + str(ANOVATest.pvalue)
          + '\n  Reject that sample groups have equal mean\n')
    # Displays objects.
else:
    print('One-way ANOVA test:\n  P value: ' + str(ANOVATest.pvalue)
          + '\n  Fail to reject that sample groups have equal mean\n')  

# Post-hoc pairwise comparisons
TkTest = sc.stats.tukey_hsd(Ary55_39, Ary39_65, Ary65_94)  # Defines result of
# Tukey's HSD test for mean equality.

print("Tukey's test:\n" + str(TkTest) + '\n')  # Displays objects.

# Assume normality and unequal variance ---------------------------------------

# Compile samples -------------------------------------------------------------

# Defines DataFrame of sample group.
df55_39 = pd.DataFrame({'Samples': Ary55_39, 'Group': 1})
df39_65 = pd.DataFrame({'Samples': Ary39_65, 'Group': 2})
df65_94 = pd.DataFrame({'Samples': Ary65_94, 'Group': 3})

dfSampleGroups = pd.concat([df55_39, df39_65, df65_94])  # Defines DataFrame
# through concatenation.

# Omnibus comparison
WlANOVATest = pg.welch_anova(
    data=dfSampleGroups, dv='Samples', between='Group')  # Defines result of
# One-way Welch's ANOVA test for mean equality.

if WlANOVATest.iloc[0, 4] < Alpha:  # Begins conditional statement to check if
    # null hypothesis is rejected or not.
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(WlANOVATest.iloc[0, 4])
          + '\n  Reject that sample groups have equal mean\n')
    # Displays objects.
else:
    print("One-way Welch's ANOVA test:\n  P value: "
          + str(WlANOVATest.iloc[0, 4])
          + '\n  Fail to reject that sample groups have equal mean\n')

# Post-hoc pairwise comparisons
GHTest = pg.pairwise_gameshowell(
    data=dfSampleGroups, dv='Samples', between='Group')  # Defines result of
# Games-Howell (nonparametric) test for mean equality.

print('Games-Howell test:\n' + str(GHTest) + '\n')  # Displays objects.

# SIGNAL END ==================================================================

print('\n\033[1m'
      + 'TRANSECT SEDIMENTATION RATE STATISTICAL ANALYSIS COMPLETED!!!'
      + '\033[0m', '\n...\n')  # Displays objects.
