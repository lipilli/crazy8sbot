# %%
class Card:
    """A card in the standard deck of crazy8, poker and so forth."""

    suits = "♠♥♣♦"

    def __init__(self, value):
        """The values represent cards in a sorted deck. This deck is sorted by rank first, and suit second.

        So for example: ♠1♥1♣1♦1♠2♥2♣2♦2♠3♥3..."""
        self.value = value

    def get_text(self):
        suit = self.suits[self.value % 4]
        rank = int((self.value - self.value % 4) / 4 + 2)

        if rank == 11:
            rank = "J"
        elif rank == 12:
            rank = "Q"
        elif rank == 13:
            rank = "K"
        elif rank == 14:
            rank = "A"

        return f"{suit}{rank}"

# %%
