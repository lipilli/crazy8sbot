import random
import logging as lg
from card import Card

lg.basicConfig(level=lg.DEBUG)


class Game:
    """Manages game states, player hands and so forth.

    Input for constructor (multiple strings): user_ids (int) for each player
    
    A player is any unique integer. A good way to realize it would be the telegram user_id.
    
    A hand is a set of cards."""

    def __init__(self, players: list):
        self.hands = {}
        self.deck = [Card(value) for value in range(52)]
        random.shuffle(self.deck)

        for player in players:
            hand = set()

            for i in range(5):
                card = self.deck.pop()
                hand.add(card)

            self.hands[player] = hand

            lg.debug(f"dealt {[str(card) for card in hand]} to {player}")

    def play_move(self, player, card):
        hand = self.hands[player]
        if card in hand:
            hand.remove(card)
            lg.debug(f"{player} played {str(card)}")
            return True
        else:
            return False

    def get_hand(self, player):
        return self.hands[player]

    def get_score(self, player):
        return 21

    def draw(self, player):
        if len(self.deck) > 0:
            card = self.deck.pop()
            self.hands[player].add(card)
            return True
        else:
            return False
