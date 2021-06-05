"""Crazy8s Bot
Bot for playing crazy eights in Telegram chat.
    param:
        Author: Deborah Djon
        Date: 06.06.2021
        Version:0.1
        license: free
"""
from telegram.error import TimedOut
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, User, ReplyKeyboardRemove
from tabulate import tabulate
from time import sleep
import logging as lg

# custom modules
from constants import messages, conversation_states, keyboards, BOT_TOKEN, MoveOutcome
from card import Card
from game import Game

# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)


# Test: start game throut adding bot and join and through adding ppl to the group


# TODO New rounds don't start, the score is not doing what It should

# -- Helper functions -- #

def hands_log_str(update: Update, context: CallbackContext) -> str:
    """Generate string for logging the hands.
        Crates a string that is used for logging the hands belonging to each player in the game.

        param:
            update (telegram.Update): represents incoming update.
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more.

        test:
            - check that return type is string
            - check number of players is >= "[" → mark beginning of hand
        """
    players = context.chat_data['players']
    my_game = context.chat_data['game']
    hands_log = "Hands:\n"
    for player in players:
        hand = str(player) \
               + "(" + get_users_name_from_id(update, context, player) + ")" \
               + ':' + str([str(card) for card in my_game.get_hand(player)]) + "\n"
        hands_log = hands_log + hand
    return hands_log


def get_user_from_id(update: Update, context: CallbackContext, user_id: int) -> User:
    """Get the user from id.
        Crates a string that is used for logging the hands belonging to each player in the game.

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions.
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more.
            user_id (int): id of user that is searched.
        test:
            - check that return type is User
            - check it is the right user: compare user.id with user_id
        """
    return context.bot.get_chat_member(update.message.chat.id, int(user_id)).user


def get_username_from_id(update: Update, context: CallbackContext, user_id: int) -> str:
    """Get the username from id.
        Returns a username based on provided user id.

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more
            user_id (int): user for which name is searched

        raises Value Error: is raised when user is missing username

        test:
            - check that return type is string.
            - check username has no illegal characters.
    """
    user = get_user_from_id(update, context, user_id)
    if user.username is None:
        if user.last_name is None:
            name = user.first_name.replace(' ', '_')
        else:
            name = user.first_name.replace(' ', '_') + "_" + user.last_name.replace(' ', '_')

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"@{name}, you seem to not have a username. Please add one to continue playing.")
        raise ValueError(f"{name} has no username", name)
    else:
        return user.username


def get_users_name_from_id(update: Update, context: CallbackContext, user_id: int) -> str:
    """Get the user's name from id.
        Returns a username based on provided user id, if user has no username the full name is provided.

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions.
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more.
            user_id (int): user for which name is searched.
        test:
            - check that return type is string
            - check username/name has no illegal characters
    """

    try:
        return get_username_from_id(update, context, user_id)
    except ValueError as e:
        return e.args[1]


def get_current_players(update: Update, context: CallbackContext) -> set:
    """get list of current players
        returns a set of strings containing the user's name and their id

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more
        test:
            - check that return type is set
            - check length set = length of context.chat_data['players']
    """
    return {str(player) + ':' + get_users_name_from_id(update, context, player)
            for player in context.chat_data['players']}


def tell_who_put_what_on_stack(update: Update, context: CallbackContext):
    """tells chat what card is on the stack
        tells chat what card is on the stack and who laid the card
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - check that message sent by the bot contains a suit
            - check that str(card in top of stack) is in the message sent by the bot
    """
    game = (context.chat_data['game'])
    card_on_stack = str(game.top_of_stack)
    player_that_made_move = list(context.chat_data['players'])[context.chat_data['turn']]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"@{get_username_from_id(update, context, player_that_made_move)} put {card_on_stack} on the stack",
                             reply_markup=make_hand_keyboard(game, player_that_made_move, False))


def leave_chat(update: Update, context: CallbackContext):
    """bot leaves chat
        makes the bot leave the chat
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - check that the bot cannot receive any messages from the chat anymore
            - check that bot cannot send messages to the chat
    """
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id,
                     text="See you next time!👋",
                     reply_markup=ReplyKeyboardRemove(remove_keyboard = True, selective = False))
    end_game(update, context)
    bot.leaveChat(update.effective_chat.id)


