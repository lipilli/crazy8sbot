import random
import logging as lg
from card import Card
from constants import MoveOutcome
from constants import suits

lg.basicConfig(level=lg.DEBUG)

class Game:
    """Manages game states, player hands and so forth.

    Input for constructor (multiple strings): user_ids (int) for each player
    
    A player is any unique integer. A good way to realize it would be the telegram user_id.
    
    A hand is a set of cards."""

    def __init__(self,players:list):
        """Initialize the game but don't start it yet.

        Input:
        players (iterable of int): unique id's for each player"""
        self.last_eights_suit = ''
        self.scores = dict([(player, 0) for player in players])
        self.players = players
        self.round_over = True
        # TODO get a table with the players names and scores: https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png
    
    def new_round(self):
        """Start a new round. That means resetting deck and stack and dealing cards to all players."""
        self.hands = {}
        self.deck = [Card(value) for value in range(52)] # TODO: generalize this to new_round
        random.seed()
        random.shuffle(self.deck)
        self.stack = [self.deck.pop()]
        self.round_over = False

        # 8 cant be the first card on stack
        while self.top_of_stack.rank == 8:
            old_top = self.top_of_stack
            self.stack.remove(old_top)
            # lg.debug(f"self.deck: {[str(card) for card in self.deck]}")
            # lg.debug(f"type of length of deck: {type(len(self.deck))}")
            # lg.debug(f"length of deck: {len(self.deck)}")
            random.seed()
            self.deck.insert(random.randint(0,len(self.deck)-1), old_top)
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
        if player == 000 and card == 000:
            return MoveOutcome.crazy8

        if self.round_over:
            raise Exception("Invalid move. New round hasn't started yet.") # TODO: This could also be another MoveOutcome

        hand = self.hands[player]
        
        # check if card can be played
        if card in hand and self.valid_move(card, self.top_of_stack):
            # reset choice if last card was an 8
            if self.top_of_stack.rank == 8:
                self.last_eights_suit = ""
            
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
            
            # check if an 8 is played, earning the privilege to choose a suit
            elif card.rank == 8:
                return MoveOutcome.crazy8

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
        """Attempts to draw one card into the specified players hand."""
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


    def can_move(self, player):
        """Returns true if there is a valid move for the specified player."""
        can_move = False

        for card in self.hands[player]:
            if self.valid_move(card, self.top_of_stack):
                lg.debug(f"player {player} can move {str(card)}")
                can_move = True

        return can_move

        # does all of the above in one line but is way less readable... :D
        # return max([valid_move(card, self.top_of_stack) for card in self.hands[1]])

    def choose_suit(self, suit: str):  # TODO choose suit function
        if suit in suits:
            self.last_eights_suit = suit
            lg.debug(f"{suit} was chosen as a new suit.")
        else:
            raise ValueError("Invalid suit")


    def valid_move(self, card_played, card_on_stack):
        """Returns true if it would be a valid move to play card_played on top of card_on_stack"""

        played_8 = card_played.rank == 8
        rank_fits = card_played.rank == card_on_stack.rank
        suit_fits = card_played.suit == card_on_stack.suit
        valid_card_on_top_of_8 = card_played.suit == self.last_eights_suit

        # irgnoring suit of top of stack if it is an 8
        if self.top_of_stack.rank == 8:
            return played_8 or valid_card_on_top_of_8
        else:
            return played_8 or rank_fits or suit_fits


