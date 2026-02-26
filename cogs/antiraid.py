import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio

class AntiRaid(commands.Cog):
    """Anti-Raid / Anti-Nuke system"""

    def __init__(self, bot):
        self.bot = bot
        self.whitelist = set()  # user IDs exempt from protection
        self.lockdown = False
        self.log_channel_id = None
        self.channel_backup = {}  # {guild_id: [channel_data]}
        self.recent_role_creations = {}  # {guild_id: [timestamps]}

    # -----------------------
    # SETTINGS COMMANDS
    # -----------------------
    @commands.command(name="whitelist-r")
    async def whitelist_cmd(self, ctx, member: discord.Member):
        self.whitelist.add(member.id)
        await ctx.send(f"✅ {member} added to whitelist.")

    @commands.command(name="unwhitelist-r")
    async def unwhitelist_cmd(self, ctx, member: discord.Member):
        self.whitelist.discard(member.id)
        await ctx.send(f"✅ {member} removed from whitelist.")

    @commands.command(name="setlogs-r")
    async def set_logs(self, ctx, channel: discord.TextChannel):
        self.log_channel_id = channel.id
        await ctx.send(f"✅ Logging channel set to {channel.mention}")

    @commands.command(name="lockdown-r")
    async def lockdown_cmd(self, ctx, mode: str):
        if mode.lower() == "on":
            self.lockdown = True
            await ctx.send("🚨 Lockdown enabled!")
        elif mode.lower() == "off":
            self.lockdown = False
            await ctx.send("✅ Lockdown disabled.")
        else:
            await ctx.send("⚠️ Use `on` or `off`")

    # -----------------------
    # EVENTS
    # -----------------------
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Auto restore deleted channels"""
        guild = channel.guild
        if guild.id not in self.channel_backup:
            self.channel_backup[guild.id] = []
        # Backup minimal data
        self.channel_backup[guild.id].append((channel.name, channel.category, channel.type, channel.position))
        # Restore
        await asyncio.sleep(1)
        new_channel = await guild.create_text_channel(channel.name) if channel.type == discord.ChannelType.text else await guild.create_voice_channel(channel.name)
        if self.log_channel_id:
            log_channel = guild.get_channel(self.log_channel_id)
            if log_channel:
                await log_channel.send(f"🛡 Channel restored: {new_channel.name}")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Detect mass role creation"""
        guild_id = role.guild.id
        if role.guild.me.guild_permissions.manage_roles:
            now = discord.utils.utcnow()
            if guild_id not in self.recent_role_creations:
                self.recent_role_creations[guild_id] = []
            self.recent_role_creations[guild_id].append(now)
            # Keep only last 5 seconds
            self.recent_role_creations[guild_id] = [t for t in self.recent_role_creations[guild_id] if (now - t).total_seconds() < 5]
            if len(self.recent_role_creations[guild_id]) > 5:
                # Too many roles created, remove them
                if self.log_channel_id:
                    log_channel = role.guild.get_channel(self.log_channel_id)
                    if log_channel:
                        await log_channel.send(f"🚫 Mass role creation detected! Roles deleted.")
                async for r in role.guild.roles[::-1]:
                    if r.name != "@everyone" and r.managed is False:
                        try:
                            await r.delete()
                        except:
                            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Anti-bot protection and whitelist check"""
        if member.bot and member.id not in self.whitelist:
            try:
                await member.kick(reason="Anti-bot protection")
            except:
                pass
            if self.log_channel_id:
                log_channel = member.guild.get_channel(self.log_channel_id)
                if log_channel:
                    await log_channel.send(f"💣 Bot {member} was kicked automatically!")

        # Lockdown mode: prevent normal joins
        if self.lockdown and member.id not in self.whitelist:
            try:
                await member.kick(reason="Lockdown active")
            except:
                pass
            if self.log_channel_id:
                log_channel = member.guild.get_channel(self.log_channel_id)
                if log_channel:
                    await log_channel.send(f"🚨 {member} tried to join during lockdown")

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))