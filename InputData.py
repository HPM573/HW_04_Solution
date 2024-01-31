from enum import Enum

# simulation settings
POP_SIZE = 5000         # cohort population size
SIM_TIME_STEPS = 50    # length of simulation (years)

P_MORTALITY = 0.15  # annual probability of death due to all causes
P_STROKE = 0.05         # annual probability of stroke in state Well
P_RE_STROKE = 0.2     # annual probability of recurrent stroke
P_SURV = 0.7       # probability of surviving a stroke


class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    POST_STROKE = 1
    STROKE_DEATH = 2
    ALL_CAUSE_DEATH = 3
    STROKE = 4


# transition probability matrix without temporary state
TRANS_PROB_MATRIX_1 = [
    [  # Well
        (1-P_MORTALITY)*(1-P_STROKE),  # Well
        (1-P_MORTALITY)*P_STROKE*P_SURV,  # Post-stroke
        (1-P_MORTALITY)*P_STROKE*(1-P_SURV),  # Stroke-death
        P_MORTALITY],   # All-cause mortality

    [  # POST_STROKE
        0,   # Well
        (1-P_MORTALITY)*((1-P_RE_STROKE) + P_RE_STROKE*P_SURV),  # Post-stroke
        (1-P_MORTALITY)*P_RE_STROKE*(1-P_SURV),  # Stroke-death
        P_MORTALITY],  # All-cause mortality

    [   # STOKE DEATH
        0,    # Well
        0,    # Post-stroke
        1,    # Stroke-death
        0],   # All-cause mortality

    [  # ALL_CAUSE DEATH
        0,  # Well
        0,  # Post-stroke
        0,  # Stroke-death
        1],  # All-cause mortality
    ]


# transition probability matrix with temporary state Stroke
TRANS_PROB_MATRIX_2 = [
    [  # Well
        (1 - P_MORTALITY) * (1 - P_STROKE),  # Well
        0,  # Post-stroke
        0,  # Stroke-death
        P_MORTALITY,  # All-cause mortality
        (1 - P_MORTALITY) * P_STROKE],  # Stroke

    [  # POST_STROKE
        0,  # Well
        (1 - P_MORTALITY) * (1 - P_RE_STROKE),  # Post-stroke
        0,  # Stroke-death
        P_MORTALITY,  # All-cause mortality
        (1 - P_MORTALITY) * P_RE_STROKE], # Stroke

    [  # STOKE DEATH
        0,  # Well
        0,  # Post-stroke
        1,  # Stroke-death
        0,  # All-cause mortality
        0], # Stroke

    [  # ALL_CAUSE DEATH
        0,  # Well
        0,  # Post-stroke
        0,  # Stroke-death
        1,  # All-cause mortality
        0],  # Stroke
    [  # STOKE
        0,  # Well
        P_SURV,  # Post-stroke
        1-P_SURV,  # Stroke-death
        0,  # All-cause mortality
        0],  # Stroke
    ]

print('Transition probability matrix without temporary state "Stroke": ', TRANS_PROB_MATRIX_1)
print('Transition probability matrix with temporary state "Stroke":', TRANS_PROB_MATRIX_2)
print('')
