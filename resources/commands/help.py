import discord
from discord.ext import commands

from resources.utils import logger


class LinkButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        support_btn = discord.ui.Button(label='Support 💰', style=discord.ButtonStyle.blurple,
                                        url='https://www.donationalerts.com/c/zenafey')
        self.add_item(support_btn)


@commands.slash_command(name="help", description="Get help information")
async def help_command(ctx):
    embed = discord.Embed(
        title="Helpful Information",
        description="This bot is designed for text2img image generation using Prodia Stable Diffusion API, to get \
started use slash command /generate and enter image description in 'prompt' field.",
        color=0x2B2A4C
    )
    await ctx.respond(embed=embed, view=LinkButtonView())


def setup(bot):
    logger.info("Loading help command..")
    bot.add_application_command(help_command)
