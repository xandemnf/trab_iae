# This module contains a single overworld area, consisting of several Tiles.
# It manages the tiles, communicates with them and holds several booleans
# determining whether the user can use certain overworld actions.

from readdata import AREADATA
from typing import List
from Tile import Tile

class Area:
    def __init__(self, id_num: int, flyable: bool = True, cycleable: bool = True):
        self.__id = id_num
        self.__map = []
        self.__encounterable = []
        self.__flyable = flyable
        self.__cycleable = cycleable

        self.create_area()


    def create_area(self):
        """
        The function creates the area from the data previously read from
        input files.
        :return: None
        """
        # Fetch the read data
        data = AREADATA[self.__id]
        i = 0
        tileinfo = {}
        # Read specific tile data until the actual map is found
        while data[i] != "MAP" and i <= len(data):
            row = data[i].split("=")
            tileinfo[row[0]] = row[1].split(",")
            i += 1
        i += 1
        # Continue reading the map data, creating tiles for each row
        while i < len(data):
            row = []
            for char in data[i]:
                # Check if tile data has been provided
                if char in tileinfo:
                    tile = Tile(*tileinfo[char])
                # else set tile as the base tile of the area
                else:
                    tile = Tile(*tileinfo["neutral"])
                row.append(tile)
            self.__map.append(row)
            i += 1

    def is_passable(self, x: int, y: int) -> bool:
        """
        :param x: x coordinate
        :param y: y coordinate
        :return: Returns a bool on whether a character can walk on the tile
        """
        return self.__map[y][x].is_walkable()

    def is_warp(self, x: int, y: int) -> bool:
        """
        :param x: x coordinate
        :param y: y coordinate
        :return: Returns a bool on whether a the tile is a warp
        """
        return self.__map[y][x].is_warp()

    def get_tile(self, x: int, y: int) -> Tile:
        """
        :param x: x coordinate
        :param y: y coordinate
        :return: Returns the tile at the given coordinates
        """
        return self.__map[y][x]

    def get_map(self) -> List[List[Tile]]:
        """
        :return: The matrix of tiles
        """
        return self.__map

    def get_encounterable(self) -> List[int]:
        return self.__encounterable

    def on_step_action(self, world, x: int, y: int):
        """
        Function calls the on step action of the tile
        :param world: Game object, so that the tile can call its functions
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """
        self.__map[y][x].on_stepped_action(world)

