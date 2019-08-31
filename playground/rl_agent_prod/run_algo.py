# Imports for if running from outside folder
import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../..")))

import random
import time

from algolib.algo_base import AlgoBase
from algolib.util import eprint

from keras_cpp_model import KerasCPPModel

class RLProdBot(AlgoBase):

    def __init__(self):
        super().__init__()

        self.state = None
        self.this_turn_spawns = []
        self.load_models()


    def load_models(self):
        self.bits_macro_model = KerasCPPModel("./rl_agent_prod/nnets/fdeep_bits_macro.json")
        self.cores_macro_model = KerasCPPModel("./rl_agent_prod/nnets/fdeep_cores_macro.json")
        self.ping_model = KerasCPPModel("./rl_agent_prod/nnets/fdeep_ping.json")
        self.emp_model = KerasCPPModel("./rl_agent_prod/nnets/fdeep_emp.json")
        self.scrambler_model = KerasCPPModel("./rl_agent_prod/nnets/fdeep_scrambler.json")

    def on_turn(self, json_state):
        """
        Runs every turn
        """
        start = time.time()
        self.this_turn_spawns = [] # NEED TO IMPLEMENT THIS
        self.state = create_state_matrix(self.p1Units, self.p2Units, self.this_turn_spawns)

        # FIGURE OUT STATE
        bits = self.game_state.get_resource(self.game_state.BITS)
        cores = self.game_state.get_resource(self.game_state.CORES)

        self.execute_cores_macro(cores)
        self.execute_bits_macro(bits)
        end = time.time()
        eprint("TURN {} took {} seconds".format(self.game_state.turn_number, end-start))


    def execute_bits_macro(self, bits):
        """
        Called every turn to see what to do with bits
        """

        action_sequence = []
        while bits >= 1:
            #action = np.argmax(self.macro_bits_model.predict(self.state.reshape((1, 420,6)))[0])
            action = self.bits_macro_model.predict(self.state)[0]
            if action == 0:
                bits -= 1
            elif action == 1:
                bits -= 1
            elif action == 2:
                bits -= 3
            elif action == 3:
                bits -= 1
            action_sequence.append(action)
        eprint(action_sequence)
        for action in action_sequence:
            if action == 0:
                continue
            elif action == 1:
                self.spawn_ping(self.ping_model.predict(self.state)[0])
                continue
            elif action == 2:
                self.spawn_emp(self.emp_model.predict(self.state)[0])
                continue
            elif action == 3:
                self.spawn_scrambler(self.scrambler_model.predict(self.state)[0])

    def execute_cores_macro(self, cores):
        """
        Called every turn to see what to do with bits
        """

        action_sequence = []
        while cores >= 1:
            #action = np.argmax(self.macro_cores_model.predict(self.state.reshape((1, 420,6)))[0])
            action = self.cores_macro_model.predict(self.state)[0]
            if action == 0:
                cores -= 1
            elif action == 1:
                cores -= 1
            elif action == 2:
                cores -= 4
            elif action == 3:
                cores -= 6
            action_sequence.append(action)

        for action in action_sequence:
            cores = self.game_state.get_resource(self.game_state.BITS)
            if action == 0:
                continue
            elif action == 1:
                """
                recommendations = self.filter_model.predict(self.state.reshape((1, 420,6)))[0]
                placement_locs = np.argsort(-recommendations)
                
                index = 0
                while not self.spawn_filter(placement_locs[index]) and index < 100:
                    index += 1
                if index >= 100:
                    continue
                
                placement_loc = index
                """
                placement_loc = random.randint(0,209)
                self.spawn_filter(placement_loc)
            elif action == 2:
                """
                recommendations = self.encryptor_model.predict(self.state.reshape((1, 420,6)))[0]
                placement_locs = np.argsort(-recommendations)
                
                index = 0
                while not self.spawn_encryptor(placement_locs[index]) and index < 100:
                    index += 1
                if index >= 100:
                    continue
                
                placement_loc = index
                """
                placement_loc = random.randint(0,209)
                self.spawn_encryptor(placement_loc)
            elif action == 3:
                """
                recommendations = self.destructor_model.predict(self.state.reshape((1, 420,6)))[0]
                placement_locs = np.argsort(-recommendations)
                
                index = 0
                while not self.spawn_destructor(placement_locs[index]) and index < 100:
                    index += 1
                if index >= 100:
                    continue
                
                placement_loc = index
                """
                placement_loc = random.randint(0,209)
                self.spawn_destructor(placement_loc)
            if action > 0:
                self.state = self.update_state(self.state, action-1, placement_loc)

    def update_state(self, state, state_i, action):
        """
        Fixes state to include spawns 
        """
        state[action][state_i] += 1
        return state

    def spawn_ping(self, action):
        action_loc = map_offensive_action_int_to_game_loc(action)

        if self.game_state.can_spawn("PI", action_loc):
            self.game_state.attempt_spawn("PI", action_loc)
    
    def spawn_emp(self, action):
        action_loc = map_offensive_action_int_to_game_loc(action)

        if self.game_state.can_spawn("EI", action_loc):
            self.game_state.attempt_spawn("EI", action_loc)
    
    def spawn_scrambler(self, action):
        action_loc = map_offensive_action_int_to_game_loc(action)

        if self.game_state.can_spawn("SI", action_loc):
            self.game_state.attempt_spawn("SI", action_loc)

    def spawn_filter(self, action):
        action_loc = map_defensive_action_int_to_game_loc(action)
        action_loc = [int(action_loc[0]), int(action_loc[1])]
        if self.game_state.can_spawn("FF", action_loc):
            self.game_state.attempt_spawn("FF", action_loc)
            return True
        else:
            return False
    
    def spawn_encryptor(self, action):
        action_loc = map_defensive_action_int_to_game_loc(action)
        action_loc = [int(action_loc[0]), int(action_loc[1])]
        if self.game_state.can_spawn("EF", action_loc):
            self.game_state.attempt_spawn("EF", action_loc)
            return True
        else:
            return False
    
    def spawn_destructor(self, action):
        action_loc = map_defensive_action_int_to_game_loc(action)
        action_loc = [int(action_loc[0]), int(action_loc[1])]
        if self.game_state.can_spawn("DF", action_loc):
            self.game_state.attempt_spawn("DF", action_loc)
            return True
        else:
            return False

    def on_spawn_frame(self, spawn_events):
        self.this_turn_spawns = spawn_events

    def on_turn_end(self):
        #eprint("TURN ENDED")
        pass

    def on_game_end(self):
        eprint("GAME END AFTER {} TURNS".format(self.game_state.turn_number))

