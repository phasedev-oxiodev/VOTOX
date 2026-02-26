import discord
from discord.ext import commands
import random
import datetime

class Utilities(commands.Cog):
    """Utility commands - fun and helpful tools for your server"""

    def __init__(self, bot):
        self.bot = bot

    # -----------------------
    # MESSAGES
    # -----------------------
    @commands.hybrid_command(name="say", description="Make the bot say something")
    async def say(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.hybrid_command(name="emoji", description="Send an emoji")
    async def emoji(self, ctx, emoji: str):
        await ctx.send(emoji)

    @commands.hybrid_command(name="reverse", description="Reverse text")
    async def reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

    @commands.hybrid_command(name="upper", description="Convert text to uppercase")
    async def upper(self, ctx, *, text: str):
        await ctx.send(text.upper())

    @commands.hybrid_command(name="lower", description="Convert text to lowercase")
    async def lower(self, ctx, *, text: str):
        await ctx.send(text.lower())

    @commands.hybrid_command(name="mock", description="Mock text in alternating case")
    async def mock(self, ctx, *, text: str):
        await ctx.send("".join([c.upper() if i % 2 else c.lower() for i, c in enumerate(text)]))

    @commands.hybrid_command(name="repeat", description="Repeat text multiple times")
    async def repeat(self, ctx, text: str, times: int = 1):
        await ctx.send(text * times)

    @commands.hybrid_command(name="shrug", description="Send a shrug")
    async def shrug(self, ctx):
        await ctx.send("¯\\_(ツ)_/¯")

    @commands.hybrid_command(name="tableflip", description="Flip a table")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°)╯︵ ┻━┻")

    @commands.hybrid_command(name="unflip", description="Unflip a table")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    # -----------------------
    # RANDOM & PICK
    # -----------------------
    @commands.hybrid_command(name="randomnumber", description="Generate a random number")
    async def randomnumber(self, ctx, min: int = 1, max: int = 100):
        await ctx.send(str(random.randint(min, max)))

    @commands.hybrid_command(name="pick", description="Pick one option")
    async def pick(self, ctx, option1: str, option2: str, option3: str = None):
        options = [option1, option2]
        if option3:
            options.append(option3)
        await ctx.send(f"Picked: {random.choice(options)}")

    @commands.hybrid_command(name="rolldice", description="Roll a dice")
    async def rolldice(self, ctx, sides: int = 6):
        await ctx.send(f"Rolled: {random.randint(1, sides)}")

    @commands.hybrid_command(name="color", description="Get a random color")
    async def color(self, ctx):
        c = discord.Color.random()
        await ctx.send(f"Random color: {c}")

    # -----------------------
    # TIME & DATE
    # -----------------------
    @commands.hybrid_command(name="time", description="Get the current UTC time")
    async def time(self, ctx):
        await ctx.send(f"UTC Time: {datetime.datetime.utcnow()}")

    @commands.hybrid_command(name="date", description="Get the current UTC date")
    async def date(self, ctx):
        await ctx.send(f"UTC Date: {datetime.datetime.utcnow().date()}")

    @commands.hybrid_command(name="uptime", description="Check bot uptime")
    async def uptime(self, ctx):
        await ctx.send("Bot uptime: Online now!")

    @commands.hybrid_command(name="ping", description="Check bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency*1000)}ms")

    # -----------------------
    # MATH COMMANDS
    # -----------------------
    @commands.hybrid_command(name="add", description="Add two numbers")
    async def add(self, ctx, a: int, b: int):
        await ctx.send(f"{a} + {b} = {a+b}")

    @commands.hybrid_command(name="subtract", description="Subtract two numbers")
    async def subtract(self, ctx, a: int, b: int):
        await ctx.send(f"{a} - {b} = {a-b}")

    @commands.hybrid_command(name="multiply", description="Multiply two numbers")
    async def multiply(self, ctx, a: int, b: int):
        await ctx.send(f"{a} × {b} = {a*b}")

    @commands.hybrid_command(name="divide", description="Divide two numbers")
    async def divide(self, ctx, a: int, b: int):
        if b == 0:
            await ctx.send("Cannot divide by zero")
        else:
            await ctx.send(f"{a} ÷ {b} = {a/b}")

    # -----------------------
    # COUNTDOWN
    # -----------------------
    @commands.hybrid_command(name="countdown", description="Countdown from a number")
    async def countdown(self, ctx, number: int):
        msg = "\n".join(str(i) for i in range(number, 0, -1))
        await ctx.send(msg)

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(Utilities(bot))