import asyncio
import discord
import os
import pytz
import sys

from datetime import date, datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv

from constants import (
    faq_message,
    error_messages as em,
    game_format,
    help_command as hc,
    max_players,
    pattern,
)
from utils import (
    check_owner,
    check_teams,
    embed_team,
    lowercase_players,
    read_json,
    remove_player,
    write_json,
)

load_dotenv()
env = "prod" if sys.argv[1] == "prod" else "dev"
TOKEN = os.getenv("DISCORD_TOKEN") if env == "prod" else os.getenv("dev_DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title=hc.get("title"),
        description=hc.get("description"),
        color=discord.Colour.dark_blue(),
    )
    embed.add_field(name=hc.get("help_name"), value=hc.get("help_value"), inline=False)
    embed.add_field(name=hc.get("faq_name"), value=hc.get("faq_value"), inline=False)
    embed.add_field(
        name=hc.get("create_name"), value=hc.get("create_value"), inline=False
    )
    embed.add_field(
        name=hc.get("teams_name"), value=hc.get("teams_value"), inline=False
    )
    embed.add_field(name=hc.get("join_name"), value=hc.get("join_value"), inline=False)
    embed.add_field(
        name=hc.get("leave_name"), value=hc.get("leave_value"), inline=False
    )
    embed.add_field(name=hc.get("add_name"), value=hc.get("add_value"), inline=False)
    embed.add_field(
        name=hc.get("remove_name"), value=hc.get("remove_value"), inline=False
    )
    embed.add_field(name=hc.get("edit_name"), value=hc.get("edit_value"), inline=False)
    embed.add_field(
        name=hc.get("delete_name"), value=hc.get("delete_value"), inline=False
    )
    embed.set_footer(text=hc.get("footer"))
    await ctx.send(embed=embed)


