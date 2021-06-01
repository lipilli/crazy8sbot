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


import logging as lg

# custom modules
from constants import messages, conversation_states, keyboards, BOT_TOKEN
from card import Card
from game import Game

# setup lg
# source: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
lg.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)

# TODO: command handlers: start, join, play, score, help rules, endgame, killbot
# TODO: Message handlers: lay cards, curse words / emojis
# TODO: Keyboard
# TODO: Classes: players, game (players, rounds, score):
# TODO: score
# TODO: Figure out when to use lg.debug and when to use logging.info
# TODO: ask cedric: when do you use info and when debug?
# TODO: Hand out hands, play card, multi level keyboard

'''Goal
Basic game playable
- Track the order ppl play in and call ppl out that want to play at the wrong turn
- I must be able to check if the card is an 8 → send ask for a color how does that work in the game? 
- Tell what card is on the stack 
- draw card functionality -> check if they can draw (they must draw until they can play) 
- You must lay a card to complete your tun 
- If sb reachse 100 pts → End the round → display score → begiin new round

- display the score: make a pic? → simplest thing is just a simple 100 - Jen ... 
- check if stack is empty?




- check if ppl have the same name, if yes display their username, other ways put numbers on their names 


'''

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
    lg.info(f"{sender.first_name} {sender.last_name} created the chat {update.message.chat.title}")
    context.chat_data['players'] = {sender.id}
    context.players_left = {}
    context.chat_data['game'] = 'lobby'
    lg.info(f"Players initialized with {str(context.chat_data['players'])} ({sender.first_name} {sender.last_name})")
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages['welcome'], reply_markup=keyboards['play'] )
    return conversation_states['lobby']
def get_user_from_id(update, context, user_id):
    return context.bot.get_chat_member(update.message.chat.id, int(user_id)).user
def get_current_players(update, context):
   return {(str(player) + ':' +
         get_user_from_id(update, context, int(player)).first_name) #TODO is int necessary here?  also test
        for player in context.chat_data['players']}

def new_player(update, context):
    want2play = {x.id for x in update.message.new_chat_members}
    lg.info(f"new member(s): {str(want2play)}")
    # TODO remove for real application
    if 'players' not in context.chat_data:
        context.chat_data['players'] = want2play
        context.players_left = {}
        context.chat_data['game'] = 'lobby'
        context.chat_data['turn'] = 0

    else:
        context.chat_data['players'].update(want2play) # TODO remove for real application
    try:
        context.chat_data['players'].remove(context.bot.get_me().id)
    except: pass
    current_players = get_current_players(update, context)
    lg.info(f"Currently in the lobby:\n {str(current_players)}")
    return conversation_states['lobby']

#TODO player left fkt
def player_left(update, context):
    """remove from players list
    When the last player leaves delete the chat in telegram and the context and delete the game
    """
    left = update.message.left_chat_member.id
    if context.chat_data['game']=='lobby':
        try:
            players_before_leaving = get_current_players(update,context)
            context.chat_data['players'].remove(left)
            players_after_leaving = get_current_players(update,context)
            lg.info(f"successfully removed {players_before_leaving.difference(players_after_leaving)}")
        except:
            lg.info("a not registered chat member left the group")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Remember to next time create a grop only with me before adding more members to the chat.😉")


#TODO delete game fkt
def delete_game():
    """deletes a game from all games"""
    pass


def create_keyboard(hand):
    # Returns a

    """ Returns a keboard like this just with the specific cards of a player
    keyboard = {
    "keyboard": [
        ["/rules", "/ruleslong", "/score"],
        ["/sudfhuhs", "/dasd", "/hkjklj"],
    ],
    "resize_keyboard": True,
    "selective" : True
    }

    I need the pages 2-4 as well
    """

def hand_out_hands(update, context):
    """
    Get array of players
    for each player create keyboard
    send reply markup to every player
    create multilevel keyboard, how do I do that again?
    can I have multiple different conversation states with different users in the chat?

    """
def tell_turn(update, context):
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    player_at_turn = get_user_from_id(update, context, players[at_turn])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Its your turn "+player_at_turn.first_name+" "+ player_at_turn.last_name)


def tell_deck(update,context):
    card_on_stack = str(context.chat_data['game'].top_of_stack)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{card_on_stack} is on the stack")


def hands_log_str(update, context):
    players = context.chat_data['players']
    my_game = context.chat_data['game']
    hands_log = "Hands:\n"
    for player in players:
        hand = str(player) \
               + "(" + get_user_from_id(update, context, player).username + ")" \
               + ':' + str([str(card) for card in my_game.get_hand(player)]) + "\n"
        hands_log = hands_log + hand
    return hands_log

def start_game(update, context): # TODo, just send a message
    players = context.chat_data['players']
    # Only the case if the bot is the only on in the group or the group was opened wrong and has unregistered players
    if len(players) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages['group_opened_wrong'])
        context.bot.leaveChat(update.effective_chat.id)
    elif len(players)==1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please add more players. 🙃")
    elif len(players) < 6:
        # my_game = context.chat_data['game'] TODO ask cedric this don't work right?
        # my_game = Game(list(players))

        # initialize the game
        context.chat_data['game'] = Game(list(players))
        context.chat_data['game'].new_round()
        #TODO hand_out_hands(update, context) ask cedric
        lg.info(f"Game initialized {hands_log_str(update, context)}") # TODO facilitate this here whith a function that returns the deck as a string

        tell_turn(update, context)
        return conversation_states['play']
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry, you have too many players 😥. {len(players)-5} members must leave the group.")
        return conversation_states['lobby']


# def join(update, context):
#     #self.players.push(update.message.from_user.id)
#     context.bot.send_message(chat_id=update.message.from_user.id, text=update.message.from_user.first_name)

def play_card (update, context):
    players = list(context.chat_data['players'])
    at_turn = context.chat_data['turn']
    made_move = update.message.from_user.id
    ## if players[at_turn] == made_move:

    move = update.message.text
    player = update.message.from_user.id
    game = context.chat_data['game']

    if player != context.chat_data['turn']:
        context.bot.send_message(chat_id=update.effectife_chat.id, text="I'm sorry but it's not your turn 😕")
    else:
      game.play_move(player, Card(move))
    """
    i = (i+1) % 5

    How do I track who's turn it is


    check if it is your turn → store in context[next turn or sth]
    check I f I can play the card
    If not tell them they can't play rn


    """


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
entry_point = [MessageHandler(Filters.status_update.chat_created, new_game),
               MessageHandler(Filters.status_update.new_chat_members, new_player)]
states = { # TODO What if the person that created the chat leaves durin sb is in the lobby?
    conversation_states['lobby']: [MessageHandler(Filters.status_update.new_chat_members, new_player),
                                   MessageHandler(Filters.status_update.left_chat_member, player_left),
                                   CommandHandler('play', start_game),],
    conversation_states['play']: [MessageHandler(Filters.regex('[♠♥♣♦]((\d\d?)|[JQKA])'), play_card)],
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


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(navigation)
    dispatcher.add_handler(unknown_command_handler)

    # start looking for chat updates
    updater.start_polling()



if __name__ == "__main__":
    main()