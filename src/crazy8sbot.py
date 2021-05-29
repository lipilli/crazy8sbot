"""
Bot for playing crazy eights.
    param:
        Author: Deborah Djon
        Date: .06.2021
        Version:0.1
        license: free

Add this bot to your telegram group and play crazy eights with your friends.

"""


from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
from telegram import  update
from typing import List


import logging

# custom modules
from constants import messages, conversation_states, keyboards, BOT_TOKEN
from game import Game

# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# TODO: command handlers: start, join, play, score, help rules, endgame, killbot
# TODO: Message handlers: lay cards, curse words / emojis
# TODO: Keyboard
# TODO: Classes: players, game (players, rounds, score):
# TODO: score
# TODO: create 2 extrabots



'''
Creates Keyboards on the fly
has a function that takes all the cards of the player in the deck and
adds them to the keyboard

Keboard laouts:

play_card_keyboard = {
    "keyboard" : [
        ["DRAW ↑"],
        ["♣75","♠","DECK"],
        ["♥8", "♦84", "MENU"]
    ],
    "resize_keyboard" : True
}



decck_keyboard = {
    "keyboard" : [
    [1,2,3,4,5]
    ]
}


Worst case Szenario 

'''


'''
TODO: Join/Leave events of members:
- Array: add when sb joins, pop when someone leaves
- always add the first 5 of the array
- kick the rest out of the group (bot needs admin rights)

message: 
new_chat_members
left_chat_member
'''

#
# class Crazy8sbot:
#     def lobby(update, context):
#         context.bot.send_message(chat_id=update.effective_chat.id,text=messages["rules"], reply_markup=keyboards['join'])
#         return conversation_states['lobby']
#
#     def join(update, context, self):
#         self.players.push(update.message.from_user.id)
#         context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.from_user.first_name)
#
#
#
#     def play_card_keyboard(player):
#         pass
#
#
#     def deck_keyboard(player, suit):
#         pass

def new_game(update, context):
    """ triggered when a new group chat adds the bot, hence, starts a game

        Function that is triggered when somebody creates a new chat with the chatbot.
        Registers the person that created the chat as player.
        TODO do I need to differentiate between creating a chat with the chatbot and creating the chat with everyone who wants to play?
        param:
            update:
            context:
        test: TODO ask if we need this here
    """
    sender = update.message.from_user
    logging.info(f"{sender.first_name} {sender.last_name} created the chat {update.message.chat.title}")
    context.chat_data['players'] = [sender.id]
    logging.info(f"Players initialized with {str(context.chat_data['players'])} ({sender.first_name} {sender.last_name})")
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages['welcome'], reply_markup=keyboards['play'] )
    return conversation_states['lobby']

#TODO player left fkt
def player_left():
    """remove from players list
    When the last player leaves delete the chat in telegram and the context and delete the game
    """
    pass

#TODO delete game fkt
def delete_game():
    """deletes a game from all games"""
    pass

def kick_players(update: update.Update, context: CallbackContext, wants2play: List[int]):
    #logging.info
    pass

def new_player(update, context):
    want2play = [x.id for x in update.message.new_chat_members]
    context.chat_data['players'].extend(want2play) # TODO does this work? is players an object / pointer?
    new_members = [(str(player)+':'+update.bot.get_member(player).user.first_name) for player in context.chat_data['players']]
    logging.info(f"These players were added to the game:\n {str(new_members)}")
    # toDO hand_out_cards(update, context)
    return conversation_states['lobby']


def hand_out_hands(update, context):
    pass


def start_game(update, context):
    players = context.chat_data['players']
    if (len(players) < 5):
        context.chat_data['game'] = Game(players)
        hand_out_hands(update, context)
        return conversation_states['play']
    else:
        # todo send message: yall x ppl gotta leave 
        return conversation_states['lobby']

    # TODO:kick_all_ecess_players(bot)
    pass

# def join(update, context):
#     #self.players.push(update.message.from_user.id)
#     context.bot.send_message(chat_id=update.message.from_user.id, text=update.message.from_user.first_name)

def play_card_keyboard(player):
    pass


def deck_keyboard(player, suit):
    pass


def menu_command(update, context):
    """
    make a command through the keyboard

    source: TODO: Cedric

    """
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=keyboards['menu'])

def kick_all_ecess_players(bot):
    pass




def rules(update, context):
    """sends a description of the game."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules"])

def rules_long(update, context):
    """sends a detailed description of the game"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["rules_long"])


def score(update, context):
    pass

def stop(update, context): # nur admin
    context.bot.send_message(chat_id=update.effective_chat.id, text="See ya 😋")
    ##delete game instance
    pass


def kill(updater):
    """kills the bot instance."""
    # source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
    updater.stop()
    updater.is_idle = False
    exit()


def bot_help(update, context):
    """sends a set of commands that can be used with the bot."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages["commands"])


def unknown_command(update, context):
    # source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry but I don't know that command😟.")

# Handlers
unknown_command_handler = MessageHandler(Filters.command, unknown_command)

# from github https://github.com/FrtZgwL/CoronaBot/blob/master/corona_bot.py
#persistence = PicklePersistence(filename="storage/bot_storage.pkl")
entry_point = [MessageHandler(Filters.status_update.chat_created, new_game)]
states = { # TODO What if the person that created the chat leaves durin sb is in the lobby?
    conversation_states['lobby']: [MessageHandler(Filters.status_update.new_chat_members, new_player), CommandHandler('play', start_game)], #@Cedric: this does not work
    conversation_states['menu']: [CommandHandler('rules', rules),
                                   CommandHandler('ruleslong', rules_long),
                                   CommandHandler('score', score),
                                   CommandHandler('help', bot_help)],
     conversation_states['deck_page1']:[]
    # conversation_states['deck_page2']:[],
    # conversation_states['deck_page3']:[],
    # conversation_states['deck_page4']:[]
    }
navigation = ConversationHandler(entry_point,
                                 states,
                                 [],#fallbacks
                                 persistent=False, # TODO do I need persistence?
                                 name="navigation")

    # new_context = CallbackContext(self.dispatcher).args.append({self.players})
    # so other handers can use it: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html

# class Crazy8sbot():
#
#     def __init__(self, bot_token):
#         self.updater = Updater(token=bot_token, use_context=True)
#         self.dispatcher = self.updater.dispatcher
#         # self.dispatcher.add_handler(Crazy8sbot.start_handler)
#         self.updater.start_polling()
#         self.dispatcher.add_handler(Crazy8sbot.menu_navigation)
#
#     def start(update, context):
#         context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#         return 0
#
#     def __init__(self, bot_token):
#         self.updater = Updater(token=bot_token, use_context=True)
#         self.dispatcher = self.updater.dispatcher
#         # self.dispatcher.add_handler(Crazy8sbot.start_handler)
#         self.updater.start_polling()
#         self.dispatcher.add_handler(Crazy8sbot.menu_navigation)
#
#     entry_points = [MessageHandler(Filters.regex('Hello crazy8sbot'), start)]
#     states = {
#         conversation_states['lobby']: [MessageHandler(Filters.regex('Hello crazy8sbot'), start)]
#         }
#     fallbacks = []
#     menu_navigation = ConversationHandler(entry_points, states, fallbacks, persistent=False, name="menu_navigation")

def main():
    # TODO kann eigentlich beides in den kontext
    game = 0
    players = 0
    players_left = 0

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(navigation)
    dispatcher.add_handler(unknown_command_handler)

    # start looking for chat updates
    updater.start_polling()



if __name__ == "__main__":
    main()
    #my_game = Game(players=my_list)

    # def start(update, context):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    #
    #
