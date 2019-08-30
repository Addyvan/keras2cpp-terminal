'''
File containing all the basic actions that can't be performed
'''
from .util import eprint
import algolib.gamelib as gamelib
from .units import FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER

class ActionHandler:
  def __init__(self):
    self.game_state = None
  
  def set_game_state(self, game_state):
    self.game_state = game_state
  
  def spawn_filter(self, x,y):
    if not self.game_state.can_spawn(FILTER, [x,y]):
      #eprint("ERROR: CAN'T SPAWN FILTER (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(FILTER, [x,y])
      return True
  
  def spawn_encrypter(self, x,y):
    if not self.game_state.can_spawn(ENCRYPTOR, [x,y]):
      #eprint("ERROR: CAN'T SPAWN ENCRYPTOR (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(ENCRYPTOR, [x,y])
      return True
  
  def spawn_destructor(self, x,y):
    if not self.game_state.can_spawn(DESTRUCTOR, [x,y]):
      eprint("ERROR: CAN'T SPAWN DESTRUCTOR (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(DESTRUCTOR, [x,y])
      return True
  
  def spawn_ping(self, x,y):
    if not self.game_state.can_spawn(PING, [x,y]):
      eprint("ERROR: CAN'T SPAWN PING (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(PING, [x,y])
      return True
  
  def spawn_emp(self, x,y):
    if not self.game_state.can_spawn(EMP, [x,y]):
      eprint("ERROR: CAN'T SPAWN EMP (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(EMP, [x,y])
      return True
  
  def spawn_scrambler(self, x,y):
    if not self.game_state.can_spawn(SCRAMBLER, [x,y]):
      eprint("ERROR: CAN'T SPAWN SCRAMBLER (Addy wrote this, not from lib)")
      return False
    else:
      self.game_state.attempt_spawn(SCRAMBLER, [x,y])
      return True