def create_state_matrix(p1Units, p2Units, this_turn_spawns):
    state = [[0 for j in range(6)] for i in range(420)]
    for p, units in enumerate([p1Units, p2Units]):
        for unit_type_index, unit_data in enumerate(units):
            for unit in unit_data:
                x = unit[0]
                y = unit[1]
                # flip if p2 since the bot will only ever play from p1's perspective
                index = map_state_loc_to_int( (x, y) )
                if unit_type_index < 6:
                    state[index][unit_type_index] += 1

    for spawn in this_turn_spawns:
        x = spawn[0][0]
        y = spawn[0][1]
        
        index = map_state_loc_to_int( (x, y) )
        if spawn[1] < 6:
            state[index][spawn[1]] += 1

    return state

def map_defensive_action_int_to_game_loc(i):
    def_locs = {0: ('13', '0'), 1: ('14', '0'), 2: ('12', '1'), 3: ('13', '1'), 4: ('14', '1'), 5: ('15', '1'), 6: ('11', '2'), 7: ('12', '2'), 8: ('13', '2'), 9: ('14', '2'), 10: ('15', '2'), 11: ('16', '2'), 12: ('10', '3'), 13: ('11', '3'), 14: ('12', '3'), 15: ('13', '3'), 16: ('14', '3'), 17: ('15', '3'), 18: ('16', '3'), 19: ('17', '3'), 20: ('9', '4'), 21: ('10', '4'), 22: ('11', '4'), 23: ('12', '4'), 24: ('13', '4'), 25: ('14', '4'), 26: ('15', '4'), 27: ('16', '4'), 28: ('17', '4'), 29: ('18', '4'), 30: ('8', '5'), 31: ('9', '5'), 32: ('10', '5'), 33: ('11', '5'), 34: ('12', '5'), 35: ('13', '5'), 36: ('14', '5'), 37: ('15', '5'), 38: ('16', '5'), 39: ('17', '5'), 40: ('18', '5'), 41: ('19', '5'), 42: ('7', '6'), 43: ('8', '6'), 44: ('9', '6'), 45: ('10', '6'), 46: ('11', '6'), 47: ('12', '6'), 48: ('13', '6'), 49: ('14', '6'), 50: ('15', '6'), 51: ('16', '6'), 52: ('17', '6'), 53: ('18', '6'), 54: ('19', '6'), 55: ('20', '6'), 56: ('6', '7'), 57: ('7', '7'), 58: ('8', '7'), 59: ('9', '7'), 60: ('10', '7'), 61: ('11', '7'), 62: ('12', '7'), 63: ('13', '7'), 64: ('14', '7'), 65: ('15', '7'), 66: ('16', '7'), 67: ('17', '7'), 68: ('18', '7'), 69: ('19', '7'), 70: ('20', '7'), 71: ('21', '7'), 72: ('5', '8'), 73: ('6', '8'), 74: ('7', '8'), 75: ('8', '8'), 76: ('9', '8'), 77: ('10', '8'), 78: ('11', '8'), 79: ('12', '8'), 80: ('13', '8'), 81: ('14', '8'), 82: ('15', '8'), 83: ('16', '8'), 84: ('17', '8'), 85: ('18', '8'), 86: ('19', '8'), 87: ('20', '8'), 88: ('21', '8'), 89: ('22', '8'), 90: ('4', '9'), 91: ('5', '9'), 92: ('6', '9'), 93: ('7', '9'), 94: ('8', '9'), 95: ('9', '9'), 96: ('10', '9'), 97: ('11', '9'), 98: ('12', '9'), 99: ('13', '9'), 100: ('14', '9'), 101: ('15', '9'), 102: ('16', '9'), 103: ('17', '9'), 104: ('18', '9'), 105: ('19', '9'), 106: ('20', '9'), 107: ('21', '9'), 108: ('22', '9'), 109: ('23', '9'), 110: ('3', '10'), 111: ('4', '10'), 112: ('5', '10'), 113: ('6', '10'), 114: ('7', '10'), 115: ('8', '10'), 116: ('9', '10'), 117: ('10', '10'), 118: ('11', '10'), 119: ('12', '10'), 120: ('13', '10'), 121: ('14', '10'), 122: ('15', '10'), 123: ('16', '10'), 124: ('17', '10'), 125: ('18', '10'), 126: ('19', '10'), 127: ('20', '10'), 128: ('21', '10'), 129: ('22', '10'), 130: ('23', '10'), 131: ('24', '10'), 132: ('2', '11'), 133: ('3', '11'), 134: ('4', '11'), 135: ('5', '11'), 136: ('6', '11'), 137: ('7', '11'), 138: ('8', '11'), 139: ('9', '11'), 140: ('10', '11'), 141: ('11', '11'), 142: ('12', '11'), 143: ('13', '11'), 144: ('14', '11'), 145: ('15', '11'), 146: ('16', '11'), 147: ('17', '11'), 148: ('18', '11'), 149: ('19', '11'), 150: ('20', '11'), 151: ('21', '11'), 152: ('22', '11'), 153: ('23', '11'), 154: ('24', '11'), 155: ('25', '11'), 156: ('1', '12'), 157: ('2', '12'), 158: ('3', '12'), 159: ('4', '12'), 160: ('5', '12'), 161: ('6', '12'), 162: ('7', '12'), 163: ('8', '12'), 164: ('9', '12'), 165: ('10', '12'), 166: ('11', '12'), 167: ('12', '12'), 168: ('13', '12'), 169: ('14', '12'), 170: ('15', '12'), 171: ('16', '12'), 172: ('17', '12'), 173: ('18', '12'), 174: ('19', '12'), 175: ('20', '12'), 176: ('21', '12'), 177: ('22', '12'), 178: ('23', '12'), 179: ('24', '12'), 180: ('25', '12'), 181: ('26', '12'), 182: ('0', '13'), 183: ('1', '13'), 184: ('2', '13'), 185: ('3', '13'), 186: ('4', '13'), 187: ('5', '13'), 188: ('6', '13'), 189: ('7', '13'), 190: ('8', '13'), 191: ('9', '13'), 192: ('10', '13'), 193: ('11', '13'), 194: ('12', '13'), 195: ('13', '13'), 196: ('14', '13'), 197: ('15', '13'), 198: ('16', '13'), 199: ('17', '13'), 200: ('18', '13'), 201: ('19', '13'), 202: ('20', '13'), 203: ('21', '13'), 204: ('22', '13'), 205: ('23', '13'), 206: ('24', '13'), 207: ('25', '13'), 208: ('26', '13'), 209: ('27', '13')}
    return def_locs[i]

