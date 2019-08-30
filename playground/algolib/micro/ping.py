"""
Current challenge to solve:
-> How to we encode multiple units residing on a single location as well as how much health is currently attributed to a unit
-> curent sol^n is to have a 6 long vector with the integer value of how many units are on a particular spot 
"""

import random
import numpy as np
from algolib.util import eprint

class PingPlacementAI:

  """
    Hyper parameters:
      -> alpha : The weight of HP damage for the reward function
      -> beta : The weight of unit damage for the reward function
  """
  def __init__(self, _alpha=10, _beta=1):
    self.alpha = _alpha # reward weight for damage done to player (hp)
    self.beta = _beta # reward weight for damage done to other units

    # For now: index in list corresponds to matching <State, Action, Reward> combos
    self.data = {
      "current_states": [],
      "current_actions": [],
      "current_unit_ids": [],
      "current_rewards": [],
    }
    self.current_tf_index = 0 # This stores which action is currently of interest to tensorflow

  def create_state_matrix(self, p1Units, p2Units):
    """
      Parses the relevant state

      State consists of: 
        -> Vector< Vector<int>(size=6) >(size=420)
        -> Combining these gives matrix 6x420 or a 1x2520 vector
    """
    state = np.zeros((420,6))
    for units in [p1Units, p2Units]:
      for unit_type_index, unit_data in enumerate(units):
        for unit in unit_data:
          index = self.map_state_loc_to_int( (unit[0], unit[1]) )
          state[index][unit_type_index] += 1
    self.data["current_states"].append(state)
    return state

  def calculate_all_rewards(self, breach_events, damage_events):
    """
      Loops through all pings spawned in a turn in order to attribute them their reward values
    """
    for i, ping_unit_id in enumerate(self.data["current_unit_ids"]):
      #eprint("getting reward for "+str(i)+"th element")
      self.data["current_rewards"].append(self.calculate_reward(ping_unit_id, breach_events, damage_events))

  def calculate_reward(self, ping_unit_id, breach_events, damage_events) -> float:
    """
      Calculates the reward of a single ping placement given an action
    """

    if ping_unit_id == -1:
      return 0.0

    damage_done_to_enemy_hp = self.get_hp_damage(ping_unit_id, breach_events)
    damage_done_to_enemy_buildings = self.get_building_damage(ping_unit_id, damage_events)
    reward = ( (self.alpha * damage_done_to_enemy_hp) + (self.beta * damage_done_to_enemy_buildings) )
    #eprint("CALCULATED REWARD: ", reward)
    return reward

  def get_hp_damage(self, ping_unit_id, breach_events):
    """
      Given a ping id, get the total hp / breach damage done by that ping
    """
    total_hp_damage = 0
    for breach in breach_events:
      if breach["unit_id"] == ping_unit_id:
        total_hp_damage += breach["damage"]
    return total_hp_damage

  def get_building_damage(self, ping_unit_id, damage_events):
    """
      Given a ping id, get the total hp / breach damage done by that ping
    """

    total_building_damage = 0
    for dmg_obj in damage_events:
      if dmg_obj["unit_id"] == ping_unit_id:
        total_building_damage += dmg_obj["damage"]
    return total_building_damage
    
  '''
    Takes as input an integer from 0 to 27 representing a placement decision
    and converts it to a game coordinate
  '''
  def map_action_int_to_game_loc(self, i):
    return [
      [0,13], # 0
      [1,12], # 1
      [2,11], # 2
      [3,10], # 3
      [4,9], # 4
      [5,8], # 5
      [6,7], # 6
      [7,6], # 7
      [8,5], # 8
      [9,4], # 9
      [10,3], # 10
      [11,2], # 11
      [12,1], # 12
      [13,0], # 13
      [14,0], # 14
      [15,1], # 15
      [16,2], # 16
      [17,3], # 17
      [18,4], # 18
      [19,5], # 19
      [20,6], # 20
      [21,7], # 21
      [22,8], # 22
      [23,9], # 23
      [24,10], # 24
      [25,11], # 25
      [26,12], # 26
      [27,13] # 27
    ][i]

  '''
    Takes as input a list or tuple representing a location in the state space
    and converts it to an integer
  '''
  def map_state_loc_to_int(self, loc) -> int:
    # so that input can be list or tuple
    if type(loc) == list:
      loc = (loc[0], loc[1])
    
    locs_map = {'0': {'13': 0, '14': 1}, '1': {'12': 2, '13': 3, '14': 4, '15': 5}, '2': {'11': 6, '12': 7, '13': 8, '14': 9, '15': 10, '16': 11}, '3': {'10': 12, '11': 13, '12': 14, '13': 15, '14': 16, '15': 17, '16': 18, '17': 19}, '4': {'9': 20, '10': 21, '11': 22, '12': 23, '13': 24, '14': 25, '15': 26, '16': 27, '17': 28, '18': 29}, '5': {'8': 30, '9': 31, '10': 32, '11': 33, '12': 34, '13': 35, '14': 36, '15': 37, '16': 38, '17': 39, '18': 40, '19': 41}, '6': {'7': 42, '8': 43, '9': 44, '10': 45, '11': 46, '12': 47, '13': 48, '14': 49, '15': 50, '16': 51, '17': 52, '18': 53, '19': 54, '20': 55}, '7': {'6': 56, '7': 57, '8': 58, '9': 59, '10': 60, '11': 61, '12': 62, '13': 63, '14': 64, '15': 65, '16': 66, '17': 67, '18': 68, '19': 69, '20': 70, '21': 71}, '8': {'5': 72, '6': 73, '7': 74, '8': 75, '9': 76, '10': 77, '11': 78, '12': 79, '13': 80, '14': 81, '15': 82, '16': 83, '17': 84, '18': 85, '19': 86, '20': 87, '21': 88, '22': 89}, '9': {'4': 90, '5': 91, '6': 92, '7': 93, '8': 94, '9': 95, '10': 96, '11': 97, '12': 98, '13': 99, '14': 100, '15': 101, '16': 102, '17': 103, '18': 104, '19': 105, '20': 106, '21': 107, '22': 108, '23': 109}, '10': {'3': 110, '4': 111, '5': 112, '6': 113, '7': 114, '8': 115, '9': 116, '10': 117, '11': 118, '12': 119, '13': 120, '14': 121, '15': 122, '16': 123, '17': 124, '18': 125, '19': 126, '20': 127, '21': 128, '22': 129, '23': 130, '24': 131}, '11': {'2': 132, '3': 133, '4': 134, '5': 135, '6': 136, '7': 137, '8': 138, '9': 139, '10': 140, '11': 141, '12': 142, '13': 143, '14': 144, '15': 145, '16': 146, '17': 147, '18': 148, '19': 149, '20': 150, '21': 151, '22': 152, '23': 153, '24': 154, '25': 155}, '12': {'1': 156, '2': 157, '3': 158, '4': 159, '5': 160, '6': 161, '7': 162, '8': 163, '9': 164, '10': 165, '11': 166, '12': 167, '13': 168, '14': 169, '15': 170, '16': 171, '17': 172, '18': 173, '19': 174, '20': 175, '21': 176, '22': 177, '23': 178, '24': 179, '25': 180, '26': 181}, '13': {'0': 182, '1': 183, '2': 184, '3': 185, '4': 186, '5': 187, '6': 188, '7': 189, '8': 190, '9': 191, '10': 192, '11': 193, '12': 194, '13': 195, '14': 196, '15': 197, '16': 198, '17': 199, '18': 200, '19': 201, '20': 202, '21': 203, '22': 204, '23': 205, '24': 206, '25': 207, '26': 208, '27': 209}, '14': {'0': 210, '1': 211, '2': 212, '3': 213, '4': 214, '5': 215, '6': 216, '7': 217, '8': 218, '9': 219, '10': 220, '11': 221, '12': 222, '13': 223, '14': 224, '15': 225, '16': 226, '17': 227, '18': 228, '19': 229, '20': 230, '21': 231, '22': 232, '23': 233, '24': 234, '25': 235, '26': 236, '27': 237}, '15': {'1': 238, '2': 239, '3': 240, '4': 241, '5': 242, '6': 243, '7': 244, '8': 245, '9': 246, '10': 247, '11': 248, '12': 249, '13': 250, '14': 251, '15': 252, '16': 253, '17': 254, '18': 255, '19': 256, '20': 257, '21': 258, '22': 259, '23': 260, '24': 261, '25': 262, '26': 263}, '16': {'2': 264, '3': 265, '4': 266, '5': 267, '6': 268, '7': 269, '8': 270, '9': 271, '10': 272, '11': 273, '12': 274, '13': 275, '14': 276, '15': 277, '16': 278, '17': 279, '18': 280, '19': 281, '20': 282, '21': 283, '22': 284, '23': 285, '24': 286, '25': 287}, '17': {'3': 288, '4': 289, '5': 290, '6': 291, '7': 292, '8': 293, '9': 294, '10': 295, '11': 296, '12': 297, '13': 298, '14': 299, '15': 300, '16': 301, '17': 302, '18': 303, '19': 304, '20': 305, '21': 306, '22': 307, '23': 308, '24': 309}, '18': {'4': 310, '5': 311, '6': 312, '7': 313, '8': 314, '9': 315, '10': 316, '11': 317, '12': 318, '13': 319, '14': 320, '15': 321, '16': 322, '17': 323, '18': 324, '19': 325, '20': 326, '21': 327, '22': 328, '23': 329}, '19': {'5': 330, '6': 331, '7': 332, '8': 333, '9': 334, '10': 335, '11': 336, '12': 337, '13': 338, '14': 339, '15': 340, '16': 341, '17': 342, '18': 343, '19': 344, '20': 345, '21': 346, '22': 347}, '20': {'6': 348, '7': 349, '8': 350, '9': 351, '10': 352, '11': 353, '12': 354, '13': 355, '14': 356, '15': 357, '16': 358, '17': 359, '18': 360, '19': 361, '20': 362, '21': 363}, '21': {'7': 364, '8': 365, '9': 366, '10': 367, '11': 368, '12': 369, '13': 370, '14': 371, '15': 372, '16': 373, '17': 374, '18': 375, '19': 376, '20': 377}, '22': {'8': 378, '9': 379, '10': 380, '11': 381, '12': 382, '13': 383, '14': 384, '15': 385, '16': 386, '17': 387, '18': 388, '19': 389}, '23': {'9': 390, '10': 391, '11': 392, '12': 393, '13': 394, '14': 395, '15': 396, '16': 397, '17': 398, '18': 399}, '24': {'10': 400, '11': 401, '12': 402, '13': 403, '14': 404, '15': 405, '16': 406, '17': 407}, '25': {'11': 408, '12': 409, '13': 410, '14': 411, '15': 412, '16': 413}, '26': {'12': 414, '13': 415, '14': 416, '15': 417}, '27': {'13': 418, '14': 419}}
    return locs_map[str(loc[0])][str(loc[1])]


if __name__ == "__main__":
  ping_placement = PingPlacementAI()
  ping_placement.create_state_matrix([1,2,3], [1,2,3])