import discord
from discord import option
from discord.ext import commands

from resources.utils import logger, prodia, inference


@commands.slash_command(name="swapface", description="Swap face inside an source with another target")
@option("source", description="Source photo(new face will be placed here)")
@option("target", description="Target photo(face from target will be placed on source image)")
async def swapface_command(
        ctx,
        source: discord.Attachment,
        target: discord.Attachment,
):
    await inference(ctx,
                    prodia.create,
                    endpoint="/faceswap",
                    sourceUrl=source.url,
                    targetUrl=target.url
    )


def setup(bot):
    logger.info("Loading swapface command..")
    bot.add_application_command(swapface_command)
