import discord
from discord.ext import commands
import sqlite3

class World(commands.Cog):
    """Word detection and role assignment with required-role restriction"""

    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("world.db")
        self.cursor = self.conn.cursor()

        # Tables: detect words + role words
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detect_words (
                guild_id INTEGER,
                word TEXT,
                response TEXT,
                PRIMARY KEY (guild_id, word)
            )
        """)
        # role_words now includes optional required_role_id
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_words (
                guild_id INTEGER,
                word TEXT,
                role_id INTEGER,
                required_role_id INTEGER,
                PRIMARY KEY (guild_id, word)
            )
        """)
        self.conn.commit()

    # -----------------------
    # ROLE WORDS
    # -----------------------
    @commands.hybrid_command(name="setroleword", description="Assign a role if a word is said")
    async def set_role_word(self, ctx, word: str, role: discord.Role, required_role: discord.Role = None):
        """Add a role-word configuration with optional required role"""
        req_id = required_role.id if required_role else None
        self.cursor.execute(
            "INSERT OR REPLACE INTO role_words (guild_id, word, role_id, required_role_id) VALUES (?, ?, ?, ?)",
            (ctx.guild.id, word.lower(), role.id, req_id)
        )
        self.conn.commit()
        if required_role:
            await ctx.send(f"✅ Saying '{word}' gives role '{role.name}' only if you have '{required_role.name}'")
        else:
            await ctx.send(f"✅ Saying '{word}' gives role '{role.name}' to anyone")

    @commands.hybrid_command(name="delroleword", description="Remove a word-role configuration")
    async def del_role_word(self, ctx, word: str):
        self.cursor.execute(
            "DELETE FROM role_words WHERE guild_id = ? AND word = ?",
            (ctx.guild.id, word.lower())
        )
        self.conn.commit()
        await ctx.send(f"✅ Configuration for '{word}' removed")

    @commands.hybrid_command(name="listrolewords", description="List all role-word configurations")
    async def list_role_words(self, ctx):
        self.cursor.execute(
            "SELECT word, role_id, required_role_id FROM role_words WHERE guild_id = ?",
            (ctx.guild.id,)
        )
        rows = self.cursor.fetchall()
        if not rows:
            await ctx.send("⚠️ No role words set on this server")
            return
        lines = []
        for word, role_id, req_id in rows:
            role = ctx.guild.get_role(role_id)
            req_role = ctx.guild.get_role(req_id) if req_id else None
            role_name = role.name if role else "❌ (role missing)"
            req_name = f"(requires {req_role.name})" if req_role else ""
            lines.append(f"**{word}** → {role_name} {req_name}")
        await ctx.send("\n".join(lines))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        self.cursor.execute(
            "SELECT word, role_id, required_role_id FROM role_words WHERE guild_id = ?",
            (message.guild.id,)
        )
        for word, role_id, required_role_id in self.cursor.fetchall():
            if word in message.content.lower():
                role = message.guild.get_role(role_id)
                req_role = message.guild.get_role(required_role_id) if required_role_id else None

                # Check required role
                if req_role and req_role not in message.author.roles:
                    continue  # user doesn't have required role, skip

                if role and role not in message.author.roles:
                    try:
                        await message.author.add_roles(role)
                        await message.channel.send(f"✅ {message.author.mention} has been given the role {role.name}!")
                    except discord.Forbidden:
                        await message.channel.send("❌ I don't have permission to assign roles.")
                break

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(World(bot))
