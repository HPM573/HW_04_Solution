import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as PathCls
from InputData import HealthState


class Patient:
    def __init__(self, id, transition_matrix):

        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.tranProbMatrix = transition_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):

        t = 0

        while self.stateMonitor.get_if_alive() and t < n_time_steps:

            # find the transition probabilities to future states
            trans_prob = self.tranProbMatrix[self.stateMonitor.currentState.value]

            # create an empirical distribution
            empirical_dist = RVGs.Empirical(probabilities=trans_prob)

            # sample from the empirical distribution to get a new state
            new_state_index = empirical_dist.sample(rng=self.rng)

            # update health state
            self.stateMonitor.update(time_step=t,new_state=HealthState(new_state_index))

            # increment time
            t += 1


class PatientBonus:
    def __init__(self, id, prob_stroke_well, prob_recurrent_stroke, prob_survive):

        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.probStrokeWell = prob_stroke_well
        self.probRecurrentStroke = prob_recurrent_stroke
        self.probSurvive = prob_survive
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):

        t = 0

        while self.stateMonitor.get_if_alive() and t < n_time_steps:

            # if the patient is in Well or Post-Stoke
            if self.stateMonitor.currentState is HealthState.WELL or HealthState.POST_STROKE:

                # find the probability of stroke
                if self.stateMonitor.currentState is HealthState.WELL:
                    p_stroke = self.probStrokeWell
                else:
                    p_stroke = self.probRecurrentStroke

                # decide if the patient will have a stroke
                if self.rng.sample() < p_stroke:

                    # increment the number of strokes
                    self.stateMonitor.nStrokes += 1

                    # decide if the patient will survive this stoke
                    if self.rng.sample() < self.probSurvive:
                        new_state_index = HealthState.POST_STROKE.value
                    else:
                        new_state_index = HealthState.DEAD.value

                else:  # no stoke
                    new_state_index = self.stateMonitor.currentState
            else:
                new_state_index = self.stateMonitor.currentState

            # update health state
            self.stateMonitor.update(time_step=t, new_state=HealthState(new_state_index))

            # increment time
            t += 1


class PatientStateMonitor:
    def __init__(self):

        self.currentState = HealthState.WELL    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nStrokes = 0

    def update(self, time_step, new_state):

        if new_state == HealthState.DEAD:
            self.survivalTime = time_step + 0.5  # correct for half cycle effect

        if self.currentState == HealthState.STROKE:
            self.nStrokes += 1

        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState != HealthState.DEAD:
            return True
        else:
            return False


class Cohort:
    def __init__(self, id, pop_size, transition_matrix):
        self.id = id
        self.patients = []
        self.cohortOutcomes = CohortOutcomes()

        for i in range(pop_size):
            patient = Patient(id=id*pop_size + i, transition_matrix=transition_matrix)
            self.patients.append(patient)

    def simulate(self, n_time_steps):

        for patient in self.patients:
            patient.simulate(n_time_steps)

        self.cohortOutcomes.extract_outcomes(self.patients)


class CohortBonus:
    def __init__(self, id, pop_size, prob_stroke_well,prob_recurrent_stroke, prob_survive):
        self.id = id
        self.patients = []
        self.cohortOutcomes = CohortOutcomes()

        for i in range(pop_size):
            patient = PatientBonus(id=id* pop_size + i,
                                   prob_stroke_well=prob_stroke_well,
                                   prob_recurrent_stroke=prob_recurrent_stroke,
                                   prob_survive=prob_survive)
            self.patients.append(patient)

    def simulate(self, n_time_steps):

        for patient in self.patients:
            patient.simulate(n_time_steps)

        self.cohortOutcomes.extract_outcomes(self.patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nStrokes = []
        self.nLivingPatients = None
        self.meanSurvivalTime = None

    def extract_outcomes(self, simulated_patients):
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
                self.nStrokes.append(patient.stateMonitor.nStrokes)

        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)

        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name = '# of living patients',
            initial_size= len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