def end_game(update: Update, context: CallbackContext):
    """ends the game for a certain chat
        ends the game and deletes all related data for the respective chat
        method is only used directly by the bot when teh game is over
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - chat side: check that no card can be played
            - bot side: check that bot cannot send messages to the chat
            - bot side: check that bot cannot receive messages from the chat
    """
    context.chat_data['players'] = {}
    context.chat_data['game'] = 0
    context.chat_data['turn'] = 0
    leave_chat(update, context)


def user_end_game(update: Update, context: CallbackContext):
    """end the game from user side
        can be used by user to end the game explicitly
        can only be triggered by group admins
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - chat side: check that no card can be played
            - bot side: check that bot cannot send messages to the chat
            - bot side: check that bot cannot receive messages from the chat
    """
    try:
        admins = update.effective_chat.get_administrators()
        admin_ids = [admin.user.id for admin in admins]
        user = update.message.from_user.id
        if user in admin_ids:
            end_game(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="I'm sorry, you must be admin to end the game 😟")
    except TimedOut:
        leave_chat(update, context)

def hand_out_hands(update: Update, context: CallbackContext) -> bool:
    """sends hands keyboards to players
        sends hands keyboards to players in the lobby
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - player_username != None
            - len(players) == len(player_usernames)
            - type(players) == list[int]
            - type(player_username) == list[str]
    """
    players = list(context.chat_data['players'])
    game = context.chat_data['game']
    try:
        player_usernames = [get_username_from_id(update, context, player) for player in players]
    except Exception as e:
        lg.debug(f"Exception in hand_out_hands:{str(e.args)}")
        return False

    for i in range(len(players)):
        hand_keyboard = make_hand_keyboard(game, players[i], False)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Handing out cards to @{player_usernames[i]}", reply_markup=hand_keyboard)
    return True

def tell_round(update: Update, context: CallbackContext):
    """tells chat what round the game is in
        tells chat what round the game is in
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - type(round) == int
            - round > 0
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Round {context.chat_data['game'].round} begins!")


def new_round(update: Update, context: CallbackContext) -> bool:
    """Start new round
        starts a new round in the game, hands out new hands
        if handing out hands is successful returns true

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - round before <= round after
            - round after > 0
            - type(round) == int
            - return type == bool
    """
    game = context.chat_data['game']
    game.new_round()
    hand_out_hands_result = hand_out_hands(update, context)
    lg.debug(f"Hand out hands result: {hand_out_hands_result}")
    if hand_out_hands_result:
        return True
    else:
        game.reset_round()
        return False


def make_hand_keyboard(game: Game, player: int, can_potentially_draw: bool) -> ReplyKeyboardMarkup:  # had page
    """Create hands keyboard.
        Creates keyboard containing cards in the hand of one player.

        param:
            game (Game): game class that is responsible for the game's logic
            player (int): payer that keyboard is requested for
            can_potentially_draw (bool): determine whether a /draw button might be sent or not
        test:
            - check that ReplyMarkup is not empty
            - check number of rows in keybord is > int(len(player.hand)/5)
    """
    sorted_hand = sorted(list(game.get_hand(player))) #TODO: are the cards sorted now?
    hand_str = [str(card) for card in sorted_hand]
    cards_per_row = 5
    # build keyboard rows with 5 cards
    full_row_count = int(len(hand_str) / cards_per_row)
    # Send draw  button only if player it is the players move and he can't move
    if can_potentially_draw:
        if game.can_move(player):
            keyboard_buttons = [['/turn', '/stack']]
        else:
            keyboard_buttons = [['/turn', '/stack', '/draw']]
    else:
        keyboard_buttons = [['/turn', '/stack']]
    card_index = 0
    for j in range(full_row_count):
        keyboard_row = []
        for k in range(cards_per_row):
            keyboard_row.append(hand_str[card_index])
            card_index += 1
        keyboard_buttons.append(keyboard_row)

    # fill the last row row with remaining cards and help button
    last_row = hand_str[full_row_count * 5:]
    last_row.append("/help")
    keyboard_buttons.append(last_row)
    return ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True, selective=True)


def check_turn(update: Update, context: CallbackContext, user_id: int) -> bool:
    """check whose turn it is
        check if the  user that played the card is at turn

       param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more
            user_id (int): user who is potentially at turn
        test:
            - return type == bool
            - type(user_id) == int
    """
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    if players[at_turn] == user_id:
        return True
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=messages['wrong_turn'])
        return False


def next_turn(context: CallbackContext):
    """increment turn
        register next player at turn

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - turn < 5
            - turn < len(players)
    """
    context.chat_data["turn"] = (context.chat_data["turn"] + 1) % len(context.chat_data['players'])


def handle_timeout(update:Update, context:CallbackContext):
    """Function that handles timeout errors.

    Function that handles timeout errors. Ends the game.

    test:
        - context.chat_data['game']==0
        - context.chat_data['players']==[]
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="My bad, had to use the bathroom. Can you say that again!")
    #end_game(update, context)
    lg.debug("Timeout Error")

