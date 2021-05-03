# %%
import random
import logging as lg
from card import Card

lg.basicConfig(level=lg.DEBUG)

# %%
class Game:
    """Manages game states, player hands and so forth.

    Input for constructor (multiple strings): user_ids (int) for each player
    
    A player is any unique integer. A good way to realize it would be the telegram user_id.
    
    A hand is a set of cards."""

    def __init__(self, *players):
        self.hands = {}
        self.deck = [Card(value) for value in range(52)]
        random.shuffle(self.deck)
        self.stack = [self.deck.pop()]

        for player in players:
            hand = set()

            for i in range(5):
                card = self.deck.pop()
                hand.add(card)

            self.hands[player] = hand

            lg.debug(f"dealt {[str(card) for card in hand]} to {player}")
        
    def play_move(self, player, card):
        hand = self.hands[player]
        if card in hand and valid_move(card, self.top_of_stack()):
            hand.remove(card)
            self.stack.append(card)

            lg.debug(f"player {player} played {str(card)} on top of {self.top_of_stack()} and now has {[str(card) for card in hand]}")

            return True
        else:
            lg.debug(f"player {player} tried to play the invalid move {str(card)} on top of {self.top_of_stack()} and now has {[str(card) for card in hand]}")

            return False

    def get_hand(self, player):
        return self.hands[player]

    def get_score(self, player):
        return 21

    def top_of_stack(self):
        return self.stack[-1]
    
    def draw(self, player):
        hand = self.hands[player]
        if len(self.deck) > 0:
            card = self.deck.pop()
            hand.add(card)

            lg.debug(f"player {player} drew {str(card)} and now has {[str(card) for card in hand]}")

            return True
        else:
            return False

def valid_move(card_played, card_on_stack):
    return card_played.get_rank() == 8 or card_played.get_rank() == card_on_stack.get_rank() or card_played.get_suit() == card_on_stack.get_suit()
# %%


# %%
