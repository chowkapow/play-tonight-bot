error_messages = {
    "duplicates": "Please do not list a player more than once!",
    "full": "Team is full!",
    "game": "Please select a game from the FAQ!",
    "join_already": "You are already part of this team!",
    "no_teams": "No teams exist!",
    "not_found": "Team not found!",
    "not_part": "You are not part of this team!",
    "too_many": "Too many players listed!",
}

game_format = {
    "au": "Among Us",
    "amongus": "Among Us",
    "apex": "Apex Legends",
    "league": "League of Legends",
    "lol": "League of Legends",
}

help_command = {
    "title": "Help Menu",
    "description": "Schedule time to play!\nWant to contribute? [Github](https://github.com/chowkapow/play-tonight-bot)",
    "help_name": "**!help**",
    "help_value": "List commands",
    "faq_name": "**!faq**",
    "faq_value": "Setup and learn how to use this bot",
    "create_name": "**!create**",
    "create_value": """Create a team with __!create time__
      __!create 8pm__ will create a team with start time 8pm
      You can add multiple players if you separate the names with spaces, e.g. __!create time playerId1 playerId2__
      Max of 5 teams can be created""",
    "teams_name": "**!teams**",
    "teams_value": "Show current teams",
    "join_name": "**!join**",
    "join_value": "Join team with __!join n__, where n is team number",
    "leave_name": "**!leave**",
    "leave_value": "Leave team with __!leave n__, where n is team number",
    "add_name": "**!add**",
    "add_value": """Add a player with __!add n playerId__, where n is team number
      You can add multiple players if you separate the names with spaces, e.g. __!add n playerId1 playerId2__
      If the name contains a space, surround it with quotes, e.g. __!add n "player id__\"""",
    "remove_name": "**!remove**",
    "remove_value": """Remove a player with __!remove n playerId__, where n is team number
      You can remove multiple players if you separate the names with spaces, e.g. __!remove n playerId1 playerId2__
      If the name contains a space, surround it with quotes, e.g. __!remove n "player id__\"""",
    "edit_name": "**!edit**",
    "edit_value": """Edit time to play with __!edit n time__, where n is team number
      __!edit 2 9pm__ will change Team 2's start time to 9pm
      You must be part of the team to edit the time""",
    "footer": "Feedback and bug reports welcome. Contact chowkapow#4085",
}

max_players = {"au": 10, "amongus": 10, "apex": 3, "league": 5, "lol": 5}
