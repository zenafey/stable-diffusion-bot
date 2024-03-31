import discord
from discord import option
from discord.ext import commands

from resources.utils import logger, prodia, inference
from resources.constants import models, samplers, style_presets


@commands.slash_command(name="transform", description="Generate image using img2img")
@option("image", description="Photo for transforming, png format is recommended")
@option("prompt", description="Describe your request")
@option("negative_prompt", description="Describe things that shouldnt be on image",
        default="bad quality, FastNegativeV2, easynegative")
@option("model", description="Model name", choices=models[:20], default="v1-5-pruned-emaonly.safetensors [d7049739]")
@option("style_preset", choices=style_presets, default=None)
@option("steps", default=30, choices=[10, 20, 25, 30, 35, 40, 45, 50])
@option("cfg_scale", default=7, choices=[2, 5, 7, 10, 12, 15, 17, 20])
@option("denoising_strength", default=0.7, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
@option("seed", default=None)
@option("upscale", default=False, choices=[True, False])
@option("sampler", choices=samplers[:20], default="DPM++ SDE Karras")
@option("width", default=512, choices=[128, 256, 512, 768, 1024])
@option("height", default=512, choices=[128, 256, 512, 768, 1024])
async def transform_command(
        ctx,
        image: discord.Attachment,
        prompt: str,
        negative_prompt: str,
        model: str,
        style_preset: str,
        steps: int,
        cfg_scale: int,
        denoising_strength: float,
        seed: int,
        upscale: bool,
        sampler: str,
        width: int,
        height: int
):
    await inference(ctx,
                    prodia.sd.transform,
                    imageUrl=image.url,
                    model=model,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    style_preset=style_preset,
                    steps=steps,
                    cfg_scale=cfg_scale,
                    denoising_strength=denoising_strength,
                    seed=seed,
                    upscale=upscale,
                    sampler=sampler,
                    width=width,
                    height=height
    )


def setup(bot):
    logger.info("Loading transform command..")
    bot.add_application_command(transform_command)