# -- End: Helper functions -- #


# -- Message handler callback functions --#
def tell_turn(update: Update, context: CallbackContext):
    """notify who's turn it is
       sends message to respective chat saying who'se turn it is

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - check that return type is string
            - check username/name has no illegal characters
    """
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    player_at_turn = get_username_from_id(update, context, players[at_turn])
    game = context.chat_data['game']
    hand_keyboard = make_hand_keyboard(game, players[at_turn], True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="It's your turn @" + player_at_turn,
                             reply_markup=hand_keyboard)


def new_game(update: Update, context: CallbackContext) -> int:
    """initiates new game
        function that initiates new game
        triggered when bot is added to a group chat, the roup can be new or existing
        registers the person that created the chat or added the bot as player
        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more
        test:
            - context.chat_data['turn'] exists
            - context.chat_data['players'] exists
            - context.chat_data['game'] exists
    """
    if update.message.group_chat_created:
        lg.debug("Group was created")
    sender = update.message.from_user.id
    lg.info(f"{get_users_name_from_id(update, context, sender)} created the chat {update.message.chat.title}")
    context.chat_data['players'] = {sender}
    context.chat_data['turn'] = 0
    context.chat_data['game'] = 0
    lg.info(f"Players initialized with {str(context.chat_data['players'])} "
            f"({get_users_name_from_id(update, context, sender)})")
    name = get_users_name_from_id(update, context, sender)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi @{name}!\n" + messages['welcome'],
                             reply_markup=keyboards['play'])
    return conversation_states['lobby']


def join(update: Update, context: CallbackContext) -> int or None:
    """For users wanting to join the game.
        For users wanting to join the game, is needed for registering players when bot was added to existing group.
        the bot does not have access to the users in a group and must keep track of them internally,
            this is done by extracting usernames from updates.

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions.
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more.

        test:
            - len(context.chat_data['players']) before join is 1 less then after
            - type(want2play) == int
    """
    want2play = update.message.from_user.id
    context.chat_data['players'].add(want2play)
    name = get_users_name_from_id(update, context, want2play)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi @{name}!",
                             reply_markup=keyboards['play'])
    lg.info(f"Currently in the lobby:\n {str(get_current_players(update, context))}")
    return conversation_states['lobby']


def bot_was_added_to_group(update: Update, context: CallbackContext) -> int or None:
    """registers that bot was added to an existing group
        registers if bot was added to existing group and if correct initiates a new game

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - return type == <class 'NoneType'> or int
            - len(new_chat_members) > 0
    """
    new_chat_members = [x.id for x in update.message.new_chat_members]
    if context.bot.get_me().id in new_chat_members:
        lg.debug("Bot was added to group")
        new_game(update, context)
        return conversation_states['lobby']
    else:
        return None


def new_player(update: Update, context: CallbackContext) -> int:
    """new player in group
        triggered when new member is in the group, that can be the bot or any other user

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - return type == int
            - if new_player != bot: check len(context.chat_data['players']) increased by 1
    """

    lg.debug("Somebody entered the group")
    want2play = {x.id for x in update.message.new_chat_members}
    lg.info(f"new member(s): {str(want2play)}")
    context.chat_data['players'].update(want2play)
    try:
        context.chat_data['players'].remove(context.bot.get_me().id)
    except KeyError:
        pass

    for player in want2play:
        name = get_users_name_from_id(update, context, player)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Hi @{name}!",
                                 reply_markup=keyboards['play'])
    lg.info(f"Currently in the lobby:\n {str(get_current_players(update, context))}")
    return conversation_states['lobby']


