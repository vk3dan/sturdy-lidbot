import os, sys, discord, wget, re, csv, time
from discord.ext import commands

# Only if you want to use variables that are in the config.py file.
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

# Here we name the cog and create a new class for the cog.
class gonkphone(commands.Cog, name="gonkphone"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="phonebook", aliases=["directory","gonkphone","gonkline"])
    async def phonebook(self, context, *, args=""):
        """
        Usage: !phonebook <query>
        Look up a GONK subscriber's gonknumber by number, name, callsign, or partial name/callsign. (If called without a query it will DM you the full list)
        """
        cleanargs=re.sub(r'[^a-zA-Z0-9]','', args)
        directoryurl = "https://docs.google.com/spreadsheets/d/1_2hc2sx31cFrpSXxE0SWSOc6-OD2sRHBHztcuRFdVoE/export?format=csv"
        directoryfile = "resources/GONKDirectory.csv"
        if os.path.isfile(directoryfile):
            os.unlink(directoryfile)
        wget.download(directoryurl, directoryfile)
        with open(directoryfile) as df:
            csv_df = csv.reader(df, delimiter=',')
            present=0
            name=""
            callsign=""
            number=""
            names=[]
            callsigns=[]
            numbers=[]
            rownum=0
            embed = discord.Embed(
                title=f"GONK directory lookup:",
                color=0x00FF00
            )
            if cleanargs == "":
                embed = discord.Embed(
                    title=f"GONK directory:",
                    color=0x00FF00
                )
                for row in csv_df:
                    rownum+=1
                    if rownum==1:
                        pass
                    else:
                        names.append(row[0])
                        callsigns.append(row[1])
                        numbers.append(row[2])
                embed.add_field(
                    name="Names:",
                    value="\n".join(names),
                    inline=True
                )
                embed.add_field(
                    name="Callsigns:",
                    value="\n".join(callsigns),
                    inline=True
                )
                embed.add_field(
                    name="Numbers:",
                    value="\n".join(numbers),
                    inline=True
                )
                user=context.message.author
                await user.send(embed=embed)
                if not isinstance(context.message.channel, discord.channel.DMChannel):
                    await context.message.delete()
                    await context.send(f"DM sent to {user.mention}")
                return 0
            elif cleanargs.isdecimal():
                rownum+=1
                if rownum==1:
                    pass
                else:
                    for row in csv_df:
                        if row[2]==cleanargs:
                            present=1
                            name=row[0]
                            number=row[2]
                            callsign=row[1]
                            embed.add_field(
                                name="Name:",
                                value=name,
                                inline=True
                            )
                            embed.add_field(
                                name="Callsign:",
                                value=callsign,
                                inline=True
                            )
                            embed.add_field(
                                name="Number:",
                                value=number,
                                inline=True
                            )
            else:
                for row in csv_df:
                    rownum+=1
                    if rownum==1:
                        pass
                    else:
                        if row[1].upper()==cleanargs.upper() or cleanargs.upper() in row[1].upper():
                            present=1
                            names.append(row[0])
                            callsigns.append(row[1])
                            numbers.append(row[2])
                        elif row[0].upper()==cleanargs.upper() or cleanargs.upper() in row[0].upper():
                            present=1
                            names.append(row[0])
                            callsigns.append(row[1])
                            numbers.append(row[2])
        if present==1:
            embed.add_field(
                name="Name(s):",
                value="\n".join(names),
                inline=True
            )
            embed.add_field(
                name="Callsign(s):",
                value="\n".join(callsigns),
                inline=True
            )
            embed.add_field(
                name="Number(s):",
                value="\n".join(numbers),
                inline=True
            )
        if present==0:
            embed = discord.Embed(
                title=f":warning: GONK directory lookup:",
                description=f"Error: \"{cleanargs}\" not found",
                color=0xFF0000
            )
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            avatarfile = open("images/gonk.png", "rb")
            avatar = avatarfile.read()
            webhook = await context.channel.create_webhook(name="lidstuff")
            await webhook.edit(avatar=avatar)
            await webhook.send(embed=embed, username=f"{cleanargs} (for {context.message.author.display_name})")
            await webhook.delete()
            await context.message.delete()
        else:
            await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(gonkphone(bot))