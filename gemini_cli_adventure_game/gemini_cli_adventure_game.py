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


# TODO: add static functions


# Creating necessary classes.


# TODO: create more necessary classes


###########################################
# GENERAL
###########################################


class Player:
    """
    This class contains attributes of the player in this game.
    """

    # TODO: implement methods


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


if __name__ == "__main__":
    main()
