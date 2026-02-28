import discord
from discord.ext import commands

class ListServers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        if not self.bot.guilds:
            return await ctx.send("I am not in any servers. But How To Did That Commands")

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
