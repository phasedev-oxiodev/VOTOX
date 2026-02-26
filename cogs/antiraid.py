import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import sqlite3
from datetime import datetime, timezone

class AntiRaid(commands.Cog):
    """Anti-Raid / Anti-Nuke system with SQLite persistence"""

    def __init__(self, bot):
        self.bot = bot
        # Connect to SQLite
        self.conn = sqlite3.connect("antiraid.db")
        self.cursor = self.conn.cursor()
        # Create tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS whitelist (
                user_id INTEGER PRIMARY KEY
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()

        # Load initial settings
        self.lockdown = self._get_setting("lockdown") == "on"
        self.log_channel_id = int(self._get_setting("log_channel") or 0)
        # Channel backup (in memory, optional to persist)
        self.channel_backup = {}
        # Track recent role creations
        self.recent_role_creations = {}

    # -----------------------
    # Database helper methods
    # -----------------------
    def _get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def _set_setting(self, key, value):
        self.cursor.execute("INSERT INTO settings (key, value) VALUES (?, ?) "
                            "ON CONFLICT(key) DO UPDATE SET value = ?", (key, value, value))
        self.conn.commit()

    def _add_whitelist(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO whitelist(user_id) VALUES(?)", (user_id,))
        self.conn.commit()

    def _remove_whitelist(self, user_id):
        self.cursor.execute("DELETE FROM whitelist WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def _is_whitelisted(self, user_id):
        self.cursor.execute("SELECT 1 FROM whitelist WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone() is not None

    # -----------------------
    # SETTINGS COMMANDS
    # -----------------------
    @commands.command(name="whitelist-r")
    async def whitelist_cmd(self, ctx, member: discord.Member):
        self._add_whitelist(member.id)
        await ctx.send(f"✅ {member} added to whitelist.")

    @commands.command(name="unwhitelist-r")
    async def unwhitelist_cmd(self, ctx, member: discord.Member):
        self._remove_whitelist(member.id)
        await ctx.send(f"✅ {member} removed from whitelist.")

    @commands.command(name="setlogs-r")
    async def set_logs(self, ctx, channel: discord.TextChannel):
        self.log_channel_id = channel.id
        self._set_setting("log_channel", str(channel.id))
        await ctx.send(f"✅ Logging channel set to {channel.mention}")

    @commands.command(name="lockdown-r")
    async def lockdown_cmd(self, ctx, mode: str):
        if mode.lower() == "on":
            self.lockdown = True
            self._set_setting("lockdown", "on")
            await ctx.send("🚨 Lockdown enabled!")
        elif mode.lower() == "off":
            self.lockdown = False
            self._set_setting("lockdown", "off")
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
            now = datetime.now(timezone.utc)
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


        # Lockdown mode: prevent normal joins
        if self.lockdown and not self._is_whitelisted(member.id):
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
