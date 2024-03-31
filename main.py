from resources import load_env
import argparse
import os

import discord
from discord.ext import commands

from resources.utils import logger


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="^", intents=intents)


@bot.event
async def on_ready():
    try:
        bot.load_extension("resources.commands.generate")
        bot.load_extension("resources.commands.transform")
        bot.load_extension("resources.commands.swapface")
        bot.load_extension("resources.commands.upscale")
        bot.load_extension("resources.commands.help")

        logger.logs(f"Extensions loaded")
    except Exception as e:
        logger.error(f"Something went wrong while loading extensions:\n{e}")

    await bot.sync_commands()

    logger.logs(f"Logged in as {bot.user}")


@bot.command()
@commands.is_owner()
async def sync_commands(ctx):
    await bot.sync_commands()
    await ctx.reply("Commands are synced!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", choices=["dev", "prod"], default="dev")
    args = parser.parse_args()

    match args.env:
        case "prod":
            discord_token = os.getenv("DISCORD_PROD")
        case _:
            discord_token = os.getenv("DISCORD")

    bot.run(discord_token)
