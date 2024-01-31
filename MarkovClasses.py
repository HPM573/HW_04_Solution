import numpy as np

from deampy.markov import MarkovJumpProcess
from deampy.plots.sample_paths import PrevalencePathBatchUpdate
from InputData import HealthStates


class Patient:
    def __init__(self, id, transition_prob_matrix):

        self.id = id
        self.transProbMatrix = transition_prob_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # jump process
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.transProbMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:
            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientBonus:
    def __init__(self, id, prob_stroke_well, prob_recurrent_stroke, prob_survive, prob_all_cause_death):

        self.id = id
        self.probStrokeWell = prob_stroke_well
        self.probRecurrentStroke = prob_recurrent_stroke
        self.probSurvive = prob_survive
        self.probAllCauseDeath = prob_all_cause_death
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):

        rng = np.random.RandomState(seed=self.id)

        k = 0

        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # if the patient is alive, decide if the patient will die from all-cause mortality
            if self.stateMonitor.currentState in (HealthStates.WELL, HealthStates.POST_STROKE):
                # if the patient dies from all-cause mortality
                if rng.random_sample() < self.probAllCauseDeath:
                    new_state_index = HealthStates.ALL_CAUSE_DEATH.value
                else:

                    # find the probability of stroke
                    if self.stateMonitor.currentState is HealthStates.WELL:
                        p_stroke = self.probStrokeWell
                    else:
                        p_stroke = self.probRecurrentStroke

                    # decide if the patient will have a stroke
                    if rng.random_sample() < p_stroke:

                        # increment the number of strokes
                        self.stateMonitor.nStrokes += 1

                        # decide if the patient will survive this stoke
                        if rng.random_sample() < self.probSurvive:
                            new_state_index = HealthStates.POST_STROKE.value
                        else:
                            new_state_index = HealthStates.STROKE_DEATH.value

                    else:  # no stoke
                        new_state_index = self.stateMonitor.currentState

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    def __init__(self):

        self.currentState = HealthStates.WELL    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nStrokes = 0

    def update(self, time_step, new_state):

        if self.currentState in (HealthStates.STROKE_DEATH, HealthStates.ALL_CAUSE_DEATH):
            return

        if new_state in (HealthStates.STROKE_DEATH, HealthStates.ALL_CAUSE_DEATH):
            self.survivalTime = time_step + 0.5  # correct for half cycle effect

        if new_state == HealthStates.STROKE:
            self.nStrokes += 1

        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState in (HealthStates.STROKE_DEATH, HealthStates.ALL_CAUSE_DEATH):
            return False
        else:
            return True


class Cohort:
    def __init__(self, id, pop_size, transition_prob_matrix):
        self.id = id
        self.popSize = pop_size
        self.transitionProbMatrix = transition_prob_matrix
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, n_time_steps):

        # populate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              transition_prob_matrix=self.transitionProbMatrix)
            # simulate
            patient.simulate(n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortBonus:
    def __init__(self, id, pop_size, prob_stroke_well, prob_recurrent_stroke, prob_survive, prob_all_cause_death):
        self.id = id
        self.popSize = pop_size
        self.probStrokeWell = prob_stroke_well
        self.probRecurrentStroke = prob_recurrent_stroke
        self.probSurvive = prob_survive
        self.probAllCauseDeath = prob_all_cause_death
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, n_time_steps):

        for i in range(self.popSize):
            patient = PatientBonus(id=self.id * self.popSize + i,
                                   prob_stroke_well=self.probStrokeWell,
                                   prob_recurrent_stroke=self.probRecurrentStroke,
                                   prob_survive=self.probSurvive,
                                   prob_all_cause_death=self.probAllCauseDeath)
            patient.simulate(n_time_steps)

            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nStrokes = []
        self.nLivingPatients = None
        self.meanSurvivalTime = None

    def extract_outcome(self, simulated_patient):

        if simulated_patient.stateMonitor.survivalTime is not None:
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        self.nStrokes.append(simulated_patient.stateMonitor.nStrokes)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)

        # survival curve
        self.nLivingPatients = PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
