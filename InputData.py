from enum import Enum

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_TIME_STEPS = 50    # length of simulation (years)

# transition matrix
TRANS_MATRIX = [
    [0.95,  0.035,    0.015], #WELL
    [0.8,     0.14,   0.06],  #POST-STROKE
    [0,     0,      1]        #DEATH
    ]


TRANS_MATRIX_STROKE = [
    [0.95, 0.035, 0, 0.015], #WELL
    [0, 0, 0.7, 0.3],  #STROKE
    [0,  0.2, 0.8, 0],#POST-STROKE
    [0, 0, 0, 1] #DEATH
    ]


class HealthState(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEAD = 3


