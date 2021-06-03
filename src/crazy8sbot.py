"""
Bot for playing crazy eights.
    param:
        Author: Deborah Djon
        Date: .06.2021
        Version:0.1
        license: free

Add this bot to your telegram group and play crazy eights with your friends.

"""

# TODO: warum rundedt int nochmal ab?

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
from telegram import Update
from typing import List, Dict

import logging as lg

# custom modules

from constants import messages, conversation_states, keyboards, BOT_TOKEN, hand_filler, MoveOutcome, TESTBOTS
from card import Card
from game import Game
import constants as c

# setup lg
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)

# TODO: command handlers: play, score, help, endgame, killbot
# TODO: Message handlers: lay cards, curse words / emojis
# TODO: Keyboard
# TODO: Classes: players, game (players, rounds, score):
# TODO: score
# TODO: Figure out when to use lg.debug and when to use logging.info
# TODO: ask cedric: when do you use info and when debug?
# TODO: Hand out hands, play card, multi level keyboard

'''Goal
Basic game playable (Goal Reached when I have seen all these in action once)
- Track the order ppl play in and call ppl out that want to play at the wrong turn
- When an 8 is played: 
    - send a seperate keyboard to the person who played it
    - tell it to the game somehow
- I must be able to check if the card is an 8 → send ask for a color how does that work in the game? 
- Tell what card is on the stack 
- draw card functionality -> check if they can draw (they must draw until they can play) 
- You must lay a card to complete your tun 
- Function new round

Keyboards: 
    - Send the play button to every body at the beginning 
    - check what a keyboard with 33 cards looks like first
    - Keyborad with 10 card slots is sent to everybody, Then 15, 20, 25, 30, 33(next to draw button)

Other: 
- Add info that a player must have a username → check when ppl start is pressed  → function check_if_all_players_have_usernames(update, context)
- display the score: make a pic? → simplest thing is just a simple "100 - Jen ..." Highlight the leading player
- check if stack is empty → new round + Message "yo stack empte, blah is leading" 
- send a sticker of the card that is on the stack 
- Users leaving the chat must be handled: 
    - In the game: dont make moves with player
    - In the bot: just rmove from player array
    - Do I need the left members array? 
 - test delete_message(chat_id, message_id, timeout=None, api_kwargs=None)
'''

"""
Keyboards senden: 
* als antwort 
* Einmal an alle 
* Nach frage 
"""


# -- Helper functions -- #

def stop(update: Update, context: CallbackContext):  # nur admin
    context.bot.send_message(chat_id=update.effective_chat.id, text="See ya 😋")
    ##delete game instance
    pass


def hands_log_str(update: Update, context: CallbackContext):
    players = context.chat_data['players']
    my_game = context.chat_data['game']
    hands_log = "Hands:\n"
    for player in players:
        hand = str(player) \
               + "(" + get_users_name_from_id(update, context, player) + ")" \
               + ':' + str([str(card) for card in my_game.get_hand(player)]) + "\n"
        hands_log = hands_log + hand
    return hands_log


def get_user_from_id(update: Update, context: CallbackContext, user_id:int):
    return context.bot.get_chat_member(update.message.chat.id, int(user_id)).user



def get_username_from_id(update: Update, context: CallbackContext, user_id:int) -> str:
    user = get_user_from_id(update, context, user_id)
    if user.username == None:
        if user.last_name == None:
            name = user.first_name.replace(' ', '-')
        else:
            name = user.first_name.replace(' ', '-') + "_" + user.last_name.replace(' ', '-')

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"@{name}, you seem to not have a username. Please add one to continue playing.")
        raise ValueError(f"{name} has no username", name)
    else: return user.username

def get_users_name_from_id(update: Update, context: CallbackContext, user_id:int) -> str:
    try:
        return get_username_from_id(update, context, user_id)
    except ValueError as e:
        return e.args[1]



def get_current_players(update: Update, context: CallbackContext):
    return {str(player) + ':' + get_users_name_from_id(update, context, player)
            for player in context.chat_data['players']}


def tell_turn(update: Update, context: CallbackContext):
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    player_at_turn = get_users_name_from_id(update, context, players[at_turn])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="It's your turn " + player_at_turn)


def tell_deck(update: Update, context: CallbackContext):
    card_on_stack = str(context.chat_data['game'].top_of_stack)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{card_on_stack} is on the stack")


def leave_chat(update: Update, context: CallbackContext):
    context.bot.leaveChat(update.effective_chat.id)


# TODO delete game fkt
def end_game(context:CallbackContext):
    """deletes a game from all games"""
    context.chat_data['players'] = {}
    context.players_left = {}
    context.chat_data['game'] = 0
    context.chat_data['turn'] = 0



# TODO hand_out hand
def hand_out_hands(update: Update, context: CallbackContext) -> bool:
    """
    function that hands out cards to all players

    """
    players = context.chat_data['players']
    try:
        player_usernames = [get_username_from_id(update, context, player) for player in players]
        for player in player_usernames:
            context.bot.send_message(text=f"Handing out cards to {player}", reply_markup=make_hand_keyboard(player))
        return True
    except:
        return False

