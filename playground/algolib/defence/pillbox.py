'''
  Class containing reusable implementation of the pillbox strategy

  Not all of this was coded cleanly 
  since I didnt want to waste too much time rewriting Andrew's code
'''
class PillboxDefence:
  def __init__(self, action_handler, game_state):
    self.action_handler = action_handler
    self.game_state = game_state
    self.pillbox_locations = [
      [2, 11],
      [25, 11],
      [6, 10],
      [21, 10],
      [10, 9],
      [17, 9]
    ]
    self.super_pillbox_locations = []

  def set_game_state(self, game_state):
    self.game_state = game_state

  '''
    Build a 'V' with a destructor and two filters
    -> Pillbox costs: 8
    -> Assumes correct resources
  '''
  def build_pillbox(self, x, y):
    destructorWasSpawned = False
    if not self.game_state.contains_stationary_unit([x, y]):
      destructorWasSpawned = self.action_handler.spawn_destructor(x, y)

    # Build walls but not if they are sniping them
    if destructorWasSpawned:
      if not( (y >= 10) and (sum( False != self.game_state.contains_stationary_unit( loc ) for loc in [[i,14] for i in range(28)]) > 10)):
        self.action_handler.spawn_filter(x - 1, y + 1)
        self.action_handler.spawn_filter(x + 1, y + 1)
  
  """
    Never again
  """
  def build_super_pillbox(self, x, y):
    
    # if they are sniping the walls, don't build them
    if not( (y >= 9) and (6 <= x <=21) and (sum( False != self.game_state.contains_stationary_unit( loc ) for loc in [[i,14] for i in range(28)]) > 10)):
      self.action_handler.spawn_filter(x - 1, y + 2)
      self.action_handler.spawn_filter(x, y + 2)
      self.action_handler.spawn_filter(x +1, y + 2)
    else:
      self.action_handler.spawn_filter(x - 1, y + 1)
      self.action_handler.spawn_filter(x + 1, y + 1)


    if (y >= 10) and (sum( False != self.game_state.contains_stationary_unit( loc ) for loc in [[i,14] for i in range(28)]) > 10):
      self.action_handler.spawn_filter(x - 1, y + 1)
      self.action_handler.spawn_filter(x + 1, y + 1)


    self.action_handler.spawn_destructor(x, y + 1)
    self.action_handler.spawn_destructor(x + 1 - 2 * (x // 14), y) # Why the floor division?

    self.build_pillbox(x, y)
    return True

  def run(self):
    ''' I hate what this has become '''
    self.run_pillbox() 
  '''
    Runs the pillbox strategy
  '''
  def run_pillbox(self):
    # check if my stuff died, if so build a super pillbox
    to_remove = []
    if self.game_state.turn_number >= 4:
      for location in self.pillbox_locations:
        if not self.game_state.contains_stationary_unit(location):
          waRzOne = location
          to_remove.append(waRzOne)
          self.super_pillbox_locations.append( waRzOne )

    self.pillbox_locations = [ l for l in self.pillbox_locations if l not in to_remove ]

    for location in self.pillbox_locations:
      if self.game_state.get_resource(self.game_state.CORES) < 8:
        return
      self.build_pillbox(location[0], location[1])

  def run_superpillbox(self):

    # check if my stuff died, if so build a super pillbox
    to_remove = []
    if self.game_state.turn_number >= 4:
      for location in self.pillbox_locations:
        if not self.game_state.contains_stationary_unit(location):
          waRzOne = location
          to_remove.append(waRzOne)
          self.super_pillbox_locations.append( waRzOne )

    self.pillbox_locations = [ l for l in self.pillbox_locations if l not in to_remove ]

    for location in self.super_pillbox_locations:
      #just dont even build the middle ones if theres a wall
      if (10 <= location[0] <= 17) and (sum( False != self.game_state.contains_stationary_unit( loc ) for loc in [[i,14] for i in range(28)]) > 10):
        if self.game_state.get_resource(self.game_state.CORES) > 18:
          self.build_pillbox(location[0], location[1])
        continue

      if not self.game_state.contains_stationary_unit(location) and self.game_state.get_resource(self.game_state.CORES) < 18:
        # don't build 1 at a time
        return
      if self.build_super_pillbox(location[0], location[1]):
        break