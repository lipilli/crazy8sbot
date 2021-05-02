"""
Bot for playing crazy eights.

Add this bot to your telegram group and play crazy eights with your friends.

"""
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

# custom modules
from constants import messages
from constants import menu_keyboard
from constants import BOT_TOKEN
from constants import states

# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
logging.basicConfig(filename="bot.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# TODO: command handlers: start, join, play, score, help rules, endgame, killbot
# TODO: Message handlers: lay cards, curse words / emojis
# TODO: Keyboard
# TODO: Classes: players, game (players, rounds, score):
# TODO: score
# TODO: create 2 extrabots


def play_card_keyboard(player):
    pass


def deck_keyboard(player, suit):
    pass

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

'''


'''
TODO: Join/Leave events of members:
- Array: add when sb joins, pop when someone leaves
- always add the first 5 of the array
- kick the rest out of the group (bot needs admin rights)
'''


def menu_command(update, context):
    """
    make a command through the keyboard

    source: TODO: Cedric

    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Text keyboard", reply_markup=menu_keyboard)


def play(update, context):
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


def kill():
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

#
# # -------Old stuff
# # Message Hanlder that returns the same message that just came in
# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#
#
#
# # echo with caps
# def caps(update, context):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
#
# caps_handler = CommandHandler('caps', caps)
#
#
# # def message_handler(update, conext):
# #     text = str(update.message.text).lower
# #     response = ch.reply(text)
# #     update.messafe.reply_text(response)


def main():
    # continuously  checks for incoming messages
    global updater
    updater = Updater(token=BOT_TOKEN, use_context=True)
    # sends updates all added handlers, the handlers send out commands or do sth. based on the input
    dispatcher = updater.dispatcher

    #TODO conversationhandler???

    # entry_points = [CommandHandler('start', start)]
    # states = {
    #     States.MENU: [CommandHandler('join', join)]
    # }
    #

    # adding all the handlers to the dispatcher
    play_handler = CommandHandler("play", play)
    dispatcher.add_handler(play_handler)

    rules_handler = CommandHandler("rules", rules)
    dispatcher.add_handler(rules_handler)

    rules_long_handler = CommandHandler("ruleslong", rules_long)
    dispatcher.add_handler(rules_long_handler)

    score_handler = CommandHandler("score", score)
    dispatcher.add_handler(score_handler)

    bot_help_handler = CommandHandler("help", bot_help)
    dispatcher.add_handler(bot_help_handler)

    unknown_command_handler = MessageHandler(Filters.command, unknown_command)
    dispatcher.add_handler(unknown_command_handler)

    # start scanning for new messages
    updater.start_polling()
    # kill_bot()


if __name__ == "__main__":
    main()
