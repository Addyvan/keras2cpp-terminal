'''
    Save up until enough Bits are available
    Check for the optimal location to drop a phat stack of EMPS
'''

import algolib
from .stack_attack import StackAttack

class EMPStack(StackAttack):
    unit = algolib.EMP
    def __init__(self, *args, **kwargs):
        super(EMPStack, self).__init__(*args, **kwargs)