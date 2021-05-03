# %%
import logging as lg

lg.basicConfig(level=lg.DEBUG)
# %%
class Card:
    """A card in the standard deck of crazy8, poker and so forth."""

    suits = "♠♥♣♦"

    def __init__(self, representation):
        """Can be initialized with a representation as string or int:
        
        int: The numbers represent cards in a sorted deck. This deck is sorted by rank first, and suit second.

        So for example: ♠1♥1♣1♦1♠2♥2♣2♦2♠3♥3...
                        0 1 2 3 4 5 6 7 8 9...
        
        string: something like "♥J","♣K","♥2"""
        if type(representation) == int:
            self.int_representation = representation

        elif type(representation) == str:
            # splitting string representation like "♣10" in suit ("♣") and rank ("10")
            suit_str, rank_str = representation[0], representation[1:]
            lg.debug(f"Processing card with suit_str={suit_str} and rank_str={rank_str}")

            # turning suit ("♣") into an integer
            suit_int = Card.suits.find(suit_str)
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
                    rank_int= 11
                elif rank_str == "Q":
                    rank_int= 12
                elif rank_str == "K":
                    rank_int= 13
                elif rank_str == "A":
                    rank_int= 14
                else:
                    raise ValueError(("Invalid rank"))

            self.int_representation = (rank_int - 2) * 4 + suit_int

        else:
            raise ValueError("Value must be str or int")

        # check for ValueErrors
        if not 0 <= self.int_representation < 52:
            raise ValueError("Invalid card name")

    def __str__(self):
        suit = self.get_suit()
        rank = self.get_rank()

        if rank == 11:
            rank = "J"
        elif rank == 12:
            rank = "Q"
        elif rank == 13:
            rank = "K"
        elif rank == 14:
            rank = "A"

        return f"{suit}{rank}"

    def __int__(self):
        return self.int_representation
    
    def get_suit(self):
        return self.suits[self.int_representation % 4]

    def get_rank(self):
        return int((self.int_representation - self.int_representation % 4) / 4 + 2)

# TODO: more exeptions
# %%
