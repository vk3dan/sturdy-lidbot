"""
Copyright vk3dan 2021
Description:
This is lidbot, a bot for lids.
It has some fairly basic features, some from the template used, and
some written by myself, with some more hopefully coming soon.


Template used Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description from template:
This is a template to create your own discord bot in python.

Version: 2.3
"""

import discord, asyncio, os, platform, sys, random, requests, json
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter
from discord.utils import get
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page):
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()
intents.members = True

ser_pref={'845344210231623690':'?'}
def get_prefix(bot, msg):	
	try:
		return ser_pref[str(msg.guild.id)]
	except:
	    return config.BOT_PREFIX

bot = Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)

statuses = ['like a lid', 'with a baofeng', 'with myself', 'with my ding-ding',
    'you.', 'myself', 'with fireworks in garage', 'with matches', 'guitar', 'sportsball',
	'tag', 'ball', 'hardball', 'the fool', 'a doctor on tv', 'around', 'VHS tapes',
	'hard to get', 'basketball', 'football', 'stupid games', 'with SSTV', 'on Brandmeister',
	'on TGIF', 'on 98003', 'Gonk Simulator', 'THE GAME. You just lost.', 'with velcro']

penguins = {'There are always worse things, like penguin herpes.':'kd1ldo', 'Did you sexually abuse penguins?':'W0CSG', 'PENGWINS.':'W0CSG'}

gonksimeditions = [' ', '2', '3', '- Remastered', '2020: Gonkdemic', '2021', '2022',
	'2047: Gonkout', 'for kids', 'with bacon', 'for linux'] 

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("-------------------")

# Setup the game status task of the bot

async def status_task():
	await bot.wait_until_ready()
	while True:
		currentstatus=random.choice(statuses)
		if currentstatus=="Gonk Simulator":
			currentstatus=f"{currentstatus} {random.choice(gonksimeditions)}"
		await bot.change_presence(activity=discord.Game(currentstatus))
		await asyncio.sleep(60)

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
	for extension in config.STARTUP_COGS:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")

# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author == bot.user or message.author.bot:
		return
	else:
		if message.author.id not in config.BLACKLIST:
			# Process the command if the user is not blacklisted
			startwords=("73","73s","hi ","heya","ohaider","👋","night","later","l8r","l9r")
			endwords=(" 73"," 73s","nini"," gn"," night"," l8r"," l9r","👋")
			if message.content.lower().startswith(tuple(startwords)) or message.content.lower().endswith(tuple(endwords)):
				await message.add_reaction("👋")
			elif message.content == "88":
				await message.add_reaction("🫂")
				await message.add_reaction("💋")
			elif "gonk" in message.content.lower() and not message.content.startswith("!"):
				await message.add_reaction("🇬")
				await message.add_reaction("🇴")
				await message.add_reaction("🇳")
				await message.add_reaction("🇰")
			elif "penguin" in message.content.lower() or "🐧" in message.content:
				webhook = await message.channel.create_webhook(name="lidstuff")
				penguinquote, penguinnick = random.choice(list(penguins.items()))
				await webhook.send(penguinquote, username=penguinnick)
				await webhook.delete()
			await bot.process_commands(message)
		else:
			# Send a message to let the user know he's blacklisted
			context = await bot.get_context(message)
			embed = discord.Embed(
				title="You're blacklisted!",
				description="Ask the owner to remove you from the list if you think it's not normal.",
				color=0xFF0000
			)
			await context.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
	if payload.user_id == bot.user.id:
		return
	else:
		if payload.user_id not in config.BLACKLIST:
			# Process the command if the user is not blacklisted
			if payload.emoji.name == "🐘":
				guild=bot.get_guild(payload.guild_id)
				channel=bot.get_channel(payload.channel_id)
				msg = await channel.fetch_message(payload.message_id)
				reaction = get(msg.reactions, emoji=payload.emoji.name)
				if reaction and reaction.count > 1:
					return
				reactor=payload.member
				name=msg.author.display_name
				quote=msg.content
				quotefile=f"resources/{payload.guild_id}quotes.json"
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
				webhook = await channel.create_webhook(name="lidstuff")
				await webhook.send(embed=embed, username=reactor.display_name, avatar_url=reactor.avatar_url)
				await webhook.delete()

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})")

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
			title="Error!",
			description="This command is on a %.2fs cooldown" % error.retry_after,
			color=0xFF0000
		)
		await context.send(embed=embed)
	raise error

# Run the bot with the token
bot.run(config.TOKEN)
