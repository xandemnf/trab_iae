import random

from typing import TYPE_CHECKING, List
from combat.event import Event, EventData, EventType
from combat.constants.status_effects import *
if TYPE_CHECKING:
    from combat.combat import Combat
    from combat.Move import Move



class MoveEffect:
    """
    The inflicted effect on the pokemon(s).
    Child classes create events which set the actual effects onto pokemons
    """
    def __init__(self, chance=None):
        self.__chance = chance

    @property
    def chance(self):
        return self.__chance

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat") -> List["Event"]:
        raise NotImplementedError("Not implemented")


class MoveInflictExactDamage(MoveEffect):
    """
    Exact damage, for example Dragon Rage
    """
    def __init__(self, damage):
        super().__init__()

    @staticmethod
    def call(event_data: "EventData"):
        damage = event_data.defender.damage(event_data.damage)
        if damage > 0:
            return Event(EventType.FINAL_ATTACK_DID_DAMAGE,
                         EventData(defender=event_data.defender, damage=damage))

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat"):
        return Event(EventType.ATTACK_DOES_EXACT_DAMAGE,
                     EventData(function=self.call, defender=defender, attacker=attacker))


class MoveInflictSleep(MoveEffect):
    """
    Sleep status inflict
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def call(event_data: "EventData"):
        # Set the status
        if event_data.defender.no_nonvolatile_status():
            event_data.defender.set_nonvol_status(SleepEffect(event_data.defender))
            return Event(EventType.FINAL_SLEEP_INFLICTED, EventData(defender=event_data.defender))

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat"):
        return Event(EventType.SLEEP_INFLICTING, EventData(defender=defender, attacker=attacker,
                                                            function=self.call))


class MoveInflictParalyzeChance(MoveEffect):
    """
    Paralyze chance
    """
    def __init__(self, chance):
        super().__init__(chance)

    @staticmethod
    def call(event_data: "EventData"):
        # Set the status if rng
        r = random.randint(0, 100)
        if event_data.chance is None or r < event_data.chance:
            if event_data.defender.no_nonvolatile_status():
                event_data.defender.set_nonvol_status(ParalyzeEffect(event_data.defender))
                return Event(EventType.FINAL_PARALYZE_INFLICTED, EventData(defender=event_data.defender))

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat"):
        return Event(EventType.PARALYZE_INFLICTING, EventData(chance=self.chance, defender=defender, attacker=attacker,
                                                               function=self.call))


class MoveInflictBurnChance(MoveEffect):
    """
    Burn chance
    """
    def __init__(self, chance):
        super().__init__(chance)

    @staticmethod
    def call(event_data: "EventData"):
        # Set the status if rng
        r = random.randint(0, 100)
        if event_data.chance is None or r < event_data.chance:
            if event_data.defender.no_nonvolatile_status():
                event_data.defender.set_nonvol_status(BurnEffect(event_data.defender))
                return Event(EventType.FINAL_BURN_INFLICTED, EventData(defender=event_data.defender))

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat"):
        return Event(EventType.BURN_INFLICTING, EventData(chance=self.chance, defender=defender, attacker=attacker,
                                                          function=self.call))


class MoveInflictFreezeChance(MoveEffect):
    """
    Freeze chance
    """
    def __init__(self, chance):
        super().__init__(chance)

    @staticmethod
    def call(event_data: "EventData"):
        # Set the status if rng
        r = random.randint(0, 100)
        if event_data.chance is None or r < event_data.chance:
            if event_data.defender.no_nonvolatile_status():
                event_data.defender.set_nonvol_status(FreezeEffect(event_data.defender))
                return Event(EventType.FINAL_FREEZE_INFLICTED, EventData(defender=event_data.defender))

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat"):
        return Event(EventType.FREEZE_INFLICTING, EventData(chance=self.chance, defender=defender, attacker=attacker,
                                                            function=self.call))


"""
def sleep_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("sleep", 0))


def burn_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "fire" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("burn", 0))


def poison_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "poison" in defender.get_types():
        return
    if "steel" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("poison", 0))


def toxic_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "poison" in defender.get_types():
        return
    if "steel" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("toxic", 1))


def paralysis_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "electric" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("para", 0))


def sleep_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("sleep", 0))


def freeze_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "ice" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("freeze", 0))


def flinch_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "flinch" in defender.get_volatile_statuses():
        return
    check = randint(0, 100)
    if check < chance:
        defender.add_volatile_status("flinch")


def confusion_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "confusion" in defender.get_volatile_statuses():
        return
    check = randint(0, 100)
    if check < chance:
        defender.add_volatile_status("confusion")


def curse_ghost(attacker: Pokemon, defender: Pokemon):
    if "curse" in defender.get_volatile_statuses():
        return
    defender.add_volatile_status("curse")


def leech_seed(attacker: Pokemon, defender: Pokemon):
    if "grass" in defender.get_types():
        return
    if "leech_seed" in defender.get_volatile_statuses():
        return
    defender.add_volatile_status("leech_seed")
"""