import gamelib
import random
import math
import warnings
from sys import maxsize
import json
import constants as c


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []


        

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        self.game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(self.game_state.turn_number))
        self.game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.starter_strategy()

        self.game_state.submit_turn()


#checks for all the different scenarios and decides a action/move based on it
    def analysis(self):
        """ Analyze opponent behavior """




        """ If they do change their layout constantly (sell most structures) """




        """ If they do not change their layout constantly (don't sell many structures) """
        
        
        #Check for lots of structures in enemy's first line
        front_enemy_structures = self.check_structures(c.enemy_front_line)
        if len(front_enemy_structures) >= 0.75*len(c.enemy_front_line):
            self.line_demolisher(1)
        
        
        
    def check_structures(self, locations):
        structures = []
        for location in locations:
            if self.game_state.game_map.in_arena_bounds(location) and self.game_state.contains_stationary_unit(location):
                for unit in self.game_state.game_map[location]:
                    if unit.player_index == 1:
                        structures.append([[location],unit.unit_type])
        return structures


    def main_defense(self):
        wall_locations =[[11, 12], [16, 12], [0, 13], [1, 13], [2, 13], [3, 13], [12, 13], [13, 13], [14, 13], [15, 13], [24, 13], [25, 13], [26, 13], [27, 13]]
        self.game_state.attempt_spawn(WALL, wall_locations)

        
        turrent_locations = [[2, 12], [12, 12], [15, 12], [25, 12]]
        self.game_state.attempt_spawn(TURRET, turrent_locations)

        self.game_state.attempt_upgrade([[12,12],[15,12]])



#If enemy has lots of units in the front
    def line_demolisher(self,line):
        wall_locations = []
        demolisher_location = []

















    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def starter_strategy(self):
        """
        For defense we will use a spread out layout and some interceptors early on.
        We will place turrets near locations the opponent managed to score on.
        For offense we will use long range demolishers if they place stationary units near the enemy's front.
        If there are no stationary units to attack in the front, we will send Scouts to try and score quickly.
        """
        # First, place basic defenses
        self.check_structures()
        """self.build_defences()
        # Now build reactive defenses based on where the enemy scored
        self.build_reactive_defense()

        # If the turn is less than 5, stall with interceptors and wait to see enemy's base
        if self.game_state.turn_number < 5:
            self.stall_with_interceptors()
        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our demolishers to attack them at long range.
            if self.detect_enemy_unit( unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.demolisher_line_strategy()
            else:
                # They don't have many units in the front so lets figure out their least defended area and send Scouts there.

                # Only spawn Scouts every other turn
                # Sending more at once is better since attacks can only hit a single scout at a time
                if self.game_state.turn_number % 2 == 1:
                    # To simplify we will just check sending them from back left and right
                    scout_spawn_location_options = [[13, 0], [14, 0]]
                    best_location = self.least_damage_spawn_location( scout_spawn_location_options)
                    self.game_state.attempt_spawn(SCOUT, best_location, 1000)

                # Lastly, if we have spare SP, let's build some supports
                support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
                self.game_state.attempt_spawn(SUPPORT, support_locations)"""


    def build_defences(self):
        """
        Build basic defenses using hardcoded locations.
        Remember to defend corners and avoid placing units in the front where enemy demolishers can attack them.
        """
        # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
        # More community tools available at: https://terminal.c1games.com/rules#Download

        # Place turrets that attack enemy units
        turret_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        self.game_state.attempt_spawn(TURRET, turret_locations)
        
        # Place walls in front of turrets to soak up damage for them
        wall_locations = [[8, 12], [19, 12]]
        self.game_state.attempt_spawn(WALL, wall_locations)
        # upgrade walls so they soak more damage
        self.game_state.attempt_upgrade(wall_locations)

    def build_reactive_defense(self):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build turret one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            self.game_state.attempt_spawn(TURRET, build_location)

    def stall_with_interceptors(self):
        """
        Send out interceptors at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = self.game_state.game_map.get_edge_locations(self.game_state.game_map.BOTTOM_LEFT) + self.game_state.game_map.get_edge_locations(self.game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own structures 
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, self.game_state)
        
        # While we have remaining MP to spend lets send out interceptors randomly.
        while self.game_state.get_resource(MP) >= self.game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            self.game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            """
            We don't have to remove the location since multiple mobile 
            units can occupy the same space.
            """

    def demolisher_line_strategy(self):
        """
        Build a line of the cheapest stationary unit so our demolisher can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [WALL, TURRET, SUPPORT]
        cheapest_unit = WALL
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, self.game_state.config)
            if unit_class.cost[self.game_state.MP] < gamelib.GameUnit(cheapest_unit, self.game_state.config).cost[self.game_state.MP]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            self.game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn demolishers next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        self.game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def least_damage_spawn_location(self, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = self.game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy turrets that can attack each location and multiply by turret damage
                damage += len(self.game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, self.game_state.config).damage_i
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in self.game_state.game_map:
            if self.game_state.contains_stationary_unit(location):
                for unit in self.game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations):
        filtered = []
        for location in locations:
            if not self.game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
