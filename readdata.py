import inspect
import os
from combat.constants.pokemon_types import PokemonType

INDEXDATA = []
MOVEDATA = []
TYPEDATA = []
NATUREDATA = []
AREADATA = []


folder = "/".join(inspect.stack()[0][1].split("/")[:-1])
if folder == "":
    folder = "."

def string_to_type(s):
    types = {
        "NORMAL" : 0,
        "FIRE" : 1,
        "WATER" : 2,
        "ELECTRIC" : 3,
        "GRASS" : 4,
        "ICE" : 5,
        "FIGHTING" : 6,
        "POISON" : 7,
        "GROUND" : 8,
        "FLYING" : 9,
        "PSYCHIC" : 10,
        "BUG" : 11,
        "ROCK" : 12,
        "GHOST" : 13,
        "DRAGON" : 14,
        "DARK" : 15,
        "STEEL" : 16,
        "FAIRY" : 17,
        "NONE" : -1
    }
    return PokemonType(types[s.upper()])


def read_indexdata():
    if len(INDEXDATA) > 0:
        return
    try:
        file = open(folder + "/data/indexdata.csv", "r", encoding="utf-8")
    except IOError:
        print("indexdata.csv not usable")
        raise AssertionError
    for row in file:
        row = row.rstrip().split(";")
        data = {}
        data["name"] = row[1]
        data["types"] = [string_to_type(row[2])]
        if row[3] != "None":
            data["types"].append(string_to_type(row[3]))
        data["stats"] = list(map(int, row[4].split(",")))
        if row[5] == "None":
            data["evolve_level"] = None
        else:
            data["evolve_level"] = int(row[5])
        if row[6] == "None":
            data["evolution"] = None
        else:
            data["evolution"] = int(row[6])
        INDEXDATA.append(data)
    file.close()

def read_naturedata():
    """
    Stores data on pokemon natures into NATUREDATA-constant list.
    List format is List[name: str, plus: int, minus: int]
    :return: None
    """
    if len(NATUREDATA) > 0:
        return
    try:
        file = open(folder + "/data/naturedata.csv", "r", encoding="utf-8")
    except IOError:
        print("naturedata.csv not usable")
        raise AssertionError
    for row in file:
        row = row.rstrip().split(",")
        row[0] = row[0].capitalize()
        row[1] = int(row[1])
        row[2] = int(row[2])
        NATUREDATA.append(row)
    file.close()

def read_movedata():
    if len(MOVEDATA) > 0:
        return

def read_typedata():
    if len(TYPEDATA) > 0:
        return

def read_areadata():
    if len(AREADATA) > 0:
        return
    try:
        file = open(folder + "/data/areadata.csv", "r", encoding="utf-8")
    except IOError:
        print("areadata.csv not usable")
        raise AssertionError
    current = []
    for row in file:
        row = row.rstrip()
        if row == "# New Area":
            if current != []:
                AREADATA.append(current)
            current = []
        if len(row) != 0 and row[0] != "#":
            current.append(row)
    if current != []:
        AREADATA.append(current)
    file.close()

read_indexdata()
read_movedata()
read_typedata()
read_naturedata()
read_areadata()