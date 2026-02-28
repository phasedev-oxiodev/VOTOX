import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

DB_NAME = "blacklist.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_blacklist (
            user_id INTEGER PRIMARY KEY
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS server_blacklist (
            guild_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

class GlobalBlacklist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        init_db()

    # ---------------- GLOBAL COMMAND CHECK ----------------
    @commands.Cog.listener()
    async def on_command(self, ctx):
        # Block blacklisted users or servers from legacy commands
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Check user
        c.execute("SELECT 1 FROM user_blacklist WHERE user_id = ?", (ctx.author.id,))
        if c.fetchone():
            await ctx.send("You are blacklisted and cannot use commands ❌")
            ctx.command.reset_cooldown(ctx)
            conn.close()
            raise commands.CheckFailure("User is blacklisted")

        # Check server
        if ctx.guild:
            c.execute("SELECT 1 FROM server_blacklist WHERE guild_id = ?", (ctx.guild.id,))
            if c.fetchone():
                await ctx.send("This server is blacklisted and cannot use commands ❌")
                ctx.command.reset_cooldown(ctx)
                conn.close()
                raise commands.CheckFailure("Server is blacklisted")

        conn.close()

    # ---------------- GLOBAL SLASH COMMAND CHECK ----------------
    async def cog_before_invoke(self, ctx_or_interaction):
        # Works for slash commands (app_commands)
        if isinstance(ctx_or_interaction, discord.Interaction):
            user_id = ctx_or_interaction.user.id
            guild_id = ctx_or_interaction.guild.id if ctx_or_interaction.guild else None

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            # User check
            c.execute("SELECT 1 FROM user_blacklist WHERE user_id = ?", (user_id,))
            if c.fetchone():
                await ctx_or_interaction.response.send_message(
                    "You are blacklisted and cannot use commands ❌", ephemeral=True
                )
                conn.close()
                raise app_commands.CheckFailure("User is blacklisted")

            # Server check
            if guild_id:
                c.execute("SELECT 1 FROM server_blacklist WHERE guild_id = ?", (guild_id,))
                if c.fetchone():
                    await ctx_or_interaction.response.send_message(
                        "This server is blacklisted and cannot use commands ❌", ephemeral=True
                    )
                    conn.close()
                    raise app_commands.CheckFailure("Server is blacklisted")

            conn.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalBlacklist(bot))
