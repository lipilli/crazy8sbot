"""Crazy8s Card
Card class used for playing crazy eights in Telegram chat.
    param:
        Author: Deborah Djon
        Date: 06.06.2021
        Version:0.1
        license: free
"""
from __future__ import annotations
import logging as lg
from constants import suits

# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)


class Card:
    """ Card.

    Card equivalent to card in standard card deck with 52 cards.
    Cards have a string representation, which is a combination of their
    rank, being one of [♠♥♣♦], and a rank so a number between 2-13 or J,Q,K or A.

    example: ♠A

    test:
        - card.rank != None
        - card.suit != None
    """

    def __init__(self, representation: str or int):
        """ Initializes a Card.

        Initializes a Card.
        A Card can be initialized with a string or int but is finally stored as an int:
            int: The numbers represent cards in a sorted deck. This deck is sorted by rank first, and suit second.
            So for example: ♠A♥A♣A♦A♠2♥2♣2♦2♠3♥3♣3 ♦3 ♠4 ♥4...
                            0 1 2 3 4 5 6 7 8 9 10 11 12 13...

        param:
            representation(str): String representation of a card

        example: string representation look something like "♥J","♣K","♥2"

        test:
            - self.int_representation != None
            - self.int_representation > -1
        """
        if type(representation) == int:
            self.int_representation = representation

        elif type(representation) == str:
            # splitting string representation like "♣10" in suit ("♣") and rank ("10")
            suit_str, rank_str = representation[0], representation[1:]
            lg.debug(f"Processing card with suit_str={suit_str} and rank_str={rank_str}")

            # turning suit ("♣") into an integer
            suit_int = suits.find(suit_str)
            if suit_int == -1:
                raise ValueError("Card string must start with one of [♠♥♣♦]")

            # turning rank ("10") into an integer
            try:
                rank_int = int(rank_str)
                if not 2 <= rank_int <= 10:
                    raise ValueError("Invalid rank")

            except ValueError:
                if rank_str == "J":
                    rank_int = 11
                elif rank_str == "Q":
                    rank_int = 12
                elif rank_str == "K":
                    rank_int = 13
                elif rank_str == "A":
                    rank_int = 1
                else:
                    raise ValueError("Invalid rank")

            self.int_representation = (rank_int - 1) * 4 + suit_int

        else:
            raise ValueError("Value must be str or int")

        # check for ValueErrors
        if not 0 <= self.int_representation < 52:
            raise ValueError("Invalid card name")

    def __str__(self) -> str:
        """Get the string representation of a card.

        Get the string representation of a card.

        test:
            - return type == str
            - len(return) == 2
            - return[0] in constants.suits
        """
        suit = self.suit
        rank = self.rank

        if rank == 11:
            rank = "J"
        elif rank == 12:
            rank = "Q"
        elif rank == 13:
            rank = "K"
        elif rank == 1:
            rank = "A"

        return f"{suit}{rank}"

    def __int__(self) -> int:
        """Get the int representation of a card.

        Get the int representation of a card.

        test:
            - return type == int
            - return < 53
            - return > -1
        """
        return self.int_representation

    def __hash__(self) -> int:
        """Get the has of a card.

        Get the hash of a card. Needed to handle cards in a set.

        test:
            - return type == int
            - return < 53
            - return > -1
        """
        return self.int_representation

    def __eq__(self, other: 'Card') -> bool:
        """ Compare this card to another card.

        Compare this card to another card.
        Here the function was only used for testing purpose but might be of use for future developers.

        param:
            other(Card): Card to compare current card with

        test:
            - type( self.int_representation) == type(other.int_representation) == int
            - self.int_representation != None & other.int_representation != None
            - other != None

        source: https://stackoverflow.com/questions/42845972/typed-python-using-the-classes-own-type-inside-class-definition
        """
        return self.int_representation == other.int_representation

    def __lt__(self, other: 'Card') -> bool:
        """ Less than implementation.

        Implementation of the less than function. Used for sorting cards with sorted([card1, card2, card3])
        param:
            other(Card): Card to compare current card with

        test:
            - type( self.int_representation) == type(other.int_representation) == int
            - self.int_representation != None & other.int_representation != None
            - other != None
        source: https://stackoverflow.com/questions/42845972/typed-python-using-the-classes-own-type-inside-class-definition
        """
        return int(self) < int(other)

    @property
    def suit(self) -> str:
        """ Get suit of a Card.

        Get suit of a card. The suits are defined in constants.suits.

        test:
            - type(self.int_representation) == int
            - self.int_representation != None
            - type(return) == str
        """
        return suits[self.int_representation % 4]

    @property
    def rank(self) -> int:
        """Get the rank of a Card.

        Get the rank of a Card as int. A will be 1, J 11, K 12, Q 13.

        test:
            - type(self.int_representation) == int
            - self.int_representation != None
            - type(return) == str
        """
        return int((self.int_representation - self.int_representation % 4) / 4 + 1)


    def get_score(self):
        """Get the value of a card.

        Get the value of a card.

        test:
            - type(return) == int
            - return < 53
        """
        rank = self.rank

        if rank == 8:
            return 50

        elif rank > 10:
            return 10

        else:
            return rank
