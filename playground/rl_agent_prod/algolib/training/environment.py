
import numpy as np

from algolib.util import eprint

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

class PingEnvironment(py_environment.Base):

  def __init__(self, rl_wrapper):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=27, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(1,2520), dtype=np.int32, minimum=0, name='observation')
    self._state = np.zeros((1,2520))
    self._episode_ended = False

    self.rl_wrapper = rl_wrapper

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def reset(self):
    self._state = 0
    self._episode_ended = False
    return ts.restart(np.array([self._state], dtype=np.int32))

  def step(self, action):
    """Applies the action and returns the new `TimeStep`."""
    
    '''
    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()
    '''
    
    state = self.rl_wrapper.get_state()
    reward = self.rl_wrapper.get_reward()

    eprint("ENV REWARD", reward)
    return ts.termination(state, reward)

if __name__ == "__main__":
  print("icit")