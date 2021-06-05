"""Crazy8s Constants
Constants used for playing crazy eights in Telegram chat.
    param:
        Author: Deborah Djon
        Date: .06.2021
        Version:0.1
        license: free
"""
from enum import Enum
from telegram import  Bot

"""Contains all constants"""

# Game constants

MoveOutcome = Enum(
    "MoveOutcome", 
    "valid_move round_won game_won invalid_move crazy8 ")

suits = "♠♥♣♦"
# suits = "shcd" # used for debugging. switch with line on top for release

hand_filler = "."
# Testing ---
TEST_B0T_TOKEN = "1796005782:AAH50veupoTsA4KbrKv9A7ZndiO0CCewa9g"

# Bot constants

BOT_TOKEN = TEST_B0T_TOKEN



keyboards = {
    'play': {
        "keyboard": [
            ["/play"]
        ],
        "resize_keyboard": True,
        "selective":True
    },
    'choose_suit':{
        "keyboard":[
            ["♥","♠"],
            ["♣","♦"]
        ],
        "resize_keyboard":True,
        "selective":True
    }
}

conversation_states = {
    'lobby': 0,
    'play': 1,
    'choose_suit': 2
}

messages = {
    'group_opened_wrong':"""The group for this game was not created correctly. 🤔 
    To play a game, create a new group with only you and me. Then add all other players and press play.""",
    'welcome':"""
    I am the crazy8s bot😜. 
    Ready for a game of crazy eights?
    To begin add 1-4 players to the group then press play.
    Players that are already in the group can also type /join. 
    """,
    'rules': f"Here are the rules:\n- Cards you play must match the color or number of the card on the deck\n- The 8s "
             f"are crazy!:Play it at anytime and define a new color. The next player must play an 8 or a card of the "
             f"same color\n- You must make a move at every turn\n- If cou cannot play a card on your turn you must "
             f"draw one\n- If there is no card on the deck\n- If the deck is empty and you can't play you are passed",

    'rules_long': """Crazy 8s:
    General:
    - Goal: get more then 100 points
    - Players: 2-5
    - The player to get rid of all their cards first, wins the round

    Card values:
    - 8 = 50 points
    - K, Q, J or 10 = 10 points
    - Ace = 1 point
    - All other: points = Card number

    Start:
    - Everyone gets 5 cards
    - The one to joins first, begins
    - Play in the order of joining the game
    - The first card is never an 8

    Play:
    - Every card (other than eight) you play must match the suit or denomination of the card on the deck
    - The eights are crazy! Play it at anytime and define a new suit. The next player must play an eight or a card of matching suit
    - You must make a move at every turn
    - If you can't play a card at your turn, you must draw one
    - If there is no card on the deck
    - If the deck is empty and you can't play you are passed
    """,
    'game_begin': """Alrighty, let's play a game of crazy 8s! 😁\n""",
    'commands': "/play: start a new game\n/rules: short version of the game rules\n/ruleslong: long version of the "
                "game rules\n/score: current score\n/newgame: start a new game\n/endgame: ends the game for all (admin only)\n/stack: card on top "
                "of the card stack\n/join: join game before pressing play\n/help: list of available commands\n/hand: gives you your current hand keyboard",
    'wrong_turn': "I'm sorry but it's not your turn 😕"
}
