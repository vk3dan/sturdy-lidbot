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

import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
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

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents, case_insensitive=True)

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
	while True:
		await bot.change_presence(activity=discord.Game("like a lid"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with a baofeng"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with myself"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with my ding ding"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("you"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("myself"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with fireworks in garage"))
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
			startwords=("73","73s","hi","hey","heya","ohaider","gm","ga","ge","gn","👋","night","later","l8r","l9r")
			endwords=(" 73"," 73s","nini"," gn"," night"," l8r"," l9r","👋")
			if message.content.startswith(tuple(startwords)) or message.content.endswith(tuple(endwords)):
				await message.add_reaction("👋")
			elif message.content == "88":
				await message.add_reaction("🫂")
				await message.add_reaction("💋")
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
