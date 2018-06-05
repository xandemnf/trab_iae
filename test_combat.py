from Pokemon import Pokemon
from combat.implementations.move_list import *
from combat.event import Event
from typing import List
from combat.util.util import flatten_events
from combat.Move import TwoTurn

if __name__ == "__main__":
    pokemon1 = Pokemon(4, 50)
    pokemon2 = Pokemon(1, 50)

    e = flatten_events(RazorWind.use(pokemon1, pokemon2))

    for i in e:
        print(i.type)
        e.extend(flatten_events(i.call()))

    e = flatten_events(TwoTurn.turn_two(pokemon1.two_turn_move, pokemon1, pokemon2))

    for i in e:
        print(i.type)
        e.extend(flatten_events(i.call()))