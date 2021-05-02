
class Keyboards():
    menu_keyboard = {
        "keyboard": [
            ["join", "leave", "play"],  # TODO Groupadmin can't leave the game
            ["rules", "ruleslong", "score"],
            ["endgame", "killbot", "help"]
        ],
        "resize_keyboard": True
    }

    def play_card_keyboard(player):
        pass

    def deck_keyboard(player, suit):
        pass


class States():
    """Stores all the states the conversation can be in"""
    MENU = 0
    PLAY_CARD = 1
    DECK_HEARTS = 2
    DECK_DIAMONDS = 3
    DECK_CLUBS = 4  # ♣
    DECK_SPADES = 5  # ♠


class Messages():
    rules = """Here are the rules: 
     - Every card (other than eight) you play must match the suit or denomination of the card on the deck 
     - The eights are crazy! Play it at anytime and define a new suit. The next player must play an eight or a card of matching suit
     - If you can't play, draw cards until you can play
     - If there is no card on the deck
     - If the deck is empty and you can't play you are passed"""
    rules_long = """Crazy 8s:
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
    """
    start = """The 8s are loose 😲😲😲!
        Get ready for a game of crazy 8s!
        Before you begin here are the commands you can use during the game:\n""",
    commands = """ /join: join a game
        /leave: leave the game
        /play: start a new game
        /rules: short version of the game rules
        /ruleslong: long version of the game rules
        /score: current score
        /endgame: ends the game for all (admin only)
        /killbot: ends the bot and the game
        /help: list of available commands"""


'''
Creates Keyboards on the fly
has a function that takes all the cards of the player in the deck and
adds them to the keyboard

Keboard laouts:

play_card_keyboard = {
    "keyboard" : [
        ["DRAW ↑"],
        ["♣7594K","♠45684","DECK"],
        ["♥48648", "♦84684", "MENU"]
    ],
    "resize_keyboard" : True
}



decck_keyboard = {
    "keyboard" : [
    [1,2,3,4,5]
    ]
}



'''




