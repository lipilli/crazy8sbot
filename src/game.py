"""Crazy8s Game
Game class used for playing crazy eights in Telegram chat.
    param:
        Author: Deborah Djon
        Date: 06.06.2021
        Version:0.1
        license: free
"""

from random import seed, shuffle, randint
import logging as lg
from card import Card
from constants import MoveOutcome
from constants import suits

# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)


class Game:
    """Manages game states, player hands and so forth.

        Class that manages the logic of a game. This includes the states, players and their hands and so fourth.
        It can be compared to a physical board game. It has all elements needed for playing but requires action
        from external forces to actually be played.

        test:
            - len(self.players) > 0
            - len([i for i in cls.__dict__.keys() if i[:1] != '_']) = 8 (source: https://stackoverflow.com/questions/9058305/getting-attributes-of-a-class)
    """

    def __init__(self, players: list):
        """Initialize Game.

            Initializes Game without starting it.
            params:
                players (list): user_ids (int) for each player (a player is any unique integer corresponding to the telegram user_id)
            test:
                -type(self.round) = int
                -self.hands != None
                -self.last_eights_suit != None
        """

        self.hands = {}
        self.last_eights_suit = ''
        self.scores = dict([(player, 0) for player in players])
        self.players = players
        self.round_over = True
        self.round = 0
        self.deck = []
        self.stack = []

    def reset_round(self):
        """Resets round.
            Decrements the round. Used when new_round was not successful.

            test:
                - type(round) == int
                - round > 0
        """
        if self.round > 1:
            self.round -= 1

    def new_round(self):
        """Starts a new round.

            Resets deck and stack and deals cards to all players.
            These cards are a set of cards stored in the players hand.
            It makes sure that there is no eight on top of the deck.

            test:
                - round > 1
                - type(round) == int
                - round before < round after
        """

        self.deck = [Card(value) for value in range(52)]
        seed()
        shuffle(self.deck)
        self.stack = [self.deck.pop()]
        self.round_over = False
        self.round += 1

        # 8 cant be the first card on stack
        while self.top_of_stack.rank == 8:
            lg.debug("An 8 was on top of initial deck")
            old_top = self.top_of_stack
            self.stack.remove(old_top)
            seed()
            self.deck.insert(randint(0, len(self.deck) - 1), old_top)
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
    def leading_player(self) -> int:
        """ Returns leading player.

        Returns player that is leading at the moment (player with most points)

        test:
            - type(leading_player) == int
            - max_score < 0
        """
        """Returns id of player with the highest score in the game"""
        max_score = 0
        _leading_player = None

        for player, score in self.scores.items():
            if score > max_score:
                max_score = score
                _leading_player = player

        return _leading_player

    def move(self, player: int, card: Card) -> MoveOutcome:
        """Attempts to put a card a player provided to the stack.

        Attempts to put a card that a player provided to the card stack. This card might not be part of his hand,
        or not playable with the current card on the stack. The function returns the according Move.Outcome

        param:
            player (int): unique id for player
            card (Card): card to be played

        test:
            - type(card)
            - len(player's hand) > 0
        """

        if self.round_over:
            raise Exception(
                "Invalid move. New round hasn't started yet.")

        hand = self.hands[player]

        # check if card can be played
        if card in hand and self.valid_move(card, self.top_of_stack):
            # reset choice if last card was an 8
            if self.top_of_stack.rank == 8:
                self.last_eights_suit = ""

            # play move
            hand.remove(card)

            lg.debug(
                f"player {player} played {str(card)} on top of {self.top_of_stack} and now has {[str(card) for card in hand]}")

            self.stack.append(card)

            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            # check if move wins the round
            if len(self.hands[player]) == 0:
                # calculate and add score for winning player
                hand_score_sum = sum([self.get_hand_score(player) for player in self.players])
                self.scores[player] += hand_score_sum
                self.round_over = True

                lg.debug(
                    f"That wins the round for player {player} with {hand_score_sum} points. Player {player} now has {self.scores[player]} in total. The other players scores are: {self.scores}")

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
            lg.debug(
                f"player {player} tried to play the invalid move {str(card)} on top of {self.top_of_stack} and now has {[str(card) for card in hand]}")
            lg.debug(f"the stack is:{[str(card) for card in self.stack]}")

            return MoveOutcome.invalid_move

    def get_hand(self, player: int) -> set:
        """Returns players hand

        Returns the hand of a player

        param:
            placer(int): user_id of player

        test:
            - hand != Null
            - player in self.players
        """
        return self.hands[player]

    def get_hand_score(self, player: int):
        return sum([card.get_score() for card in self.hands[player]])

    @property
    def top_of_stack(self) -> Card:
        """Returns card on top of the stack

        Returns card on top of the card stack.

        test:
            - len(self.stack) > 0
            - self.stack != None
        """
        return self.stack[-1]

    def draw(self, player: int) -> bool:
        """ Attempts drawing a card into the hand of the specified player

        Attempts to draw a card from the deck and put it in the hand of the specified player.

        param:
            player(int): user_id of player

        test:
            - len(self.hands[player]) > 0
            - return type == bool
        """

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

    def can_move(self, player: int) -> bool:
        """Determines if a player can make a valid move

            Determines if the  specified player can make a valid move.
            This is done by checking if any of the cards in the hand of the player would make a valid move.

            param:
                player(int): user_id of player

            test:
                - len(self.hands[player]) > 0
                - max([type(card)==Card for card in self.hands[player]]) == 1
        """
        can_move = False

        for card in self.hands[player]:
            if self.valid_move(card, self.top_of_stack):
                lg.debug(f"player {player} can move {str(card)}")
                can_move = True

        return can_move

        # does all of the above in one line but is way less readable... :D
        # return max([valid_move(card, self.top_of_stack) for card in self.hands[1]])

    def choose_suit(self, suit: str):
        """Choose the suit of the last eight played.

        Is used when an eight is played. Can be used to set it's suit.

        param:
            suit(str): chosen suit

        test:
            - type(suit) == str
            - self.last_eights_suit != None
        """
        if suit in suits:
            self.last_eights_suit = suit
            lg.debug(f"{suit} was chosen as a new suit.")
        else:
            raise ValueError("Invalid suit")

    def valid_move(self, card_played: Card, card_on_stack: Card) -> bool:
        """Determines if a move is valid.

        Determines if a move is valid.
        Returns True if it would be a valid move to play card_played on top of card_on_stack
            param:
                card_played(Card): card played by player
                card_on_stack(Card): card on top of the card stack

            test:
                - type(card_played) == type(card_played) == Card
                - self.top_of_stack != None
        """

        played_8 = card_played.rank == 8
        rank_fits = card_played.rank == card_on_stack.rank
        suit_fits = card_played.suit == card_on_stack.suit
        valid_card_on_top_of_8 = card_played.suit == self.last_eights_suit

        # ignoring suit of top of stack if it is an 8
        if self.top_of_stack.rank == 8:
            return played_8 or valid_card_on_top_of_8
        else:
            return played_8 or rank_fits or suit_fits
