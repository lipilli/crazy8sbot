# %%
import logging as lg

lg.basicConfig(level=lg.DEBUG)
# %%
class Card:
    """A card in the standard deck of crazy8, poker and so forth."""

    suits = "♠♥♣♦"

    def __init__(self, value):
        """The values represent cards in a sorted deck. This deck is sorted by rank first, and suit second.

        So for example: ♠1♥1♣1♦1♠2♥2♣2♦2♠3♥3..."""
        self.value = value

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
        return self.value
    
    def get_suit(self):
        return self.suits[self.value % 4]

    def get_rank(self):
        return int((self.value - self.value % 4) / 4 + 2)

    def str_to_card(string):
        """Returns the card object that corresponds to a string representation of a card.

        Input (str): string representation of card. 
        Output (Card): card object

        Examples:
        str_to_card("♥J") -> Card(37)
        str_to_card("♣K") -> Card(46)
        str_to_card("♥2") -> Card(1)
        """
        suit_str, rank_str = string[0], string[1:]
        lg.debug(f"Processing card with suit_str={suit_str} and rank_str={rank_str}")

        suit_int = Card.suits.find(suit_str)
        if suit_int == -1:
            raise ValueError("Card string must start with one of [♠♥♣♦]")
            return
        
        try:
            rank_int = int(rank_str)
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

        value = (rank_int - 2) * 4 + suit_int
        return Card(value)

# TODO: more exeptions
# %%
