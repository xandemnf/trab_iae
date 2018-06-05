from Menubox import Menubox

class Startmenu:
    def __init__(self):
        self.__visual = None
        self.__items = []
        self.__shown = []
        self.__current = 0

    def add_visual(self, menubox:Menubox):
        self.__visual = menubox

    def show_menu(self):
        pass

    def hide_menu(self):
        pass

    def move_up(self):
        self.__current -= 1
        self.__current %= len(self.__shown)
        self.__visual.update()

    def move_down(self):
        self.__current += 1
        self.__current %= len(self.__shown)
        self.__visual.update()