def player_left_in_game(update:Update, context:CallbackContext):
    """Removes player that left during the game.

        Removes player that left during the game. If after there are no more registered players, the bot leaves the chat.

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - if bot left: check that bot cannot send anymore messages to respective chatt
            - len(context.chat_data['players']) decreased by 1
    """
    #
    lg.debug("A player during the game left")
    player_left_in_lobby(update, context)

    if len(context.chat_data['players']) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="There are not enough registered players 😔")
        leave_chat(update, context)


def player_left_in_lobby(update: Update, context: CallbackContext) -> int or None :
    """remove player that left the group
        removes user that left the group from game

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - len(context.chat_data['players']) decreased by 1
            - return type == int
    """
    lg.debug("A player left")
    left = update.message.left_chat_member.id
    try:
        players_before_leaving = get_current_players(update, context)
        context.chat_data['players'].remove(left)
        players_after_leaving = get_current_players(update, context)
        lg.info(f"successfully removed {players_before_leaving.difference(players_after_leaving)}")

    except:  # TODO what error is this?
        lg.info("a not registered chat member left the group")
    if context.chat_data['game'] == 0:
        return conversation_states['lobby']
    else:
        return None

def start_game(update: Update, context: CallbackContext) -> int:
    """begin game
        begins game and first round

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - return type == int
            - return == 0 or 1
    """
    lg.debug("/play was pressed")
    players = context.chat_data['players']
    # not enough players
    if len(players) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please add more players. 🙃")
        return conversation_states['lobby']
    # game running
    elif len(players) < 6 and context.chat_data['game'] != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The game is already running")
        return conversation_states['lobby']
    # game can start
    elif len(players) < 6:
        # initialize the game
        context.chat_data['game'] = Game(list(players))
        new_round_succeeded = new_round(update, context)
        if new_round_succeeded:  # fails if a player is missing a username
            lg.debug(f"Game initialized {hands_log_str(update, context)}")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=messages['game_begin'] + messages['rules'])
            tell_round(update, context)
            tell_turn(update, context)
            tell_top_of_stack(update, context)
            return conversation_states['play']
        else:  # reset the game
            lg.debug(f"New round could not be started")
            context.chat_data['game'] = 0
            return conversation_states['lobby']
    # too many players
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Sorry, you have too many players 😥. {len(players) - 5} members must leave the group.")
        return conversation_states['lobby']


def choose_suit(update: Update, context: CallbackContext) -> int:
    """chose suit for 8
        choose suit for crazy 8

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - type(suit) == str
            - type(choice) == str
            - len (suit) < 5
    """
    lg.debug("A player wants to choose a suit")
    player = update.message.from_user.id
    suit = update.message.text
    game = context.chat_data['game']
    choice = ''
    check_turn_outcome = check_turn(update, context, player)
    if check_turn_outcome:
        if suit == '♠' or suit == '♠️':
            choice = '♠'
            game.choose_suit(choice)
        elif suit == '♥' or suit == '♥️':
            choice = '♥'
            game.choose_suit(choice)
        elif suit == '♣' or suit == '♣️':
            choice = '♣'
            game.choose_suit(choice)
        elif suit == '♦' or suit == '♦️':
            choice = '♦'
            game.choose_suit(choice)
        lg.debug(f"Suit {choice} was chosen")
        lg.debug(f"last eight suit of game is {game.last_eights_suit}")

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"@{get_username_from_id(update, context, player)} chose suit {game.last_eights_suit}. The next card must match this suit.",
                                 reply_markup=make_hand_keyboard(game, player, False))
        next_turn(context)
        tell_turn(update, context)
        return conversation_states['play']
    else:
        return conversation_states['choose_suit']