def map_offensive_action_int_to_game_loc(i):
    return [[0,13], [1,12],[2,11], [3,10], [4,9],[5,8],[6,7], [7,6],[8,5], [9,4], [10,3], [11,2],[12,1], [13,0], [14,0], [15,1], [16,2], [17,3], [18,4],[19,5], [20,6], [21,7], [22,8], [23,9], [24,10], [25,11], [26,12], [27,13] ][i]

def map_state_loc_to_int(loc):
    # so that input can be list or tuple
    if type(loc) == list:
        loc = (loc[0], loc[1])

    locs_map = {'0': {'13': 0, '14': 1}, '1': {'12': 2, '13': 3, '14': 4, '15': 5}, '2': {'11': 6, '12': 7, '13': 8, '14': 9, '15': 10, '16': 11}, '3': {'10': 12, '11': 13, '12': 14, '13': 15, '14': 16, '15': 17, '16': 18, '17': 19}, '4': {'9': 20, '10': 21, '11': 22, '12': 23, '13': 24, '14': 25, '15': 26, '16': 27, '17': 28, '18': 29}, '5': {'8': 30, '9': 31, '10': 32, '11': 33, '12': 34, '13': 35, '14': 36, '15': 37, '16': 38, '17': 39, '18': 40, '19': 41}, '6': {'7': 42, '8': 43, '9': 44, '10': 45, '11': 46, '12': 47, '13': 48, '14': 49, '15': 50, '16': 51, '17': 52, '18': 53, '19': 54, '20': 55}, '7': {'6': 56, '7': 57, '8': 58, '9': 59, '10': 60, '11': 61, '12': 62, '13': 63, '14': 64, '15': 65, '16': 66, '17': 67, '18': 68, '19': 69, '20': 70, '21': 71}, '8': {'5': 72, '6': 73, '7': 74, '8': 75, '9': 76, '10': 77, '11': 78, '12': 79, '13': 80, '14': 81, '15': 82, '16': 83, '17': 84, '18': 85, '19': 86, '20': 87, '21': 88, '22': 89}, '9': {'4': 90, '5': 91, '6': 92, '7': 93, '8': 94, '9': 95, '10': 96, '11': 97, '12': 98, '13': 99, '14': 100, '15': 101, '16': 102, '17': 103, '18': 104, '19': 105, '20': 106, '21': 107, '22': 108, '23': 109}, '10': {'3': 110, '4': 111, '5': 112, '6': 113, '7': 114, '8': 115, '9': 116, '10': 117, '11': 118, '12': 119, '13': 120, '14': 121, '15': 122, '16': 123, '17': 124, '18': 125, '19': 126, '20': 127, '21': 128, '22': 129, '23': 130, '24': 131}, '11': {'2': 132, '3': 133, '4': 134, '5': 135, '6': 136, '7': 137, '8': 138, '9': 139, '10': 140, '11': 141, '12': 142, '13': 143, '14': 144, '15': 145, '16': 146, '17': 147, '18': 148, '19': 149, '20': 150, '21': 151, '22': 152, '23': 153, '24': 154, '25': 155}, '12': {'1': 156, '2': 157, '3': 158, '4': 159, '5': 160, '6': 161, '7': 162, '8': 163, '9': 164, '10': 165, '11': 166, '12': 167, '13': 168, '14': 169, '15': 170, '16': 171, '17': 172, '18': 173, '19': 174, '20': 175, '21': 176, '22': 177, '23': 178, '24': 179, '25': 180, '26': 181}, '13': {'0': 182, '1': 183, '2': 184, '3': 185, '4': 186, '5': 187, '6': 188, '7': 189, '8': 190, '9': 191, '10': 192, '11': 193, '12': 194, '13': 195, '14': 196, '15': 197, '16': 198, '17': 199, '18': 200, '19': 201, '20': 202, '21': 203, '22': 204, '23': 205, '24': 206, '25': 207, '26': 208, '27': 209}, '14': {'0': 210, '1': 211, '2': 212, '3': 213, '4': 214, '5': 215, '6': 216, '7': 217, '8': 218, '9': 219, '10': 220, '11': 221, '12': 222, '13': 223, '14': 224, '15': 225, '16': 226, '17': 227, '18': 228, '19': 229, '20': 230, '21': 231, '22': 232, '23': 233, '24': 234, '25': 235, '26': 236, '27': 237}, '15': {'1': 238, '2': 239, '3': 240, '4': 241, '5': 242, '6': 243, '7': 244, '8': 245, '9': 246, '10': 247, '11': 248, '12': 249, '13': 250, '14': 251, '15': 252, '16': 253, '17': 254, '18': 255, '19': 256, '20': 257, '21': 258, '22': 259, '23': 260, '24': 261, '25': 262, '26': 263}, '16': {'2': 264, '3': 265, '4': 266, '5': 267, '6': 268, '7': 269, '8': 270, '9': 271, '10': 272, '11': 273, '12': 274, '13': 275, '14': 276, '15': 277, '16': 278, '17': 279, '18': 280, '19': 281, '20': 282, '21': 283, '22': 284, '23': 285, '24': 286, '25': 287}, '17': {'3': 288, '4': 289, '5': 290, '6': 291, '7': 292, '8': 293, '9': 294, '10': 295, '11': 296, '12': 297, '13': 298, '14': 299, '15': 300, '16': 301, '17': 302, '18': 303, '19': 304, '20': 305, '21': 306, '22': 307, '23': 308, '24': 309}, '18': {'4': 310, '5': 311, '6': 312, '7': 313, '8': 314, '9': 315, '10': 316, '11': 317, '12': 318, '13': 319, '14': 320, '15': 321, '16': 322, '17': 323, '18': 324, '19': 325, '20': 326, '21': 327, '22': 328, '23': 329}, '19': {'5': 330, '6': 331, '7': 332, '8': 333, '9': 334, '10': 335, '11': 336, '12': 337, '13': 338, '14': 339, '15': 340, '16': 341, '17': 342, '18': 343, '19': 344, '20': 345, '21': 346, '22': 347}, '20': {'6': 348, '7': 349, '8': 350, '9': 351, '10': 352, '11': 353, '12': 354, '13': 355, '14': 356, '15': 357, '16': 358, '17': 359, '18': 360, '19': 361, '20': 362, '21': 363}, '21': {'7': 364, '8': 365, '9': 366, '10': 367, '11': 368, '12': 369, '13': 370, '14': 371, '15': 372, '16': 373, '17': 374, '18': 375, '19': 376, '20': 377}, '22': {'8': 378, '9': 379, '10': 380, '11': 381, '12': 382, '13': 383, '14': 384, '15': 385, '16': 386, '17': 387, '18': 388, '19': 389}, '23': {'9': 390, '10': 391, '11': 392, '12': 393, '13': 394, '14': 395, '15': 396, '16': 397, '17': 398, '18': 399}, '24': {'10': 400, '11': 401, '12': 402, '13': 403, '14': 404, '15': 405, '16': 406, '17': 407}, '25': {'11': 408, '12': 409, '13': 410, '14': 411, '15': 412, '16': 413}, '26': {'12': 414, '13': 415, '14': 416, '15': 417}, '27': {'13': 418, '14': 419}}
    return locs_map[str(loc[0])][str(loc[1])]


if __name__ == "__main__":
    algo = RLProdBot()
    algo.start()