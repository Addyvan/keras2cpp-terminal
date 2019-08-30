'''
Path finding Functions

'''

import algolib
from typing import Dict, Tuple, Sequence
from algolib import eprint
from collections import defaultdict
from algolib.gamelib.advanced_game_state import AdvancedGameState
from algolib.gamelib.unit import GameUnit
from functools import lru_cache

health_of_unit = {
        algolib.SCRAMBLER : 1,
        algolib.EMP : 1,
        algolib.PING : 15
        }

inverse_speed_of_unit = {
        algolib.SCRAMBLER : 1,
        algolib.EMP : 1,
        algolib.PING : 1
        }


range_of_unit = {
        algolib.SCRAMBLER : 4.5,
        algolib.EMP : 4.5,
        algolib.PING : 3.5
        }

building_damage_of_unit = {
        algolib.SCRAMBLER : 0.2,
        algolib.EMP : 12,
        algolib.PING : 2
}

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def get_available_spawn_points( game_state ) -> Sequence[Tuple[int, int]]:
    """
    
    """
    game_map = game_state.game_map
    edges = game_map.get_edge_locations(game_map.BOTTOM_LEFT) + game_map.get_edge_locations(game_map.BOTTOM_RIGHT)
    
    valid_spawns = [e for e in edges if not game_state.contains_stationary_unit(e) ]

    if not len(valid_spawns):
        eprint("No Places to spawn units >:(")

    return valid_spawns

def get_path_from_spawn( location, game_state ) -> Sequence[Tuple[int,int]]:
    """
    Compute path for an invincible unit
    """
    is_left_spawn = location[0] < game_state.game_map.HALF_ARENA
    target_edge = game_state.game_map.TOP_RIGHT if is_left_spawn else game_state.game_map.TOP_LEFT
    return [tuple(loc) for loc in game_state.find_path_to_edge(location, target_edge)]

def get_shielding_for_path( path, game_state ) -> float:
    """
    Compute the total amount of incremental shielding accrued for an individual unit
    """
    shield_map = get_shielding_coverage(game_state)
    shield_total = 0
    for p in path:
        shield_total += shield_map[p[0]][p[1]]
    return shield_total

def get_shielding_coverage(game_state):
    """
    Return the map where each node is annotated with the amount of shield that a unit would receive if
    it reaches the node
    """
    our_half = game_state.game_map.get_bottom_half()
    shield_map = defaultdict(int)
    for x, y in our_half:
        maybe_unit = game_state.contains_stationary_unit((x, y))
        if maybe_unit == algolib.ENCRYPTOR:
            # Assume encryptor range is 3
            locations_in_shield_range = game_state.game_map.get_locations_in_range((x, y), 3)
            for shield_loc in locations_in_shield_range:
                shield_x, shield_y = shield_loc
                shield_map[(shield_x, shield_y)] += 0
    return shield_map


def get_survival_record(path, game_state, unit_type:str, unit_count:int) -> Sequence[int]:
    """
    use get_defensive_cover

    test: path = length output
    """
    total_health = health_of_unit[unit_type] * unit_count
    
    survival_record = []
    total_dmg = 0

    defensive_coverage = get_defensive_coverage(game_state)
    # shielding_record = get_shielding_coverage(game_state)
    for loc in path:
        total_dmg += defensive_coverage[loc] * inverse_speed_of_unit[unit_type]
        remaining_health = max(0, total_health - total_dmg)
        remaining_units = remaining_health // health_of_unit[unit_type]
        survival_record.append(remaining_units)

    return survival_record

# @lru_cache()
def get_defensive_coverage(game_state):
    """
    Return a game_map of dmg output per tick for all open spaces from defensive structures
    """
    top_half = game_state.game_map.get_bottom_half()
    damage_map = defaultdict(int)
    for x, y in top_half:
        maybe_unit = game_state.contains_stationary_unit([x, y])
        if maybe_unit == False:
            continue

        if maybe_unit.unit_type == "DF" and maybe_unit.player_index != 0:
            # Assume destructor range is 3
            locations_in_dmg_range = game_state.game_map.get_locations_in_range((x, y), 3)
            for dmg_loc in locations_in_dmg_range:
                dmg_x, dmg_y = dmg_loc
                damage_map[(dmg_x, dmg_y)] += 5
    return damage_map

def get_damage_dealt(path, game_state, unit_type, unit_count):
    """
    Get damage dealt to enemy structures
    """

    cum_dmg = 0
    survival_record = get_survival_record(path, game_state, unit_type, unit_count)
    assert(len(path) == len(survival_record))
    for loc, surviving in zip(path, survival_record):

        unit = objectview({
            "x" : loc[0],
            "y" : loc[1],
            "unit_type" : unit_type,
            "range" : range_of_unit[unit_type],
            "player_index" : 0,
        })
        if AdvancedGameState.get_target(game_state, unit ):
            cum_dmg += inverse_speed_of_unit[unit_type] * building_damage_of_unit[unit_type]
    
    return cum_dmg

def get_points_scored( path, game_state,unit_type,unit_count  ):
    """
    Get number of points scored
    """
    survival_record = get_survival_record(path,game_state,unit_type,unit_count)
    eprint(survival_record)
    return survival_record[-1]