def play_card(update: Update, context: CallbackContext) -> int or None:
    """play card
        interpret the card a player tries to put on the card stack

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - len(move) < 5
            - type(player) == type(players[at_turn] == int
    """
    lg.debug("A card was played")
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    player = update.message.from_user.id
    move = update.message.text
    lg.debug(f"player: {player} on turn: {players[at_turn]} tried move: {move}")
    lg.debug(f"player: {player} \nturn: {context.chat_data['turn']}")

    game = context.chat_data['game']

    if player == players[at_turn]:
        lg.debug("Player tried move on right turn")
        move_return = game.move(player, Card(move))
        lg.debug(f"player: {player} on turn: {players[at_turn]} made move: {move}  outcome is: {move_return}")
        if move_return == MoveOutcome.valid_move:
            lg.debug("Player made valid move")
            tell_who_put_what_on_stack(update, context)
            next_turn(context)
            tell_turn(update, context)
            return conversation_states['play']
        elif move_return == MoveOutcome.crazy8:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Careful a crazy 8😲!\n@{get_username_from_id(update, context, player)} what suit do you choose?",
                                     reply_markup=keyboards['choose_suit'])
            return conversation_states['choose_suit']
        elif move_return == MoveOutcome.invalid_move:
            lg.debug("Player made invalid move")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="I'm sorry this move is not valid")
            return conversation_states['play']

        elif move_return == MoveOutcome.round_won:
            lg.debug("Round over")

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="The round is over.\n" +
                                          get_users_name_from_id(update, context, game.leading_player) +
                                          " is leading")
            score(update, context)
            new_round(update, context)
            tell_round(update, context)
            tell_turn(update, context)
            tell_top_of_stack(update, context)
            return conversation_states['play']
        elif move_return == MoveOutcome.game_won:
            lg.debug("Game over")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="The game is over.\n" +
                                          get_users_name_from_id(update, context, game.leading_player) +
                                          ", you won! 🎉")
            score(update, context)
            sleep(2)  # ensure game is not ended before score can be displayed
            end_game(update, context)
            leave_chat(update, context)
            return None

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages['wrong_turn'])
        lg.debug("Player tried move on wrong turn")
        return conversation_states['play']

    """
    check if it is your turn → store in context[next turn or sth]
    check I f I can play the card
    If not tell them they can't play rn
    """


def draw_card(update, context):
    """draw card
        player drawing card from card deck

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - if player's turn: len(player.hand) increased by 1
            - if not player's turn: len(player.hand) unchanged
    """
    lg.debug("PLayer pressed /draw")
    game = context.chat_data['game']
    player = update.message.from_user.id
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']

    if player == players[at_turn]:
        lg.debug("Player tried to draw a card on right turn")
        if not game.can_move(player):
            game.draw(player)
            hand_keyboard = make_hand_keyboard(game, players[at_turn], False)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"@{get_username_from_id(update, context, player)} drew a card",
                                     reply_markup=hand_keyboard)
            tell_top_of_stack(update, context)
            next_turn(context)
            tell_turn(update, context)
        else:
            hand_keyboard = make_hand_keyboard(game, players[at_turn], False)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"I'm sorry @{get_username_from_id(update, context, player)} you can't draw "
                                          f"cards if you can play cards. Please play a card.",
                                     reply_markup=hand_keyboard)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages['wrong_turn'])
        lg.debug("Player tried to draw card on wrong turn")
    return conversation_states['play']


def tell_top_of_stack(update: Update, context: CallbackContext):
    """tell what card is on top of the card stack
        tells what card is on top of the card stack

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - type(card_on_stack) == str
            - len(card_on_stack) == 2
    """
    game = (context.chat_data['game'])
    card_on_stack = str(game.top_of_stack)
    player_that_made_move = list(context.chat_data['players'])[context.chat_data['turn']]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{card_on_stack} is on the stack",
                             reply_markup=make_hand_keyboard(game, player_that_made_move, False))
    return conversation_states['play']


def unknown_command(update: Update, context: CallbackContext):
    """tells command is not known
        triggered when non-existing command is called or command is not available in current conversation state

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - "/" in update.message.text
            - type(update.message.text) == str

        source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry but I don't know that command😟.")


# -- End: Message handler callback functions --#


# -- Command callback functions -- #

def rules(update: Update, context: CallbackContext):
    """sends a description of the game
        sends a description of the game

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - "/" in update.message.text
            - type(update.message.text) == str

    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules"])


