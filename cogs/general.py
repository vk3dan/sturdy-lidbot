import os, sys, discord, platform, random, aiohttp, json, re, wolframalpha, subprocess, math, discord.ext, maidenhead,urllib.parse
from discord.ext.commands import context
from discord.embeds import Embed
from time import strftime
from discord.ext import commands
from currency_symbols import CurrencySymbols
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from discord import Webhook, RequestsWebhookAdapter
from datetime import datetime, time
from dateutil import relativedelta, tz
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get some useful (or not) information about the bot.
        """
        embed = discord.Embed(
            description="vk3dan's lidbot",
            color=0x00FF00
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="vk3dan",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config.BOT_PREFIX}",
            inline=False
        )
        embed.set_footer(
            text="lidbot is based on Krypton's Bot Template"
        )
        await context.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Get some useful (or not) information about the server.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x00FF00
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Pong!",
            value=f":ping_pong: server latency {self.bot.latency:.4}s",
            inline=True
        )
        embed.set_footer(
            text=f"Pong requested by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="ding")
    async def ding(self, context):
        """
        Check if the dong is alive.
        """
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Dong!",
            value=":eggplant:",
            inline=True
        )
        embed.set_footer(
            text=f"Dong requested by {context.message.author}"
        )
        await context.send(embed=embed)

#    @commands.command(name="invite")
#    async def invite(self, context):
#        """
#        Get the invite link of the bot to be able to invite it.
#        """
#        await context.send("I sent you a private message!")
#        await context.author.send(f"Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id={config.APPLICATION_ID}&scope=bot&permissions=8")

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author.display_name} • React to vote!"
        )
        await context.message.delete()
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
        """
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.', 'Eat my dongus ya fuckin\' nerd']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x00FF00
        )
        await context.send(embed=embed)

    @commands.command(name="btc", aliases=["bitcoin"])
    async def bitcoin(self, context,*,args=""):
        """
        Usage: !bitcoin <currency> - Gets the current price of bitcoin.
        output defaults to USD.
        """
        if len(args)==3:
            cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
            cur=cleanargs.upper()
        else:
            cur="USD"
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            rate = response['bpi']['USD']['rate'].replace(',', '')
            try:
                converted = await self.convertcurrency(rate, "USD", cur)
                cursymbol = CurrencySymbols.get_symbol(cur)
            except:
                embed = discord.Embed(
                    title=":warning: Bitcoin Error",
                    description="Currency error: check that you are requesting correct\nISO 4217 currency code",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            embed = discord.Embed(
                title="Bitcoin",
                color=0x00FF00
            )
            embed.add_field(
                name="Bitcoin price is:",
                value=f"{cursymbol}{converted:,.4f} {cur}",
                inline=False
            )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/256px-Bitcoin.svg.png")
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="doge", aliases=["dogecoin"])
    async def dogecoin(self, context,*,args=""):
        """
        usage: !doge <currency> - Gets the current price of dogecoin.
        output defaults to USD *TO THE MOON*.
        """
        if len(args)==3:
            cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
            cur=cleanargs.upper()
        else:
            cur="USD"
        url = "https://sochain.com/api/v2/get_price/DOGE/USD"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            rate=""
            exchangename=""
            numprices=0
            prices=[]
            for x in range(len(response['data']['prices'])):
                if float(response['data']['prices'][x]['price']) > 0.0:
                    prices.append(float(response['data']['prices'][x]['price']))
                    numprices+=1
            if numprices == 1:
                for x in range(len(response['data']['prices'])):
                    if float(response['data']['prices'][x]['price']) > 0.0:
                        rate = response['data']['prices'][x]['price']
                        exchangename = response['data']['prices'][x]['exchange']
            elif numprices == 0:
                embed = discord.Embed(
                    title=":warning: Doge Error",
                    description="Error: Doge API did not provide a price",
                    color=0xFF0000
                )
            else:
                rate = sum(prices) / numprices
                exchangename="Avg from multiple exchanges"
            try:
                converted = await self.convertcurrency(rate, "USD", cur)
                cursymbol = CurrencySymbols.get_symbol(cur)
            except:
                embed = discord.Embed(
                    title=":warning: Doge Error",
                    description="Currency error: check that you are requesting correct\nISO 4217 currency code",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            embed = discord.Embed(
                title="<:doge:829928818508431400> Dogecoin to the moon :rocket:",
                color=0x00FF00
            )
            if args.lower()=="doge":                   
                embed.add_field(
                    name="Dogecoin price is:",
                    value="1 doge = 1 doge",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Dogecoin price is:",
                    value=f"{cursymbol}{converted:,.7f} {cur} ({exchangename.capitalize()})",
                    inline=False
                )
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/829928818508431400.png")
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="cat", aliases=["kitty","neko"])
    async def kitty(self, context):
        """
        Fetch a random cat pic from r/catpics on reddit.
        """
        url = "https://www.reddit.com/r/catpics/random.json"
        # Async HTTP request
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),headers=headers) as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=f":cat: Have a cat!",
                color=0x00FF00
            )
            embed.add_field(
                name=f"{response[0]['data']['children'][0]['data']['title']} *by u/{response[0]['data']['children'][0]['data']['author']}*",
                value=f"[View on Reddit](https://reddit.com{response[0]['data']['children'][0]['data']['permalink']} 'View post on r/catpics')",
                inline=False
            )
            try:
                embed.set_image(url=f"https://i.redd.it/{response[0]['data']['children'][0]['data']['gallery_data']['items'][0]['media_id']}.jpg")
            except:
                embed.set_image(url=response[0]['data']['children'][0]['data']['url'])
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(embed=embed)

    @commands.command(name="stonk", aliases=["stock"])
    async def stonk(self, context, *, args):
        """
        Usage: !stonk <code> 
        Get some info about a stonk from its ticker code.
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9.]','', args)
        url = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols="+cleanargs
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            stonkname=""
            cursymbol = CurrencySymbols.get_symbol(response['quoteResponse']['result'][0]['financialCurrency'])
            try:
                stonkname=response['quoteResponse']['result'][0]['displayName']
            except:
                stonkname=response['quoteResponse']['result'][0]['longName']
            try:
                regularMarketPrice = round(float(f"{response['quoteResponse']['result'][0]['regularMarketPrice']}"),5)
                regularMarketChange = round(float(f"{response['quoteResponse']['result'][0]['regularMarketChange']}"),5)
                regularMarketChangePercent = round(float(f"{response['quoteResponse']['result'][0]['regularMarketChangePercent']}"),2)
                if regularMarketChange < 0:
                    directionEmoji = "<:red_arrow_down:821559140345315348>"
                elif regularMarketChange > 0:
                    directionEmoji = "<:green_arrow_up:821559109031559179>"
                else:
                    directionEmoji = ":sleeping:"
            except:
                embed = discord.Embed(
                    title=f":warning: Stonk error:",
                    description=f"symbol {cleanargs} not found.",
                    color=0xFF0000
                )
            else:
                embed = discord.Embed(
                    title=f":money_with_wings: Stonk: {stonkname} ({response['quoteResponse']['result'][0]['fullExchangeName']})",
                    description=f"{response['quoteResponse']['result'][0]['symbol']} market price is: {cursymbol}{regularMarketPrice} {response['quoteResponse']['result'][0]['financialCurrency']} ( {directionEmoji} {cursymbol}{regularMarketChange} | {regularMarketChangePercent}% change )",
                    color=0x00FF00
                )
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="gonk")
    async def gonk(self, context):
        """
        Gonk.
        """
        embed = discord.Embed(
            color=0x0000FF
        )
        embed.add_field(
            name="WHAT THE FUCK IS GONK?",
            value=":regional_indicator_g: :regional_indicator_o: :regional_indicator_n: :regional_indicator_k:",
            inline=True
        )
        embed_message = await context.send(embed=embed)
        await context.message.delete()
        await embed_message.add_reaction("🇬")
        await embed_message.add_reaction("🇴")
        await embed_message.add_reaction("🇳")
        await embed_message.add_reaction("🇰")
        
    @commands.command(name="apod")
    async def apod(self, context):
        """
        Uses NASA api to fetch the astronomy picture of the day.
        """
        url="https://api.nasa.gov/planetary/apod?api_key="+config.DATA_GOV_API_KEY
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=f":ringed_planet: NASA APOD {response['date']} {response['title']}",
                color=0x00FF00
            )
            embed.set_image(url=response['hdurl'])
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(embed=embed)

    @commands.command(name="wx", aliases=["weather"])
    async def wx(self, context, *args):
        """
        Usage: !wx <location>
        Fetch the weather for the place requested.
        """
        user=context.message.author.id
        location=[]
        if len(args)==0:
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
                cleanargs=f"{coords[0]}, {coords[1]}"
        else:
            cleanargs=re.sub(r'[^a-zA-Z0-9\,\. -]','', str(args))
        location=await self.geocode(cleanargs)
        if "1" in location:
            embed = discord.Embed(
                    title=":warning: Weather error",
                    description=f"place {cleanargs} not found",
                color=0xFF0000
                )
            await context.send(embed=embed)
            return 1
        for each in location['address_components']:
            if 'locality' in each['types']:
                locality = each['long_name']
            if 'administrative_area_level_1' in each['types']:
                state = each['long_name']
            if 'country' in each['types']:
                country = each['long_name']
        outputlocation= f"{locality}, {state}, {country}"
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={str(location['geometry']['location']['lat'])}&lon={str(location['geometry']['location']['lng'])}&exclude=minutely,hourly&appid="+config.OPENWEATHER_API_KEY
        print(url)
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            try:
                tempc = round(float(response['current']['temp']-272.15),1)
                tempf = round(float(response['current']['temp']*1.8-459.67),1)
                flc = round(float(response['current']['feels_like']-272.15),1)
                flf = round(float(response['current']['feels_like']*1.8-459.67),1)
                minc = round(float(response['daily'][0]['temp']['min']-272.15),1)
                minf = round(float(response['daily'][0]['temp']['min']*1.8-459.67),1)
                maxc = round(float(response['daily'][0]['temp']['max']-272.15),1)
                maxf = round(float(response['daily'][0]['temp']['max']*1.8-459.67),1)
                windspeedms = round(float(response['current']['wind_speed']),1)
                windspeedkmh = round(windspeedms * 3.6,1)
                windspeedmph = round(windspeedms * 2.236936,1)
                winddirection = await self.direction_from_degrees(int(response['current']['wind_deg']))
                gusts = ""
                windymfer=" "
                try:
                    gustspeedms = round(float(response['current']['wind_gust']),1)
                    gustspeedkmh = round(gustspeedms * 3.6,1)
                    gustspeedmph = round(gustspeedms * 2.246936,1)
                    if gustspeedkmh>90:
                        windymfer="\n**That's one windy motherfucker!**"
                    gusts = f" with gusts up to {gustspeedkmh} km/h | {gustspeedmph} mph{windymfer}"
                except:
                    pass
            except:
                embed = discord.Embed(
                    title=":warning: Weather error",
                    description=f"error occurred fetching weather data",
                color=0xFF0000
                )
            else:
                embed = discord.Embed(
                    title=f":sun_with_face: Weather for {outputlocation}",
                    description=f"**Current Conditions:** {response['current']['weather'][0]['description'].capitalize()}",
                    color=0x00FF00
                )
                embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{response['current']['weather'][0]['icon']}@2x.png")
                embed.add_field(name="Temperature:", value=f"{tempc} °C ({tempf} °F)", inline=True)
                embed.add_field(name="*Feels like:*", value=f"*{flc} °C ({flf} °F)*", inline=True)
                embed.add_field(name="Humidity:", value=f"{response['current']['humidity']}%", inline=True)
                embed.add_field(name="Daily Minimum:", value=f"{minc} °C ({minf} °F)", inline=True)
                embed.add_field(name="Daily Maximum:", value=f"{maxc} °C ({maxf} °F)", inline=True)
                embed.add_field(name="Pressure:", value=f"{response['current']['pressure']} hPa", inline=True)
                embed.add_field(name="Wind:", value=f"{winddirection} @ {windspeedkmh} km/h | {windspeedmph} mph{gusts}", inline=True)
                try:
                    embed.add_field(name=f"**ALERT: {response['alerts']['event']}** from {response['alerts']['sender_name']}", value=f"{response['alerts']['description']}", inline=False)
                except:
                    pass
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="ask", aliases=["wolfram"])
    async def askwolfram(self, context, *, args):
        """
        Usage: !ask <input> 
        Give a question, some math, whatever; get answer back hopefully.
        """
        try:
            client=wolframalpha.Client(config.WOLFRAMALPHA_API_KEY)
            res=client.query(args)
            response=next(res.results).text
            escapedargs=re.escape(args)
            print(escapedargs)
        except:
            embed = discord.Embed(
                title=":teacher: Wolfram|Alpha Error:",
                description="I don't have a good answer for that.",
                color=0xFF0000
            )
        else:
            embed = discord.Embed(
                title=":teacher: Wolfram|Alpha",
                color=0x00FF00
            )
            embed.add_field(name="My Answer:", value=response, inline=True)
        await context.send(embed=embed)

    @commands.command(name="exchange", aliases=["convertcurrency", "currency"])
    async def currency(self, context, *args):
        """
        Usage: !exchange <value> <sourcecurrency> <outputcurrency>
        For example !exchange 56 AUD USD
        Converts an amount of currency to another.
        """
        if len(args)==3:
            cleaninputamount=re.sub(r'[^0-9\.]','', args[0])
            in_cur=args[1].upper()
            out_cur=args[2].upper()
        elif len(args)==4:
            cleaninputamount=re.sub(r'[^0-9\.]','', args[0])
            in_cur=args[1].upper()
            out_cur=args[3].upper()
        else:
            embed = discord.Embed(
                title=":warning: Exchange Error",
                description="Input error: incorrect input.\nUsage: !exchange <value> <sourcecurrency> <outputcurrency>",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return
        try:
            convertedamount = await self.convertcurrency(cleaninputamount, in_cur, out_cur)
            inputcursymbol = CurrencySymbols.get_symbol(in_cur)
            if inputcursymbol == None:inputcursymbol=""
            outputcursymbol = CurrencySymbols.get_symbol(out_cur)
            if outputcursymbol == None:outputcursymbol=""
        except:
            embed = discord.Embed(
                title=":warning: Exchange Error",
                description="Currency error: check that you are using correct\nISO 4217 currency code",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                title=":coin: Exchange:",
                color=0x00FF00
            )
            embed.add_field(name="Input", value=f"{inputcursymbol}{float(cleaninputamount):,.2f} {in_cur}", inline=True)
            embed.add_field(name="Output", value=f"{outputcursymbol}{float(convertedamount):,.2f} {out_cur}", inline=True)
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="spacex")
    async def spacex(self, context):
        """
            Get info on next SpaceX launch.
        """
        url = "https://api.spacexdata.com/v4/launches/next"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            launchpadurl = f"https://api.spacexdata.com/v4/launchpads/{response['launchpad']}"
            raw_response = await session.get(launchpadurl)
            launchpadresponse = await raw_response.text()
            launchpadresponse = json.loads(launchpadresponse)
            launchtime = response['date_unix']
            launchtime = datetime.fromtimestamp(launchtime, tz.UTC)
            now = datetime.now(tz=tz.tzutc())
            countdown = relativedelta.relativedelta(launchtime, now)
            launchtime = launchtime.strftime("%Y-%m-%d %H:%M:%S UTC")
            cd = "L- "
            if countdown.days > 0:
                cd += f"{countdown.days} days, "
            if countdown.hours > 0:
                cd += f"{countdown.hours} hours, \n"
            if countdown.minutes > 0:
                cd += f"{countdown.minutes} mins, "
            cd += f"{countdown.seconds} secs"
            embed = discord.Embed(
                title="Next SpaceX launch:",
                color=0x00FF00
            )
            embed.add_field(name="Name:", value=f"{response['name']}", inline=False)
            if not str(response['links']['patch']['small']).startswith("https"):
                embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-256/spacex-282142.png")
            else:
                embed.set_thumbnail(url=response['links']['patch']['small'])
            if str(response['links']['wikipedia']).startswith("https"):
                embed.add_field(name="Wikipedia:", value=f"[{response['name']} page]({response['links']['wikipedia']})", inline=False)
            embed.add_field(name="Launch time:", value=launchtime, inline=True)
            embed.add_field(name="Launches in:", value=cd, inline=True)
            embed.add_field(name="Launches From:", value=f"{launchpadresponse['full_name']}, {launchpadresponse['region']}", inline=False)
            embed.add_field(name="Details:", value=response['details'])
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    @commands.command(name="reverse", aliases=["backwards", "reverseit"])
    async def reverseit(self, context, *, args):
        """
        Usage: !reverse <input text>
        Reverse text.
        """
        reversed=args[::-1]
        reverseduname=context.message.author.display_name[::-1]
        webhook = await context.channel.create_webhook(name="lidstuff")
        await webhook.send(reversed, username=reverseduname, avatar_url=context.message.author.avatar_url)
        await webhook.delete()
        await context.message.delete()

    @commands.command(name="missyelliot", aliases=["missy", "missify", "upsidedown"])
    async def missyelliot(self, context, *, args):
        """
        Usage: !missyelliot <input text>
        Put your thang down, flip it and reverse it.
        """
        missify = args[::-1]
        outputtext=""
        missifiedname=""
        nosjyssim = {}
        with open("resources/missify.json") as file:
            missyjson = json.load(file)
        for key, value in missyjson.items():
            nosjyssim[value] = key
        missyjson = {**missyjson, **nosjyssim}
        for char in missify:
            try:
                outputtext += missyjson[char]
            except KeyError:
                outputtext += " "
        for char in context.message.author.display_name:
            try:
                missifiedname += missyjson[char]
            except KeyError:
                missifiedname += " "
        filename="avatar.webp"
        await context.message.author.avatar_url.save(filename)
        avatarrotated=subprocess.check_output(f"/usr/bin/convert {filename} -rotate 180 png:-",shell=True)
        missifiedname = missifiedname[::-1]
        webhook = await context.channel.create_webhook(name="lidstuff")
        await webhook.edit(avatar=avatarrotated)
        await webhook.send(missifiedname, username=outputtext)
        await webhook.delete()
        await context.message.delete()

    @commands.command(name="addquote")
    async def addquote(self, context, *args):
        """
        Add a quote (server specific)
        Usage: !addquote MessageID (Dev option in context menu)
           Or: !addquote MessageURL (copy message link in context menu on message you want to quote)
           Or: !addquote <DisplayName> quotetext (Display Name must be inside '<' and '>' if there are spaces in the name otherwise optional)
        """
        if isinstance(context.message.channel, discord.channel.DMChannel):
            embed = discord.Embed(
                title=":warning: Error",
                description="Error adding quote: This command cannot be used in a DM as quotes can only be added from the server the quote should be associated with.\nPlease try again in a server channel.",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        inputstring=' '.join(args)
        if len(args)==0:
            embed = discord.Embed(
                title=":warning: Error",
                description="Error adding quote: no quote specified.\nUsage: !addquote <MessageID>\n   Or: !addquote <DisplayName> <quote>",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        elif args[0].isdecimal() or args[0].startswith("http"):
            if args[0].isdecimal():
                msgID=args[0]
            else:
                msgID=args[0].rsplit('/', 1)[-1]
            try:
                msg = await context.message.channel.fetch_message(msgID)
            except:
                embed = discord.Embed(
                    title=":warning: Error",
                    description=f"Error adding quote: Message {msgID} not found",
                    color=0xFF0000
                )
                await context.send(embed=embed)
                return 1
            member=msg.guild.get_member(msg.author.id)
            name=member.nick
            if name==None or name=="" or name=="None":
                name=msg.author.display_name
            quote=msg.content
        elif str(args[0]).startswith("["):
            inputstring=re.sub(r'\[.+?\] ', '', inputstring)
            if inputstring.startswith("<"):
                name, sep, quote=inputstring.partition('> ')
                if quote=="":
                    name, sep, quote=inputstring.partition('>: ')
                name = name[1:]
        elif str(args[0]).startswith("<"):
            name, sep, quote=inputstring.partition('> ')
            if quote=="":
                name, sep, quote=inputstring.partition('>: ')
            name = name[1:]
        else:
            name=args[0]
            quote=' '.join(args[1:])
        if name.endswith(":"):
            name= re.sub(r'(:)(?=$)',r'',name)
        quotefile=f"resources/{context.message.guild.id}quotes.json"
        justincaseempty=open(quotefile,"a")
        justincaseempty.close
        with open(quotefile,"r") as quotejson:
            try:
                data = json.loads(quotejson.read())
            except:
                data={}
            quotes={}
            quotenum=len(data)+1
            quotes[int(quotenum)]={
                'name':name,
                'quote':quote
            }
        data.update(quotes)
        data=json.dumps(data)
        with open(quotefile,"w") as quotejson:
            quotejson.write(data)
        embed = discord.Embed(
            title="Quote added",
            description=f"Added quote {quotenum} - \"{name}: {quote}\" to quotes",
            color=0x00FF00
        )
        webhook = await context.channel.create_webhook(name="lidstuff")
        await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
        await webhook.delete()
        await context.message.delete()

    @commands.command(name="quote")
    async def quote(self, context, *, args=""):
        """
        Display a quote (server specific)
        Usage: !quote
           Or: !quote <quotenumber>
        """
        if isinstance(context.message.channel, discord.channel.DMChannel):
            embed = discord.Embed(
                title=":warning: Error",
                description="Error: Quotes can only be accessed from the server they are associated with.\nPlease try again from a server channel.",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        quotefile=f"resources/{context.message.guild.id}quotes.json"
        if os.path.isfile(quotefile):
            print(f"{quotefile} found")
        else:
            embed = discord.Embed(
                title=":warning: Error",
                description=f"Quote data does not exist for {context.message.guild},\ntry adding a quote with !addquote first",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        with open(quotefile) as quotejson:
            quotes = json.loads(quotejson.read())
            quotemax=len(quotes)
            if args.isdecimal():
                if int(args)>quotemax:
                    embed = discord.Embed(
                        title=":warning: Error",
                        description=f"Quote number {args} does not exist yet.",
                        color=0xFF0000
                    )
                    await context.send(embed=embed)
                    return 1
                else:
                    quotenum=int(args)
            else:
                quotenum=random.randint(1, quotemax)
            print(f"Displaying quote {quotenum}:")
            name=quotes[f"{quotenum}"]['name']
            quote=quotes[f"{quotenum}"]['quote']
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.send(quote, username=f"{name} ({quotenum})", avatar_url="http://2.bp.blogspot.com/-xJg2euabxZo/UjDaFUUJmUI/AAAAAAAAAM0/y0ILnK5A0bg/s1600/quotes.png")
            await webhook.delete()

    @commands.command(name="quotesearch", aliases=["searchquote", "findquote"])
    async def quotesearch(self, context, *, args=""):
        """
        Find a quote (server specific). Returns quotes via DM
        Usage: !quotesearch <keyword>
        """
        if isinstance(context.message.channel, discord.channel.DMChannel):
            embed = discord.Embed(
                title=":warning: Error",
                description="Error: Quotes can only be searched from the server they are associated with.\nPlease try again from a server channel.",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        quotefile=f"resources/{context.message.guild.id}quotes.json"
        if os.path.isfile(quotefile):
            print(f"{quotefile} found")
        else:
            embed = discord.Embed(
                title=":warning: Error",
                description=f"Quote data does not exist for {context.message.guild},\ntry adding a quote with !addquote first",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        if args=="":
            embed = discord.Embed(
                title=":warning: Error",
                description="Input error. Usage !quotesearch <keyword>",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return 1
        keyword=args
        matchlist=""
        with open(quotefile) as quotejson:
            quotes = json.loads(quotejson.read())
            quotemax=len(quotes)+1
            for i in range(1,quotemax):
                name=quotes[f"{i}"]['name']
                quote=quotes[f"{i}"]['quote']
                if keyword.lower() in name.lower() or keyword.lower() in quote.lower():
                    if matchlist=="":
                        matchlist+=f"Quotes found for server ***{context.message.guild}***:\n"
                    matchlist+=f"Quote {i}: {name}: {quote}\n"
        if matchlist=="":
            matchlist+=f"No quotes found matching {keyword.lower()} for server ***{context.message.guild}***"
        user=context.message.author
        await user.send(matchlist)
        await context.send(f"DM sent to {user.mention}")
        await context.message.delete()

    @commands.command(name="setgeo")
    async def setgeo(self, context, *args):
        """
        Usage: !setgeo <location>
        Set your location. location can be text (eg: "Melbourne vic"), decimal coords (eg: "-37.8136,144.9631", or grid square (eg: "QF22qf").)
        This will mean you don't need to input your location when using !wx unless you want a different location.
        """
        if len(args)==0:
            embed = discord.Embed(
                title=":warning: Error",
                description="Error: No location provided.\nUsage: !setgeo <location>\nlocation can be text (eg: \"Melbourne vic\"), decimal coords (eg: \"-37.8136,144.9631\", or grid square. eg: \"QF22le\"",
                color=0xFF0000
            )
            await context.send(embed=embed) 
            return 1
        qthfile="resources/locations.json"
        justincaseempty=open(qthfile,"a")
        justincaseempty.close
        with open(qthfile,"r") as qthjson:
            try:
                data = json.loads(qthjson.read())
            except:
                data={}
        user=context.message.author.id
        qthjson=""
        coords=[]
        argstr=' '.join(args)
        if re.search("^[-+]?[0-9]*\.?[0-9]+[, ]+[-+]?[0-9]*\.?[0-9]+",argstr):
            coords=argstr.split(',')
            if coords[1].startswith(" "):
                coords[1][:1]
            coords=[float(i) for i in coords]
            print(coords)
        elif re.match("[a-zA-Z][a-zA-Z][0-9]+", argstr):
            coords=list(maidenhead.to_location(argstr,center=True))
        else:
            try:
                location = await self.geocode(argstr)
                coords = [location['geometry']['location']['lat'], location['geometry']['location']['lng']]
                print(coords)
            except:
                embed = discord.Embed(
                    title=":warning: Error",
                    description="Error: Input error.\nUsage: !setgeo <location>\nlocation can be text (eg: \"Melbourne vic\"), decimal coords (eg: \"-37.8136,144.9631\", or grid square. eg: \"QF22le\"",
                    color=0xFF0000
                )
                await context.send(embed=embed) 
                return 1
        print(coords)
        data[str(user)]=[coords[0],coords[1]]
        with open(qthfile,"w") as qthjson:
            json.dump(data,qthjson,indent=4)
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            await context.send(f"DM sent to {context.message.author.mention}")
            await context.message.delete()
        await context.message.author.send(f"QTH set to {coords}") 

    @commands.command(name="getgeo")
    async def getgeo(self, context, *args):
        """
        Usage: !getgeo <location>
        Check your saved location. this will be sent to you as a DM
        """
        qthfile="resources/locations.json"
        justincaseempty=open(qthfile,"a")
        justincaseempty.close
        coords=[]
        user=context.message.author
        userid=str(context.message.author.id)
        with open(qthfile,"r") as qthjson:
            try:
                data = json.loads(qthjson.read())
                try:
                    coords = data[userid]
                except:
                    await user.send(f"Error: No QTH found for {user}")
                    await context.send(f"DM sent to {user.mention}")
                    return 1
            except:
                await context.send("Error opening location file.")
        await user.send(f"Saved QTH is {coords}")
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            await context.send(f"DM sent to {user.mention}")
            await context.message.delete()

    @commands.command(name="roll", aliases=["mobius", "flip", "coin", "d4", "d6", "d8", "d10", "d12", "d16", "d18", "d20", "d24", "d100", "privateroll", "proll"])
    async def roll(self, context, *args):
        """
        Usage: !roll <args>
        Roll dice. or flip coins. examples: "!roll 4d6 +5" "!privateroll d20" "!coin" "!d6" etc.
        """
        rng = random.SystemRandom()
        if len(args)==0:
            if context.invoked_with=="roll":
                sides="6"
            elif context.invoked_with.startswith("d"):
                sides=context.invoked_with[1:]
            elif context.invoked_with == "mobius":
                sides="1"
            elif context.invoked_with == "flip" or context.invoked_with == "coin":
                answer=rng.randint(0,6000)
                if answer<3000:
                    coinstate="HEADS"
                elif answer >3000:
                    coinstate="TAILS"
                else:
                    coinstate="EDGE.... it. landed. on. the. fucking. edge.\nTHAT CAN'T HAPPEN!"
                await context.send(f"The coin is showing {coinstate}")
                return
        elif re.match("^[1-9]?[0-9]?d[1-9][0-9]?[0-9]? ?([+-][0-9])?",''.join(args).lower()):
            change="0"
            op=""
            dies="1"
            if ("+" in ''.join(args)) or ("-" in ''.join(args)):
                if "+" in ''.join(args):
                    diesandsides,op,change=''.join(args).lower().partition("+")
                    if not diesandsides.startswith("d"):
                        dies,ded,sides=diesandsides.partition("d")
                    else:
                        sides=diesandsides[1:]
                else:
                    diesandsides,op,change=''.join(args).lower().partition("-")
                    if not diesandsides.startswith("d"):
                        dies,ded,sides=diesandsides.partition("d")
                    else:
                        sides=diesandsides[1:]
            else:
                if not ''.join(args).startswith("d"):
                    dies,ded,sides=''.join(args).lower().partition("d")
                else:
                    sides=''.join(args)[1:]
            changeint=int(change)
            sidesint=int(sides)
            if sidesint > 999:
                embed = discord.Embed(
                    title=":warning: Error",
                    description="Error: Too many sides.",
                    color=0xFF0000
                )
                await context.send(embed=embed) 
                return 1
            results=[]
            for x in range(int(dies)):
                results.append(str(rng.randint(1,int(sides))))
            resultsint = [int(s) for s in results]
            resultstotal=sum(resultsint)
            results = " + ".join(results)
            if op != "" and change != "0":
                if op=="+":
                    resultstotal=resultstotal + changeint
                if op=="-":
                    resultstotal=resultstotal - changeint
                results = f"{results} ({op}{change}) = {resultstotal}"
            else:
                if changeint == 0:
                    results = f"{results} = {resultstotal}"
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                if context.invoked_with=="privateroll" or context.invoked_with == "proll":
                    user=context.message.author
                    await user.send(f"You rolled {results}")
                    await context.send(f"DM sent to {user.mention}")
                else:
                    webhook = await context.channel.create_webhook(name="lidstuff")
                    await webhook.send(f"I rolled {results}", username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                    await webhook.delete()
            else:
                await context.send(f"You rolled {results}")
            return
        elif str(args[0]).isdecimal():
            sides=str(args[0])
        try:
            sidesint=int(sides)
            if sidesint > 999:
                raise Exception("Too many sides")
        except:
            embed = discord.Embed(
                    title=":warning: Error",
                    description="Error: I dunno what you did but this is... dice, it's not that hard to do this right lol.",
                    color=0xFF0000
            )
            await context.send(embed=embed) 
            return 1
        answer=rng.randint(1,sidesint)
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            if context.invoked_with=="privateroll" or context.invoked_with == "proll":
                user=context.message.author
                await user.send(f"You rolled {answer}")
                await context.send(f"DM sent to {user.mention}")
            else:
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(f"I rolled {answer}", username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
        else:
            await context.send(f"You rolled {answer}")

    @commands.command(name="jjj", aliases=["triplej"])
    async def jjj(self, context):
        """
        Usage: !jjj
        Returns currently playing song on Triple J
        """
        url="http://music.abcradio.net.au/api/v1/plays/search.json?limit=1&station=triplej"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            songname = response['items'][0]['recording']['title']
            artistname = response['items'][0]['recording']['artists'][0]['name']
            try:
                albumcover = response['items'][0]['recording']['releases'][0]['artwork'][0]['url']
            except:
                albumcover = "https://www.abc.net.au/cm/rimage/8558756-1x1-large.jpg?v=4"
            embed = discord.Embed(
                title="Currently playing on Triple J",
                color=0x00FF00
            )
            embed.add_field(
                name="Artist:",
                value=artistname,
                inline=True
            )
            embed.add_field(
                name="Track:",
                value=songname,
                inline=True
            )
            try:
                embed.set_image(url=albumcover)
            except:
                pass
            embed.add_field(
                name="Search for this track on:",
                value=f"[YouTube](https://www.youtube.com/results?search_query={urllib.parse.quote(artistname,safe='')}%20{urllib.parse.quote(songname,safe='')}) | [Spotify](https://play.spotify.com/search/{urllib.parse.quote(artistname,safe='')}%20{urllib.parse.quote(songname,safe='')})",
                inline=False
            )
            if not isinstance(context.message.channel, discord.channel.DMChannel):
                webhook = await context.channel.create_webhook(name="lidstuff")
                await webhook.send(embed=embed, username=context.message.author.display_name, avatar_url=context.message.author.avatar_url)
                await webhook.delete()
                await context.message.delete()
            else:
                await context.send(embed=embed)

    async def convertcurrency(self, amount, fromcurrency, tocurrency):
        currencyurl=f"https://v6.exchangerate-api.com/v6/{config.EXCHANGERATE_API_KEY}/latest/{fromcurrency}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(currencyurl)
            response = await raw_response.text()
            response = json.loads(response)
            answer = float(amount)*float(response['conversion_rates'][(tocurrency)])
            return answer

    async def geocode(self, location):
        geo = GoogleV3(api_key=config.GOOGLEGEO_API_KEY, user_agent="lidbot")
        try:
            output = geo.geocode(location).raw
            print(f"Google geocode request for {output['formatted_address']}")
            print(output)
        except:
            output = {1:1}
        print(output)
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
    bot.add_cog(general(bot))
