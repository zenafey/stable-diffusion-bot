import discord
from zenlogger import Logger
import aiohttp
from io import BytesIO
from prodiapy import AsyncProdia, Prodia
import os

prodia = AsyncProdia(os.getenv("PRODIA"))
syncprodia = Prodia(os.getenv("PRODIA"))


logger = Logger("zenbot")


async def aload(image_url):
    async with aiohttp.ClientSession() as s:
        async with s.get(image_url) as r:
            r.raise_for_status()

            return BytesIO(await r.read())


async def inference(ctx, method, **kwargs):
    msg = await ctx.respond(f"<a:loading_line:1178306728861913118> Processing your request...")

    try:
        job = await method(**kwargs)
        result = await prodia.wait(job, raise_on_fail=False)

        if result.failed:
            await msg.edit_original_response(content=f"Job failed, please try again\nJob id: {result.job_id}")

        file = discord.File(await aload(result.image_url), filename=f"{result.job_id}.png")
        await msg.edit_original_response(content=f"**{kwargs.get('prompt') or 'Result'}** - {ctx.user.mention}",
                                         file=file)


    except Exception as e:
        logger.error(f"{e}")
        await msg.edit_original_response(content=f"Unknown error occurred")