def rules_long(update: Update, context: CallbackContext):
    """sends a detailed description of the game
        sends a detailed description of the game

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - "/" in update.message.text
            - type(update.message.text) == str
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules_long"])


def bot_help(update: Update, context: CallbackContext):
    """sends a list of available commands
        sends a list of available commands

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - "/" in update.message.text
            - type(update.message.text) == str
    """
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages["commands"])
    except TimedOut:

        handle_timeout(update, context)

def score(update: Update, context: CallbackContext):
    """sends current store
        sends current store

        param:
            update (telegram.Update): represents incoming update - Accordingly in all following functions
            context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

        test:
            - "/" in update.message.text
            - type(update.message.text) == str
    """
    try:
        game = context.chat_data['game']
        players = context.chat_data['players']
        scores = [["Pts.", "Player"]]
        for player in players:
            p_score = [game.scores[player], get_username_from_id(update, context, player)]
            scores.append(p_score)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=tabulate(scores))
    except TimedOut:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I had an issue, could you ask for the /score again?")
    return conversation_states['play']


def send_hand(update: Update, context:CallbackContext):
    """Give player hands keyboard.

    Give player hands keyboard. Is useful since the keyboards are are tied to messages from the bot.
    Meaning the serve as a reply blue print. However, if a player tries to respond to another message in the chat,
    it can be hard to find the bot's message that has the player's hands keyboard (reply blue print)

    param:
        update (telegram.Update): represents incoming update - Accordingly in all following functions
        context (telegram.ext.CallbackContext):  callback called by telegram.ext.Handler, stores information about the bot, the chat and users and more

    test:
        - type(hand_keybard) == ReplyMarkup
        - player_requesting_hand != None
    """
    try:
        player_requesting_hand = update.message.from_user.id
        at_turn = context.chat_data['turn']
        players = context.chat_data['players']
        if player_requesting_hand == players[at_turn]:
            can_potentially_draw = True
        else:
            can_potentially_draw = False
        hand_keyboard = make_hand_keyboard(context.chat_data['game'], player_requesting_hand, can_potentially_draw)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Here is your hand @{get_username_from_id(update, context, player_requesting_hand)}",
                                 reply_markup=hand_keyboard)
    except ValueError:
        pass
    except TimedOut:
        handle_timeout(update, context)
    return conversation_states['play']

# -- End: Command callback functions -- #


# -- Handlers -- #

unknown_command_handler = MessageHandler(Filters.command, unknown_command)

# source https://github.com/FrtZgwL/CoronaBot/blob/master/corona_bot.py
entry_point = [MessageHandler(Filters.status_update.chat_created, new_game),
               MessageHandler(Filters.status_update.new_chat_members, bot_was_added_to_group),
               CommandHandler('newgame', new_game)]
# states conversation can be in an available Message/CommandHandlers
states = {
    conversation_states['lobby']: [MessageHandler(Filters.status_update.new_chat_members, new_player),
                                   MessageHandler(Filters.status_update.left_chat_member, player_left_in_lobby),
                                   CommandHandler('play', start_game),
                                   CommandHandler('help', bot_help),
                                   CommandHandler('rules', rules),
                                   CommandHandler('ruleslong', rules_long),
                                   CommandHandler('join', join)],
    conversation_states['play']: [
                                    MessageHandler(Filters.text & Filters.regex('([♠♥♣♦]|[♠️♣️♥️♦️])((2|3|4|5|6|7|8|9|10|11|12)|[JQKA])'),
                                                   play_card),
                                    MessageHandler(Filters.status_update.left_chat_member, player_left_in_game),
                                    CommandHandler('draw', draw_card),
                                    CommandHandler('stack', tell_top_of_stack),
                                    CommandHandler('help', bot_help),
                                    CommandHandler('rules', rules),
                                    CommandHandler('ruleslong', rules_long),
                                    CommandHandler('score', score),
                                    CommandHandler('endgame', user_end_game),
                                    CommandHandler('turn', tell_turn),
                                    CommandHandler('hand', send_hand)],
    conversation_states['choose_suit']: [
        MessageHandler(Filters.text & Filters.regex('([♠♥♣♦]|[♠️♣️♥️♦️])'), choose_suit)]
}

navigation = ConversationHandler(entry_point,
                                 states,
                                 [],  # fallbacks
                                 persistent=False,
                                 name="navigation",
                                 per_user=False)
# -- End: Handlers -- #


def main():
    """main function
        main function, initializes bot, updater, dispatcher, adds handlers and starts polling

        testing:
            - updater != None
            - dispatcher != None
    """
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(navigation)
    dispatcher.add_handler(unknown_command_handler)


    # start looking for chat updates
    updater.start_polling()




if __name__ == "__main__":
    main()
