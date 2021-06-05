# crazy8sbot

Telegrambot for playing crazy8s

## Start the bot up locally
This is how you can run a local instance of the crazy8sbot. If you want you can also simply start with step 4
and work with the bot instance that is already running at my uberspace server. 

**1) import requirements** 

```bash 
$ pip install -r requirements.txt
```

**2) run the script**
```bash 
$ python crazy8sbot.py
```

**3) Create bot (optional)**

You can create your own bot by following this tutorial: 
You then have to exchange the BOT_TOKEN in the constants with the token of the bot you just created. 
But if you are lazy you can just use the bot token that I have already provided you with in the constants. 

**4) Create a grop**

Create a telegram group with 2-5 people and the crazy8sbot.


**5) Start the game and play**
Everyone in the group must enter "/join" to get registered for the game.

Anyone can press the provided "/play" button when everybody is ready.

All following steps are described by the bot.





## Notes

### Change in Approach 
First the game was intended to work as follows:
 
Group with one person is created with the bot. 

Then users are added and automatically registered. 

Finally play is pressed. 

To start a game a new groups had to be created every time. 

This turned out to be more work especially when there was a mistake 
(eg. player pressed "/play" before all were ready). To facilitate that and be error proof 
the commands "/join" and "/newgame" were introduced to start games explicitly. However many 
functions that are revolved around starting the game are still based on the old game structure. 
 

### Nice Features

The bot has several features that makes sure the ame requirements are met. For example: 

**8s**

The eights are what make the game special. They are wildcards that let you change the current 
suit that must be played. When an eight is played the bot registeres that, lets the player choose 
a suit and then continues the game as usual. 

**Username***

Players must have a username. This is essential for sending the ReplyMarkup with the cards
to the players. The game cannot be started if one or more players have no username. The bot
notifies these useres and addresses them by ther normal name. 


**Drawing cards only if no move possible**

A user can only draw cards at their turn and when there is no card that can be played. 
To signal this to the user the "/draw" button is only available on the hand of the player
if they have no card on their hand that can be played. 


**Commands**

The bot supports several commands that make playing the game easier. Such as "/stack" 
which helps when many messages were sent after the message that states the card on top of the card
stack. Another example is "/turn" which tells you whose turn it is. These are the most used
commands and therefore always present in the keyboard. All other available commands can be seen
with the "/help" command. 



### Known Issues:

The bot runns into Timeout errors every now and then. They are mostly not handled. 

**Troubleshoot:**

* /endgame

* /newgame

* remove bot from chat then add it again 

