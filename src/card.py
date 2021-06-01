# %%
import logging as lg
import constants

lg.basicConfig(level=lg.DEBUG)


class Card:
    """A card in the standard deck of crazy8, poker and so forth."""

    def __init__(self, representation):
        """Can be initialized with a representation as string or int:
        
        int: The numbers represent cards in a sorted deck. This deck is sorted by rank first, and suit second.

        So for example: ♠A♥A♣A♦A♠2♥2♣2♦2♠3♥3♣3 ♦3 ♠4 ♥4...
                        0 1 2 3 4 5 6 7 8 9 10 11 12 13...
        
        string: something like "♥J","♣K","♥2"""
        if type(representation) == int:
            self.int_representation = representation

        elif type(representation) == str:
            # splitting string representation like "♣10" in suit ("♣") and rank ("10")
            suit_str, rank_str = representation[0], representation[1:]
            lg.debug(f"Processing card with suit_str={suit_str} and rank_str={rank_str}")

            # turning suit ("♣") into an integer
            suit_int = constants.suits.find(suit_str)
            if suit_int == -1:
                raise ValueError("Card string must start with one of [♠♥♣♦]")
                return
            
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
                    raise ValueError(("Invalid rank"))

            self.int_representation = (rank_int - 1) * 4 + suit_int

        else:
            raise ValueError("Value must be str or int")

        # check for ValueErrors
        if not 0 <= self.int_representation < 52: # TODO: this can go up
            raise ValueError("Invalid card name")

    def __str__(self):
        """string representation of card. See constructor."""
        suit = self.suit # TODO: in property umwandeln!
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

    def __int__(self):
        """int representation of card. See constructor."""
        return self.int_representation

    def __eq__(self, other):
        return self.int_representation == other.int_representation

    def __hash__(self):
        return self.int_representation
    
    @property
    def suit(self):
        """Return rank of card as a string. These ranks are defined in constants.rank"""
        return constants.suits[self.int_representation % 4]

    @property
    def rank(self):
        """Return rank of card as integer. A will be 1, J 11, K 12, Q 13."""
        return int((self.int_representation - self.int_representation % 4) / 4 + 1)
        # return int((self.value - self.value % 4) / 4 + 2)
    def get_score(self):
        """Output: Crazy8s score value for this card"""
        rank = self.rank

        if rank == 8:
            return 50

        elif rank > 10:
            return 10

        else:
            return rank