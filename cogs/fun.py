import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Fun Category - Fun commands for your Discord server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="8ball", description="Ask the magic ball a question")
    async def eight_ball(self, ctx, question: str):
        """Answers a question with a random response"""
        responses = ["Yes", "No", "Maybe", "Definitely!", "Ask later."]
        await ctx.send(f"🎱 {random.choice(responses)}")

    @commands.hybrid_command(name="dice", description="Roll a dice")
    async def dice(self, ctx):
        """Rolls a dice and displays the result"""
        await ctx.send(f"🎲 You rolled a `{random.randint(1,6)}`")

    @commands.hybrid_command(name="joke", description="Get a random joke")
    async def joke(self, ctx):
        """Displays a random joke"""
        jokes = [
            "Why did the developer go broke? Because he used up all his cache!",
            "Why do Java developers wear glasses? Because they don't see C#!",
            "I told my computer I needed a break... now it keeps sending me KitKats."
        ]
        await ctx.send(random.choice(jokes))

    @commands.hybrid_command(name="meme", description="Send a random meme (coming soon)")
    async def meme(self, ctx):
        """Displays a meme (feature coming soon)"""
        await ctx.send("🤣 Meme feature coming soon!")


async def setup(bot):
    """Loads the Fun category into the bot"""
    await bot.add_cog(Fun(bot))