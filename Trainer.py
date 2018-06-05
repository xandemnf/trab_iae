from enum import Enum

class TrainerMovementType(Enum):
    WALKING = 0         # Most usual type of movement
    RUNNING = 1         # If B is held while walking
    CYCLING = 2         # If on a bike
    SURFING = 3         # If on water
    FORCED_MOVEMENT = 4 # Spin tiles or cutscene movement
    CLIPPING = 5        # For debugging perhaps?


class Trainer:
    def __init__(self, name, model):
        self.__name = name
        self.__model = model
        self.__movetype = TrainerMovementType.WALKING
        self.__inventory = []
        self.__party = []
        self.__money = 0
        self.__badges = []
        self.__location = ""
        self.__x = 0
        self.__y = 0

    def add_to_party(self, new_pokemon):
        if len(self.__party) >= 6:
            return False
        else:
            self.__party.append(new_pokemon)
        return True

    def remove_from_party(self, index):
        if len(self.__party) <= 1:
            return None
        else:
            removed = self.__party[index]
            del self.__party[index]
            return removed

    def add_money(self, amount):
        if self.__money + amount > 999999:
            self.__money = 999999
        else:
            self.__money += amount

    def remove_money(self, amount):
        if self.__money - amount < 0:
            return False
        else:
            self.__money -= amount
            return True

    def add_badge(self, new_badge):
        if new_badge in self.__badges:
            return False
        else:
            self.__badges.append(new_badge)
            return True

    def add_to_inventory(self, item, amount=1):
        assert amount <= 99
        if item.is_key_item():
            self.__inventory.append(item)
        elif item in self.__inventory:
            items = [elem for elem in self.__inventory if elem.get_name() == item]
            for element in items:
                if element.get_amount() < 999:
                    amount = element.add_amount(amount)

    def remove_from_inventory(self, slot, amount):
        item = self.__inventory[slot]
        assert amount <= item.get_amount()
        if item.reduce_amount(amount):
            if item.get_amount() == 0:
                del self.__inventory[slot]

    def move_up(self, area):
        if not area.occupied(self.__x, self.__y + 1):
            self.__y += 1

    def move_down(self, area):
        if not area.occupied(self.__x, self.__y - 1):
            self.__y -= 1

    def move_right(self, area):
        if not area.occupied(self.__x + 1, self.__y):
            self.__x += 1

    def move_left(self, area):
        if not area.occupied(self.__x - 1, self.__y):
            self.__x -= 1