@bot.command()
async def faq(ctx):
    embed = discord.Embed(title="FAQ", color=discord.Colour.dark_blue())
    for key, val in faq_message.items():
        embed.add_field(name=key, value=val, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def create(ctx, game, time, *args):
    if game not in game_format:
        await ctx.send(em.get("select_game"))
        return
    elif not (pattern.match(time)):
        await ctx.send(em.get("time"))
        return
    elif len(args) != len(set(lowercase_players(args))):
        await ctx.send(em.get("duplicate_player"))
        return
    elif len(args) >= max_players.get(game):
        await ctx.send(em.get("too_many_players"))
        return
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    players = [ctx.author.name]
    if len(args) > 0:
        for p in args:
            players.append(p)
    if server_id in data:
        server_teams = data.get(server_id)
        count = len(server_teams)
        id = int(server_teams[count - 1].get("id")) + 1 if count > 0 else 1
        new_team = {"id": id, "game": game, "time": time, "players": players}
        server_teams.append(new_team)
    else:
        id = 1
        new_team = {"id": 1, "game": game, "time": time, "players": players}
        data[server_id] = [new_team]

    write_json(data)
    await ctx.send("Created team {}.".format(id))
    await ctx.send(embed=embed_team(new_team))


@bot.command()
@check_teams
async def teams(ctx, game=""):
    if game != "" and game not in game_format:
        await ctx.send(em.get("select_game"))
        return
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    teams_title = (
        "Teams " + date.today().strftime("%b %-d")
        if game == ""
        else game_format.get(game) + " Teams\n" + date.today().strftime("%b %-d")
    )
    embed = discord.Embed(title=teams_title, color=discord.Colour.dark_blue())
    for t in data[server_id]:
        if game != "" and t.get("game") != game:
            continue
        i = 1
        players = "\n"
        for p in t.get("players"):
            players += "{}. {}\n".format(i, p)
            i += 1
        team_name = (
            "Team {}\n{}\nTime: {}".format(
                str(t.get("id")), game_format.get(t.get("game")), t.get("time")
            )
            if game == ""
            else "Team {}\nTime: {}".format(str(t.get("id")), t.get("time"))
        )
        embed.add_field(
            name=team_name, value=players + "--------------------", inline=False
        )
    await ctx.send(embed=embed)


@bot.command()
@check_teams
async def join(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            if ctx.author.name.lower() in lowercase_players(t.get("players")):
                await ctx.send(em.get("existing_member"))
                return
            if len(t.get("players")) >= max_players.get(t.get("game")):
                await ctx.send(em.get("team_full"))
                return
            t.get("players").append(ctx.author.name)
            write_json(data)
            await ctx.send(embed=embed_team(t))
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_teams
async def leave(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            if ctx.author.name.lower() not in lowercase_players(t.get("players")):
                await ctx.send(em.get("non_member"))
            else:
                remove_player(t.get("players"), ctx.author.name)
                if len(t.get("players")) == 0:
                    data[server_id].remove(t)
                    await ctx.send("All players removed from team {}.".format(id))
                else:
                    await ctx.send("You have been removed from team {}.".format(id))
                    await ctx.send(embed=embed_team(t))
                write_json(data)
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_teams
async def add(ctx, id, *args):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            players = t.get("players")
            lc_players = lowercase_players(players)
            if ctx.author.name.lower() not in lc_players:
                await ctx.send(em.get("non_member"))
            elif len(players) == max_players.get(t.get("game")):
                await ctx.send(em.get("team_full"))
            elif len(args) != len(set(lowercase_players(args))):
                await ctx.send(em.get("duplicate_player"))
            elif len(args) + len(players) > max_players.get(t.get("game")):
                await ctx.send(em.get("too_many_players"))
            else:
                new_players = []
                for p in args:
                    if p.lower() not in lc_players:
                        players.append(p)
                        new_players.append(p)
                    else:
                        await ctx.send("{} is already part of the team!".format(p))
                write_json(data)
                if len(new_players) > 0:
                    await ctx.send(
                        "{} have been added to team {}.".format(
                            ", ".join(new_players), id
                        )
                    ) if len(new_players) > 1 else await ctx.send(
                        "{} has been added to team {}.".format(new_players[0], id)
                    )
                    await ctx.send(embed=embed_team(t))
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_teams
async def remove(ctx, id, *args):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            players = t.get("players")
            lc_players = lowercase_players(players)
            if ctx.author.name.lower() not in lc_players:
                await ctx.send(em.get("non_member"))
            elif len(args) != len(set(lowercase_players(args))):
                await ctx.send(em.get("duplicate_player"))
            elif len(players) - len(args) < 0:
                await ctx.send(em.get("too_many_players"))
            else:
                removed_players = []
                for p in args:
                    if p.lower() in lc_players:
                        remove_player(players, p)
                        removed_players.append(p)
                    else:
                        await ctx.send("{} is not part of the team!".format(p))
                if len(players) == 0:
                    data[server_id].remove(t)
                    await ctx.send("All players removed from team {}.".format(id))
                elif len(removed_players) > 0:
                    await ctx.send(
                        "{} have been removed from team {}.".format(
                            ", ".join(removed_players), id
                        )
                    ) if len(removed_players) > 1 else await ctx.send(
                        "{} has been removed from team {}.".format(
                            removed_players[0], id
                        )
                    )
                    await ctx.send(embed=embed_team(t))
                write_json(data)
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_teams
async def edit(ctx, id, time):
    if not (pattern.match(time)):
        await ctx.send(em.get("time"))
        return
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            if ctx.author.name.lower() not in lowercase_players(t.get("players")):
                await ctx.send(em.get("non_member"))
                return
            t.update({"time": time})
            write_json(data)
            await ctx.send("Team {}'s start time changed to {}.".format(id, time))
            await ctx.send(embed=embed_team(t))
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_teams
async def delete(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    for t in data[server_id]:
        if str(t.get("id")) == id:
            if ctx.author.name.lower() != t.get("players")[0].lower():
                await ctx.send(em.get("non_creator"))
                return
            data[server_id].remove(t)
            write_json(data)
            await ctx.send("Team {} has been deleted.".format(id))
            return
    await ctx.send(em.get("team_not_found"))


@bot.command()
@check_owner
@check_teams
async def destroy(ctx, id=""):
    server_id = str(ctx.message.guild.id)
    data = read_json("src/teams.json")
    if id != "":
        for t in data[server_id]:
            if str(t.get("id")) == id:
                data[server_id].remove(t)
                write_json(data)
                await ctx.send("Team {} has been deleted.".format(id))
                return
        await ctx.send(em.get("team_not_found"))
    else:
        data[server_id] = []
        write_json(data)
        await ctx.send("All teams removed.")


@tasks.loop(hours=24)
async def reset_teams():
    write_json({})


@reset_teams.before_loop
async def before():
    tz = pytz.timezone("America/Chicago")
    d = datetime.now(tz)
    if d.hour < 3:
        reset = datetime(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=3,
            minute=0,
            second=0,
            tzinfo=tz,
        )
    else:
        tomorrow = d + timedelta(days=1)
        reset = datetime(
            year=tomorrow.year,
            month=tomorrow.month,
            day=tomorrow.day,
            hour=3,
            minute=0,
            second=0,
            tzinfo=tz,
        )
    await asyncio.sleep((reset - d).total_seconds())
    await bot.wait_until_ready()


reset_teams.start()

bot.run(TOKEN)
