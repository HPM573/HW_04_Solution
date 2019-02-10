import HW4 as Cls
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig
import InputData as D

myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      transition_matrix=D.TRANS_MATRIX_STROKE)

myCohort.simulate(n_time_steps=D.SIM_TIME_STEPS)

PathCls.graph_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

Fig.graph_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)

Fig.graph_histogram(
    data=myCohort.cohortOutcomes.nStrokes,
    title='Histogram of Number of Strokes',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)
