"""
Bot for playing crazy eights.

Add this bot to your telegram group and play crazy eights with your friends.

"""
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import ConversationHandler
import logging

# custom modules
from constants import messages
from constants import conversation_states
from constants import keyboards
from constants import BOT_TOKEN


# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

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


class Crazy8sbot:
    def __init__(self, bot_token):
        self.game = None
        self.players = []
        self.players_left = []

        # continuously  checks for incoming messages
        self.updater = Updater(token=bot_token, use_context=True)
        # sends updates all added handlers, the handlers send out commands or do sth. based on the input
        self.dispatcher = self.updater.dispatcher
        # adding handlers
        self.dispatcher.add_handler(Crazy8sbot.navigation)
        self.dispatcher.add_handler(Crazy8sbot.unknown_command_handler)

        # start scanning for new messages
        self.updater.start_polling()


    def lobby(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,text=messages["rules"], reply_markup=keyboards['join'])
        return conversation_states['lobby']

    def join(update, context, self):
        self.players.push(update.message.from_user.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.from_user.first_name)
        #print(update.message.from_user.first_name)


    def play_card_keyboard(player):
        pass


    def deck_keyboard(player, suit):
        pass


class Crazy8sbot:
    def __init__(self, bot_token):
        self.game = None
        self.players = []
        self.players_left = []

        # continuously  checks for incoming messages
        self.updater = Updater(token=bot_token, use_context=True)
        # sends updates all added handlers, the handlers send out commands or do sth. based on the input
        self.dispatcher = self.updater.dispatcher
        # adding handlers
        self.dispatcher.add_handler(Crazy8sbot.navigation)
        self.dispatcher.add_handler(Crazy8sbot.unknown_command_handler)

        # start scanning for new messages
        self.updater.start_polling()


    def lobby(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,text=messages["rules"], reply_markup=keyboards['join'])
        return conversation_states['lobby']

    def join(update, context, self):
        self.players.push(update.message.from_user.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.from_user.first_name)
        #print(update.message.from_user.first_name)


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


    def play(update, context):
        # TODO:kick_all_ecess_players(bot)
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

    entry_points = [MessageHandler(Filters.regex('@crazy8sbot'), lobby)]
    states = {
        conversation_states['lobby']: [CommandHandler('join', join), CommandHandler('play', play)], #add leave
        conversation_states['menu']: [ CommandHandler('rules', rules),
                                       CommandHandler('ruleslong', rules_long),
                                       CommandHandler('score', score),
                                       CommandHandler('help', bot_help)],
         conversation_states['deck_page1']:[]
        # conversation_states['deck_page2']:[],
        # conversation_states['deck_page3']:[],
        # conversation_states['deck_page4']:[]
        }
    fallbacks = []
    navigation = ConversationHandler(entry_points,
                                     states,
                                     fallbacks,
                                     persistent=False,
                                     name="navigation")

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
    unknown_command_handler = MessageHandler(Filters.command, unknown_command)


if __name__ == "__main__":
    Crazy8sbot(BOT_TOKEN)
    # def start(update, context):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    #
    #
    # updater = Updater(token=BOT_TOKEN, use_context=True)
    # dispatcher = updater.dispatcher
    # start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)
    # updater.start_polling()
