# Python Discord Bot For lids

## Description
This is a python discord bot for lids, made for use in our private server. It
was adapted from **[@kkrypt0nn](https://github.com/kkrypt0nn)**'s
bot template.

It has had some features added sofar such as dogecoin price, random cat
pictures, flipping text, a quote system and a couple of ham radio related commands.

lidbot uses some code and the list of known reddit hams from **[@molo1134's qrmbot](https://github.com/molo1134/qrmbot)** irc bot in the qrz command. this portion of the code is under the BSD 2-clause license, a copy of which is located in qrmbot.LICENSE.md. My bot in general draws heavy inspiration from his amazing bot project.

lidbot uses APRS (Amateur Packet Reporting System) data from **[aprs.fi](https://aprs.fi)'s** API

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
Usage: !addquote MessageID (Dev option in context menu)
   Or: !addquote MessageURL (copy message link in context menu on message you want to quote)
   Or: !addquote <DisplayName> quotetext (Display Name must be inside '<' and '>' if there are spaces in the name otherwise optional)
!quote - Display a quote (server specific)
Usage: !quote
   Or: !quote <quotenumber>
!quotesearch - Find a quote (server specific). Returns quotes via DM
Usage: !quotesearch <keyword>
!setgeo - Usage: !setgeo <location>
Set your location. location can be text (eg: "Melbourne vic"), decimal coords (eg: "-37.8136,144.9631", or grid square (eg: "QF22qf").)
This will mean you don't need to input your location when using !wx unless you want a different location.
!getgeo - Usage: !getgeo <location>
Check your saved location. this will be sent to you as a DM
!roll - Usage: !roll <args>
Roll dice. or flip coins. examples: "!roll 4d6 +5" "!privateroll d20" "!coin" "!d6" etc.
!jjj - Usage: !jjj
Returns currently playing song on Triple J
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
!aprs - Usage: !aprs <callsign-SSID>
Fetch latest APRS data for callsign-SSID from aprs.fi
eg: !aprs VK3DAN-9
```
#### Commands in Gonkphone Cog
```
!phonebook - Usage: !phonebook <query>
Look up a GONK subscriber's gonknumber by number, name, callsign, or partial name/callsign. (If called without a query it will DM you the full list)
```

## Authors
* **[vk3dan](https://github.com/vk3dan)** - That's me
* **[Krypton (@kkrypt0nn)](https://github.com/kkrypt0nn)** - Author of the template used

## License

This project is licensed under the Apache License 2.0 (except for the qrz portion of qrmbot that is mentioned above) - see the [LICENSE.md](LICENSE.md) file for details
