import os, sys, discord, platform, random, aiohttp, json
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class ham(commands.Cog, name="ham"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="bands")
    async def bands(self, context):
        """
        Fetch an image about HF band conditions.
        """
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Bands",
            value="Band Conditions:",
            inline=True
        )
        embed.set_image(url="http://www.hamqsl.com/solarbc.php")
        embed.set_footer(
            text=f"Request by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="solar")
    async def solar(self, context):
        """
        Fetch an image about solar conditions.
        """
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Solar",
            value="Solar Conditions:",
            inline=True
        )
        embed.set_image(url="https://www.hamqsl.com/solarn0nbh.php?image=sdo_131")
        embed.set_footer(
            text=f"Request by {context.message.author}"
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(ham(bot))
