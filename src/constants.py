from enum import Enum

"""Contains all constants"""

# Game constants

MoveOutcome = Enum(
    "MoveOutcome", 
    "valid_move round_won game_won invalid_move")

# suits = "♠♥♣♦" 
suits = "shcd" # used for debugging. switch with line on top for release

# Bot constants

BOT_TOKEN = "1665894053:AAHxd8VUNhV1Q8ncLrF9IvljRPcGG9zfH60"
TESTB0T_TOKEN1 = "1796005782:AAH50veupoTsA4KbrKv9A7ZndiO0CCewa9g"
TESTBOT_TOKEN2 = "1792398859:AAGoeCc9y2GX3MsUaHPRd0f2I9_lLxTUFgA"

keyboards = {
    'menu': {
        "keyboard": [
            # TODO: game master: can get rules, score, end the game, request help
            # TODO: you should be able to leave the game by exiting the group
            ["rules", "ruleslong", "score"],
            ["endgame", "help", "deck"]
        ],
        "resize_keyboard": True
    },
    # 'join': {
    #     "keyboard": [
    #         ["/join"]
    #     ],
    #     "resize_keyboard": True
    # },
    # 'leave': {
    #     "keyboard": [
    #         ["/leave"]
    #     ],
    #     "resize_keyboard": True
    # },
    'play': {
        "keyboard": [
            ["/play"]
        ],
        "resize_keyboard": True
    }
}

conversation_states = {
    'lobby': 0,
    'deck_page1': 1,
    'deck_page2': 2,
    'deck_page3': 3,
    'deck_page4': 4,
    'menu': 5
}

messages = {
    'welcome':"""
    Hi! I am the crazy8s bot😜. 
    Ready for a game of crazy eights?\n
    To begin you must promote me to admin. Then add 1-4 players to the group in one batch.
    """,
    'rules': """Here are the rules: 
     - Cards you play must match the color or number of the card on the deck
     
     - The 8s are crazy! 
     Play it at anytime and define a new color. 
     The next player must play an 8 or a card of the same color
     
     - If you can't play, draw cards until you can play
     
     - If there is no card on the deck
     
     - If the deck is empty and you can't play you are passed""",

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
    - If you can't play, draw cards until you can play
    - If there is no card on the deck
    - If the deck is empty and you can't play you are passed
    """,
    'start': """The 8s are loose 😲😲😲!
        Get ready for a game of crazy 8s!
        Before you begin here are the commands you can use during the game:\n""",
    'commands': """ /join: join a game
        /leave: leave the game
        /play: start a new game
        /rules: short version of the game rules
        /ruleslong: long version of the game rules
        /score: current score
        /endgame: ends the game for all (admin only)
        /killbot: ends the bot and the game
        /help: list of available commands"""
}
