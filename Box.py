from tkinter import *
from typing import Tuple

class Box:
    def __init__(self, canvas: Canvas, ul_corner: Tuple[int, int], lr_corner: Tuple[int, int], zoom: int=1, border:int=0):

        self.__canvas = canvas
        self.__zoom = zoom
        self.__border = border
        self.__ul_corner = ul_corner
        self.__lr_corner = lr_corner
        self.__contents = []
        self.__images = {"l_l_c": PhotoImage(file="./data/text/l_l_corner.png").zoom(zoom, zoom),
                     "u_l_c": PhotoImage(file="./data/text/u_l_corner.png").zoom(zoom, zoom),
                     "l_r_c": PhotoImage(file="./data/text/l_r_corner.png").zoom(zoom, zoom),
                     "u_r_c": PhotoImage(file="./data/text/u_r_corner.png").zoom(zoom, zoom),
                     "u_b": PhotoImage(file="./data/text/up_border.png").zoom(zoom, zoom),
                     "d_b": PhotoImage(file="./data/text/down_border.png").zoom(zoom, zoom),
                     "l_b": PhotoImage(file="./data/text/left_border.png").zoom(zoom, zoom),
                     "r_b": PhotoImage(file="./data/text/right_border.png").zoom(zoom, zoom),
                     "white": PhotoImage(file="./data/images/white.png").zoom(zoom, zoom)
                     }
        self.create_box()

    def create_box(self):
        """
        Function draws a box onto the canvas
        :return: None
        """
        # Shorten the names of corners
        lr = self.__lr_corner
        ul = self.__ul_corner
        # Calculate the remaining corners
        ur = (lr[0], ul[1])
        ll = (ul[0], lr[1])
        # Calculate the difference of the corner coordinates to get loop variables
        y = lr[1] - ul[1] + 1
        x = lr[0] - ul[0] + 1
        # Paint the are white
        for i in range(y):
            for j in range(x):
                self.__contents.append(self.__canvas.create_image((16 * (j + ul[0]) + 8 ) * self.__zoom, (16 * (i + ul[1]) + 8 ) * self.__zoom, image=self.__images["white"]))
        # Add corners
        self.__contents.append(self.__canvas.create_image((16 * ul[0] + 8) * self.__zoom, (16 * ul[1] + 9) * self.__zoom, image=self.__images["u_l_c"]))
        self.__contents.append(self.__canvas.create_image((16 * ll[0] + 8) * self.__zoom, (16 * ll[1] + 8) * self.__zoom, image=self.__images["l_l_c"]))
        self.__contents.append(self.__canvas.create_image((16 * ur[0] + 8) * self.__zoom, (16 * ur[1] + 9) * self.__zoom, image=self.__images["u_r_c"]))
        self.__contents.append(self.__canvas.create_image((16 * lr[0] + 8) * self.__zoom, (16 * lr[1] + 8) * self.__zoom, image=self.__images["l_r_c"]))
        # Add sides for the box
        for i in range(1, x - 1):
            self.__contents.append(self.__canvas.create_image((16 * (i + ul[0]) + 8) * self.__zoom, (16 * ul[1] + 9) * self.__zoom, image=self.__images["u_b"]))
            self.__contents.append(self.__canvas.create_image((16 * (i + ul[0]) + 8) * self.__zoom, (16 * ll[1] + 8) * self.__zoom, image=self.__images["d_b"]))
        for i in range(1, y):
            self.__contents.append(self.__canvas.create_image((16 * ul[0] + 8) * self.__zoom, (16 * (i + ul[1])) * self.__zoom, image=self.__images["l_b"]))
            self.__contents.append(self.__canvas.create_image((16 * ur[0] + 8) * self.__zoom, (16 * (i + ul[1])) * self.__zoom, image=self.__images["r_b"]))

    def delete_box(self):
        for image in self.__contents:
            self.__canvas.delete(image)
