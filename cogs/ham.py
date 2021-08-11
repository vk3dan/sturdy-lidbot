import os, sys, discord, platform, random, aiohttp, json, re, xmltodict, time, csv, wget, subprocess, xml.etree.ElementTree, math
from time import strftime
from datetime import datetime
from discord import embeds
from discord.ext import commands
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from dateutil import tz
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

    @commands.command(name="phonetics", aliases=["phoneticize", "phoneticise"])
    async def phonetics(self, context, *, args):
        """
        Usage: !phonetics <message> - Convert input text to random and sometimes humorous phonetics.
        """
        cleanargs=re.sub(r'[^A-Za-z0-9 ]+','', args)
        outputtext=""
        phlist=[]
        with open("/usr/share/dict/words") as file:
            phlist = file.readlines()
            for char in cleanargs:
                if char==" ":
                    pass
                elif char.isnumeric():
                    outputtext += f"{char} "
                else:
                    choices = [x.rstrip() for x in phlist if x.startswith(char)]
                    outputtext += random.choice(choices).replace("\'s","")
                    outputtext += " "
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
        response=subprocess.check_output(f"qrz --xml {callsign}",shell=True)
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
                    value=f"{response['QRZDatabase']['Callsign']['addr1']}\n{response['QRZDatabase']['Callsign']['addr2']}",            
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
                user=str(context.message.author.id)
                qthfile="resources/locations.json"
                justincaseempty=open(qthfile,"a")
                justincaseempty.close
                coords=[]
                with open(qthfile,"r") as qthjson:
                    try:
                        data = json.loads(qthjson.read())
                        try:
                            print(data[user])
                            coords = data[user]
                        except:
                            pass
                    except:
                        pass
                if coords:
                    howfar=await self.howfar(float(coords[0]),float(coords[1]),float(response['QRZDatabase']['Callsign']['lat']),float(response['QRZDatabase']['Callsign']['lon']))
                    print(howfar)
                    distance=howfar[0]
                    bearing=howfar[1]
                    direction=howfar[2]
                    embed.add_field(
                        name="Distance:",
                        value=f"{round(distance,2)} km\n{round(bearing)}° *({direction})*",
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

    @commands.command(name="aprs", aliases=["aprs.fi"])
    async def aprs(self, context, *, args=None):
        """
        Usage: !aprs <callsign-SSID>
        Fetch latest APRS data for callsign-SSID from aprs.fi
        eg: !aprs VK3DAN-9
        """
        if args==None:
            embed=discord.Embed(
                title=f":warning: Error:",
                description=f"No arguments:\nUsage: !aprs <callsign-SSID>",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        cleanargs=re.sub(r'[^a-zA-Z0-9\-]','', args)
        url = f"https://api.aprs.fi/api/get?name={cleanargs}&what=loc&apikey={config.APRS_FI_API_KEY}&format=json"
        # Async HTTP request
        headers={'User-Agent': config.APRS_FI_HTTP_AGENT}
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True),headers=headers) as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            print (response)
            response = json.loads(response)
            if response['result']=="fail":
                embed=discord.Embed(
                    title=f":warning: APRS.fi error:",
                    description=f"request failed",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            if response['found']==0:
                embed=discord.Embed(
                    title=f":warning: APRS.fi error:",
                    description=f"No entries found matching request",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            try:
                embed = discord.Embed(
                    title=f"APRS.fi data for {response['entries'][0]['srccall']}:",
                    color=0x00FF00
                )
                embed.add_field(
                    name="Callsign",
                    value=response['entries'][0]['srccall'],
                    inline=True
                )
                if response['entries'][0]['type']=="l":
                    type="APRS station"
                elif response['entries'][0]['type']=="a":
                    type="AIS"
                elif response['entries'][0]['type']=="i":
                    type="APRS item"
                elif response['entries'][0]['type']=="o":
                    type="APRS object"
                elif response['entries'][0]['type']=="w":
                    type="Weather station"
                else:
                    type="Unknown"
                embed.add_field(
                    name="Type:",
                    value=type,
                    inline=True
                )
                try:
                    time = int(response['entries'][0]['time'])
                    time = datetime.fromtimestamp(time, tz.UTC)
                    time = time.strftime("%Y-%m-%d %H:%M:%S UTC")
                    embed.add_field(
                        name="Time:",
                        value=time,            
                        inline=True
                    )
                except:
                    pass
                location=await self.geocode(f"{response['entries'][0]['lat']}, {response['entries'][0]['lng']}")
                for each in location['address_components']:
                    if 'locality' in each['types']:
                        locality = each['long_name']
                    if 'administrative_area_level_1' in each['types']:
                        state = each['long_name']
                    if 'country' in each['types']:
                        country = each['long_name']
                outputlocation= f"{locality}, {state}, {country}"
                embed.add_field(
                    name="Location:",
                    value=f"{outputlocation}\n{response['entries'][0]['lat']}, {response['entries'][0]['lng']}",
                    inline=True
                )
                try:
                    alt=round(float(response['entries'][0]['altitude']))
                    altft=round(alt*3.28084)
                    embed.add_field(
                        name="Altitude:",
                        value=f"{alt} m *({altft} ft)*",
                        inline=True
                    )
                except:
                    pass
                try:
                    direction=await self.direction_from_degrees(int(response['entries'][0]['course']))
                    speed=round(float(response['entries'][0]['speed']))
                    speedmph=round(speed*0.62137119223733)
                    embed.add_field(
                        name="Heading:",
                        value=f"{response['entries'][0]['course']}° ({direction})\n{speed} km/h *({speedmph} mph)*",
                        inline=True
                    )
                except:
                    pass
                try:
                    embed.add_field(
                        name="Comment:",
                        value=response['entries'][0]['comment'],
                        inline=True
                    )
                except:
                    pass
                embed.add_field(
                    name="Path:",
                    value=response['entries'][0]['path'],
                    inline=True
                )
            except:
                embed=discord.Embed(
                    title=f":warning: APRS.fi error:",
                    description=f"JSON read failed",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)


    async def geocode(self, location):
        geo = GoogleV3(api_key=config.GOOGLEGEO_API_KEY, user_agent="lidbot")
        try:
            output = geo.geocode(location).raw
            print(f"Google geocode request for {output['formatted_address']}")
        except:
            output = {1:1}
        return output

    async def howfar(self, startlat, startlon, finishlat, finishlon):
        startloc=(float(startlat),float(startlon))
        finishloc=(float(finishlat),float(finishlon))
        dLon = math.radians(finishlon) - math.radians(startlon)
        y = math.sin(dLon) * math.cos(math.radians(finishlat))
        x = math.cos(math.radians(startlat))*math.sin(math.radians(finishlat)) - math.sin(math.radians(startlat))*math.cos(math.radians(finishlat))*math.cos(dLon)
        bearing = math.degrees(math.atan2(y, x))
        if bearing < 0:
            bearing+= 360
        direction=await self.direction_from_degrees(bearing)
        output=[geodesic(startloc, finishloc).km, bearing, direction]
        return(output)

    async def direction_from_degrees(self, degrees):
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
        compass_direction = round(degrees / 22.5)
        return directions[compass_direction]

def setup(bot):
    bot.add_cog(ham(bot))
