import discord
from discord.ext import commands

ALLOWED_USERS = [1320349118102769767, 1461537788754399232]

class ListServers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        # Permission check
        if ctx.author.id not in ALLOWED_USERS:
            return await ctx.send("You are not allowed to use this command.")

        if not self.bot.guilds:
            return await ctx.send("I am not in any servers.")

        embed = discord.Embed(
            title="Votox Server List",
            color=discord.Color.blurple()
        )

        for guild in self.bot.guilds:
            invite_link = "No permission"

            # Try to create invite
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    try:
                        invite = await channel.create_invite(
                            max_age=0,
                            max_uses=0,
                            reason="Server list command"
                        )
                        invite_link = invite.url
                        break
                    except:
                        continue

            embed.add_field(
                name=guild.name,
                value=invite_link,
                inline=False
            )

        embed.set_footer(text=f"Total Servers: {len(self.bot.guilds)}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ListServers(bot))
