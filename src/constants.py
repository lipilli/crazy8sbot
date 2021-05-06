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

menu_keyboard = {
    "keyboard": [
          # TODO Groupadmin can't leave the game
        ["rules", "ruleslong", "score"],
        ["endgame", "help", "deck"]
    ],
    "resize_keyboard": True
}

states = {
    """Stores all the states the conversation can be in"""
    'menu': 0,
    'play_cards' : 1, ##
    'deck_heats' : 2,
    'Deck_diamonds' : 3,
    'deco_clubs' : 4,  # ♣
    'deck_spades' : 5  # ♠
}



messages = {
    'rules' : """Here are the rules: 
     - Every card (other than eight) you play must match the suit or denomination of the card on the deck 
     - The eights are crazy! Play it at anytime and define a new suit. The next player must play an eight or a card of matching suit
     - If you can't play, draw cards until you can play
     - If there is no card on the deck
     - If the deck is empty and you can't play you are passed""" ,
    'rules_long' : """Crazy 8s:
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
    'start' : """The 8s are loose 😲😲😲!
        Get ready for a game of crazy 8s!
        Before you begin here are the commands you can use during the game:\n""",
    'commands' : """ /join: join a game
        /leave: leave the game
        /play: start a new game
        /rules: short version of the game rules
        /ruleslong: long version of the game rules
        /score: current score
        /endgame: ends the game for all (admin only)
        /killbot: ends the bot and the game
        /help: list of available commands"""
 }
