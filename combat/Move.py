from typing import List
from combat.constants.move_effects import MoveEffect
from combat.constants.move_categories import MoveCategory
from combat.constants.pokemon_types import PokemonType
from combat.constants.status_effects import *
from Pokemon import Pokemon
from combat.event import Event, EventData, EventType
from random import random, randint
from combat.util.util import flatten_events
from combat.constants.pokemon_types import type_multiplier


class Move:
    def __init__(self, name: str, power: int, accuracy: int, types,
                 category: MoveCategory, contact: bool = None, effects: List[MoveEffect]=None, use_function=None,
                 recoil_percent=None, absorb_percent=None, crit_chance=None):
        self.__name = name
        self.__power = power
        self.__accuracy = accuracy
        self.__types = types if isinstance(types, list) else [types]
        self.__category = category
        self.__contact = contact if contact is not None else True if category == MoveCategory.PHYSICAL else False
        self.__effects = effects if effects is not None else list()
        self.__recoil_percent = recoil_percent
        self.__absorb_percent = absorb_percent
        self.__function = NormalAttackFlow.normal_use if use_function is None else use_function

        # Normal flow functions
        self.attack_hit_check = NormalAttackFlow.attack_hit_check
        self.attack_hits = NormalAttackFlow.attack_hits
        self.type_mult_check = NormalAttackFlow.typemult_check
        self.critical_check = NormalAttackFlow.critical_check
        self.critical_damage = NormalAttackFlow.critical_damage
        self.normal_damage = NormalAttackFlow.normal_damage

        self.__crit_chance = crit_chance if crit_chance is not None else 100/16  # TODO: real crit chance?

    def get_hit_chance(self, attacker: "Pokemon", defender: "Pokemon"):
        # TODO: use accuracy and evasion modifiers
        return self.accuracy

    def use(self, attacker: Pokemon, defender: Pokemon) -> List[Event]:
        return self.__function(self, attacker, defender)

    def calculate_unmodified_damage(self, attacker: Pokemon, defender: Pokemon):
        # TODO: calculate damage
        return self.power

    @staticmethod
    def calculate_real_damage_with_multiplier(event_data: "EventData"):
        base = event_data.damage
        multiplied = base * event_data.type_multiplier * event_data.other_multiplier
        return multiplied

    @property
    def recoil_percent(self):
        return self.__recoil_percent

    @property
    def absorb_percent(self):
        return self.__absorb_percent

    @property
    def effects(self):
        return self.__effects

    @property
    def name(self):
        return self.__name

    @property
    def power(self):
        return self.__power

    @property
    def accuracy(self):
        return self.__accuracy

    @property
    def types(self):
        return self.__types

    @property
    def category(self):
        return self.__category

    @property
    def contact(self):
        return self.__contact

    @property
    def effects(self):
        return self.__effects

    @property
    def crit_chance(self):
        return self.__crit_chance


