from enum import Enum

# simulation settings
POP_SIZE = 5000         # cohort population size
SIM_TIME_STEPS = 50    # length of simulation (years)

PROB_STROKE_WELL = 0.05         # annual probability of stroke in state Well
PROB_RECURRENT_STROKE = 0.2     # annual probability of recurrent stroke
PROB_SURVIVE_STROKE = 0.7       # probability of surviving a stroke

# transition probability matrix without temporary state
TRANS_PROB_MATRIX_1 = [
    [1-PROB_STROKE_WELL, PROB_STROKE_WELL*PROB_SURVIVE_STROKE, PROB_STROKE_WELL*(1-PROB_SURVIVE_STROKE)], # WELL
    [1-PROB_RECURRENT_STROKE, PROB_RECURRENT_STROKE*PROB_SURVIVE_STROKE, PROB_RECURRENT_STROKE*(1-PROB_SURVIVE_STROKE)], # POST-STROKE
    [0, 0, 1]   # DEATH
    ]


# transition probability matrix with temporary state Stroke
TRANS_PROB_MATRIX_2 = [
    [1-PROB_STROKE_WELL, PROB_STROKE_WELL*PROB_SURVIVE_STROKE, PROB_STROKE_WELL*(1-PROB_SURVIVE_STROKE), 0], # WELL
    [0,  PROB_RECURRENT_STROKE*PROB_SURVIVE_STROKE, PROB_RECURRENT_STROKE*(1-PROB_SURVIVE_STROKE), 1-PROB_RECURRENT_STROKE],  # POST-STROKE 0.3*0.2
    [0, 0, 0, 1],    # DEATH
    [0, 1, 0, 0]  # STROKE
    ]


class HealthState(Enum):
    """ health states of patients """
    WELL = 0
    POST_STROKE = 1
    DEAD = 2
    STROKE = 3


print('Transition probability matrix without Stroke: ', TRANS_PROB_MATRIX_1)
print('Transition probability matrix with Stroke:', TRANS_PROB_MATRIX_2)
