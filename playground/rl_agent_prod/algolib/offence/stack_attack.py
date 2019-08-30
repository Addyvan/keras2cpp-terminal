'''
    Save up until enough Bits are available
    Check for the optimal location to drop a phat stack of %UNIT%
'''
import algolib
import random
from abc import ABC
from algolib import initializer, eprint

class StackAttack(ABC):
    unit = None

    @initializer
    def __init__( self, agent, action_handler, game_state, fund_threshold = 10, debug=False ):
        cls = self.__class__
        self.unit = cls.unit
        pass

    def run(self):
        self.game_state = self.agent.game_state

        if not self.have_enough_funds():
            if self.debug:
                eprint( "Don't have enough money!" )
            return

        deployment_location = self.find_optimal_deployment_location()

        self.deploy_pings(deployment_location)

    def have_enough_funds(self):
        """ 
        Return a Bool whether or not we have enough dough or should save up
        """
        return self.game_state.get_resource(self.game_state.BITS) >= self.fund_threshold

    def deploy_pings(self, location):
        """
        Build as many pings as possible at the given location
        """
        # while self.action_handler.spawn_ping(self.unit, location):
        #     #lol hope this function is well tested or this will be an infinite loop
        #     pass

        # this is safer but less fun
        for i in range(1,100):
            if not self.game_state.attempt_spawn(self.unit, location ):
                if self.debug:
                    eprint( "POW!POW! I just sent {} {}! Take that!!".format(i, self.unit) )
                break


    def find_optimal_deployment_location(self):   
        """ TODO this may not be optimal...
        """
        friendly_edges = self.game_state.game_map.get_edge_locations(self.game_state.game_map.BOTTOM_LEFT) + self.game_state.game_map.get_edge_locations(self.game_state.game_map.BOTTOM_RIGHT)
        deploy_locations = self.filter_blocked_locations(friendly_edges)
        
        # They'll never see it coming!
        return random.choice( deploy_locations )

    def filter_blocked_locations(self, locations):
        filtered = []
        for location in locations:
            if not self.game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered
