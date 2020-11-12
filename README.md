# play-tonight-bot

Discord chat bot for scheduling time to play games with your friends

Tired of asking friends if they are free to play? Instead, let them know when YOU are free to play! The purpose of this bot is share what times you are available to play games. Your friends will see this and can join if they want to play as well.

Add your times via the bot commands to share with your friends. Let's play tonight!

# Bot commands

```
!help
List commands
!faq
Learn how to use this bot, what games are supported, and advanced commands
!create
Create a team with !create game time
!create lol 8pm will create a League of Legends team with start time 8pm
!teams
Show current teams
You can filter teams by game using !teams game
!join
Join team with !join n, where n is team number
!leave
Leave team with !leave n, where n is team number
Team will be deleted if there are no more players
!add
Add a player with !add n playerId, where n is team number
!remove
Remove a player with !remove n playerNumber, where n is team number and playerNumber is the player's position in the team
!remove 1 2 will remove Player 2 from Team 1
!edit
Edit time to play with !edit n time, where n is team number
!edit 2 9pm will update Team 2's start time to 9pm
!delete
Delete the entire team with !delete n, where n is team number
Only Player 1 can delete the team
```

# Sample Pics

<img src="https://user-images.githubusercontent.com/6621087/98969277-4be68f80-24d4-11eb-9b6d-1508ca8818a3.png" width="20%" height="20%">
<img src="https://user-images.githubusercontent.com/6621087/98969359-5f91f600-24d4-11eb-981f-ca35cf4c5540.png" width="20%" height="20%">

# Changelog

v1.3.0 - Update !join/!leave to handle multiple teams, ':' is optional when specifying time, fix timezone for !teams

v1.2.0 - Update !remove to remove a player by index

v1.1.0 - Increase team size, added Minecraft to games, allow time to have a range, !destroy command for owners
