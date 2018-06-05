# This module is responsible for choosing the correct frame for walking
# animation. It keeps track of which foot was used to take the last step
# and returns strings which are compatible with the images stored in the
# GUI module.

# Singleton
class Walk_animation:
    def __init__(self):
        # Flip-flop. Tracks the foot the last step was taken with.
        # True means left, false means right.
        self.__previous = True
        self.__direction = "down"

        # Flip-flop. Tracks whether the previous frame was a standing frame
        # or a walking frame. True for walking, False for standing.
        self.__movement = False

    # Setter
    def set_direction(self, new_direction: str):
        self.__direction = new_direction

    def next_frame(self) -> str:
        """
        The funcion figures out which frame is needed. It flips the flip-flops
        when necessary, so that every other frame is a standing frame, and
        every other moving frame is with a different foot. Moving left and right
        only have one frame independent of the foot.
        :return: String, which is a key to the images-dict in GUI module.
        """
        self.__movement = not self.__movement
        if self.__movement:
            self.__previous = not self.__previous
            walkstring = "walk_" + self.__direction
            if not self.__previous or self.__direction in ["left", "right"]:
                return walkstring
            else:
                return walkstring + "_l"

        else:
            return self.__direction