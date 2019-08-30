'''
    Save up until enough Bits are available
    Check for the optimal location to drop a phat stack of %UNIT%
'''
import algolib
import random
import time
from . import path_finding
from abc import ABC
from algolib import initializer, eprint

cost_of_unit = {
        algolib.SCRAMBLER : 3,
        algolib.EMP : 3,
        algolib.PING : 1
        }

'''
Return the value given the projected number of points
and total firewall damage
'''
def objective_function(points, dmg, opponent_health, alpha=100, beta=1):
    if points >= opponent_health:
        return (1000 * (points + 1 - opponent_health), True)
    return (points * alpha + dmg * beta, False)

class CalculatedStack():

    @initializer
    def __init__( self, agent, action_handler, game_state=None, fund_threshold=15, debug=False , timeout=2.5):
        cls = self.__class__
        

    def run(self):
        self.game_state = self.agent.game_state

        spawn_locations = path_finding.get_available_spawn_points(self.game_state)

        best_spawn = spawn_locations[0]
        best_unit = algolib.PING
        best_score = (0,0)
        best_value = 0

        opponent_health = self.game_state.enemy_health

        next_turn_bits = self.game_state.project_future_bits()

        timeout_start = time.time()
        can_win = False
        for unit_type in [algolib.PING, algolib.EMP]:

            unit_count = self.game_state.get_resource(self.game_state.BITS) // cost_of_unit[unit_type]
            for spawn_location in spawn_locations:
                if time.time() > timeout_start + self.timeout:
                    eprint("Ran out of time! Taking what we've got!")
                    break
                    
                path = path_finding.get_path_from_spawn(spawn_location, self.game_state )
                points = path_finding.get_points_scored( path, self.game_state, unit_type, unit_count )
                dmg = path_finding.get_damage_dealt( path, self.game_state, unit_type, unit_count  )
                value, can_win = objective_function(points, dmg, opponent_health)
                if value > best_value:
                    best_value = value
                    best_spawn = spawn_location
                    best_unit = unit_type
                # if points > best_score[0]:
                #     best_score = (points, dmg)
                #     best_spawn = spawn_location
                #     best_unit = unit_type
                # elif points == best_score[0] and dmg > best_score[1]:
                #     best_score = (points, dmg)
                #     best_spawn = spawn_location
                #     best_unit = unit_type

        next_turn_best_spawn = spawn_locations[0]
        next_turn_best_unit = algolib.PING
        next_turn_best_score = (0,0)
        next_turn_best_value = 0

        # Re-run sim but with future bits
        for unit_type in [algolib.PING, algolib.EMP]:
            unit_count = next_turn_bits // cost_of_unit[unit_type]
            for spawn_location in spawn_locations:
                path = path_finding.get_path_from_spawn(spawn_location, self.game_state )
                points = path_finding.get_points_scored( path, self.game_state, unit_type, unit_count )
                dmg = path_finding.get_damage_dealt( path, self.game_state, unit_type, unit_count  )
                value, can_win = objective_function(points, dmg, opponent_health)
                if value > next_turn_best_value:
                    next_turn_best_value = value
                    next_turn_best_spawn = spawn_location
                    next_turn_best_unit = unit_type

                # eprint(path)
                # eprint(points)
                # eprint(dmg)
                # if points > next_turn_best_score[0]:
                #     next_turn_best_score = (points, dmg)
                #     next_turn_best_spawn = spawn_location
                #     next_turn_best_unit = unit_type
                # elif points == next_turn_best_score[0] and dmg > next_turn_best_score[1]:
                #     next_turn_best_score = (points, dmg)
                #     next_turn_best_spawn = spawn_location
                #     next_turn_best_unit = unit_type

        # go_this_turn = self.evaluate_options(best_score, next_turn_best_score)
        go_this_turn = self.evaluate_options(best_value, next_turn_best_value)
        if go_this_turn or can_win:
            deployment_location = best_spawn
            if self.debug:
                eprint("Deploying as many '%s' as possible at (%d, %d). Expected %d hp dmg and bldg damage of %d." % (best_unit, spawn_location[0], spawn_location[1], best_score[0], best_score[1]))
            self.deploy_pings(deployment_location, best_unit)
        else:
            if self.debug:
                eprint("Deciding to delay")

    # Do we go now?
    def evaluate_options(self, best_value, next_turn_best_value):
        if self.game_state.turn_number <= 0:
            if self.debug:
                eprint("Turn number is zero, not taking action")
            return False
        if self.game_state.get_resource(self.game_state.BITS) >= self.fund_threshold:
            if self.debug:
                eprint("Bits exceeded fund threshold; going no matter what")
            return True
        if best_value == 0:
            if self.debug:
                eprint("No damage possible this turn. Doing nothing")
            return False
        if next_turn_best_value > best_value + 200:
            return False
        return True

    def deploy_pings(self, location, unit_type):
        """
        Build as many pings as possible at the given location
        """
        # while self.action_handler.spawn_ping(self.unit, location):
        #     #lol hope this function is well tested or this will be an infinite loop
        #     pass

        # this is safer but less fun
        for i in range(1,100):
            if not self.game_state.attempt_spawn(unit_type, location ):
                if self.debug:
                    eprint( "POW!POW! I just sent {} {}! Take that!!".format(i, unit_type) )
                break
