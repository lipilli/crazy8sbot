# crazy8sbot

Telegrambot for playing crazy8s

## Start the bot up locally

**1) import requirements** 

```bash 
$ e 
```

**2) run the script**
```bash 
$ python crazy8sbot.py
```


**3) Create a grop**

Create a telegram group with 2-5 people and the crazy8sbot.



**4) Start the game and play**
Everyone in the group must enter "/join" to get registered for the game.

Anyone can press the provided "/play" button when everybody is ready.

All following steps are described by the bot.





## Notes
First the game was intended to work as follows:
 
Group with one person is created with the bot. 

Then users are added and automatically registered. 

Finally play is pressed. 

To start a game a new groups had to be created every time. 

This turned out to be more work especially when there was a mistake 
(eg. player pressed "/play" before all were ready). To facilitate that and be error proof 
the commands "/join" and "/newgame" were introduced to start games explicitly. However many 
functions that are revolved around starting the game are still based on the old game structure. 
 