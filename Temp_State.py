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
        t=0

        while self.stateMonitor.get_if_alive() and t < n_time_steps:
            trans_prob = self.tranProbMatrix[self.stateMonitor.currentState.value] # find the transition probabilities to future states

            empirical_dist = RVGs.Empirical(probabilities=trans_prob) #creae an empirical distribution

            new_state_index = empirical_dist.sample(rng=self.rng) #sample from the empirical distribution to get a new state

            self.stateMonitor.update(time_step=t,new_state=HealthState(new_state_index)) #update health state

            t += 1 #increment time


class PatientStateMonitor:
    def __init__(self):

        self.currentState = HealthState.WELL
        self.survivalTime = None
        self.stroke_num = 0

    def update(self, time_step, new_state):

        if new_state == HealthState.DEAD:
            self.survivalTime = time_step + 0.5 #correct for half cycle effect

        if self.currentState == HealthState.STROKE:
            self.stroke_num += 1

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
            patient = Patient(id=id* pop_size + i, transition_matrix=transition_matrix)
            self.patients.append(patient)

    def simulate(self, n_time_steps):

        for patient in self.patients:
            patient.simulate(n_time_steps)

        self.cohortOutcomes.extract_outcomes(self.patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nLivingPatients = None
        self.nStrokes = []
        self.meanSurvivalTime = None

    def extract_outcomes(self, simulated_patients):
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            if not (patient.stateMonitor.stroke_num is 0):
                self.nStrokes.append(patient.stateMonitor.stroke_num)

        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)

        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name = '# of living patients',
            initial_size= len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )

