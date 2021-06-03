# Python Discord Bot For lids

## Description
This is a python discord bot for lids, made for use in our private server. It
was adapted from **[@kkrypt0nn](https://github.com/kkrypt0nn)**'s
bot template.

It has had some features added sofar such as dogecoin price, random cat
pictures, flipping text, a quote system and a couple of ham radio related commands.

lidbot uses some code from **[@molo1134's qrmbot](https://github.com/molo1134/qrmbot)** irc bot in the qrz command. this portion of the code is under the BSD 2-clause license, a copy of which is located in qrmbot.LICENSE.md. My bot in general draws heavy inspiration from his amazing bot project.

## Commands

#### Commands in General Cog
```
!info - Get some useful (or not) information about the bot.
!serverinfo - Get some useful (or not) information about the server.
!ping - Check if the bot is alive.
!ding - Check if the dong is alive.
!poll - Create a poll where members can vote.
!8ball - Ask any question to the bot.
!btc - Usage: !bitcoin <currency> - Gets the current price of bitcoin.
output defaults to USD.
!doge - usage: !doge <currency> - Gets the current price of dogecoin.
output defaults to USD *TO THE MOON*.
!cat - Fetch a random cat pic from r/catpics on reddit.
!stonk - Usage: !stonk <code> 
Get some info about a stonk from its ticker code.
!gonk - Gonk.
!apod - Uses NASA api to fetch the astronomy picture of the day.
!wx - Usage: !wx <location>
Fetch the weather for the place requested.
!ask - Usage: !ask <input> 
Give a question, some math, whatever; get answer back hopefully.
!exchange - Usage: !exchange <value> <sourcecurrency> <outputcurrency>
For example !exchange 56 AUD USD
Converts an amount of currency to another.
!spacex - Get info on next SpaceX launch.
!reverse - Usage: !reverse <input text>
Reverse text.
!missyelliot - Usage: !missyelliot <input text>
Put your thang down, flip it and reverse it.
!addquote - Add a quote (server specific)
Usage: !addquote MessageID
   Or: !addquote <DisplayName> quotetext (Display Name must be inside '<' and '>' if there are spaces in the name otherwise optional)
!quote - Display a quote (server specific)
Usage: !quote
   Or: !quote <quotenumber>
!quotesearch - Find a quote (server specific). Returns quotes via DM
Usage: !quotesearch <keyword>
```
#### Commands in Help Cog
```
!help - List all commands from every Cog the bot has loaded.
```
#### Commands in Owner Cog
```
!shutdown - Make the bot shutdown
!say - The bot will say anything you want.
!embed - The bot will say anything you want, but within embeds.
!blacklist - Lets you add or remove a user from not being able to use the bot.
```
#### Commands in Ham Cog
```
!bands - Fetch an image about HF band conditions.
!solar - Fetch an image about solar conditions.
!dmr - Usage: !dmr <callsign/dmrid> - Get DMR ID from callsign, or vice-versa
!morse - Usage: !morse <message> - Convert input text to morse code.
!demorse - Usage: !demorse <message in -- --- .-. ... . / -.-. --- -.. .> 
Convert morse code input to text.
!qrz - Usage: !qrz <callsign> - Lookup callsign on qrz.com
!dxcc - Usage: !dxcc <prefix/callsign/dxccnumber> - Lookup dxcc from
number, callsign or prefix
```

## Authors
* **[vk3dan](https://github.com/vk3dan)** - That's me
* **[Krypton (@kkrypt0nn)](https://github.com/kkrypt0nn)** - Author of the
  template used

To use this you can do the following:
* Clone/Download the repository
    * To clone it and get the updates you can definitely use the command
    `git clone`
* Create a discord bot [here](https://discord.com/developers/applications)
* Get your bot token
* Invite your bot on servers using the following invite:
https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot&permissions=8 (Replace `YOUR_APPLICATION_ID_HERE` with the application ID)

## How to setup

To setup the bot Krypton made it as simple as possible. he created a [config.py](config.py) file where you can put the needed things to edit.

Here is an explanation of what everything is:

| Variable          | What it is                                                            |
| ------------------| ----------------------------------------------------------------------|
| BOT_PREFIX        | The prefix(es) of your bot                                            |
| TOKEN             | The token of your bot                                                 |
| APPLICATION_ID    | The application ID of your bot                                        |
| OWNERS            | The user ID of all the bot owners                                     |
| BLACKLIST         | The user ID of all the users who can't use the bot                    |
| STARTUP_COGS      | The cogs that should be automatically loaded when you start the bot   |

Then there are various API keys that I have added for other features.

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows) or your Command Prompt (Windows).

Before running the bot you will need to install all the requirements with this command:
```
pip install -r requirements.txt
```

If you have multiple versions of python installed (2.x and 3.x) then you will need to use the following command:
```
python3 bot.py
```
or eventually
```
python3.8 bot.py
```
<br>

If you have just installed python today, then you just need to use the following command:
```
python bot.py
```

## Built With

* [Python 3.8](https://www.python.org/)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
