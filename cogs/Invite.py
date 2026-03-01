import discord
from discord.ext import commands

class InviteCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="invite-bot")
    async def invite_bot(self, ctx: commands.Context):
        """Sends the bot's invite link via DM."""
        invite_link = "https://discord.com/oauth2/authorize?client_id=1477383391744888863&scope=bot%20applications.commands&permissions=8"
        try:
            await ctx.author.send(f"Here is the invite link for the bot:\n{invite_link}")
            await ctx.send(f"{ctx.author.mention}, I've sent you the invite link in DMs!")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I couldn't DM you. Please check your privacy settings.")

# In discord.py v2.x, setup function must be async
async def setup(bot: commands.Bot):
    await bot.add_cog(InviteCog(bot))