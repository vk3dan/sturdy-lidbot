import os, sys, discord, platform, random, aiohttp, json
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

#    @commands.command(name="serverinfo")
#    async def serverinfo(self, context):
#        """
#        Get some useful (or not) information about the server.
#        """
#        server = context.message.guild
#        roles = [x.name for x in server.roles]
#        role_length = len(roles)
#        if role_length > 50:
#            roles = roles[:50]
#            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
#        roles = ", ".join(roles)
#        channels = len(server.channels)
#        time = str(server.created_at)
#        time = time.split(" ")
#        time = time[0]
#
#        embed = discord.Embed(
#            title="**Server Name:**",
#            description=f"{server}",
#            color=0x00FF00
#        )
#        embed.set_thumbnail(
#            url=server.icon_url
#        )
#        embed.add_field(
#            name="Owner",
#            value=f"{server.owner}\n{server.owner.id}"
#        )
#        embed.add_field(
#            name="Server ID",
#            value=server.id
#        )
#        embed.add_field(
#            name="Member Count",
#            value=server.member_count
#        )
#        embed.add_field(
#            name="Text/Voice Channels",
#            value=f"{channels}"
#        )
#        embed.add_field(
#            name=f"Roles ({role_length})",
#            value=roles
#        )
#        embed.set_footer(
#            text=f"Created at: {time}"
#        )
#        await context.send(embed=embed)

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

#    @commands.command(name="invite")
#    async def invite(self, context):
#        """
#        Get the invite link of the bot to be able to invite it.
#        """
#        await context.send("I sent you a private message!")
#        await context.author.send(f"Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id={config.APPLICATION_ID}&scope=bot&permissions=8")

#    @commands.command(name="server")
#    async def server(self, context):
#        """
#        Get the invite link of the discord server of the bot for some support.
#        """
#        await context.send("I sent you a private message!")
#        await context.author.send("Join my discord server by clicking here: https://discord.gg/HzJ3Gfr")

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
    async def bitcoin(self, context):
        """
        Get the current price of bitcoin in USD.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":coin: Bitcoin",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']} USD",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="doge", aliases=["dogecoin"])
    async def dogecoin(self, context):
        """
        Get the current price of dogecoin in USD *TO THE MOON*.
        """
        url = "https://my.dogechain.info/api/v2/get_price/doge/usd"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title="<:doge:805916026310492170> Dogecoin to the moon :rocket:",
                description=f"Dogecoin price is: ${response['data']['prices'][0]['price']} USD",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="cat", aliases=["kitty","neko"])
    async def kitty(self, context):
        """
        Fetch a random cat pic from reddit.
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
            embed.set_image(url=response[0]['data']['children'][0]['data']['url'])
            await context.send(embed=embed)

    @commands.command(name="stonk", aliases=["stock"])
    async def stonk(self, context, *, args):
        """
        Get some info about a stonk from its ticker code.
        """
        url = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols="+args
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            regularMarketPrice = round(float(f"{response['quoteResponse']['result'][0]['regularMarketPrice']}"),2)
            regularMarketChange = round(float(f"{response['quoteResponse']['result'][0]['regularMarketChange']}"),2)
            regularMarketChangePercent = round(float(f"{response['quoteResponse']['result'][0]['regularMarketChangePercent']}"),2)
            if regularMarketChange < 0:
                directionEmoji = "<:red_arrow_down:821559140345315348>"
            elif regularMarketChange > 0:
                directionEmoji = "<:green_arrow_up:821559109031559179>"
            else:
                directionEmoji = ":sleeping:"
            embed = discord.Embed(
                title=f":money_with_wings: Stonk: {response['quoteResponse']['result'][0]['displayName']} ({response['quoteResponse']['result'][0]['fullExchangeName']})",
                description=f"{response['quoteResponse']['result'][0]['symbol']} market price is: {regularMarketPrice} USD ( {directionEmoji} ${regularMarketChange} | {regularMarketChangePercent}% change )",
                color=0x00FF00
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
