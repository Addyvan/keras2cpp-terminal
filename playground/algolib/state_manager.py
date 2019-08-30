'''
Use this to parse and store state in game

USAGE:
-> On TurnType 1 use parse_state_action
'''
from .util import eprint

class StateManager:
  
  def __init__(self):
    self.states = []
    self.current_damages = [] # too much to store with action phase stuff

  """
    Parses the state at the time of deployment for a turn. Contains:
      -> restorationPhase : FEEL FREE TO 
  """
  def parse_deployment_phase_state(self, state):

    self.current_damages = []

    state_obj = {
      "restorationPhase": self.get_restoration_phase_data(state)
    }
    self.states.append(state_obj)
    return state_obj


  '''
    ANYTHING PARSED HERE WILL REMAIN FOR THE GAME. ONLY PUT THINGS THAT NEED TO BE LOOKED AT BACK IN TIME
    Parses the results of a turn. Contains:
      -> breaches
      -> 
      -> spawns
  '''
  def parse_action_phase_state(self, state, turnIndex):
    if not "actionPhase" in self.states[turnIndex]:
      self.states[turnIndex]["actionPhase"] = {
        "breaches": [],
        "spawns": self.get_spawn_events(state)
      }
    breaches = self.get_breach_events(state)
    self.current_damages = self.current_damages + self.get_damage_events(state)
    self.states[turnIndex]["actionPhase"]["breaches"] = self.states[turnIndex]["actionPhase"]["breaches"] + breaches
  
  def get_breach_events(self, frame):
    breaches = []
    for data in frame["events"]["breach"]:
      breaches.append({
        "player": self.get_player(data[4]),
        "unit_id": data[3],
        "position": {"x": data[0][0], "y": data[0][1]},
        "damage": data[1]
      })
    return breaches

  def get_damage_events(self, frame):
    damages = []
    for data in frame["events"]["damage"]:
      damages.append({
        "player": self.get_player(data[4]),
        "unit_id": data[3],
        "damage": data[2],
        "position": {"x": data[0][0], "y": data[0][1]},
      })
    return damages

  def get_spawn_events(self, frame):
    spawns = []
    for data in frame["events"]["spawn"]:
      spawns.append({
        "player": self.get_player(data[3]),
        "unitType": self.get_unit_type(data[1]),
        "position": {"x": data[0][0], "y": data[0][1]},
        "unit_id": data[2]
      })
    return spawns
  
  def get_player(self, playerIndex):
    if playerIndex == 1:
      return "P1"
    else:
      return "P2"
  
  def get_unit_type(self, unitIndex):
    if unitIndex == 0:
      return "FF"
    elif unitIndex == 1:
      return "EF"
    elif unitIndex == 2:
      return "DF"
    elif unitIndex == 3:
      return "PI"
    elif unitIndex == 4:
      return "EI"
    elif unitIndex == 5:
      return "SI"
  
  '''
    0 : 
    1 : 
    2 : 
  '''
  def get_frame_info(self, turnInfo):
    return int(turnInfo[0]), int(turnInfo[1]), int(turnInfo[2])
  
  def get_restoration_phase_data(self, state):
    p1Stats = self.get_stats(state, "p1")
    p2Stats = self.get_stats(state, "p2")
    return {
      "p1Health": p1Stats["health"],
      "p2Health": p2Stats["health"],
      "p1Cores": p1Stats["cores"],
      "p2Cores": p2Stats["cores"],
      "p1Bits": p1Stats["bits"],
      "p2Bits": p2Stats["bits"]
    }

  def get_stats(self, state, player):
    return {
      "health": state[player + "Stats"][0],
      "cores": state[player + "Stats"][1],
      "bits": state[player + "Stats"][2]
    }