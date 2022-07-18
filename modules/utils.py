import io
import os
import discord
from PIL import Image
from pyppeteer import launch
from discord import app_commands
from discord.ext.commands import Bot, Cog


class UtilCog(Cog, name="Utility"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="applestatus", description="Get Apple's current system statuses.")
    async def apple_status(self, interaction: discord.Interaction):
        await interaction.response.defer()
        browser = await launch()
        page = await browser.newPage()
        await page.goto("https://www.apple.com/support/systemstatus/")
        await page.setViewport({'width': 1920, 'height': 1080})
        image = await page.screenshot()
        image = Image.open(io.BytesIO(image))
        image = image.crop((464, 95, 1454, 982))
        image.save("screenshot.png")
        await interaction.followup.send(file=discord.File("screenshot.png"))
        os.remove("screenshot.png")

    @app_commands.command(name="dev-applestatus", description="Get Apple's current dev system statuses.")
    async def dev_apple_status(self, interaction: discord.Interaction):
        await interaction.response.defer()
        browser = await launch()
        page = await browser.newPage()
        await page.goto("https://developer.apple.com/support/system-status/")
        await page.setViewport({'width': 1920, 'height': 1080})
        image = await page.screenshot()
        image = Image.open(io.BytesIO(image))
        # image = image.crop((464, 95, 1454, 982))
        image.save("screenshot.png")
        await interaction.followup.send(file=discord.File("screenshot.png"))
        os.remove("screenshot.png")

async def setup(client: Bot):
    await client.add_cog(UtilCog(client))
