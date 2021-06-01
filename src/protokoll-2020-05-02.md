
# Protokoll


## UX

* Alle gehen in eine Telegrammgruppe (automatisch im spiel)
    - Bot kickt automatisch überschüssige 
* Einer drückt play
* Bot sagt hallo wilkommen
* Hand und Menü wird an einzelne Personen schicken (Keyboard)
    Mentions der einzelnen Sieler 
    
    
    
    
Was passiert mit dem conversation handler? 

## Überlegungen Keyboard: 

man speichert alle Karten im keyboard: 
Man hat max 33 Karten auf der hand: --> 4 Seiten
   
   >Worst case Szenario: 
   > 2 Spieler*innen, eine zieht die ganze Zeit, die andere zieht einmal und legt einmal
   >  
   > →  Wenn man 100 Küge hat sind 100 Karten bei A(2/3 der Karten) und 50 bei B (1/3 der Karten)
   >
   > Bei 52 Karten und 5 Anfangskarten sind das bei A dann 5 + (52-10)*1/3 ~ 33 Karten   

````python
"keyboard":  [
    ["Draw"],
    ["♠1","♣2","♥","menu"],
    ["♠1","♣2","♥", "←"],
    ["♠1","♣2","♥", "→"]
]


````






    
*Keyboards an bestimmte User senden*
keyboard = {
    "keyboard": [
        ["/rules", "/ruleslong", "/score"],
        ["/sudfhuhs", "/dasd", "/hkjklj"],
    ],
    "resize_keyboard": True,
    "selective" : True
}

def echo(update, context):
    message = update.message.text
    context.bot.send_message(reply_to_message_id=update.message.message_id, chat_id=update.effective_chat.id, text=message.replace('bot1',''), reply_markup=keyboard)


