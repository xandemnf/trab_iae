from tkinter import *
from time import time, sleep
from random import randint
from Textbox import Textbox
from Menubox import Menubox
from Walk_animation import Walk_animation

ZOOM = 5
# Gameboy Screen is 10x9 tiles, and the player recides at 4, 4 while the world moves
# The overworld sprites are 16x16 pixels, so width and height are hardcoded, then
# adjusted with the ZOOM-factor
WIDTH = 160 * ZOOM
HEIGHT = 144 * ZOOM

ANIMATION_DELAY = 50

# Command keys for GameBoy-buttons
A = "x"
B = "c"
START = "Return"

class GUI:
    def __init__(self, world):
        self.__mw = Tk()
        self.__mw.title("Pokemon")

        self.__parent = world

        self.__ow_sprites = {"red": PhotoImage(file="./data/images/red.png").zoom(ZOOM, ZOOM),
                             "up": PhotoImage(file="./data/images/trainer/up.png").zoom(ZOOM, ZOOM),
                             "down": PhotoImage(file="./data/images/trainer/down.png").zoom(ZOOM, ZOOM),
                             "right": PhotoImage(file="./data/images/trainer/right.png").zoom(ZOOM, ZOOM),
                             "left": PhotoImage(file="./data/images/trainer/left.png").zoom(ZOOM, ZOOM),
                             "walk_up": PhotoImage(file="./data/images/trainer/up_w_r.png").zoom(ZOOM, ZOOM),
                             "walk_down": PhotoImage(file="./data/images/trainer/down_w_r.png").zoom(ZOOM, ZOOM),
                             "walk_up_l": PhotoImage(file="./data/images/trainer/up_w_l.png").zoom(ZOOM, ZOOM),
                             "walk_down_l": PhotoImage(file="./data/images/trainer/down_w_l.png").zoom(ZOOM, ZOOM),
                             "walk_right": PhotoImage(file="./data/images/trainer/right_w.png").zoom(ZOOM, ZOOM),
                             "walk_left": PhotoImage(file="./data/images/trainer/left_w.png").zoom(ZOOM, ZOOM),
                             "block": PhotoImage(file="./data/images/block.png").zoom(ZOOM, ZOOM),
                             "tree": PhotoImage(file="./data/images/tree.png").zoom(ZOOM, ZOOM),
                             "grass": PhotoImage(file="./data/images/grass.png").zoom(ZOOM, ZOOM),
                             "white": PhotoImage(file="./data/images/white.png").zoom(ZOOM, ZOOM),
                             "warp": PhotoImage(file="./data/images/warp.png").zoom(ZOOM, ZOOM),
                             "bg_grass": PhotoImage(file="./data/images/bg_grass.png").zoom(ZOOM, ZOOM),
                             "t_black": PhotoImage(file="./data/images/transition_black.png").zoom(ZOOM, ZOOM)
                            }

        self.__canvas = Canvas(self.__mw, width=WIDTH, height=HEIGHT)
        self.__canvas.config(background="white")
        self.__canvas.pack(expand=1, fill=BOTH)

        self.__walk_animation = Walk_animation()
        self.__ongoing_animation = False

        self.__x = 4
        self.__y = 4

        self.__blocks = []
        self.refocus()

        self.__num = 0
        self.__numlbl = Label(self.__mw, text="0")
        self.__numlbl.pack()

        self.__movement_enabled = True
        self.__state = "overworld"
        self.__held_keys = {}
        self.__textbox = None
        self.__mw.bind("<KeyPress>", self.key_press)
        self.__mw.bind("<KeyRelease>", self.key_release)


        self.__mw.after(10, self.ticker)
        self.__mw.after(ANIMATION_DELAY, self.advance)

    def advance(self):
        """
        Function that actually keeps the game going. When it finishes, it
        calls the mainwindow to call the function again after a delay.
        The function checks what state the game is in and performs
        actions depending on the pressed keys and the state.
        :return: None
        """
        # For debugging, quits the program
        if "Escape" in self.__held_keys:
            self.quit()
            return

        # If an animation is ongoing, wait a while and try again
        if self.__ongoing_animation:
            self.__mw.after(2 * ANIMATION_DELAY, self.advance)
            return

        # For debugging
        if "space" in self.__held_keys and self.key_check("space"):
            self.key_disable("space")
            self.__state = "overworld"
            self.__textbox.delete_box()
            self.refocus()

        # Toggle between start menu and overworld
        if START in self.__held_keys and self.key_check(START):
            self.key_disable(START)
            self.__textbox = Textbox(self.__canvas, text="moi", zoom=ZOOM)

            """
            if self.__state == "overworld":
                self.__state = "menu"
            else:
                self.__state = "overworld"
            #TODO: Open / close start menu
            """

        if self.__state == "overworld":
            self.movement_action()

        elif self.__state == "menu":
            self.menu_action()

        elif self.__state == "combat":
            pass

        elif self.__state == "text":
            pass

        elif self.__state == "dialogue":
            pass

        self.__mw.after(2 * ANIMATION_DELAY, self.advance)

    def key_press(self, event):
        """
        Function puts the given key event into held_keys if not already there.
        :param event: Tkinter keypress object
        :return: None
        """
        if event.keysym not in self.__held_keys:
            self.__held_keys[event.keysym] = True

    def key_check(self, event: str) -> bool:
        """
        Function checks whether a key has been "spent". This is used
        when holding a key should not do repeated actions.
        :param event: Name of the key
        :return: Boolean on whether key is spent
        """
        return self.__held_keys[event]

    def key_disable(self, event: str):
        """
        Marks a key spent, so it doesn't do repeated actions while held.
        :param event: Name of the key
        :return: None
        """
        self.__held_keys[event] = False

    def key_release(self, event):
        """
        Removes a held key from the datastructure
        :param event: Tkinter keypress object
        :return: None
        """
        if event.keysym in self.__held_keys:
            del self.__held_keys[event.keysym]

    def movement_action(self):
        moved = False

        if self.__movement_enabled:
            if "Up" in self.__held_keys:
                self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["up"])
                self.__walk_animation.set_direction("up")
                if self.__parent.is_passable(self.__x, self.__y - 1):
                    self.__y -= 1
                    self.movement_animation(0, 1)
                    moved = True
                else:
                    print("Bump")
                    #TODO: bump-sound

            elif "Down" in self.__held_keys:
                self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["down"])
                self.__walk_animation.set_direction("down")
                if self.__parent.is_passable(self.__x, self.__y + 1):
                    self.__y += 1
                    self.movement_animation(0, -1)
                    moved = True
                else:
                    print("Bump")
                    #TODO: bump-sound


            elif "Right" in self.__held_keys:
                self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["right"])
                self.__walk_animation.set_direction("right")
                if self.__parent.is_passable(self.__x + 1, self.__y):
                    self.__x += 1
                    self.movement_animation(-1, 0)
                    moved = True
                else:
                    print("Bump")
                    #TODO: bump-sound

            elif "Left" in self.__held_keys:
                self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["left"])
                self.__walk_animation.set_direction("left")
                if self.__parent.is_passable(self.__x - 1, self.__y):
                    self.__x -= 1
                    self.movement_animation(1, 0)
                    moved = True
                else:
                    print("Bump")
                    #TODO: bump-sound

            if moved:
                self.__parent.on_step_action(self.__x, self.__y)

    def menu_action(self):
        pass

    def combat_action(self):
        pass

    def text_action(self):
        if self.__textbox.line_finished and (
                             A in self.__held_keys and self.key_check(A)
                             or B in self.__held_keys and self.key_check(B)
                            ):
            self.key_disable(A)
            self.key_disable(B)
            self.__textbox.next_line()


    def dialogue_action(self):
        pass


    def refocus(self, draw_trainer=True):
        delta_x = self.__x - 4
        delta_y = self.__y - 4
        print(self.__x, self.__y, delta_x, delta_y)
        self.__canvas.delete(ALL)
        self.__blocks = []
        map = self.__parent.get_map().get_map()
        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                self.__blocks.append(self.__canvas.create_image(
                    (16 * (j - delta_x) + 8) * ZOOM,
                    (16 * (i - delta_y) + 8) * ZOOM,
                    image=self.__ow_sprites[tile.get_type()])
                )
        self.fade_in_animation()
        self.__trainer = self.__canvas.create_image(
            (16 * (self.__x - delta_x ) + 8) * ZOOM,
            (16 * (self.__y - delta_y - (0 if draw_trainer else 5)) + 8) * ZOOM,
            image=self.__ow_sprites["down"])
        print(len(self.__blocks))

    def ticker(self):
        self.up()
        self.__mw.after(10, self.ticker)

    # For debugging
    def up(self):
        self.__num += 0.01
        self.__numlbl["text"] = "{:.2f}".format(self.__num)

    def down(self):
        self.__num -= 0.01
        self.__numlbl["text"] = str(self.__num)

    def movement_animation(self, x, y):
        self.__ongoing_animation = True
        for block in self.__blocks:
            self.__mw.after(ANIMATION_DELAY, self.__canvas.move, block, 4 * x * ZOOM, 4 * y * ZOOM)
            self.__mw.after(ANIMATION_DELAY * 2, self.__canvas.move, block, 4 * x * ZOOM, 4 * y * ZOOM)
            self.__mw.after(ANIMATION_DELAY * 3, self.__canvas.move, block, 4 * x * ZOOM, 4 * y * ZOOM)
            self.__mw.after(ANIMATION_DELAY * 4, self.__canvas.move, block, 4 * x * ZOOM, 4 * y * ZOOM)
        self.__mw.after(ANIMATION_DELAY, self.update_trainer_sprite, self.__walk_animation.next_frame())
        self.__mw.after(ANIMATION_DELAY * 4, self.update_trainer_sprite, self.__walk_animation.next_frame())
        self.__mw.after(ANIMATION_DELAY * 4, self.animation_over)

    def warp(self, x, y):
        self.__x = x
        self.__y = y
        self.warp_out_animation()

    def warp_out_animation(self):
        self.disable_movement()
        while self.__ongoing_animation:
            return self.__mw.after(10, self.warp_out_animation)
        self.__ongoing_animation = True
        self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["down"])
        self.__mw.update()
        for i in range(1, 11):
            self.__mw.after(ANIMATION_DELAY * i, self.__canvas.move, self.__trainer, 0, -8 * ZOOM)
        self.__mw.after(ANIMATION_DELAY * 11, self.refocus, False)
        self.__mw.after(ANIMATION_DELAY * 12, self.warp_in_animation)

    def warp_in_animation(self):
        for i in range(1, 11):
            self.__mw.after(ANIMATION_DELAY * i, self.__canvas.move, self.__trainer, 0, 8 * ZOOM)
        self.__mw.after(ANIMATION_DELAY * 12, self.animation_over)
        self.__mw.after(ANIMATION_DELAY * 13, self.enable_movement)

    def fade_in_animation(self):
        pass

    def fade_out_animation(self):
        pass

    def battle_start(self, combat):
        # TODO: Change to combat music
        self.battle_start_animation()
        # TODO: Change to combat

    def battle_start_animation(self):
        while self.__ongoing_animation:
            return self.__mw.after(10, self.battle_start_animation)
        self.__ongoing_animation = True
        # TODO: A few screen flashes here
        for i in range(20):
            for j in range(9):
                self.__mw.after(ANIMATION_DELAY * i, self.battle_start_animation_draw, (4 + i * 8) * ZOOM,
                                (4 + 16 * j) * ZOOM, "t_black")
                self.__mw.after(ANIMATION_DELAY * i, self.battle_start_animation_draw, (156 - i * 8) * ZOOM,
                                (4 + 16 * j + 8) * ZOOM, "t_black")
        i = 20
        self.__mw.after(ANIMATION_DELAY * i, self.animation_over)

    def battle_start_animation_draw(self, x, y, image):
        if not self.__ongoing_animation:
            return
        self.__canvas.create_image(x, y, image=self.__ow_sprites[image])
        self.__mw.update()

    def update_trainer_sprite(self, sprite):
        self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites[sprite])

    def animation_over(self):
        self.__ongoing_animation = False

    def quit(self):
        self.disable_movement()
        self.fade_away()

    def fade_away(self):
        alpha = self.__mw.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self.__mw.attributes("-alpha", alpha)
            self.__mw.after(50, self.fade_away)
        else:
            self.__mw.destroy()

    def enable_movement(self):
        self.__movement_enabled = True

    def disable_movement(self):
        self.__movement_enabled = False

    def start(self):
        self.__mw.mainloop()


#def main():
#    GUI()


#main()