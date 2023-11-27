from zenlogger import Logger
import aiohttp
from io import BytesIO

logger = Logger("zenbot")


async def aload(image_url):
    async with aiohttp.ClientSession() as s:
        async with s.get(image_url) as r:
            r.raise_for_status()

            return BytesIO(await r.read())