class NormalAttackFlow:
    @staticmethod
    def absorb_health(data: EventData):
        healed = data.defender.heal(data.damage)
        if healed > 0:
            return Event(EventType.FINAL_HEALTH_ABSORBED,
                         EventData(defender=data.defender, damage=healed, move=data.move))

    @staticmethod
    def recoil_damage(data: EventData):
        took = data.defender.damage(data.damage)
        if took > 0:
            return Event(EventType.FINAL_TOOK_RECOIL_DAMAGE,
                         EventData(defender=data.defender, damage=took, move=data.move))

    @staticmethod
    def damage_adds(self, damage: int, attacker: "Pokemon"):
        events = []
        if self.recoil_percent is not None:
            events.append(Event(EventType.RECOIL_DAMAGE,
                                EventData(
                                    function=NormalAttackFlow.recoil_damage, move=self,
                                    defender=attacker, damage=damage * self.recoil_percent,)
                                )
                          )

        if self.absorb_percent is not None:
            events.append(Event(EventType.ABSORB_HEALTH,
                                EventData(
                                    function=NormalAttackFlow.absorb_health, move=self,
                                    defender=attacker, damage=damage * self.absorb_percent)
                                )
                          )
        return events

    @staticmethod
    def type_effect_events(damage, data: "EventData"):
        if data.type_multiplier > 1:
            event = Event(EventType.FINAL_MOVE_SUPER_EFFECTIVE,
                          EventData(attacker=data.attacker, defender=data.defender, move=data.move, damage=damage))
        elif data.type_multiplier == 0:
            event = Event(EventType.FINAL_MOVE_DOESNT_AFFECT,
                          EventData(attacker=data.attacker, defender=data.defender, move=data.move, damage=damage))
        elif data.type_multiplier < 1:
            event = Event(EventType.FINAL_MOVE_NOT_VERY_EFFECTIVE,
                          EventData(attacker=data.attacker, defender=data.defender, move=data.move, damage=damage))
        else:
            event = None
        return event

    @staticmethod
    def move_effects(e_d: "EventData"):
        return list(map(lambda e: e.affect(e_d.attacker, e_d.defender, None), e_d.move.effects))

    @staticmethod
    def damage_events(e_d: "EventData", event_type: "EventType", type_effect=True):
        potential_dmg = e_d.move.calculate_real_damage_with_multiplier(e_d)
        damage = e_d.defender.damage(potential_dmg)
        events = [Event(event_type, EventData(damage=e_d.damage, defender=e_d.defender, move=e_d.move))]
        if type_effect:
            events.append(NormalAttackFlow.type_effect_events(damage, e_d))
        # Create events for possible other effects of the attack (absorb, recoil, status chances, ...)
        events.extend(NormalAttackFlow.damage_adds(e_d.move, damage, e_d.attacker))
        events.extend(NormalAttackFlow.move_effects(e_d))
        return events

    @staticmethod
    def normal_damage(e_d: "EventData"):
        return NormalAttackFlow.damage_events(e_d, EventType.FINAL_ATTACK_NORMAL_DAMAGE)

    @staticmethod
    def critical_damage(e_d: "EventData"):
        return NormalAttackFlow.damage_events(e_d, EventType.FINAL_ATTACK_CRIT_DAMAGE)

    @staticmethod
    def critical_check(e_d: "EventData"):
        if e_d.chance is None or e_d.chance < 100 * random():
            normal_damage = e_d.move.normal_damage
            return Event(EventType.ATTACK_DAMAGE_NORMAL,
                         EventData(defender=e_d.defender, attacker=e_d.attacker, function=normal_damage,
                                   type_multiplier=e_d.type_multiplier, other_multiplier=1, move=e_d.move,
                                   damage=e_d.move.calculate_unmodified_damage(e_d.attacker, e_d.defender)))
        else:
            crit_damage = e_d.move.critical_damage
            return Event(EventType.ATTACK_DAMAGE_CRIT,
                         EventData(defender=e_d.defender, attacker=e_d.attacker, function=crit_damage,
                                   type_multiplier=e_d.type_multiplier, other_multiplier=1, move=e_d.move,
                                   damage=e_d.move.calculate_unmodified_damage(e_d.attacker, e_d.defender)))

    @staticmethod
    def typemult_check(e_d: "EventData"):
        if e_d.type_multiplier == 0:
            return Event(EventType.FINAL_MOVE_DOESNT_AFFECT,
                         EventData(defender=e_d.defender, attacker=e_d.attacker))
        else:
            critical_check = e_d.move.critical_check
            return Event(EventType.ATTACK_CRIT_CHECK,
                         EventData(function=critical_check, defender=e_d.defender, attacker=e_d.attacker,
                                   damage=e_d.damage, move=e_d.move, chance=e_d.move.crit_chance,
                                   type_multiplier=e_d.type_multiplier))

    @staticmethod
    def attack_hits(event_data: "EventData"):
        typemult_check = event_data.move.type_mult_check
        return Event(EventType.ATTACK_TYPE_MULT_CHECK,
                     EventData(function=typemult_check, defender=event_data.defender, attacker=event_data.attacker,
                               damage=event_data.damage, move=event_data.move,
                               type_multiplier=type_multiplier(event_data.move.types, event_data.defender.types),
                               ))

    @staticmethod
    def attack_hit_check(event_data: "EventData"):
        if event_data.chance is None or event_data.chance >= 100 * random():
            return event_data.move.attack_hits(event_data)
        else:
            return Event(EventType.FINAL_ATTACK_MISS,
                         EventData(defender=event_data.defender, attacker=event_data.attacker, move=event_data.move,
                                   damage=event_data))

    @staticmethod
    def normal_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        attacker.last_move_used = self
        return Event(EventType.ATTACK_ACCURACY_CHECK,
                     EventData(
                          function=self.attack_hit_check,
                          defender=defender, attacker=attacker, damage=self.power, move=self,
                          chance=self.accuracy,
                          type_multiplier=type_multiplier(self.types, defender.types)))


