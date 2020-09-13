import discord
import json


def embed_team(team):
    id = team.get("id")
    time = team.get("time")
    players = team.get("players")
    embed = discord.Embed(title="Team {}".format(id), color=discord.Colour.dark_blue())
    i = 1
    result = ""
    for p in players:
        result += "{}. {}\n".format(i, p)
        i += 1
    embed.add_field(name="Time: " + time, value=result, inline=False)
    return embed


def read_json(filename):
    with open(filename) as readfile:
        data = json.load(readfile)
        return data


def write_json(data):
    with open("teams.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
