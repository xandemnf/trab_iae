from typing import List, TYPE_CHECKING
from random import randint
if TYPE_CHECKING:
    from Pokemon import Pokemon
    from combat.event import Event, EventType, EventData
    from combat.Move import Move


class StatusEffect:
    """
    Status effect on a pokemon. Has turn count and event emitter and handler
    """
    def __init__(self, pokemon: "Pokemon"):
        """
        :param pokemon: Affected pokemon
        :return:
        """
        self.__turns = 0
        self.__pokemon = pokemon

    def handle(self, event: "Event") -> ("Event", List["Event"]):
        """
        Handle function modifies the original event, and return a list of new events to be dispatched
        :param event: The event the function reacts to
        :return: Tuple of the (possibly modified) original event, and a possibly empty list of new events
        """
        raise NotImplementedError("Not implemented")

    @property
    def turns(self):
        return self.__turns

    def increment_turns(self):
        self.__turns += 1

    @property
    def pokemon(self):
        return self.__pokemon


class SleepEffect(StatusEffect):
    def __init__(self, pokemon: "Pokemon", max_turns=randint(1, 3)):
        super().__init__(pokemon)
        self.__max_turns = max_turns

    def handle(self, event: "Event"):
        if event.type == EventType.ATTACK_ACCURACY_CHECK:
            pass
            # TODO: Prevent pokemon from doing anything except sleep talk etc.

        if event.type == EventType.TURN_END:
            self.increment_turns()
            if self.turns > self.__max_turns:
                def call(event_data: EventData):
                    self.pokemon.remove_nonvol_status()
                return event, [Event(EventType.STATUS_REMOVE, EventData(function=call, defender=self.pokemon))]


class ParalyzeEffect(StatusEffect):
    def __init__(self, pokemon: "Pokemon"):
        super().__init__(pokemon)

    def handle(self, event: "Event"):
        if event.type == EventType.ATTACK_ACCURACY_CHECK:
            pass
            # TODO: Paralyze chance!


class BurnEffect(StatusEffect):
    def __init__(self, pokemon: "Pokemon"):
        super().__init__(pokemon)

    def handle(self, event: "Event"):
        if event.type == EventType.ATTACK_ACCURACY_CHECK:
            pass
            # TODO: Burn halve attack

        elif event.type == EventType.TURN_END:
            # TODO: Do damage
            pass


class FreezeEffect(StatusEffect):
    def __init__(self, pokemon: "Pokemon"):
        super().__init__(pokemon)

    def handle(self, event: "Event"):
        if event.type == EventType.ATTACK_ACCURACY_CHECK:
            pass
            # TODO: Don't let pokemon attack except if it thaws


class TwoTurnMoveTrap(StatusEffect):
    """
    Traps attacker into a two turn move, like solar beam
    """

    def __init__(self, attacker: "Pokemon", move: "Move", turn_two):
        self.__move = move
        self.__turn_two = turn_two
        super().__init__(attacker)

    def handle(self, event: "Event") -> ("Event", List["Event"]):
        # TODO: Once we have implemented actual turn action check / input,
        # intercept that here, and choose attacking with the move
        self.__turn_two(event.data.move, event.data.attacker, event.data.defender)
        pass


# Just for copying maths from
def burn_event(affected: "Pokemon"):
    """
    Affected pokemon loses 1/16 of it's max HP at the end of turn
    :param affected: Pokemon affected by burn
    :return: None
    """
    affected.damage(affected.get_max_hp() // 16)
    # TODO: Game prints information
    # TODO: Call for animation


def poison_event(affected: "Pokemon"):
    """
    Affected pokemon loses 1/8 of it's max HP at the end of turn
    :param affected: Pokemon affected by poison
    :return: None
    """
    affected.damage(affected.get_max_hp() // 8)
    # TODO: Game prints information
    # TODO: Call for animation


def toxic_event(affected: "Pokemon"):
    """
    Affected pokemon loses a cumulative 1/16 of it's max HP at the end of turn,
    then cumulative toxic count gets raised
    :param affected: Pokemon affected by toxic
    :return: None
    """
    toxic_count = affected.get_nonvol_status()[1]
    affected.damage(toxic_count * (affected.get_max_hp() // 16))
    affected.set_nonvol_status(("toxic", toxic_count + 1))

    # TODO: Game prints information
    # TODO: Call for animation


def leech_seed_event(affected: "Pokemon", receiver: "Pokemon"):
    """
    Affected pokemon loses 1/8 of it's max HP, and the receiving pokemon gains
    an equal amount
    :param affected: Pokemon affected by Leech Seed
    :param receiver: Pokemon that gets healed
    :return: None
    """
    hp_lost = affected.damage(affected.get_max_hp() // 8)
    # TODO: Game prints information
    # TODO: Call for animation
    receiver.heal(hp_lost)
    # TODO: Game prints information


def flinch_event(affected: "Pokemon"):
    """
    Removes flinch from affected pokemon
    :param affected: Pokemon affected by flinch
    :return: None
    """
    affected.decrease_volatile_status_counter("flinch")


def curse_ghost_event(affected: "Pokemon"):
    """
    Deals damage to affected pokemon equal to 1/4 of it's max HP
    :param affected: Pokemon affected by curse
    :return: None
    """
    affected.damage(affected.get_max_hp() // 4)
    # TODO: Game prints information
    # TODO: Call for animation