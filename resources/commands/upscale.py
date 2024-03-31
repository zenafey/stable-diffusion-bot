import discord
from discord import option
from discord.ext import commands

from resources.utils import logger, prodia, inference


@commands.slash_command(name="upscale", description="Upscale image using Real-ESRGAN")
@option("image", description="Photo for upscaling, png format is recommended")
@option("resize", choices=[2, 4], default=2)
async def upscale_command(
        ctx,
        image: discord.Attachment,
        resize: int
):

    if 'image' not in image.content_type:
        await ctx.respond(content=f"Your attachment type isnt supported, please use png image.")
        return

    await inference(
        ctx,
        prodia.upscale,
        imageUrl=image.url,
        resize=resize
    )


def setup(bot):
    logger.info("Loading upscale command..")
    bot.add_application_command(upscale_command)