# TODO: Is there a cleaner way overall to implement that only the last of a multi hit will trigger effectiveness event?
class MultiHit:
    @staticmethod
    def multi_hit_times(e_d: "EventData"):
        events = [MultiHit.multi_hit_damages(e_d) for _ in range(e_d.other_multiplier - 1)]
        events.append(NormalAttackFlow.attack_hits(e_d))
        return events

    @staticmethod
    def normal_damage(e_d: "EventData"):
        return NormalAttackFlow.damage_events(e_d, EventType.FINAL_ATTACK_NORMAL_DAMAGE, False)

    @staticmethod
    def crit_damage(e_d: "EventData"):
        return NormalAttackFlow.damage_events(e_d, EventType.FINAL_ATTACK_CRIT_DAMAGE, False)

    @staticmethod
    def critical_check(e_d: "EventData"):
        if e_d.chance is None or e_d.chance < 100 * random():
            return Event(EventType.ATTACK_DAMAGE_NORMAL,
                         EventData(defender=e_d.defender, attacker=e_d.attacker, function=MultiHit.normal_damage,
                                   type_multiplier=e_d.type_multiplier, other_multiplier=1, move=e_d.move,
                                   damage=e_d.move.calculate_unmodified_damage(e_d.attacker, e_d.defender)))
        else:
            return Event(EventType.ATTACK_DAMAGE_CRIT,
                         EventData(defender=e_d.defender, attacker=e_d.attacker, function=MultiHit.crit_damage,
                                   type_multiplier=e_d.type_multiplier, other_multiplier=1, move=e_d.move,
                                   damage=e_d.move.calculate_unmodified_damage(e_d.attacker, e_d.defender)))

    @staticmethod
    def typemult_check(e_d: "EventData"):
        if e_d.type_multiplier == 0:
            return Event(EventType.FINAL_MOVE_DOESNT_AFFECT,
                         EventData(defender=e_d.defender, attacker=e_d.attacker))
        else:
            return Event(EventType.ATTACK_CRIT_CHECK,
                         EventData(function=MultiHit.critical_check, defender=e_d.defender, attacker=e_d.attacker,
                                   damage=e_d.damage, move=e_d.move, chance=e_d.move.crit_chance,
                                   type_multiplier=e_d.type_multiplier))

    @staticmethod
    def multi_hit_damages(e_d: "EventData"):
        return Event(EventType.ATTACK_TYPE_MULT_CHECK,
                     EventData(function=MultiHit.typemult_check, defender=e_d.defender, attacker=e_d.attacker,
                               damage=e_d.damage, move=e_d.move,
                               type_multiplier=type_multiplier(e_d.move.types, e_d.defender.types),
                               ))

    @staticmethod
    def multi_hit_hits(ed: "EventData"):
        times = [2, 2, 3, 3, 4, 5][randint(0, 5)]
        return Event(EventType.MULTI_HIT_TIMES,
                     EventData(other_multiplier=times, attacker=ed.attacker, defender=ed.defender,
                               function=MultiHit.multi_hit_times, damage=ed.damage, move=ed.move))

    @staticmethod
    def multi_hit(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        attacker.last_move_used = self
        self.attack_hits = MultiHit.multi_hit_hits
        return NormalAttackFlow.normal_use(self, attacker, defender)


class OneHitKO:
    @staticmethod
    def one_hit_kill_dmg(e_d: "EventData"):
        return Event(EventType.FINAL_ONE_HIT_KILL_DAMAGES,
                     EventData(defender=e_d.defender, attacker=e_d.attacker, damage=e_d.damage))

    @staticmethod
    def one_hit_kill(e_d: "EventData"):
        return Event(EventType.ONE_HIT_KILL_DAMAGE,
                     EventData(defender=e_d.defender, attacker=e_d.attacker, function=OneHitKO.one_hit_kill_dmg,
                               damage=e_d.defender.get_hp()))

    @staticmethod
    def one_hit_ko_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        self.critical_check = OneHitKO.one_hit_kill
        attacker.last_move_used = self
        return NormalAttackFlow.normal_use(self, attacker, defender)


class TwoTurn:
    @staticmethod
    def turn_one_complete(e_d: "EventData"):
        e_d.attacker.add_volatile_status(TwoTurnMoveTrap(e_d.attacker, e_d.move, TwoTurn.turn_two))

    @staticmethod
    def two_turn_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        return Event(EventType.TWO_TURN_MOVE,
                     EventData(function=TwoTurn.turn_one_complete, attacker=attacker, move=self, defender=defender))

    @staticmethod
    def turn_two(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        attacker.two_turn_move = None
        attacker.last_move_used = self
        return NormalAttackFlow.normal_use(self, attacker, defender)
