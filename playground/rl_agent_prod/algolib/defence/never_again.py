from algolib.util import eprint
from algolib.units import *
import math
from .pillbox import PillboxDefence
from .hallway_of_encouragement import HallwayOfEncouragement
def required_defense(x):
    # return min(max(int(math.sqrt(x)), 5), 1)
    return 2

'''
Class containing the implementation of the Never-Again defense strategy.
'''
class NeverAgain:
    def __init__(self, action_handler, game_state, no_go_coords=[]):
        self.action_handler = action_handler
        self.breach_points = {}
        self.no_go_coords = no_go_coords
        self.pillbox = PillboxDefence(action_handler, game_state)
        self.hall = HallwayOfEncouragement(action_handler=action_handler, debug=False)

    def run(self, game_state, state_history):
        game_state.suppress_warnings(True)
        # Cool down
        # for k, v in self.breach_points.items():
        #     self.breach_points[k] = max(self.breach_points[k]-1, 0)
        if game_state.turn_number == 0:
            self.first_turn(game_state)
        try:
            breaches = state_history[-2]["actionPhase"]["breaches"]
            for breach in breaches:
                try:
                    self.breach_points[(breach["position"]["x"], breach["position"]["y"])] += 1
                except:
                    self.breach_points[(breach["position"]["x"], breach["position"]["y"])] = 1
            # We also want to immediately address new breaches

            copy_dict = dict(self.breach_points)
            for k, v in copy_dict.items():
                copy_dict[k] = min(3, v)
            sorted_points = list(sorted(self.breach_points.items(), key=lambda x: x[1], reverse=True))
            sorted_points = list(map(lambda x: ((x["position"]["x"], x["position"]["y"]), 2), breaches)) + sorted_points
            first_point = sorted_points[0][0]
            eprint(first_point)
            while copy_dict[first_point] > 0:
                for k, v in sorted_points:
                    if copy_dict[k] < 1:
                        continue
                    around_points = self.around(k, required_defense(self.breach_points[k]))
                    for p in around_points:
                        if game_state.can_spawn(DESTRUCTOR, [p[0], p[1]]):
                            if p in self.no_go_coords:
                                continue
                            self.action_handler.spawn_destructor(p[0], p[1])
                            break
                    copy_dict[k] -= 1

            for i in range(10):
                self.hall.run()

            self.spend_extra_money(game_state)
        except Exception as e:
            eprint(str(e))
            eprint("ah shit")
            pass

    def first_turn(self, game_state):
        ''' build some dope def on turn 1
        '''
        self.pillbox.set_game_state(game_state)
        self.pillbox.run()

    def spend_extra_money(self,game_state):
        '''
        '''
        if game_state.get_resource(game_state.CORES) >15:
            self.pillbox.set_game_state(game_state)
            self.pillbox.run_superpillbox()

    '''
        point : tuple (coordinate)
        distance : int
    '''
    def around(self, point, distance):
        points = [point]
        vert_last = []
        hori_last = []
        for i in range(-distance, distance+1):
            for j in range(-distance, distance+1):
                if i == 0:
                    hori_last.append((point[0]+i, point[1]+j))
                elif j == 0:
                    vert_last.append((point[0]+i, point[1]+j))
                else:
                    points.append((point[0]+i, point[1]+j))
        return points + hori_last + vert_last
