from discord import option
from discord.ext import commands

from resources.utils import logger, prodia, inference
from resources.constants import models, samplers, style_presets


@commands.slash_command(name="generate", description="Generate image using text2img")
@option("prompt", description="Describe your request")
@option("negative_prompt", description="Describe things that shouldnt be on image",
        default="bad quality, FastNegativeV2, easynegative")
@option("model", description="Model name", choices=models[:20], default="v1-5-pruned-emaonly.safetensors [d7049739]")
@option("style_preset", choices=style_presets, default=None)
@option("steps", default=30, choices=[10, 20, 25, 30, 35, 40, 45, 50])
@option("cfg_scale", default=7, choices=[2, 5, 7, 10, 12, 15, 17, 20])
@option("seed", default=None)
@option("upscale", default=False, choices=[True, False])
@option("sampler", choices=samplers[:20], default="DPM++ SDE Karras")
@option("aspect_ratio", description="Will be overwritten if width/height is used",
        choices=["square", "landscape", "portrait"], default="square")
@option("width", default=512, choices=[128, 256, 512, 768, 1024])
@option("height", default=512, choices=[128, 256, 512, 768, 1024])
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
    await inference(ctx,
                    prodia.sd.generate,
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


def setup(bot):
    logger.info("Loading generate command..")
    bot.add_application_command(generate_command)
