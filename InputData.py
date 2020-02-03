from enum import Enum

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_TIME_STEPS = 50    # length of simulation (years)

P_STROKE = 0.05         # annual probability of stroke in state Well
P_RE_STROKE = 0.2     # annual probability of recurrent stroke
P_SURV = 0.7       # probability of surviving a stroke


class HealthState(Enum):
    """ health states of patients """
    WELL = 0
    POST_STROKE = 1
    DEAD = 2
    STROKE = 3


# transition probability matrix without temporary state
TRANS_PROB_MATRIX_1 = [
    [1-P_STROKE,    P_STROKE*P_SURV,                    P_STROKE*(1-P_SURV)],       # WELL
    [0,             (1-P_RE_STROKE)+P_RE_STROKE*P_SURV, P_RE_STROKE*(1-P_SURV)],    # POST-STROKE
    [0,             0,                                  1]                          # DEATH
    ]


# transition probability matrix with temporary state Stroke
TRANS_PROB_MATRIX_2 = [
    [1 - P_STROKE,  0,              0,          P_STROKE],      # WELL
    [0,             1-P_RE_STROKE,  0,          P_RE_STROKE],   # POST-STROKE
    [0,             0,              0,          1],             # DEATH
    [0,             P_SURV,         1-P_SURV,   0]              # STROKE
    ]

print('Transition probability matrix without temporary state "Stroke": ', TRANS_PROB_MATRIX_1)
print('Transition probability matrix with temporary state "Stroke":', TRANS_PROB_MATRIX_2)
print('')
