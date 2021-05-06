# %%
import random
import logging as lg
from card import Card
from constants import MoveOutcome

lg.basicConfig(level=lg.DEBUG)

class Game:
    """Manages game states, player hands and so forth.

    Input for constructor (multiple strings): user_ids (int) for each player
    
    A player is any unique integer. A good way to realize it would be the telegram user_id.
    
    A hand is a set of cards."""

    def __init__(self, *players):
        """Initialize the game but don't start it yet.

        Input:
        players (iterable of int): unique id's for each player"""
        self.scores = dict([(player, 0) for player in players])
        self.players = players
        self.round_over = True
        
    
    def new_round(self):
        """Start a new round. That means resetting deck and stack and dealing cards to all players."""
        self.hands = {}
        self.deck = [Card(value) for value in range(52)] # TODO: generalize this to new_round
        random.shuffle(self.deck)
        self.stack = [self.deck.pop()]
        self.round_over = False

        # 8 cant be the first card on stack
        while self.top_of_stack.rank == 8:
            old_top = self.top_of_stack
            self.stack.remove(old_top)
            self.deck.insert(len(self.deck/2), old_top) # TODO: This could be more random
            self.stack.append(self.deck.pop())

        lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

        for player in self.players:
            hand = set()

            for i in range(5):
                card = self.deck.pop()
                hand.add(card)

            self.hands[player] = hand

            lg.debug(f"dealt {[str(card) for card in hand]} to {player}")

    @property
    def leading_player(self):
        """Returns id of player with the highest score in the game"""
        max_score = 0
        _leading_player = None

        for player, score in self.scores.items():
            if score > max_score:
                max_score = score
                _leading_player = player

        return _leading_player


    def move(self, player, card):
        """Attempts to play one card on the stack.

        Input:
        player (int): unique id for player
        card (Card): card to be played"""
        if self.round_over:
            raise Exception("Invalid move. New round hasn't started yet.") # TODO: This could also be another MoveOutcome

        hand = self.hands[player]
        
        # check if card can be played
        if card in hand and valid_move(card, self.top_of_stack):
            # play move
            hand.remove(card)

            lg.debug(f"player {player} played {str(card)} on top of {self.top_of_stack} and now has {[str(card) for card in hand]}")

            self.stack.append(card)

            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            # check if move wins the round
            if len(self.hands[player]) == 0:
                # calculate and add score for winning player
                hand_score_sum = sum([self.get_hand_score(player) for player in self.players])
                self.scores[player] += hand_score_sum
                self.round_over = True

                lg.debug(f"That wins the round for player {player} with {hand_score_sum} points. Player {player} now has {self.scores[player]} in total. The other players scores are: {self.scores}")

                # check if move also wins the game
                if self.scores[self.leading_player] >= 100:
                    lg.debug(f"And it wins the game for player {player} with {self.scores[player]} points.")

                    return MoveOutcome.game_won
                else:
                    return MoveOutcome.round_won

            # nothing is won, just a normal valid move
            else:
                return MoveOutcome.valid_move
        
        else:
            # invalid move
            lg.debug(f"player {player} tried to play the invalid move {str(card)} on top of {self.top_of_stack} and now has {[str(card) for card in hand]}")
            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            return MoveOutcome.invalid_move

    def get_hand(self, player):
        return self.hands[player]

    def get_hand_score(self, player):
        return sum([card.get_score() for card in self.hands[player]])

    @property
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
            cards_by_suit[card.suit] = cards_by_suit[card.suit] + str(card)[1:] # TODO: hier vtll `+ " "`?

        keyboard = {
            "keyboard" : [
                ["DRAW ↑"],
                ["♠" + cards_by_suit["♠"],"♥" + cards_by_suit["♥"],"DECK"],
                ["♣" + cards_by_suit["♣"], "♦" + cards_by_suit["♦"], "MENU"]
            ],
            "resize_keyboard" : True
        }

        return keyboard

    def can_move(self, player):
        can_move = False

        for card in self.hands[player]:
            if valid_move(card, self.top_of_stack):
                lg.debug(f"player {player} can move {str(card)}")
                can_move = True

        return can_move

        # does all of the above in one line but is way less readable... :D
        # return max([valid_move(card, self.top_of_stack) for card in self.hands[1]])

def valid_move(card_played, card_on_stack):
    crazy8 = card_played.rank == 8
    rank_fits = card_played.rank == card_on_stack.rank
    suit_fits = card_played.suit == card_on_stack.suit

    return crazy8 or rank_fits or suit_fits