# TODO I need a draw function

def new_round(update: Update, context:CallbackContext, game: Game) -> bool:  # TODO add sending new keyboards
    game.new_round()
    if (hand_out_hands(update, context)):
        return True
    else:
        return False


# TODO do I need this?
def kill(updater:Updater):
    """kills the bot instance."""
    # source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
    updater.stop()
    updater.is_idle = False
    exit()

def make_hand_keyboard(game:Game, player:int):  # had page
    sorted_hand = sorted(game.get_hand(player))
    hand_str = [str(card) for card in sorted_hand]
    cards_per_row = 5
    # build keyboard rows with 5 cards
    full_row_count = int(len(hand_str)/cards_per_row)
    keyboard_buttons = [['/draw']]
    card_index = 0
    for j in range(full_row_count): #TODO: can I make this more efficient? Dictionaries?
        keyboard_row = []
        for k in range(cards_per_row):
            keyboard_row.append(hand_str[card_index])
            card_index += 1
        keyboard_buttons.append(keyboard_row)

    # fill the last row row with remaining cards and help button
    last_row = hand_str[full_row_count*5:]
    last_row.append("/help")
    keyboard_buttons.append(last_row)

    keyboard = {
        "keyboard": keyboard_buttons,
        "resize_keyboard": True,
        "selective": True
    }
    return keyboard

# -- End: Helper functions -- #

# -- Testing -- #
def new_game_test(update: Update, context: CallbackContext):
    # TODO remove for real application
    lg.debug("New game started")
    context.chat_data['players'] = {857950388, 1848549159}
    context.players_left = {}
    context.chat_data['game'] = 0
    context.chat_data['turn'] = 0
    # initialize the game
    context.chat_data['game'] = Game(list(context.chat_data['players']))
    new_round_succeeded = new_round(update, context, context.chat_data['game'])
    if new_round_succeeded:
        lg.debug(f"Game initialized {hands_log_str(update, context)}")
        tell_turn(update, context)
        tell_deck(update, context)
        return conversation_states['play']
    else:
        lg.debug(f"New round could not be started")
        return conversation_states['lobby']

# -- End: Testing -- #


# -- Message handler callback functions --#


def new_game(update: Update, context: CallbackContext):
    lg.debug("A group was created")
    """ triggered when a new group chat adds the bot, hence, starts a game

        Function that is triggered when somebody creates a new chat with the chatbot.
        Registers the person that created the chat as player.
        TODO do I need to differentiate between creating a chat with the chatbot and creating the chat with everyone who wants to play?
        param:
            update:
            context:
        test: TODO ask if we need this here
    """

    sender = update.message.from_user.id
    lg.info(f"{get_users_name_from_id(update, context, sender)} created the chat {update.message.chat.title}")
    context.chat_data['players'] = {sender}
    context.players_left = {}
    context.chat_data['turn'] = 0
    context.chat_data['game'] = 0
    lg.info(f"Players initialized with {str(context.chat_data['players'])} "
            f"({get_users_name_from_id(update, context, sender)})")
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages['welcome'],
                             reply_markup=keyboards['play']) #TODO edit welcome message
    return conversation_states['lobby']


def new_player(update: Update, context: CallbackContext):
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
                                 reply_markup=keyboards['play'])  # TODO edit welcome message

    lg.info(f"Currently in the lobby:\n {str(get_current_players(update, context))}")
    return conversation_states['lobby']



# TODO player left fkt
def player_left(update: Update, context: CallbackContext):
    """remove from players list
    When the last player leaves delete the chat in telegram and the context and delete the game
    """
    lg.debug("A player left")
    left = update.message.left_chat_member.id
    if context.chat_data['game'] == 'lobby':
        try:
            players_before_leaving = get_current_players(update, context)
            context.chat_data['players'].remove(left)
            players_after_leaving = get_current_players(update, context)
            lg.info(f"successfully removed {players_before_leaving.difference(players_after_leaving)}")
            return conversation_states['lobby']

        except:  # TODO what error is this?
            lg.info("a not registered chat member left the group")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Remember to next time create a grop only with me before adding more members to the chat.😉")
            return conversation_states['lobby']


def start_game(update: Update, context: CallbackContext):  # TODo, just send a message
    lg.debug("/play was pressed")
    players = context.chat_data['players']
    # Only the case if the bot is the only on in the group or the group was opened wrong and has unregistered players
    if len(players) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages['group_opened_wrong'])
        leave_chat(update, context)
        return conversation_states['lobby']
    elif len(players) == 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please add more players. 🙃")
        return conversation_states['lobby']
    elif len(players < 6 and context.chat_data['game']!= 0):
        context.bot.send_message(chat_id=update.effective_chat.id, text="The game is already running")
        return conversation_states['lobby']
    elif len(players) < 6:
        # initialize the game
        context.chat_data['game'] = Game(list(players))
        new_round_succeeded = new_round(update, context, context.chat_data['game'])
        if new_round_succeeded: # fails if a player is missing a username
            lg.debug(f"Game initialized {hands_log_str(update, context)}")
            rules(update, context)
            tell_turn(update, context)
            tell_deck(update, context)
            return conversation_states['play']
        else: # reset the game
            lg.debug(f"New round could not be started")
            context.chat_data['game'] = 0
            return conversation_states['lobby']
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Sorry, you have too many players 😥. {len(players) - 5} members must leave the group.")
        return conversation_states['lobby']

