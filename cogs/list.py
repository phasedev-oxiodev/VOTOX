import discord
from discord.ext import commands

class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    async def list_servers(self, ctx):
        if not self.bot.guilds:
            await ctx.send("The bot is not in any servers.")
            return

        embed = discord.Embed(
            title="Servers I'm In",
            color=discord.Color.green()
        )

        for guild in self.bot.guilds:
            invite_link = "No permission to create invite."

            # Try to create invite
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    try:
                        invite = await channel.create_invite(max_age=0, max_uses=0)
                        invite_link = invite.url
                        break
                    except:
                        continue

            embed.add_field(
                name=guild.name,
                value=f"Members: {guild.member_count}\nInvite: {invite_link}",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerList(bot))