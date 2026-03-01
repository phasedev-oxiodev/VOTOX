import discord
from discord.ext import commands

class Info(commands.Cog):
    """Information commands about users, roles, and channels"""

    def __init__(self, bot):
        self.bot = bot

    # -----------------------
    # USER INFO
    # -----------------------
    @commands.hybrid_command(name="userinfo", description="Get info about a user")
    async def userinfo(self, ctx, member: discord.Member = None):
        """Displays information about a user"""
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member}", color=0x7289da)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    # -----------------------
    # ROLE INFO
    # -----------------------
    @commands.hybrid_command(name="roleinfo", description="Get info about a role")
    async def roleinfo(self, ctx, role: discord.Role):
        """Displays information about a role"""
        embed = discord.Embed(title=f"🏷️ Role: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d"), inline=True)
        await ctx.send(embed=embed)

    # -----------------------
    # CHANNEL INFO
    # -----------------------
    @commands.hybrid_command(name="channelinfo", description="Get info about a channel")
    async def channelinfo(self, ctx, channel: discord.abc.GuildChannel = None):
        """Displays information about a channel"""
        channel = channel or ctx.channel
        embed = discord.Embed(title=f"📺 Channel: {channel.name}", color=0x95a5a6)
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Type", value=str(channel.type).title(), inline=True)
        embed.add_field(name="Created", value=channel.created_at.strftime("%Y-%m-%d"), inline=True)
        await ctx.send(embed=embed)

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(Info(bot))