
# Protokoll


## UX

* Alle gehen in eine Telegrammgruppe (automatisch im spiel)
    - Bot kickt automatisch überschüssige 
* Einer drückt play
* Bot sagt hallo wilkommen
* Hand und Menü wird an einzelne Personen schicken (Keyboard)
    Mentions der einzelnen Sieler 
    
    
*Keyboards an bestimmte User senden*
keyboard = {
    "keyboard": [
          # TODO Groupadmin can't leave the game
        ["/rules", "/ruleslong", "/score"],
        ["/sudfhuhs", "/dasd", "/hkjklj"],
    ],
    "resize_keyboard": True,
    "selective" : True
}

def echo(update, context):
    message = update.message.text
    context.bot.send_message(reply_to_message_id=update.message.message_id, chat_id=update.effective_chat.id, text=message.replace('bot1',''), reply_markup=keyboard)


