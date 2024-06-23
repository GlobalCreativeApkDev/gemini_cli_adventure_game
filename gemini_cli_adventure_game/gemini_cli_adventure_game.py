"""
This file contains implementation of the game "Gemini CLI Adventure Game".
Author: GlobalCreativeApkDev
"""


# Game version: 1


# Importing necessary libraries


import sys
import time
import uuid
import pickle
import copy
import google.generativeai as gemini
import random
from datetime import datetime
import os
from dotenv import load_dotenv
from functools import reduce

from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True


# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
     "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER",
     "OTHER", "OTHER", "OTHER"]
]


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def list_to_string(a_list: list) -> str:
    res: str = "["  # initial value
    for i in range(len(a_list)):
        if i == len(a_list) - 1:
            res += str(a_list[i])
        else:
            res += str(a_list[i]) + ", "

    return res + "]"


def tabulate_element_chart() -> str:
    return str(tabulate(ELEMENT_CHART, headers='firstrow', tablefmt='fancy_grid'))


def generate_random_name() -> str:
    res: str = ""  # initial value
    name_length: int = random.randint(3, 25)
    for i in range(name_length):
        res += LETTERS[random.randint(0, len(LETTERS) - 1)]

    return res.capitalize()


# TODO: creating function to generate random legendary creature.


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def get_elemental_damage_multiplier(element1: str, element2: str) -> mpf:
    if element1 == "TERRA":
        return mpf("2") if element2 in ["ELECTRIC, DARK"] else mpf("0.5") if element2 in ["METAL", "WAR"] else mpf("1")
    elif element1 == "FLAME":
        return mpf("2") if element2 in ["NATURE", "ICE"] else mpf("0.5") if element2 in ["SEA", "WAR"] else mpf("1")
    elif element1 == "SEA":
        return mpf("2") if element2 in ["FLAME", "WAR"] else mpf("0.5") if element2 in ["NATURE", "ELECTRIC"] else \
            mpf("1")
    elif element1 == "NATURE":
        return mpf("2") if element2 in ["SEA", "LIGHT"] else mpf("0.5") if element2 in ["FLAME", "ICE"] else mpf("1")
    elif element1 == "ELECTRIC":
        return mpf("2") if element2 in ["SEA", "METAL"] else mpf("0.5") if element2 in ["TERRA", "LIGHT"] else mpf("1")
    elif element1 == "ICE":
        return mpf("2") if element2 in ["NATURE", "WAR"] else mpf("0.5") if element2 in ["FLAME", "METAL"] else mpf("1")
    elif element1 == "METAL":
        return mpf("2") if element2 in ["TERRA", "ICE"] else mpf("0.5") if element2 in ["ELECTRIC", "DARK"] else \
            mpf("1")
    elif element1 == "DARK":
        return mpf("2") if element2 in ["METAL", "LIGHT"] else mpf("0.5") if element2 == "TERRA" else mpf("1")
    elif element1 == "LIGHT":
        return mpf("2") if element2 in ["ELECTRIC", "DARK"] else mpf("0.5") if element2 == "NATURE" else mpf("1")
    elif element1 == "WAR":
        return mpf("2") if element2 in ["TERRA", "FLAME"] else mpf("0.5") if element2 in ["SEA", "ICE"] else mpf("1")
    elif element1 == "PURE":
        return mpf("2") if element2 == "LEGEND" else mpf("0.5") if element2 == "PRIMAL" else mpf("1")
    elif element1 == "LEGEND":
        return mpf("2") if element2 == "PRIMAL" else mpf("0.5") if element2 == "PURE" else mpf("1")
    elif element1 == "PRIMAL":
        return mpf("2") if element2 == "PURE" else mpf("0.5") if element2 == "LEGEND" else mpf("1")
    elif element1 == "WIND":
        return mpf("2") if element2 == "WIND" else mpf("1")
    else:
        return mpf("1")


