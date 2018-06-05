from tkinter import *
from Box import Box
from Text import Text

class Textbox(Box):
    def __init__(self, canvas:Canvas, text:str="", zoom:int=1, border:int=0, speed:int=0):
        Box.__init__(self, canvas, (0, 6), (9, 8), zoom, border)
        self.__text = text
        self.__current_line = []
        self.__speed = speed
        self.__line_finished = True


    @property
    def line_finished(self) -> bool:
        return self.__line_finished

    def show_line(self):
        pass

    def empty_box(self):
        for image in self.__current_line:
            self.__canvas.delete(image)
