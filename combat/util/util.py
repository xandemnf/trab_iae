from combat.event import Event
from typing import List

def flatten_events(ev, result=None) -> List["Event"]:
    if result is None:
        result = list()
    if isinstance(ev, Event):
        result.append(ev)
    elif isinstance(ev, list):
        for e in ev:
            flatten_events(e, result)
    return result