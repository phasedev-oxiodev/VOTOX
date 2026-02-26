import discord
from discord.ext import commands
from collections import defaultdict
import time
import sqlite3

class AntiNuke(commands.Cog):
    """Anti-Nuke system with SQLite persistence"""

    def __init__(self, bot):
        self.bot = bot
        self.logs = defaultdict(list)
        self.threshold = 3
        self.time_window = 10  # seconds

        # SQLite setup
        self.conn = sqlite3.connect("antinuke.db")
        self.cursor = self.conn.cursor()
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

        # Load settings
        self.lockdown = self._get_setting("lockdown") == "on"
        self.log_channel_id = int(self._get_setting("log_channel") or 0)

        # Load whitelist from DB
        self.whitelist = set()
        self.cursor.execute("SELECT user_id FROM whitelist")
        for row in self.cursor.fetchall():
            self.whitelist.add(row[0])

    # -----------------------
    # Database helpers
    # -----------------------
    def _get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def _set_setting(self, key, value):
        self.cursor.execute("INSERT INTO settings(key, value) VALUES(?, ?) "
                            "ON CONFLICT(key) DO UPDATE SET value = ?", (key, value, value))
        self.conn.commit()

    def _add_whitelist(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO whitelist(user_id) VALUES(?)", (user_id,))
        self.conn.commit()
        self.whitelist.add(user_id)

    def _remove_whitelist(self, user_id):
        self.cursor.execute("DELETE FROM whitelist WHERE user_id = ?", (user_id,))
        self.conn.commit()
        self.whitelist.discard(user_id)

    # -----------------------
    # Utility
    # -----------------------
    async def log(self, guild, message):
        if self.log_channel_id:
            channel = guild.get_channel(self.log_channel_id)
            if channel:
                await channel.send(message)

    async def punish(self, guild, user):
        if user.id in self.whitelist:
            return

        member = guild.get_member(user.id)
        if not member:
            return

        try:
            for role in member.roles:
                if role.permissions.administrator:
                    await member.remove_roles(role, reason="AntiNuke Triggered")

            await member.ban(reason="AntiNuke Protection")
            await self.log(guild, f"🚨 **{member} banned by AntiNuke**")
        except discord.Forbidden:
            print("Missing permissions to punish.")

    async def check(self, guild, user):
        if user.bot:
            return

        now = time.time()
        self.logs[user.id].append(now)
        self.logs[user.id] = [t for t in self.logs[user.id] if now - t <= self.time_window]

        if len(self.logs[user.id]) >= self.threshold:
            await self.punish(guild, user)
            self.logs[user.id].clear()

    # -----------------------
    # Events
    # -----------------------
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if self.lockdown:
            await channel.guild.create_text_channel(
                name=channel.name,
                overwrites=channel.overwrites
            )
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            await self.check(channel.guild, entry.user)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            await self.check(role.guild, entry.user)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            await self.check(guild, entry.user)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot and member.id not in self.whitelist:
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                if entry.user.id not in self.whitelist:
                    await member.ban(reason="Unauthorized bot added")
                    await self.log(member.guild, f"💣 Bot {member} banned (unauthorized add)")

    # -----------------------
    # Commands
    # -----------------------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, user: discord.Member):
        self._add_whitelist(user.id)
        await ctx.send(f"🔒 {user} added to whitelist.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwhitelist(self, ctx, user: discord.Member):
        self._remove_whitelist(user.id)
        await ctx.send(f"🔓 {user} removed from whitelist.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogs(self, ctx, channel: discord.TextChannel):
        self.log_channel_id = channel.id
        self._set_setting("log_channel", str(channel.id))
        await ctx.send(f"📢 Logs set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx, mode: str):
        if mode.lower() == "on":
            self.lockdown = True
            self._set_setting("lockdown", "on")
            await ctx.send("🧨 Lockdown enabled.")
        else:
            self.lockdown = False
            self._set_setting("lockdown", "off")
            await ctx.send("🟢 Lockdown disabled.")

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
