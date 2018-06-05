from math import floor
from random import randint, shuffle
from typing import List, Tuple, Dict, TYPE_CHECKING
from readdata import INDEXDATA, NATUREDATA

if TYPE_CHECKING:
    from combat.constants.status_effects import StatusEffect
    from combat.constants.pokemon_types import PokemonType



class Pokemon:
    def __init__(self, index: int, level: int):
        # Acquire data from previously read files
        data = INDEXDATA[index]
        self.__index = index
        self.__level = level
        self.__name = data["name"]
        self.__types = data["types"]
        self.__base_stats = data["stats"]
        # Calculate individual values
        self.random_IVs()
        self.__nature = NATUREDATA[randint(0, 24)]
        self.__EVs = [0, 0, 0, 0, 0, 0]
        self.__hp = self.get_max_hp()
        self.__exp = 1
        self.__moves = []
        self.__vol_statuses = []
        self.__evolve_level = data["evolve_level"]
        self.__evolution = data["evolution"]
        self.__last_move_used = None

        # Combat variables
        # Att, Def, SpA, SpD, Spe, Acc, Eva
        self.__stat_changes = [0, 0, 0, 0, 0, 0, 0]
        self.__nonvol_status = None

    def random_IVs(self):
        """
        Calculates random Individual Values between 0 and 31 for an encountered pokemon.
        Legendary pokemon always get 3 maximum IVs.
        Calculated values are put into self.__IVs list.
        :return: None
        """
        # Start with random
        self.__IVs = [randint(0,31) for i in range(6)]
        # TODO: poista debugit
        if self.__index == 13:
            self.__IVs = [31, 31, 31, 31, 31, 31]
        # Check if legendary
        if self.__index in [144, 145, 146, 150, 151]:
            all = list(range(0, 5))
            shuffle(all)
            # Choose three different IVs to be maxed
            forced = all[:3]
            for value in forced:
                self.__IVs[value] = 31

    # Getters
    def get_hp(self):
        return self.__hp

    def get_max_hp(self):
        # Calculate max HP, formula borrowed from Bulbapedia
        return floor(((2 * self.__base_stats[0] + self.__IVs[0] + floor(self.__EVs[0] / 4 )) * self.__level) / 100) + self.__level + 10

    def calculate_stat(self, stat: int):
        # Calculate for all other stats, formula borrowed from Bulbapedia
        nature = 1.1 if self.__nature[1] == stat else 0.9 if self.__nature[2] == stat else 1
        return floor((floor(((2 * self.__base_stats[stat] + self.__IVs[stat] + floor(self.__EVs[stat] / 4)) * self.__level) / 100) + 5) * nature)

    def get_attack(self):
        return self.calculate_stat(1)

    @property
    def last_move_used(self):
        return self.__last_move_used

    @last_move_used.setter
    def last_move_used(self, move):
        self.__last_move_used = move

    def get_defence(self):
        return self.calculate_stat(2)

    def get_sp_att(self):
        return self.calculate_stat(3)

    def get_sp_def(self):
        return self.calculate_stat(4)

    def get_speed(self):
        return self.calculate_stat(5)

    def get_IVs(self) -> List[int]:
        # For debudding
        return self.__IVs

    def get_nature(self) -> Tuple[str, int, int]:
        return self.__nature

    @property
    def types(self) -> List["PokemonType"]:
        return self.__types

    def get_nonvol_status(self) -> Tuple[str, int]:
        return self.__nonvol_status

    def get_volatile_statuses(self) -> Dict[str, int]:
        return self.__vol_statuses

    def no_nonvolatile_status(self) -> bool:
        return self.__nonvol_status is None

    def set_nonvol_status(self, new_status: "StatusEffect"):
        self.__nonvol_status = new_status

    def add_volatile_status(self, new_status: "StatusEffect"):
        self.__vol_statuses.append(new_status)

    def remove_volatile_status(self, to_be_removed: "StatusEffect"):
        self.__vol_statuses.remove(to_be_removed)

    def remove_nonvol_status(self):
        self.__nonvol_status = None

    def damage(self, amount: int) -> int:
        """
        Function damages the pokemon. Negative damage cannot occur.
        :param amount: Int, how much damage is to be dealt
        :return: Int how much damage was actually dealt (necessary for recoil etc.)
        """
        if amount < 0:
            return 0
        if self.__hp <= amount:
            old_hp = self.__hp
            self.__hp = 0
            # TODO: Call fainting here
            return old_hp
        else:
            self.__hp -= amount
        return amount

    def heal(self, amount: int) -> int:
        """
        Function heals the pokemon. Negative healing cannot occur.
        :param amount: Int, how much health is to be restored
        :return: Int, stating the amount that was actually restored
        """
        if amount < 0:
            return 0
        if self.get_max_hp() < self.__hp + amount:
            healed = self.get_max_hp() - self.__hp
            self.__hp = self.get_max_hp()
            return healed
        else:
            self.__hp += amount
            return amount

    def revive(self, max: bool = False) -> bool:
        """
        Function revives a fainted pokémon, filling it's hp to half
        :param max: Boolean stating whether a max revive was used
        :return: Boolean stating whether a revive was successful
        """
        # Can't revive if not fainted
        if self.__hp == 0:
            # Max Revive fills hp to max instead of half
            if max:
                self.__hp = self.get_max_hp()
            else:
                self.__hp = self.get_max_hp() // 2
            return True
        return False

    def gain_EVs(self, gain_list: List[int]):
        """
        Pokemon gains effort values depending on the defeated pokemon.
        :param gain_list: list of defeated pokemon's EV gain
        :return:
        """
        # Loop through the given list
        for i in range(0, 6):
            # Skip the zeroes
            if gain_list[i] > 0:
                # Add gained EV if individual and EV totals don't exceed maximum
                if self.__EVs[i] < 252 and sum(self.__EVs) < 511:
                    self.__EVs[i] += gain_list[i]
                    # Fix the result in case of EV overflow
                    if self.__EVs[i] > 252:
                        self.__EVs[i] = 252

    def gain_exp(self, amount: int):
        if self.__exp < 1000000:
            self.__exp += amount
        # TODO: tsekkaa level up jotenkin

    def level_up(self):

        if self.__level < 100:
            self.__level += 1
            if self.__evolve_level is not None and self.__level >= self.__evolve_level:
                self.evolve()

    def evolve(self):
        # TODO: dialogue during animation
        data = INDEXDATA[self.__evolution]
        self.__index = self.__evolution
        self.__name = data["name"]
        self.__types = data["types"]
        self.__base_stats = data["stats"]
        self.__evolve_level = data["evolve_level"]
        self.__evolution = data["evolution"]
        # TODO: On-evolve move learning

"""
c = Pokemon(3, 100)
print(c.get_max_hp(), c.get_attack(), c.get_defence(), c.get_sp_att(), c.get_sp_def(), c.get_speed())
print(c.get_IVs())
c.damage(1000)
print(c.revive())
print(c.get_hp())
"""