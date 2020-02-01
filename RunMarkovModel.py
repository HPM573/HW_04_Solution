import MarkovClasses as Cls
import SimPy.Plots.SamplePaths as Path
import SimPy.Plots.Histogram as Hist
import InputData as D

# Markov model without temp state
myCohortNoTemp = Cls.Cohort(id=1,
                            pop_size=D.POP_SIZE,
                            transition_matrix=D.TRANS_PROB_MATRIX_1)
# Markov model with temp state
myCohortWithTemp = Cls.Cohort(id=1,
                              pop_size=D.POP_SIZE,
                              transition_matrix=D.TRANS_PROB_MATRIX_2)
# Bonus model
myCohorBonus = Cls.CohortBonus(id=1,
                               pop_size=D.POP_SIZE,
                               prob_stroke_well=D.P_STROKE,
                               prob_recurrent_stroke=D.P_RE_STROKE,
                               prob_survive=D.P_SURV)

# simulate all models
myCohortNoTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)
myCohortWithTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)
myCohorBonus.simulate(n_time_steps=D.SIM_TIME_STEPS)

# sample paths
Path.plot_sample_path(
    sample_path=myCohortNoTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model without Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)
Path.plot_sample_path(
    sample_path=myCohortWithTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)
Path.plot_sample_path(
    sample_path=myCohorBonus.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Bonus model)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# histograms of survival times
Hist.plot_histogram(
    data=myCohortNoTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model without Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)
Hist.plot_histogram(
    data=myCohortWithTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)
Hist.plot_histogram(
    data=myCohorBonus.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Bonus Model)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)

# histogram of number of strokes
Hist.plot_histogram(
    data=myCohortWithTemp.cohortOutcomes.nStrokes,
    title='Histogram of Number of Strokes',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)
Hist.plot_histogram(
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
