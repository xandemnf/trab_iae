# This module is responsible for the whole game. It owns the user interface
# and other objects related to the overworld, and
# TODO: communicates with the combat module.

from GUI import GUI
from Area import Area
# TODO: Import everything

# Singleton
class Game:
    def __init__(self):
        self.__state = None # Cutscene, overworld, combat
        self.__area = 0 # Area of the map currently displayed
        self.__map = Area(0)
        self.__UI = GUI(self)
        self.__UI.start()


    def is_passable(self, x, y):
        return self.__map.is_passable(x, y)

    def get_map(self):
        return self.__map

    def on_step_action(self, x, y):
        self.__map.on_step_action(self, x, y)

    def warp(self, coordinates):
        # Don't recreate if warped to the same map
        new_area = coordinates[0]
        x = coordinates[1]
        y = coordinates[2]
        if self.__area != new_area:
            self.__area = new_area
            self.__map = Area(new_area)
        self.__UI.warp(x, y)

    def encounter(self):
        # This doesn't really do anything yet
        self.__state = "combat"
        # TODO: Create combat here, ask map for encounterables
        new_combat = None
        self.__UI.battle_start(new_combat)
