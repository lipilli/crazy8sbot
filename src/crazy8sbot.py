"""
Bot for playing crazy eights.

Add this bot to your telegram group and play crazy eights with your friends.

"""
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

# custom modules
import constants as const
import conversation_handler as ch
# setup logging
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
logging.basicConfig(filename="bot.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# TODO: command handlers: start, join, play, score, help rules, endgame, killbot
# TODO: Message handlers: lay cards, curse words / emojis
# TODO: Keyboard
# TODO: Classes: players, game (players, rounds, score):
# TODO: score
# TODO: create 2 extrabots

messages = {
    'rules': """Here are the rules: 
     - Every card (other than eight) you play must match the suit or denomination of the card on the deck 
     - The eights are crazy! Play it at anytime and define a new suit. The next player must play an eight or a card of matching suit
     - If you can't play, draw cards until you can play
     - If there is no card on the deck
     - If the deck is empty and you can't play you are passed""",
    'rules_long': """Crazy 8s:
        General:
        - Goal: get more then 100 points
        - Players: 2-5
        - The player to get rid of all their cards first, wins the round
        
        Card values:
        - 8 = 50 points
        - K, Q, J or 10 = 10 points
        - Ace = 1 point
        - All other: points = Card number
        
        Start:
        - Everyone gets 5 cards
        - The one to joins first, begins
        - Play in the order of joining the game
        - The first card is never an 8
        
        Play:
        - Every card (other than eight) you play must match the suit or denomination of the card on the deck
        - The eights are crazy! Play it at anytime and define a new suit. The next player must play an eight or a card of matching suit
        - If you can't play, draw cards until you can play
        - If there is no card on the deck
        - If the deck is empty and you can't play you are passed
    """,
    'start': """The 8s are loose 😲😲😲!
        Get ready for a game of crazy 8s!
        Before you begin here are the commands you can use during the game:\n""",
    'commands': """  
    /join: join a game
    /leave: leave the game
    /play: start a new game
    /rules: short version of the game rules
    /ruleslong: long version of the game rules
    /score: current score
    /endgame: ends the game for all (admin only)
    /killbot: ends the bot and the game
    /help: list of available commands"""
}
"""
object with attributes 
+ I want to follow an OO aproach 
"""


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages['start'])


def join(update, context):
    pass


def leave():
    pass


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


def end_game(update, context):
    pass


def kill_bot(update, context):
    """kills the bot instance."""
    # source https://github.com/python-telegram-bot/python-telegram-bot/issues/801
    context.bot.send_message(chat_id=update.effective_chat.id, text="See ya 😋")


    updater.stop()
    # context.bot.getUpdates(offset=update.update_id + 1)
    # updater.is_idle = False
    exit()


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


# -------Old stuff
# Message Hanlder that returns the same message that just came in
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)



# echo with caps
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)





def message_handler(update, conext):
    text = str(update.message.text).lower
    response = ch.reply(text)
    update.messafe.reply_text(response)


def main():
    # continuously  checks for incoming messages
    global updater
    updater = Updater(token=const.BOT_TOKEN, use_context=True)
    # sends updates all added handlers, the handlers send out commands or do sth. based on the input
    dispatcher = updater.dispatcher

    # TODO: Persictence?

    # adding all the handlers to the dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    join_handler = CommandHandler('join', join)
    dispatcher.add_handler(join_handler)

    leave_handler = CommandHandler("leave", leave)
    dispatcher.add_handler(leave_handler)

    play_handler = CommandHandler("play", play)
    dispatcher.add_handler(play_handler)

    rules_handler = CommandHandler("rules", rules)
    dispatcher.add_handler(rules_handler)

    rules_long_handler = CommandHandler("ruleslong", rules_long)
    dispatcher.add_handler(rules_long_handler)

    score_handler = CommandHandler("score", score)
    dispatcher.add_handler(score_handler)

    end_game_handler = CommandHandler("endgame", end_game)
    dispatcher.add_handler(end_game_handler)

    kill_bot_handler = CommandHandler("killbot", kill_bot)
    dispatcher.add_handler(kill_bot_handler)

    bot_help_handler = CommandHandler("help", bot_help)
    dispatcher.add_handler(bot_help_handler)

    unknown_command_handler = MessageHandler(Filters.command, unknown_command)
    dispatcher.add_handler(unknown_command_handler)

    # start scanning for new messages
    updater.start_polling()
    # kill_bot()


if __name__ == "__main__":
    main()
