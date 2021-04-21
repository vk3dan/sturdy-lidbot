import os, sys, discord, platform, random, aiohttp, json, re, xmltodict
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
        Usage: !dmr <callsign/dmrid> - Get DMR ID from callsign, or vice-versa
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
                    title=f"DMR ID result:",
                    color=0x00FF00
                )
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/829926368824918046.png")
                embed.add_field(
                    name="Callsign:",
                    value=response['results'][0]['callsign'],
                    inline=False
                )
                embed.add_field(
                    name="DMR ID(s):",
                    value=dmrid,
                    inline=False
                )
                embed.add_field(
                    name="Name:",
                    value=f"{response['results'][0]['fname']} {response['results'][0]['surname']}",
                    inline=True
                )
                embed.add_field(
                    name="QTH:",
                    value=f"{response['results'][0]['city']}, {response['results'][0]['state']}",
                    inline=True
                )
                embed.add_field(
                    name="Country:",
                    value=response['results'][0]['country'],
                    inline=True
                )
            await context.send(embed=embed)

    @commands.command(name="morse", aliases=["cw"])
    async def morse(self, context, *, args):
        """
        Usage: !morse <message> - Convert input text to morse code.
        """
        cleanargs=re.sub(r'[^\x00-\x7F]+',' ', args)
        outputtext=""
        with open("resources/morse.json") as file:
            morsejson = json.load(file)
        for char in cleanargs.lower():
            try:
                outputtext += morsejson[char]
            except KeyError:
                outputtext += ":shrug:"
            outputtext += " "
        await context.send(outputtext)

    @commands.command(name="demorse", aliases=["unmorse","uncw"])
    async def demorse(self, context, *, args):
        """
        Usage: !demorse <message in -- --- .-. ... . / -.-. --- -.. .> 
        Convert morse code input to text.
        """
        outputtext=""
        inputmorse=args.split("/")
        inputmorse = [word.split() for word in inputmorse]
        with open("resources/morse.json") as file:
            morsejson = json.load(file)
        morsejson.pop(" ")
        textdict={}
        for key, value in morsejson.items():
            textdict[value] = key
        for word in inputmorse:
            for char in word:
                try:
                    outputtext += textdict[char]
                except KeyError:
                    outputtext += ":shrug:"
            outputtext += " "
        await context.send(outputtext)

    @commands.command(name="qrz", aliases=["call","lookup","dox"])
    async def qrz(self, context, *, args):
        """
        Usage: !qrz <callsign> - Lookup callsign on qrz.com
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        qrzpassword=urllib.parse.quote(config.QRZ_PASSWORD, safe='')
        keyurl = f"https://xmldata.qrz.com/xml/current/?username={config.QRZ_USERNAME};password={qrzpassword}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(keyurl)
            response = await raw_response.text()
            response = xmltodict.parse(response)
            sessionkey=response['QRZDatabase']['Session']['Key']
            url = f"https://xmldata.qrz.com/xml/current/?s={sessionkey};callsign={cleanargs.upper()}"
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = xmltodict.parse(response)
        try:
            embed = discord.Embed(
                title=f"QRZ lookup result:",
                color=0x00FF00
            )
            qrzlogo=file = discord.File("images/qrz.png", filename="qrz.png")
            embed.set_thumbnail(url=f"attachment://qrz.png")
            embed.add_field(
                name="Callsign:",
                value=f"[{response['QRZDatabase']['Callsign']['call']}](https://www.qrz.com/db/{response['QRZDatabase']['Callsign']['call']})",
                inline=False
            )
            embed.add_field(
                name="Name:",
                value=f"{response['QRZDatabase']['Callsign']['fname']} {response['QRZDatabase']['Callsign']['name']}",
                inline=False
            )
            embed.add_field(
                name="QTH:",
                value=response['QRZDatabase']['Callsign']['addr2'],            
                inline=True
            )
            try:
                embed.add_field(
                    name="State:",
                    value=response['QRZDatabase']['Callsign']['state'],
                    inline=True
                )
            except KeyError:
                pass
            embed.add_field(
                name="Country:",
                value=response['QRZDatabase']['Callsign']['country'],
                inline=True
            )
        except:
            embed=discord.Embed(
                title=f":warning: QRZ error:",
                description=f"Callsign {cleanargs.upper()} not found",
                color=0xFF0000
            )
        await context.send(file=qrzlogo, embed=embed)

    @commands.command(name="dxcc", aliases=["country"])
    async def dxcc(self, context, *, args):
        """
        Usage: !dxcc <prefix/callsign/dxccnumber> - Lookup dxcc from
        number, callsign or prefix
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        qrzpassword=urllib.parse.quote(config.QRZ_PASSWORD, safe='')
        keyurl = f"https://xmldata.qrz.com/xml/current/?username={config.QRZ_USERNAME};password={qrzpassword}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(keyurl)
            response = await raw_response.text()
            response = xmltodict.parse(response)
            sessionkey=response['QRZDatabase']['Session']['Key']
            url = f"https://xmldata.qrz.com/xml/current/?s={sessionkey};dxcc={cleanargs.upper()}"
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = xmltodict.parse(response)
        try:
            embed = discord.Embed(
                title=f"DXCC for {cleanargs.upper()}:",
                color=0x00FF00
            )
            embed.add_field(
                name="DXCC number:",
                value=response['QRZDatabase']['DXCC']['dxcc'],
                inline=True
            )
            embed.add_field(
                name="Name:",
                value=response['QRZDatabase']['DXCC']['name'],
                inline=True
            )
            embed.add_field(
                name="Continent:",
                value=response['QRZDatabase']['DXCC']['continent'],            
                inline=True
            )
            embed.add_field(
                name="ITU zone:",
                value=response['QRZDatabase']['DXCC']['ituzone'],
                inline=True
            )
            embed.add_field(
                name="CQ zone:",
                value=response['QRZDatabase']['DXCC']['cqzone'],
                inline=True
            )
            try:
                embed.add_field(
                    name="Timezone:",
                    value=f"UTC {float(response['QRZDatabase']['DXCC']['timezone']):+.1f}",
                    inline=True
                )
            except KeyError:
                pass
            embed.add_field(
                name="Coordinates:",
                value=f"Lon: {response['QRZDatabase']['DXCC']['lon']}, Lat: {response['QRZDatabase']['DXCC']['lat']}",
                inline=True
            )
#            print(f"https://maps.geoapify.com/v1/staticmap?style=dark-matter-purple-roads&width=400&height=320&center=lonlat:{response['QRZDatabase']['DXCC']['lon']},{response['QRZDatabase']['DXCC']['lat']}&zoom=2&scaleFactor=1&marker=lonlat:{response['QRZDatabase']['DXCC']['lon']},{response['QRZDatabase']['DXCC']['lat']};type:awesome;color:%23e01401&apiKey={config.GEOAPIFY_API_KEY}")
#            embed.set_image(url=f"https://maps.geoapify.com/v1/staticmap?style=dark-matter-purple-roads&width=400&height=320&center=lonlat:{response['QRZDatabase']['DXCC']['lon']},{response['QRZDatabase']['DXCC']['lat']}&zoom=2&scaleFactor=1&marker=lonlat:{response['QRZDatabase']['DXCC']['lon']},{response['QRZDatabase']['DXCC']['lat']};type:awesome&apiKey={config.GEOAPIFY_API_KEY}")
        except:
            embed=discord.Embed(
                title=f":warning: DXCC error:",
                description=f"DXCC {cleanargs.upper()} not found",
                color=0xFF0000
            )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(ham(bot))
