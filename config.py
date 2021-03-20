# To use this bot you need to set up the bot in here,
# You need to decide the prefix you want to use,
# and you need your Token and Application ID from
# the discord page where you manage your apps and bots.
# You need your User ID which you can get from the
# context menu on your name in discord under Copy ID.
# if you want to make more than 30 requests per hour to 
# data.gov apis like nasa you will need to get an api key to
# replace "DEMO_KEY".

BOT_PREFIX = ("YOUR_BOT_PREFIX_HERE")
TOKEN = "YOUR_TOKEN_HERE"
APPLICATION_ID = "YOUR_APPLICATION_ID"
OWNERS = [123456789, 987654321]
DATA_GOV_API_KEY = "DEMO_KEY"
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
BLACKLIST = []
 # Default cogs that I use in the bot at the moment
STARTUP_COGS = [
    "cogs.general", "cogs.help", "cogs.owner", "cogs.ham",
]