import os, sys, discord, platform, random, aiohttp, json, re, wolframalpha
from discord.ext import commands
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
            text=f"Based on Krypton's Bot Template\nRequested by {context.message.author}"
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
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
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
            text=f"Pong request by {context.message.author}"
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
            text=f"Dong request by {context.message.author}"
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
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
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
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.', 'Suck my dongus ya fuckin\' nerd']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="btc", aliases=["bitcoin"])
    async def bitcoin(self, context,*,args=""):
        """
        Usage: !bitcoin <currency> Gets the current price of bitcoin.
        defaults to USD, but can take other currency as an argument
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
            converted = await self.convertcurrency(rate, "USD", cur)
            embed = discord.Embed(
                title=":coin: Bitcoin",
                description=f"Bitcoin price is: ${converted:,.4f} {cur}",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="doge", aliases=["dogecoin"])
    async def dogecoin(self, context,*,args=""):
        """
        Get the current price of dogecoin in USD *TO THE MOON*.
        """
        if len(args)==3:
            cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
            cur=cleanargs.upper()
        else:
            cur="USD"
        url = "https://my.dogechain.info/api/v2/get_price/doge/usd"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            rate = response['data']['prices'][0]['price']
            converted = await self.convertcurrency(rate, "USD", cur)
            embed = discord.Embed(
                title="<:doge:805916026310492170> Dogecoin to the moon :rocket:",
                description=f"Dogecoin price is: ${converted:,.7f} {cur}",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="cat", aliases=["kitty","neko"])
    async def kitty(self, context):
        """
        Fetch a random cat pic from r/catpics on reddit.
        """
        url = "https://www.reddit.com/r/catpics/random.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=f":cat: {response[0]['data']['children'][0]['data']['title']}",
                color=0x00FF00
            )
            try:
                embed.set_image(url=f"https://i.redd.it/{response[0]['data']['children'][0]['data']['gallery_data']['items'][0]['media_id']}.jpg")
            except:
                embed.set_image(url=response[0]['data']['children'][0]['data']['url'])
            await context.send(embed=embed)

    @commands.command(name="stonk", aliases=["stock"])
    async def stonk(self, context, *, args):
        """
        Usage: !stonk <code> 
        Get some info about a stonk from its ticker code.
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        url = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols="+cleanargs
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            try:
                regularMarketPrice = round(float(f"{response['quoteResponse']['result'][0]['regularMarketPrice']}"),2)
                regularMarketChange = round(float(f"{response['quoteResponse']['result'][0]['regularMarketChange']}"),2)
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
                    title=f":money_with_wings: Stonk: {response['quoteResponse']['result'][0]['displayName']} ({response['quoteResponse']['result'][0]['fullExchangeName']})",
                    description=f"{response['quoteResponse']['result'][0]['symbol']} market price is: {regularMarketPrice} USD ( {directionEmoji} ${regularMarketChange} | {regularMarketChangePercent}% change )",
                    color=0x00FF00
                )
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
            await context.send(embed=embed)

    @commands.command(name="wx", aliases=["weather"])
    async def wx(self, context, *, args):
        """
        Usage: !wx <location>
        Fetch the weather for the place requested.
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9\, -]','', args)
        if re.match(".* ..$",cleanargs):
            cleanargs=f"{cleanargs[:-3]},{cleanargs[-3:]}"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cleanargs}&appid="+config.OPENWEATHER_API_KEY
        print(url)
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            try:
                tempc = round(float(response['main']['temp']-272.15),1)
                tempf = round(float(response['main']['temp']*1.8-459.67),1)
                flc = round(float(response['main']['feels_like']-272.15),1)
                flf = round(float(response['main']['feels_like']*1.8-459.67),1)
                minc = round(float(response['main']['temp_min']-272.15),1)
                minf = round(float(response['main']['temp_min']*1.8-459.67),1)
                maxc = round(float(response['main']['temp_max']-272.15),1)
                maxf = round(float(response['main']['temp_max']*1.8-459.67),1)
            except:
                embed = discord.Embed(
                    title=":warning: Weather error",
                    description=f"place {cleanargs} not found",
                color=0xFF0000
                )
            else:
                embed = discord.Embed(
                    title=f":sun_with_face: Weather for {response['name']}, {response['sys']['country']}",
                    description=f"**Current Conditions:** {response['weather'][0]['description'].capitalize()}",
                    color=0x00FF00
                )
                embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png")
                embed.add_field(name="Temperature:", value=f"{tempc} ºC ({tempf} ºF)", inline=True)
                embed.add_field(name="*Feels like:*", value=f"*{flc} ºC ({flf} ºF)*", inline=True)
                embed.add_field(name="Humidity:", value=f"{response['main']['humidity']}%", inline=True)
                embed.add_field(name="Daily Minimum:", value=f"{minc} ºC ({minf} ºF)", inline=True)
                embed.add_field(name="Daily Maximum:", value=f"{maxc} ºC ({maxf} ºF)", inline=True)
                embed.add_field(name="Pressure:", value=f"{response['main']['pressure']} hPa", inline=True)
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
                description=f"**Answer:** {response}",
                color=0x00FF00
            )
        await context.send(embed=embed)

    async def convertcurrency(self, amount, fromcurrency, tocurrency):
        currencyurl=f"https://v6.exchangerate-api.com/v6/{config.EXCHANGERATE_API_KEY}/latest/{fromcurrency}"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(currencyurl)
            response = await raw_response.text()
            response = json.loads(response)
            answer = float(amount)*float(response['conversion_rates'][(tocurrency)])
            return answer

def setup(bot):
    bot.add_cog(general(bot))
