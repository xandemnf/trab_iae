from enum import Enum, auto
from typing import Callable, List, TYPE_CHECKING, Any
import random

if TYPE_CHECKING:
    from Pokemon import Pokemon
    from combat.Move import Move


class EventType(Enum):
    SLEEP_INFLICTING = auto()
    FINAL_SLEEP_INFLICTED = auto()
    PARALYZE_INFLICTING = auto()
    FINAL_PARALYZE_INFLICTED = auto()
    ATTACK_ACCURACY_CHECK = auto()
    ATTACK_CRIT_CHECK = auto()
    ATTACK_TYPE_MULT_CHECK = auto()
    ATTACK_DAMAGE_NORMAL = auto()
    ATTACK_DAMAGE_CRIT = auto()
    FINAL_ATTACK_CRIT_DAMAGE = auto()
    FINAL_ATTACK_NORMAL_DAMAGE = auto()
    RECOIL_DAMAGE = auto()
    FINAL_TOOK_RECOIL_DAMAGE = auto()
    ABSORB_HEALTH = auto()
    FINAL_HEALTH_ABSORBED = auto()
    STATUS_REMOVE = auto()
    TURN_END = auto()
    FINAL_ATTACK_MISS = auto()
    ATTACK_DOES_EXACT_DAMAGE = auto()
    FINAL_ATTACK_FAIL = auto()
    MULTI_HIT_TIMES = auto()
    BURN_INFLICTING = auto()
    FINAL_BURN_INFLICTED = auto()
    FINAL_MOVE_SUPER_EFFECTIVE = auto()
    FINAL_MOVE_NOT_VERY_EFFECTIVE = auto()
    FINAL_MOVE_DOESNT_AFFECT = auto()
    FREEZE_INFLICTING = auto()
    FINAL_FREEZE_INFLICTED = auto()
    ONE_HIT_KILL_DAMAGE = auto()
    FINAL_ONE_HIT_KILL_DAMAGES = auto()
    TWO_TURN_MOVE = auto()


class EventData:
    def __init__(self, function: Callable[["EventData"], Any]=lambda ed: None, field=None, type_multiplier: float=None,
                 defender: "Pokemon"=None, attacker: "Pokemon"=None, damage=0, chance: float=None,
                 move: "Move"=None, other_multiplier: float=None):
        """
        Function is a function which, when called, executes the event
        :param function:
        :param field:
        :param defender:
        :param attacker:
        :param damage:
        :param chance:
        """
        self.__type_multiplier = type_multiplier
        self.__other_multiplier = other_multiplier
        self.__field = field
        self.__defendant = defender
        self.__attacker = attacker
        self.__def_damage = damage
        self.__chance = chance
        self.__call = function
        self.__move = move

    def call(self):
        return self.__call(self)

    @property
    def field(self):
        return self.__field

    @property
    def defender(self):
        return self.__defendant

    @property
    def attacker(self):
        return self.__attacker

    @property
    def damage(self):
        return self.__def_damage

    @property
    def chance(self):
        return self.__chance

    @property
    def type_multiplier(self):
        return self.__type_multiplier

    @property
    def other_multiplier(self):
        return self.__other_multiplier

    @property
    def move(self):
        return self.__move


class Event:
    def __init__(self, event_type: EventType, data_object: EventData):
        self.__type = event_type
        self.__data = data_object

    def call(self):
        return self.__data.call()

    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return self.__data
