from tkinter import *
from Box import Box

# Enumeration for items
POKEDEX = 0
POKEMON = 1
ITEM = 2
PLAYER = 3
SAVE = 4
OPTION = 5
EXIT = 6

class Menubox(Box):
    def __init__(self, canvas:Canvas, zoom:int=1, border:int=0):
        Box.__init__(self, canvas, (5, 0), (9, 8), zoom, border)
        Box.__init__(self, canvas, (0, 1), (3, 3), zoom, border)
        self.__items = [POKEDEX, POKEMON, ITEM, PLAYER, SAVE, OPTION, EXIT]
        self.__shown_items = [False, False, True, True, True, True, True]
        self.__current = 0

    def show_item(self, index: int):
        self.__shown_items[index] = True

    def update(self):
        # TODO: Move cursor to correct position
        pass

    def move_down(self):
        self.__current += 1
        self.__current %= len(self.__items)
        self.update()

    def move_up(self):
        self.__current -= 1
        self.__current %= len(self.__items)
        self.update()
