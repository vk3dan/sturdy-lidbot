import os, sys, discord, platform, random, aiohttp, json, re
from discord.ext import commands
import urllib.parse
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

    @commands.command(name="dmr", aliases=["dmrid"])
    async def dmr(self, context, *, args):
        """
        Get DMR ID from callsign, or vice-versa
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        try:
            int(cleanargs)
            requesttype="id"
            print(f"numeric input, search id {cleanargs}")
        except:
            requesttype="callsign"
            print(f"alphanumeric input, search callsign {cleanargs}")
        
        url = f"https://www.radioid.net/api/dmr/user/?{requesttype}={cleanargs}"
        print(url)
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            try:
                response = await raw_response.text()
                response = json.loads(response)
            except:
                embed=discord.Embed(
                    title=f":warning: DMR ID error:",
                    description=f"{requesttype} {cleanargs} not found",
                    color=0xFF0000
                )
            else:
                response = await raw_response.text()
                response = json.loads(response)
                for x in range(len(response['results'])):
                    if x==0:
                        dmrid=response['results'][0]['id']
                    else:
                        dmrid=f"{dmrid}, {response['results'][x]['id']}"
                embed = discord.Embed(
                    title=f"<:hytera:782159393822343209> DMR ID result:",
                    description=f"Callsign: {response['results'][0]['callsign']}\nDMR ID(s): {dmrid}\nName: {response['results'][0]['fname']} {response['results'][0]['surname']}\nQTH: {response['results'][0]['city']}, {response['results'][0]['state']}\nCountry: {response['results'][0]['country']}",
                    color=0x00FF00
                )
            await context.send(embed=embed)

    @commands.command(name="morse")
    async def morse(self, context, *, args):
        """
        Convert input text to morse code.
        """
        cleanargs=re.sub(r'[^\x00-\x7F]+',' ', args)
        cleanargs=urllib.parse.quote(cleanargs, safe='')
        url = f"http://www.morsecode-api.de/encode?string={cleanargs}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
        outputtext = response['morsecode'].replace(".......","/")
        await context.send(outputtext)

    @commands.command(name="demorse")
    async def demorse(self, context, *, args):
        """
        Convert morse code to text.
        """
        cleanargs=args.replace("/",".......")
        cleanargs=urllib.parse.quote(cleanargs, safe='')
        url = f"http://www.morsecode-api.de/decode?string={cleanargs}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
        await context.send(response['plaintext'])

def setup(bot):
    bot.add_cog(ham(bot))