# TODO command for getting the card on the stack

def play_card(update: Update, context: CallbackContext):  # TODO uff, muss das?
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
        lg.debug(
            f"player: {player} on turn: {context.chat_data['player']} made move: {move}  outcome is: {move_return}")
        if move_return == MoveOutcome.valid_move:
            lg.debug("Player made valid move")
            context.chat_data["turn"] = (context.chat_data["turn"] + 1) % len(context.chat_data['players'])
            tell_deck(update, context)
            tell_turn(update, context)
            return conversation_states['play']

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
                                          "is leading")
            new_round(game)
            tell_turn(update, context)
            tell_deck(update, context)
            return conversation_states['play']
            # TODO Score()
        elif move_return == MoveOutcome.game_won:
            lg.debug("Game over")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="The game is over.\n" +
                                          get_users_name_from_id(update, context, game.leading_player) +
                                          ", you won! 🎉")
            end_game(context)
            leave_chat(update, context)
            return conversation_states['play']

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry but it's not your turn 😕")
        lg.debug("Player tried move on wrong turn")
        return conversation_states['play']

    # TODO Feedback an player invalid move
    """
    check if it is your turn → store in context[next turn or sth]
    check I f I can play the card
    If not tell them they can't play rn
    """

#
# def unknown_command(update, context):
#     # source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry but I don't know that command😟.")
#     current_conversation_state = context.m


# -- End: Message handler callback functions --#


# -- Command callback functions -- #

def rules(update: Update, context: CallbackContext):
    """sends a description of the game."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules"])


def rules_long(update: Update, context: CallbackContext):
    """sends a detailed description of the game"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules_long"])


def bot_help(update: Update, context: CallbackContext):
    """sends a set of commands that can be used with the bot."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["commands"])


# TODO: Send a score
def score(update: Update, context: CallbackContext):
    pass


# -- End: Command callback functions -- #


# if page * 9 > len(sorted_hand):
#  hand_section = [hand_filler for i in range(9)]
# requested page has some cards
# else:
# hand_section = sorted_hand[page * 9:]
# hand_section.extend([hand_filler for i in range(9-len(hand_section))])

# hand_section = [str(card) for card in hand_section]
# hs = hand_section # shorter name





"""
import crazy8sbot as c
import game as g
from telegram import Bot
cb = Bot("1665894053:AAHxd8VUNhV1Q8ncLrF9IvljRPcGG9zfH60")
mg = g.Game([1,2,3])
mg.new_round()
for i in range (33): mg.draw(1)
keyboard = c.make_hand_keyboard(mg, 1)
cb.send_message(chat_id =-597750631, text="hi", reply_markup=c.make_hand_keyboard(mg, 1))
"""

# -- Handlers -- #

# unknown_command_handler = MessageHandler(Filters.command, unknown_command)

# from github https://github.com/FrtZgwL/CoronaBot/blob/master/corona_bot.py
# persistence = PicklePersistence(filename="storage/bot_storage.pkl")
entry_point = [MessageHandler(Filters.status_update.chat_created, new_game),
               CommandHandler('ng', new_game_test)]  # Testing
states = {  # TODO What if the person that created the chat leaves durin sb is in the lobby?
    conversation_states['lobby']: [MessageHandler(Filters.status_update.new_chat_members, new_player),
                                   MessageHandler(Filters.status_update.left_chat_member, player_left),
                                   CommandHandler('play', start_game), ],  # pla PLay button an alle
    conversation_states['play']: [
        MessageHandler(Filters.text & Filters.regex('([♠♥♣♦]|[♠️♣️♥️♦️])((2|3|4|5|6|7|8|9|10|11|12)|[JQKA])'),
                       play_card),
        CommandHandler('ng', new_game_test),
        MessageHandler(Filters.text(['ng']), new_game_test)],  # Testing
    conversation_states['menu']: [CommandHandler('rules', rules),
                                  CommandHandler('ruleslong', rules_long),
                                  CommandHandler('score', score),
                                  CommandHandler('help', bot_help)],  # TODO Back

}
navigation = ConversationHandler(entry_point,
                                 states,
                                 [],  # fallbacks
                                 persistent=False,  # TODO do I need persistence?
                                 name="navigation")


# -- End: Handlers -- #

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(navigation)
    # dispatcher.add_handler(unknown_command_handler)

    # start looking for chat updates
    updater.start_polling()


if __name__ == "__main__":
    main()