def load_game_data(file_name):
    # type: (str) -> SavedGameData
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (SavedGameData, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes.


# TODO: create more necessary classes


###########################################
# ADVENTURE MODE
###########################################


class Action:
    """
    This class contains attributes of an action which can be carried out during battles.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]

    # TODO: implement methods

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class Battle:
    """
    This class contains attributes of a battle in this game.
    """

    def __init__(self, player1):
        # type: (Player) -> None
        self.player1: Player = player1

    def clone(self):
        # type: () -> Battle
        return copy.deepcopy(self)


class PVPBattle(Battle):
    """
    This class contains attributes of a battle between players.
    """

    def __init__(self, player1, player2):
        # type: (Player, Player) -> None
        Battle.__init__(self, player1)
        self.player2: Player = player2


class City:
    """
    This class contains attributes of a city in this game.
    """

    def __init__(self, name, tiles):
        # type: (str, list) -> None
        self.name: str = name
        self.__tiles: list = tiles

    def get_tile_at(self, x, y):
        # type: (int, int) -> CityTile or None
        if x < 0 or x >= len(self.__tiles[0]) or y < 0 or y >= len(self.__tiles):
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        res: str = str(self.name)
        all_tiles: list = []  # initial value
        for y in range(len(self.__tiles)):
            curr_tiles: list = []  # initial value
            for x in range(len(self.__tiles[y])):
                curr_tile: CityTile = self.get_tile_at(x, y)
                curr_tiles.append(str(curr_tile))

            all_tiles.append(curr_tiles)
        return res + "\n" + str(tabulate(all_tiles, headers='firstrow', tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> City
        return copy.deepcopy(self)


class CityTile:
    """
    This class contains attributes of a tile in a city.
    """

    def __init__(self):
        # type: () -> None
        self.__game_characters: list = []  # initial value
        self.is_portal: bool = False
        self.can_encounter_wild_battles: bool = False

    def get_game_characters(self):
        # type: () -> list
        return self.__game_characters

    def add_game_character(self, game_character):
        # type: (GameCharacter) -> None
        self.__game_characters.append(game_character)

    def remove_game_character(self, game_character):
        # type: (GameCharacter) -> bool
        if game_character in self.__trainers:
            self.__game_characters.remove(game_character)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return "(" + str(type(self).__name__) + ")\nAND\n" + list_to_string(
            [game_character.name for game_character in self.__game_characters])

    def clone(self):
        # type: () -> CityTile
        return copy.deepcopy(self)


# TODO: add more classes related to adventure mode (e.g., types of city tiles)


###########################################
# ADVENTURE MODE
###########################################


###########################################
# ITEM
###########################################


class Item:
    """
    This class contains attributes of an item in this game.
    """

    def __init__(self, name, description, dollars_cost):
        # type: (str, str, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.dollars_cost: mpf = dollars_cost

    def clone(self):
        # type: () -> Item
        return copy.deepcopy(self)


###########################################
# ITEM
###########################################


###########################################
# GENERAL
###########################################


class GameCharacter:
    """
    This class contains attributes of a game character.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.character_id: str = str(uuid.uuid1())
        self.name: str = name

    def clone(self):
        # type: () -> GameCharacter
        return copy.deepcopy(self)


class NPC(GameCharacter):
    """
    This class contains attributes of a non-player character in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        GameCharacter.__init__(self, name)


class Player(GameCharacter):
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        GameCharacter.__init__(self, name)
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.dollars: mpf = mpf("5e6")

        # TODO: add more required class attributes

    # TODO: implement methods

    def interact_with_npc(self, npc):
        # type: (NPC) -> None
        pass  # TODO: implement this method


class AIPlayer(Player):
    """
    This class contains attributes of an AI controlled player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        Player.__init__(self, name)


class Mission:
    """
    This class contains attributes of a mission in this game.
    """

    def __init__(self, name, description, clear_reward):
        # type: (str, str, Reward) -> None
        self.name: str = name
        self.description: str = description
        self.clear_reward: Reward = clear_reward

    def clone(self):
        # type: () -> Mission
        return copy.deepcopy(self)


class Reward:
    """
    This class contains attributes of a reward gained for accomplishing something in this game.
    """

    def __init__(self, player_reward_exp, player_reward_dollars):
        # type: (mpf, mpf) -> None
        self.player_reward_exp: mpf = player_reward_exp
        self.player_reward_dollars: mpf = player_reward_dollars

    def clone(self):
        # type: () -> Reward
        return copy.deepcopy(self)


class AdventureModeLocation:
    """
    This class contains attributes of the location of a player in adventure mode of this game.
    """

    def __init__(self, tile_x, tile_y):
        # type: (int, int) -> None
        self.tile_x: int = tile_x
        self.tile_y: int = tile_y

    def clone(self):
        # type: () -> AdventureModeLocation
        return copy.deepcopy(self)


class SavedGameData:
    """
    This class contains attributes of the saved game data in this game.
    """

    def __init__(self, trainer_name, temperature, top_p, top_k, max_output_tokens, player_data):
        # type: (str, float, float, float, int, Trainer) -> None
        self.trainer_name: str = trainer_name
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.top_k: float = top_k
        self.max_output_tokens: int = max_output_tokens
        self.player_data: Player = player_data

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += str(self.trainer_name).upper() + "\n"
        res += "Temperature: " + str(self.temperature) + "\n"
        res += "Top P: " + str(self.top_p) + "\n"
        res += "Top K: " + str(self.top_k) + "\n"
        res += "Max output tokens: " + str(self.max_output_tokens) + "\n"
        return res

    def clone(self):
        # type: () -> SavedGameData
        return copy.deepcopy(self)


###########################################
# GENERAL
###########################################


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Gemini safety settings
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    # Saved game data
    saved_game_data: SavedGameData

    # The player's name
    player_name: str = ""  # initial value

    # Gemini Generative Model
    model = gemini.GenerativeModel(model_name="gemini-1.5-pro",
                                       generation_config={
                                           "temperature": 1,
                                           "top_p": 0.95,
                                           "top_k": 64,
                                           "max_output_tokens": 8192,
                                           "response_mime_type": "text/plain",
                                       },
                                       safety_settings=safety_settings)  # initial value

    print("Enter \"NEW GAME\" to create new saved game data.")
    print("Enter \"LOAD GAME\" to load existing saved game data.")
    action: str = input("What do you want to do? ")

    # TODO: implement in-game functionality

    # Start playing the game.
    while True:
        clear()


if __name__ == "__main__":
    main()
