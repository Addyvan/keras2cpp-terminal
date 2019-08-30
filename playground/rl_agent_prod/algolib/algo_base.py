from .util import eprint
import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"./gamelib")))
import random
import math
import warnings
from sys import maxsize
import json
from .gamelib.util import get_command, debug_write, BANNER_TEXT, send_command
from .gamelib.algocore import AlgoCore
from .gamelib.game_state import GameState

from .state_manager import StateManager
from .action_handler import ActionHandler

'''
AlgoBase - The class which our algos will inherit
'''

class AlgoBase(AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

        self.player_string = "" # either p1 or p2

        self.state_manager = StateManager()
        self.action_handler = ActionHandler()
        self.game_state = None
        self.current_state = None
        self.state_history = None
        self.has_on_spawn_run = False

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        debug_write('Configuring your custom algo strategy...')
        self.config = config

    def start(self):
        debug_write(BANNER_TEXT)

        while True:
            game_state_string = get_command()
            
            if "replaySave" in game_state_string:
                """
                This means this must be the config file. So, load in the config file as a json and add it to your AlgoStrategy class.
                """
                parsed_config = json.loads(game_state_string)
                self.on_game_start(parsed_config)
            elif "turnInfo" in game_state_string:
                state = json.loads(game_state_string)
                phase, currentTurnIndex, currentFrameIndex = self.state_manager.get_frame_info(state.get("turnInfo"))
                #eprint(phase, currentTurnIndex, currentFrameIndex)

                # While phase is 0, we send the game state string to on_turn in order to make decisions
                if phase == 0:
                    self.has_on_spawn_run = False
                    if currentTurnIndex > 0:
                        self.on_turn_end()
                    self.game_state = GameState(self.config, game_state_string)
                    #eprint('Turn: {} '.format(self.game_state.turn_number))
                    self.action_handler.set_game_state(self.game_state)
                    self.state_history = self.state_manager.states
                    self.current_state = self.state_manager.parse_deployment_phase_state(state)
                    

                    # temp for AI testing
                    self.p1Units = state["p1Units"]
                    self.p2Units = state["p2Units"]


                    self.on_turn(state)
                    self.game_state.submit_turn()

                # While phase is 1, we parse the action phase to see what the results of the turn are
                elif phase == 1:
                    """
                    If stateType == 1, this game_state_string string represents the results of an action phase
                    """
                    self.state_manager.parse_action_phase_state(state, currentTurnIndex)

                    if not self.has_on_spawn_run:
                        self.on_spawn_frame(state["events"]["spawn"])
                        self.has_on_spawn_run = True
                
                # If phase is 2 then the game is over
                elif phase == 2:
                    self.on_game_end()
                    debug_write("Got end state quitting bot.")
                    break # If this isn't there, program never leaves loop and thus never quits
                
                else:
                    debug_write("Got unexpected string with turnInfo: {}".format(game_state_string))
            else:
                debug_write("Got unexpected string : {}".format(game_state_string))

    def on_turn(self):
        
        eprint("Looks like you forgot to implement on_turn or you are running AlgoBase directly...")

    def on_spawn_frame(self, spawn_events):
        pass
        #eprint("Looks like you forgot to implement on_spawn_frame or you are running AlgoBase directly...")

    def on_turn_end(self):
        pass
        #eprint("Looks like you forgot to implement on_turn_end or you are running AlgoBase directly")

    def on_game_end(self):
        pass
        #eprint("Looks like you forgot to implement on_game_end !")

if __name__ == "__main__":
    test = AlgoBase()
    
