'''
    Save up until enough Bits are available
    Check for the optimal location to drop a phat stack of PINGS
'''

import algolib
from .stack_attack import StackAttack

class PingStack(StackAttack):
    unit = algolib.PING
    def __init__(self, *args, **kwargs):
        super(PingStack, self).__init__(*args, **kwargs)