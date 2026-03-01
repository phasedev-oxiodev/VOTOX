import discord
from discord.ext import commands

class NukeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nuke")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        """Nukes the current channel safely via a separate task."""
        guild = ctx.guild
        old_channel = ctx.channel

        # Save channel info
        name = old_channel.name
        category = old_channel.category
        overwrites = old_channel.overwrites or {}
        topic = old_channel.topic
        nsfw = old_channel.nsfw
        slowmode = old_channel.slowmode_delay
        position = old_channel.position

        # Create a temporary notification in another channel first
        # You can send in the first text channel of the guild if needed
        fallback_channel = guild.text_channels[0] if guild.text_channels else None
        if fallback_channel:
            await fallback_channel.send(f"{ctx.author.mention} nuked #{old_channel.name}!")

        # Schedule deletion + recreation as a background task
        async def recreate_channel():
            new_channel = await guild.create_text_channel(
                name=name,
                overwrites=overwrites,
                category=category,
                topic=topic,
                nsfw=nsfw,
                slowmode_delay=slowmode,
                reason=f"Nuked by {ctx.author}"
            )
            try:
                await new_channel.edit(position=position)
            except Exception:
                pass
            embed = discord.Embed(
                title="First Lol",
                description=f"{ctx.author.mention} nuked this channel!",
                color=discord.Color.red()
            )
            await new_channel.send(embed=embed)
            # Delete old channel
            try:
                await old_channel.delete()
            except Exception:
                pass

        # Run in the background
        ctx.bot.loop.create_task(recreate_channel())

# Async setup
async def setup(bot):
    await bot.add_cog(NukeCog(bot))