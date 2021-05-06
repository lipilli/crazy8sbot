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
        self.rounds = []
        self.stack = [self.deck.pop()]

        # 8 cant be the first card on stack
        while self.top_of_stack().get_rank() == 8:
            self.stack.append(self.deck.pop())

        lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

        for player in players:
            hand = set()

            for i in range(5):
                card = self.deck.pop()
                hand.add(card)

            self.hands[player] = hand

            lg.debug(f"dealt {[str(card) for card in hand]} to {player}")
    
    def new_round(self):
        return

    def play_move(self, player, card):
        hand = self.hands[player]
        if card in hand and valid_move(card, self.top_of_stack()):
            hand.remove(card)

            lg.debug(f"player {player} played {str(card)} on top of {self.top_of_stack()} and now has {[str(card) for card in hand]}")

            self.stack.append(card)

            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            return True
        else:
            lg.debug(f"player {player} tried to play the invalid move {str(card)} on top of {self.top_of_stack()} and now has {[str(card) for card in hand]}")
            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            return False

    def get_hand(self, player):
        return self.hands[player]

    def get_hand_score(self, player):
        return sum([card.get_score() for card in self.hands[player]])

    def top_of_stack(self):
        return self.stack[-1]
    
    def draw(self, player):
        hand = self.hands[player]
        if len(self.deck) > 0:
            card = self.deck.pop()
            hand.add(card)

            lg.debug(f"player {player} drew {str(card)} and now has {[str(card) for card in hand]}")
            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            return True
        else:
            lg.debug(f"player {player} tried to draw but the deck was empty")
            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")
            return False

    def get_keyboard(self, player):
        cards_by_suit = {"♠":"", "♥":"", "♣":"", "♦":""}

        for card in self.hands[player]:
            cards_by_suit[card.get_suit()] = cards_by_suit[card.get_suit()] + str(card)[1:] # TODO: hier vtll `+ " "`?

        keyboard = {
            "keyboard" : [
                ["DRAW ↑"],
                ["♠" + cards_by_suit["♠"],"♥" + cards_by_suit["♥"],"DECK"],
                ["♣" + cards_by_suit["♣"], "♦" + cards_by_suit["♦"], "MENU"]
            ],
            "resize_keyboard" : True
        }

        return keyboard

            

def valid_move(card_played, card_on_stack):
    crazy8 = card_played.get_rank() == 8
    rank_fits = card_played.get_rank() == card_on_stack.get_rank()
    suit_fits = card_played.get_suit() == card_on_stack.get_suit()

    return crazy8 or rank_fits or suit_fits
# %%


# %%
