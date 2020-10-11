import re

available_games = """Among Us [amongus, au]
Apex Legends [apex]
League of Legends [league, lol]"""

error_messages = {
    "duplicate_player": "Please do not list a player more than once!",
    "existing_member": "You are already part of this team!",
    "no_teams": "No teams exist!",
    "non_creator": "You are not Player 1 of this team!",
    "non_member": "You are not part of this team!",
    "select_game": "Please select a game from the FAQ!",
    "team_full": "Team is full!",
    "team_not_found": "Team not found!",
    "time": "Please enter a valid time!",
    "too_many_players": "Too many players listed!",
}

faq_message = {
    "1. How does this bot help me?": "This bot helps you schedule times with friends to play your favorite games. Create a team or join an existing one!",
    "2. What games does this bot support?": "Currently this bot supports:\n\n{}\n\nPlease use one of the formats specified in the [] when creating a team.".format(
        available_games
    ),
    "3. How do I enter the time?": "Please enter the time as Ham / HH:MMam (or pm). No space between the time and period.",
    "4. Why is Player 1 able to delete a team?": "Player 1 is generally the creator of the team, so only he/she can delete.",
    "5. Want to add more games to the list?": "Contact chowkapow#4085",
    "\u200b": "Advanced Commands Usage",
    "Listing multiple players in one command": """You can add multiple players if you separate the names with spaces, e.g. __!create game time playerId1 playerId2__
If the name contains a space surround it with quotes, e.g. __!create game time "player id__"
This also applies to __!add__, __!remove__""",
}

game_format = {
    "amongus": "Among Us",
    "au": "Among Us",
    "apex": "Apex Legends",
    "league": "League of Legends",
    "lol": "League of Legends",
}

help_command = {
    "title": "Help Menu",
    "description": "Schedule time to play games with friends!\nWant to contribute? [Github](https://github.com/chowkapow/play-tonight-bot)",
    "help_name": "**!help**",
    "help_value": "List commands",
    "faq_name": "**!faq**",
    "faq_value": "Learn how to use this bot, what games are supported, and advanced commands usage",
    "create_name": "**!create**",
    "create_value": """Create a team with __!create game time__
__!create lol 8pm__ will create a League of Legends team with start time 8pm""",
    "teams_name": "**!teams**",
    "teams_value": """Show current teams
You can filter teams by game using __!teams game__""",
    "join_name": "**!join**",
    "join_value": "Join team with __!join n__, where n is team number",
    "leave_name": "**!leave**",
    "leave_value": """Leave team with __!leave n__, where n is team number
Team will be deleted if there are no more players""",
    "add_name": "**!add**",
    "add_value": "Add a player with __!add n playerId__, where n is team number",
    "remove_name": "**!remove**",
    "remove_value": "Remove a player with __!remove n playerId__, where n is team number",
    "edit_name": "**!edit**",
    "edit_value": """Edit time to play with __!edit n time__, where n is team number
__!edit 2 9pm__ will change Team 2's start time to 9pm""",
    "delete_name": "**!delete**",
    "delete_value": """Delete the entire team with __!delete n__, where n is team number
Only Player 1 can delete the team""",
    "footer": "Feedback and bug reports welcome. Contact chowkapow#4085",
}

max_players = {"amongus": 10, "au": 10, "apex": 3, "league": 5, "lol": 5}

pattern = re.compile("(1[0-2]|0?[1-9])([AaPp][Mm])")
pattern_minutes = re.compile("(1[0-2]|0?[1-9]):([0-5][0-9])([AaPp][Mm])")
