import discord
import os
import sys

from discord.ext import commands
from dotenv import load_dotenv
from utils import read_json, write_json

load_dotenv()
env = "prod" if len(sys.argv) == 1 else "dev"
TOKEN = os.getenv("DISCORD_TOKEN") if env == "prod" else os.getenv("dev_DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None)


@bot.command()
async def help(ctx):
    await ctx.send(
        """Help Menu
Schedule time to play league!
Want to contribute? Github
    **!help**
        List Commands
    **!faq**
        Setup and learn how to use this bot
    **!create**
        Start a list/team and specify time using !create n 00:00
        Time is based on 24 hour format i.e. 20:00 is 8pm
    **!teams**
        Shows current team list
    **!join**
        Join team with !join n
    **!leave**
        Leave team with !leave n
    **!edittime**
        Edit time to play with !edittime n 00:00"""
    )


@bot.command()
async def create(ctx):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data:
        server_teams = data.get(server_id)
        id = (
            int(server_teams[len(server_teams) - 1].get("id")) + 1
            if len(server_teams) > 0
            else 1
        )
        new_team = {"id": id, "time": "7 PM", "players": [ctx.author.name]}
        server_teams.append(new_team)
    else:
        id = 1
        data[server_id] = [{"id": 1, "time": "7 PM", "players": [ctx.author.name]}]

    write_json(data)
    await ctx.send("Created team {}".format(id))
    await teams(ctx)


@bot.command()
async def teams(ctx):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        list_of_teams = "**TEAMS**\n"
        for t in data[server_id]:
            i = 1
            players = "\n"
            for p in t.get("players"):
                players += "\t{}. {}\n".format(i, p)
                i += 1
            list_of_teams += "**Team {}**\n**Time**: {}\n**Players** {}".format(
                t.get("id"), t.get("time"), players
            )
            list_of_teams += "\n"
        await ctx.send(list_of_teams)
    else:
        await ctx.send("No teams exist!")


bot.run(TOKEN)
