import discord
from discord.ext import commands

class PingResponder(commands.Cog):
    """Responds when someone pings the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots and DMs
        if message.author.bot or not message.guild:
            return

        # Check if the bot was mentioned
        if self.bot.user in message.mentions:
            await message.channel.send(f"Hey {message.author.mention}! Don't ping me please bruh 😅")

# Setup function to load the cog
async def setup(bot):
    await bot.add_cog(PingResponder(bot))