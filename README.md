# Python Discord Bot For lids

## Description
This is a python discord bot for lids, made for use in our private server. It
was adapted from **[Krypton (@kkrypt0nn)](https://github.com/kkrypt0nn)**'s
bot template.

It has had some features added sofar such as dogecoin price, random cat
pictures and a couple of ham radio related commands.

## Commands

#### General
```
!info - Get some useful (or not) information about the bot.
!serverinfo - Get some useful (or not) information about the server.
!ping - Check if the bot is alive.
!ding - Check if the dong is alive.
!poll - Create a poll where members can vote.
!8ball - Ask any question to the bot.
!btc - Usage: !bitcoin <currency> Gets the current price of bitcoin.
defaults to USD, but can take other currency as an argument
!doge - Get the current price of dogecoin in USD *TO THE MOON*.
!cat - Fetch a random cat pic from r/catpics on reddit.
!stonk - Usage: !stonk <code> 
Get some info about a stonk from its ticker code.
!gonk - Gonk.
!apod - Uses NASA api to fetch the astronomy picture of the day.
!wx - Usage: !wx <location>
Fetch the weather for the place requested.
!ask - Usage: !ask <input> 
Give a question, some math, whatever; get answer back hopefully.
```
#### Help
```
!help - List all commands from every Cog the bot has loaded.
```
#### Owner
```
!shutdown - Make the bot shutdown
!say - The bot will say anything you want.
!embed - The bot will say anything you want, but within embeds.
!blacklist - Lets you add or remove a user from not being able to use the bot.
```
#### Ham
```
!bands - Fetch an image about HF band conditions.
!solar - Fetch an image about solar conditions.
!dmr - Get DMR ID from callsign, or vice-versa
!morse - Convert input text to morse code.
!demorse - Convert morse code to text.
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
