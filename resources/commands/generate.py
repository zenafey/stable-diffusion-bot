import discord
from discord import option
from discord.ext import commands

from resources.utils import logger, aload
from resources.constants import models, samplers, style_presets, loading_line
from resources.inference import prodia


@commands.slash_command(name="generate", description="Generate image using text2img")
@option("prompt", description="Describe your request")
@option("negative_prompt", description="Describe things that shouldnt be on image", default="bad quality")
@option("model", description="Model name", choices=models, default="v1-5-pruned-emaonly.safetensors [d7049739]")
@option("style_preset", choices=style_presets, default=None)
@option("steps", default=30, choices=[10, 20, 25, 30, 35, 40, 45, 50])
@option("cfg_scale", default=7, choices=[2, 5, 7, 10, 12, 15, 17, 20])
@option("seed", default=None)
@option("upscale", default=False, choices=[True, False])
@option("sampler", choices=samplers, default="DPM++ SDE Karras")
@option("aspect_ratio", choices=["square", "landscape", "portrait"], default="square")
async def generate_command(
        ctx,
        prompt: str,
        negative_prompt: str,
        model: str,
        style_preset: str,
        steps: int,
        cfg_scale: int,
        seed: int,
        upscale: bool,
        sampler: str,
        aspect_ratio: str
):
    msg = await ctx.respond(f"{loading_line} Generating image...")

    try:
        job = await prodia.sd.generate(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            style_preset=style_preset,
            steps=steps,
            cfg_scale=cfg_scale,
            seed=seed,
            upscale=upscale,
            sampler=sampler,
            aspect_ratio=aspect_ratio
        )
        result = await prodia.wait(job, raise_on_fail=False)

        if result.failed:
            await msg.edit_original_response(f"Job failed, please try again\nJob id: {result.job_id}")

        file = discord.File(await aload(result.image_url), filename=f"{result.job_id}.png")
        await msg.edit_original_response(content=f"**{prompt}** - {ctx.user.mention}", file=file)

    except Exception as e:
        logger.error(f"{e}")
        await msg.edit_original_response(f"Unknown error occurred")


def setup(bot):
    logger.info("Loading generate command..")
    bot.add_application_command(generate_command)
