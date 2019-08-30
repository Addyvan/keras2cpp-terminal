'''
  Builds a corridor of encryptors
'''
from algolib.util import eprint

class HallwayOfEncouragement:
  # girth only goes up to 3
  def __init__(self, action_handler, corridor_height=4, girth=3, debug=False):
    self.debug = debug
    self.action_handler = action_handler
    self.corridor_locations = [
      [12,1],
      [15,1],
      [12,2],
      [15,2],
      [12,3],
      [15,3],
      [12,4],
      [15,4],
      [12,6],
      [13,6],
      [14,6],
      [15,6],
    ]

    self.left_door_location = [12,5]
    self.right_door_location = [15,5]

    """
    for i in range(corridor_height):
      self.corridor_locations.append([12, i + 1])
      self.corridor_locations.append([15, i + 1])
      if girth > 1 and i > 0:
        self.corridor_locations.append([11, i + 1])
        self.corridor_locations.append([16, i + 1])
      if girth > 2 and i > 1:
        self.corridor_locations.append([10, i + 1])
        self.corridor_locations.append([17, i + 1])
    """

    self.current_nodes = []
    self.empty_nodes = []

  '''
    Checks the game state for what pieces of the hallway are already built
  '''
  def calculate_current_nodes(self):
    for loc in self.corridor_locations:
      node = self.action_handler.game_state.contains_stationary_unit( loc )
      if node:
        self.current_nodes.append( loc )
      else:
        self.empty_nodes.append( loc )

  '''
    Build an encrypter on the first empty node location
  '''
  def add_node(self):
    if self.debug:
      eprint("CURRENT", self.current_nodes)
      eprint("EMPTY", self.empty_nodes)
    for loc in self.empty_nodes:
      self.action_handler.spawn_encrypter(loc[0], loc[1])
      break
    
    self.empty_nodes = []
    self.current_nodes = []

  def is_left_door_open(self):
    if self.action_handler.game_state.contains_stationary_unit( self.left_door_location ):
      return False
    else:
      return True

  def is_right_door_open(self):
    if self.action_handler.game_state.contains_stationary_unit( self.right_door_location ):
      return False
    else:
      return True

  def toggle_left_door(self):
    if self.action_handler.game_state.contains_stationary_unit( self.left_door_location ):
      self.action_handler.game_state.attempt_remove( self.left_door_location )
    else:
      self.action_handler.spawn_encrypter(self.left_door_location[0], self.left_door_location[1])

  def toggle_right_door(self):
    if self.action_handler.game_state.contains_stationary_unit( self.right_door_location ):
      self.action_handler.game_state.attempt_remove( self.right_door_location )
    else:
      self.action_handler.spawn_encrypter(self.right_door_location[0], self.right_door_location[1])

  def is_full_close(self):
    if self.action_handler.game_state.contains_stationary_unit( self.right_door_location ) and self.action_handler.game_state.contains_stationary_unit( self.left_door_location ):
      return True
    else:
      return False

  def run(self):
    self.current_nodes = []
    self.calculate_current_nodes()
    self.add_node()