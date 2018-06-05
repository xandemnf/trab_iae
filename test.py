from tkinter import *
from time import time, sleep
from random import randint

WIDTH = 400
HEIGHT = 400

class GUI:
    def __init__(self):
        self.__mw = Tk()
        self.__mw.title("Pokemon")

        self.__red_image = PhotoImage(file="Red.png")
        self.__block_image = PhotoImage(file="block.png")

        self.__canvas = Canvas(self.__mw, width=WIDTH, height=HEIGHT)
        self.__canvas.pack(expand=1, fill=BOTH)

        self.__x = WIDTH / 2
        self.__y = HEIGHT / 2

        self.__red = self.__canvas.create_image(self.__x, self.__y, image=self.__red_image)
        self.__blocks = []
        for i in range(50):
            self.__blocks.append(self.__canvas.create_image(randint(2, 38) * 10, randint(2, 38) * 10, image=self.__block_image))

        self.__num = 0
        self.__numlbl = Label(self.__mw, text="0")
        self.__numlbl.pack()

        self.__mw.bind("<KeyPress>", self.key_event)

        self.__mw.after(10, self.ticker)
        self.__mw.mainloop()


    def key_event(self, event):
        if event.keysym == "Escape":
            self.__mw.destroy()

        elif event.keysym == "Up":
            self.__y -= 10
            for block in self.__blocks:
                self.__canvas.move(block, 0, 10)

        elif event.keysym == "Down":
            self.__y += 10
            for block in self.__blocks:
                self.__canvas.move(block, 0, -10)

        elif event.keysym == "Right":
            self.__x += 10
            for block in self.__blocks:
                self.__canvas.move(block, -10, 0)

        elif event.keysym == "Left":
            self.__x -= 10
            for block in self.__blocks:
                self.__canvas.move(block, 10, 0)


    def ticker(self):
        self.up()
        self.__mw.after(10, self.ticker)

    def up(self):
        self.__num += 0.01
        self.__numlbl["text"] = "{:.2f}".format(self.__num)

    def down(self):
        self.__num -= 1
        self.__numlbl["text"] = str(self.__num)




def main():
    GUI()


main()