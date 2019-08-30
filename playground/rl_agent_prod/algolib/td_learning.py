"""

Shelving this until we get a simulator going

<state, action, reward>

St -> At -> Rt -> St+1 -> At+1 -> Rt+1 -> St+2 ...

"""

"""
TD(1) Update Rule

Episode T
  For all S, e(s)=0 at start of episode, Vt(S) = Vt-1(S)
  After St-1 -> Rt -> St : (step t)
    e(St-1) = e(St-1) + 1
  For all s,
    Vt(s) = Vt(s) + alpha_t*(Rt + gamma*Vt-1(St) - Vt-1(St-1))e(S)
    e(s) = gamma * e(s)

"""


class TDLearner:
  def __init__(self, learning_rate):
    self.learning_rate = learning_rate

  """
  """
  def reward(self):
    pass
  
  """
  """
  def run_episode(self):
    pass
  
