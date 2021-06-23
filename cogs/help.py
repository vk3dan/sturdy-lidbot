import os, sys, discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context):
        """
        List all commands from every Cog the bot has loaded.
        """
        prefix = config.BOT_PREFIX
        user=context.message.author
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands:", color=0x00FF00)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed = discord.Embed(title=f"Commands in {i.capitalize()} Cog", description=f'```{help_text}```', color=0x00FF00)
            await user.send(embed=embed)
        if not isinstance(context.message.channel, discord.channel.DMChannel):
            await context.send(f"DM sent to {user.mention}")
            await context.message.delete()

def setup(bot):
    bot.add_cog(Help(bot))