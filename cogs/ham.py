import os, sys, discord, platform, random, aiohttp, json, re, xmltodict, time, csv, wget, subprocess, xml.etree.ElementTree
from discord import embeds
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(embed=embed)

    @commands.command(name="dmr", aliases=["dmrid"])
    async def dmr(self, context, *, args):
        """
        Usage: !dmr <callsign/dmrid> - Get DMR ID from callsign, or vice-versa
        """
        callsign=re.sub(r'[^a-zA-Z0-9]','', args)
        try:
            int(callsign)
            requesttype="id"
            print(f"numeric input, search id {callsign}")
        except:
            requesttype="callsign"
            print(f"alphanumeric input, search callsign {callsign}")
        
        url = f"https://www.radioid.net/api/dmr/user/?{requesttype}={callsign}"
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
                    description=f"{requesttype} {callsign} not found",
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
                callsign = response['results'][0]['callsign']
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=f"{callsign} (for {context.message.author.display_name})", avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(outputtext, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(outputtext, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(outputtext)

    @commands.command(name="qrz", aliases=["call","lookup","dox"])
    async def qrz(self, context, *, args):
        """
        Usage: !qrz <callsign> - Lookup callsign on qrz.com
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        redditurl = "https://raw.githubusercontent.com/molo1134/qrmbot/master/lib/nicks.csv"
        redditfile = "resources/nicks.csv"
        callsign=cleanargs.upper()
        current_time = time.time()
        if os.path.isfile(redditfile):
            print("nicks.csv found")
            creation_time = os.path.getctime(redditfile)
            if (current_time - creation_time) // (24 * 3600) >= 28:
                print("file over 28 days old, fetching current version (<1MB)\n")
                os.unlink(redditfile)
                wget.download(redditurl, redditfile)
            else:
                print("nicks.csv current\n")
        else:
            print("fetching reddit hams csv file (<1MB)\n")
            wget.download(redditurl, redditfile)
        with open(redditfile) as rf:
            csv_rf = csv.reader(rf, delimiter=',')
            redditor=0
            redditname=""
            for row in csv_rf:
                if row[0].upper()==cleanargs.upper():
                    redditor=1
                    redditname=row[2]
                    break
                else:
                    redditor=0
#        qrzpassword=urllib.parse.quote(config.QRZ_PASSWORD, safe='')
#        keyurl = f"https://xmldata.qrz.com/xml/current/?username={config.QRZ_USERNAME};password={qrzpassword}"
#        async with aiohttp.ClientSession() as session:
#            raw_response = await session.get(keyurl)
#            response = await raw_response.text()
#            response = xmltodict.parse(response)
#            sessionkey=response['QRZDatabase']['Session']['Key']
#            url = f"https://xmldata.qrz.com/xml/current/?s={sessionkey};callsign={cleanargs.upper()}"
#            raw_response = await session.get(url)
#            response = await raw_response.text()
        response=subprocess.check_output(f"./qrz --xml {callsign}",shell=True)
        response=xmltodict.parse(response)
        print(response)
        if redditor==1:
            qrzlogo=file = discord.File("images/qrz+reddit.png", filename="qrz.png")
        else:
            qrzlogo=file = discord.File("images/qrz.png", filename="qrz.png")
        try:
            callsign=response['QRZDatabase']['Callsign']['call']
            embed = discord.Embed(
                title=f"QRZ lookup result:",
                color=0x00FF00
            )
            embed.add_field(
                name="Callsign:",
                value=f"[{callsign}](https://www.qrz.com/db/{callsign})",
                inline=True
            )
            try:
                embed.add_field(
                    name="Aliases:",
                    value=response['QRZDatabase']['Callsign']['aliases'],
                    inline=True
                )
            except:
                pass
            try:
                firstname=response['QRZDatabase']['Callsign']['fname']
                lastname=response['QRZDatabase']['Callsign']['name']
                name=f"{firstname} {lastname}"
            except:
                try:
                    name=response['QRZDatabase']['Callsign']['name']
                except:
                    try:
                        name=response['QRZDatabase']['Callsign']['fname']
                    except:
                        name=""
            embed.add_field(
                name="Name:",
                value=name,
                inline=True
            )
            try:
                embed.add_field(
                    name="Born:",
                    value=response['QRZDatabase']['Callsign']['born'],
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name="QSL via:",
                    value=response['QRZDatabase']['Callsign']['qslmgr'],
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name="Email:",
                    value=response['QRZDatabase']['Callsign']['email'],
                    inline=True
                )
            except:
                pass
            if redditor==1 and redditname!="":
                embed.add_field(
                    name="Reddit:",
                    value=redditname[1:],
                    inline=True
                )
            else:
                pass
            try:
                embed.add_field(
                    name="QTH:",
                    value=f"{response['QRZDatabase']['Callsign']['addr1']}, {response['QRZDatabase']['Callsign']['addr2']}",            
                    inline=True
                )
            except:
                embed.add_field(
                    name="QTH:",
                    value=response['QRZDatabase']['Callsign']['addr2'],            
                    inline=True
                )
            try:
                embed.add_field(
                    name="Attn:",
                    value=response['QRZDatabase']['Callsign']['attn'],            
                    inline=True
                )
            except:
                pass
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
            try:
                embed.add_field(
                    name="Grid:",
                    value=response['QRZDatabase']['Callsign']['grid'],
                    inline=True
                )
            except:
                pass
            try:
                user=context.message.author.id
                qthfile=f"resources/locations.json"
                justincaseempty=open(qthfile,"a")
                justincaseempty.close
                with open(qthfile,"r") as qthjson:
                    try:
                        data = json.loads(qthjson.read())
                        try:
                            coords = data[f"{user}"]
                        except:
                            pass
                    except:
                        pass
                if coords:
                    howfar=await general.howfar(response['QRZDatabase']['DXCC']['lon'],response['QRZDatabase']['DXCC']['lat'],coords[0],coords[1])
                    distance=howfar[0]
                    bearing=howfar[1]
                    direction=howfar[2]
                    embed.add_field(
                        name="Distance:",
                        value=f"{distance} km, {bearing}°*({direction})*",
                        inline=True
                    )
            except:
                pass
        except:
            embed=discord.Embed(
                title=f":warning: QRZ error:",
                description=f"Callsign {cleanargs.upper()} not found",
                color=0xFF0000
            )
        embed.set_thumbnail(url=f"attachment://qrz.png")
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(file=qrzlogo, embed=embed, username=f"{callsign} (for {context.message.author.display_name})", avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
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
        dxcc=cleanargs.upper()
        try:
            embed = discord.Embed(
                title=f"DXCC for {dxcc}:",
                color=0x00FF00
            )
            embed.add_field(
                name="DXCC number:",
                value=response['QRZDatabase']['DXCC']['dxcc'],
                inline=True
            )
            dxcc=response['QRZDatabase']['DXCC']['name']
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
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=f"{dxcc} (for {context.message.author.display_name})", avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(ham(bot))
