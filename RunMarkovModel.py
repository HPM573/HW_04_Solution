import MarkovClasses as Cls
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig
import InputData as D

# Markov model without temp state
myCohortNoTemp = Cls.Cohort(id=1,
                            pop_size=D.POP_SIZE,
                            transition_matrix=D.TRANS_PROB_MATRIX_1)
# Markov model with temp state
myCohortWithTemp = Cls.Cohort(id=1,
                              pop_size=D.POP_SIZE,
                              transition_matrix=D.TRANS_PROB_MATRIX_2)

# simulate both models
myCohortNoTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)
myCohortWithTemp.simulate(n_time_steps=D.SIM_TIME_STEPS)

# sample paths
PathCls.graph_sample_path(
    sample_path=myCohortNoTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model without Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)
PathCls.graph_sample_path(
    sample_path=myCohortWithTemp.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with Temp State)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# histograms of survival times
Fig.graph_histogram(
    data=myCohortNoTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model without Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)
Fig.graph_histogram(
    data=myCohortWithTemp.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with Temp State)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)

# histogram of number of strokes
Fig.graph_histogram(
    data=myCohortWithTemp.cohortOutcomes.nStrokes,
    title='Histogram of Number of Strokes',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)

# print the patient survival time
print('Mean survival time for the model without temp state (years):',
      myCohortNoTemp.cohortOutcomes.meanSurvivalTime)
print('Mean survival time for the model with temp state (years):',
      myCohortWithTemp.cohortOutcomes.meanSurvivalTime)
