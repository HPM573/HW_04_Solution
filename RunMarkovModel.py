import MarkovClasses as Cls
import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path
import InputData as D

# -------------------------------------------------------------------------
# ------ Markov model (first version -- without temporary state) ----------
# -------------------------------------------------------------------------
# build the model
myCohortNoTemp = Cls.Cohort(id=1,
                            pop_size=D.POP_SIZE,
                            transition_prob_matrix=D.TRANS_PROB_MATRIX_1)
# simulate
myCohortNoTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)

# plot the survival curve
path.plot_sample_path(
    sample_path=myCohortNoTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model without Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# plot histograms of survival times
hist.plot_histogram(
    data=myCohortNoTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model without Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# -------------------------------------------------------------------------
# ------ Markov model (second version -- with a temporary state) ----------
# -------------------------------------------------------------------------
# build the model
myCohortWithTemp = Cls.Cohort(id=1,
                              pop_size=D.POP_SIZE,
                              transition_prob_matrix=D.TRANS_PROB_MATRIX_2)

# simulate
myCohortWithTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)

# plot the survival curve
path.plot_sample_path(
    sample_path=myCohortWithTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# plot histograms of survival times
hist.plot_histogram(
    data=myCohortWithTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# histogram of number of strokes
hist.plot_histogram(
    data=myCohortWithTemp.cohortOutcomes.nStrokes,
    title='Histogram of Number of Strokes',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)

# -------------------------------------------------------------------------
# ------ Markov model (third version -- more accurate approach) -----------
# -------------------------------------------------------------------------
myCohorBonus = Cls.CohortBonus(id=1,
                               pop_size=D.POP_SIZE,
                               prob_stroke_well=D.P_STROKE,
                               prob_recurrent_stroke=D.P_RE_STROKE,
                               prob_survive=D.P_SURV)

# simulate
myCohorBonus.simulate(n_time_steps=D.SIM_TIME_STEPS)

# plot the survival curve
path.plot_sample_path(
    sample_path=myCohorBonus.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Bonus model)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# plot histograms of survival times
hist.plot_histogram(
    data=myCohorBonus.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Bonus Model)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# histogram of number of strokes
hist.plot_histogram(
    data=myCohorBonus.cohortOutcomes.nStrokes,
    title='Histogram of Number of Strokes (Bonus Model)',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)

# print the patient survival time
print('Mean survival time for the model without temp state (years):',
      myCohortNoTemp.cohortOutcomes.meanSurvivalTime)
print('Mean survival time for the model with temp state (years):',
      myCohortWithTemp.cohortOutcomes.meanSurvivalTime)
print('Mean survival time for the bonus model (years):',
      myCohorBonus.cohortOutcomes.meanSurvivalTime)
