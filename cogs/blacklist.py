import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

DB_NAME = "blacklist.db"
ALLOWED_USERS = [1320349118102769767, 1461537788754399232]

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

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        init_db()
        self.tree = bot.tree
        self.tree.add_command(self.blacklist_user)
        self.tree.add_command(self.unblacklist_user)
        self.tree.add_command(self.blacklist_server)
        self.tree.add_command(self.unblacklist_server)

    # ----------------- USER BLACKLIST -----------------
    @app_commands.command(name="blacklist_user", description="Blacklist a user from using the bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def blacklist_user(self, interaction: discord.Interaction, user: discord.User):
        if interaction.user.id not in ALLOWED_USERS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO user_blacklist (user_id) VALUES (?)", (user.id,))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"{user.mention} has been blacklisted 🔒")

    @app_commands.command(name="unblacklist_user", description="Remove a user from the blacklist")
    async def unblacklist_user(self, interaction: discord.Interaction, user: discord.User):
        if interaction.user.id not in ALLOWED_USERS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM user_blacklist WHERE user_id = ?", (user.id,))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"{user.mention} has been removed from the blacklist ✅")

    # ----------------- SERVER BLACKLIST -----------------
    @app_commands.command(name="blacklist_server", description="Blacklist this server from using the bot")
    async def blacklist_server(self, interaction: discord.Interaction):
        if interaction.user.id not in ALLOWED_USERS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO server_blacklist (guild_id) VALUES (?)", (interaction.guild.id,))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"This server `{interaction.guild.name}` has been blacklisted 🔒")

    @app_commands.command(name="unblacklist_server", description="Remove this server from the blacklist")
    async def unblacklist_server(self, interaction: discord.Interaction):
        if interaction.user.id not in ALLOWED_USERS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM server_blacklist WHERE guild_id = ?", (interaction.guild.id,))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"This server `{interaction.guild.name}` has been removed from the blacklist ✅")

    # ----------------- CHECKS -----------------
    @commands.Cog.listener()
    async def on_command(self, ctx):
        # Check user
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM user_blacklist WHERE user_id = ?", (ctx.author.id,))
        if c.fetchone():
            await ctx.send("You are blacklisted and cannot use commands ❌")
            ctx.command.reset_cooldown(ctx)
            raise commands.CheckFailure("User is blacklisted")

        # Check server
        c.execute("SELECT * FROM server_blacklist WHERE guild_id = ?", (ctx.guild.id,))
        if c.fetchone():
            await ctx.send("This server is blacklisted and cannot use commands ❌")
            ctx.command.reset_cooldown(ctx)
            raise commands.CheckFailure("Server is blacklisted")
        conn.close()

async def setup(bot):
    await bot.add_cog(Blacklist(bot))
