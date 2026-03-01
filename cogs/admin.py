import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import sqlite3

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Connect to SQLite
        self.conn = sqlite3.connect("admin.db")
        self.cursor = self.conn.cursor()
        # Create warnings table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                warnings INTEGER DEFAULT 0
            )
        """)
        # Create mutes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mutes (
                user_id INTEGER PRIMARY KEY
            )
        """)
        self.conn.commit()

    # -----------------------
    # MODERATION COMMANDS
    # -----------------------
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} has been kicked. Reason: {reason}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} has been banned. Reason: {reason}")

    @commands.command(name="serverban")
    @commands.has_permissions(ban_members=True)
    async def serverban(self, ctx, user_id: int, *, reason="No reason"):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"🔨 {user} has been banned via ID. Reason: {reason}")

    @commands.command(name="forcekick")
    @commands.has_permissions(kick_members=True)
    async def forcekick(self, ctx, user_id: int, *, reason="No reason"):
        user = await self.bot.fetch_user(user_id)
        member = ctx.guild.get_member(user.id)
        if member:
            await member.kick(reason=reason)
            await ctx.send(f"👢 {user} has been kicked via ID. Reason: {reason}")
        else:
            await ctx.send("❌ User not found on this server.")

    # -----------------------
    # UNBAN BY ID
    # -----------------------
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            banned_users = await ctx.guild.bans()
            user = next((entry.user for entry in banned_users if entry.user.id == user_id), None)
            if user:
                await ctx.guild.unban(user)
                await ctx.send(f"✅ {user} has been unbanned.")
            else:
                await ctx.send("❌ User not found in the ban list.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unban users.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ An error occurred: {e}")

    # -----------------------
    # MUTE / UNMUTE
    # -----------------------
    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason"):
        muted_role = get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        await member.add_roles(muted_role, reason=reason)
        # Add to database
        self.cursor.execute("INSERT OR IGNORE INTO mutes(user_id) VALUES(?)", (member.id,))
        self.conn.commit()
        await ctx.send(f"🔇 {member} has been muted. Reason: {reason}")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            # Remove from database
            self.cursor.execute("DELETE FROM mutes WHERE user_id = ?", (member.id,))
            self.conn.commit()
            await ctx.send(f"🔊 {member} has been unmuted.")
        else:
            await ctx.send("❌ This member is not muted.")

    @commands.command(name="muteall")
    @commands.has_permissions(manage_channels=True)
    async def muteall(self, ctx):
        for channel in ctx.guild.voice_channels:
            for member in channel.members:
                await member.edit(mute=True)
        await ctx.send("🔇 All members in voice have been muted.")

    # -----------------------
    # WARNINGS (SQLite)
    # -----------------------
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        user_id = member.id
        self.cursor.execute("SELECT warnings FROM warnings WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            new_count = result[0] + 1
            self.cursor.execute("UPDATE warnings SET warnings = ? WHERE user_id = ?", (new_count, user_id))
        else:
            new_count = 1
            self.cursor.execute("INSERT INTO warnings (user_id, warnings) VALUES (?, ?)", (user_id, new_count))
        self.conn.commit()
        await ctx.send(f"⚠️ {member} has received a warning. Total: {new_count} | Reason: {reason}")

    @commands.command(name="clearwarns")
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        self.cursor.execute("DELETE FROM warnings WHERE user_id = ?", (member.id,))
        self.conn.commit()
        await ctx.send(f"✅ Warnings for {member} have been cleared.")

    @commands.command(name="warns")
    async def warns(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.cursor.execute("SELECT warnings FROM warnings WHERE user_id = ?", (member.id,))
        result = self.cursor.fetchone()
        count = result[0] if result else 0
        await ctx.send(f"⚠️ {member} has {count} warning(s).")

    # -----------------------
    # CHANNEL CONTROL
    # -----------------------
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔒 This channel is now locked.")

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔓 This channel is now unlocked.")

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🌀 Slowmode set to {seconds} seconds.")

    # -----------------------
    # NICKNAMES
    # -----------------------
    @commands.command(name="setnick")
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nickname: str):
        await member.edit(nick=nickname)
        await ctx.send(f"✏️ {member}'s nickname has been changed to {nickname}")

    @commands.command(name="nickname")
    async def nickname(self, ctx, *, nickname: str):
        await ctx.author.edit(nick=nickname)
        await ctx.send(f"✏️ Your nickname has been changed to {nickname}")

    # -----------------------
    # ANNOUNCEMENTS
    # -----------------------
    @commands.command(name="announce")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, message: str):
        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
        await ctx.send(embed=embed)

    # -----------------------
    # MESSAGE CONTROL
    # -----------------------
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"🧹 {amount} messages deleted.", delete_after=5)

    # -----------------------
    # ROLES
    # -----------------------
    @commands.command(name="roleadd")
    @commands.has_permissions(manage_roles=True)
    async def roleadd(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"✅ Role {role.name} added to {member}")

    @commands.command(name="roleremove")
    @commands.has_permissions(manage_roles=True)
    async def roleremove(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"❌ Role {role.name} removed from {member}")

    # -----------------------
    # DMS
    # -----------------------
    @commands.command(name="dm")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, message: str):
        try:
            await member.send(message)
            await ctx.send(f"📩 Message sent to {member.mention}")
        except discord.Forbidden:
            await ctx.send("⚠️ Cannot send DM: user has blocked private messages.")
        except discord.HTTPException:
            await ctx.send("❌ An error occurred while sending the message.")

    @commands.command(name="dmall")
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx, *, message: str):
        success = 0
        failed = 0
        await ctx.send("📨 Sending messages...")
        for member in ctx.guild.members:
            if member.bot:
                continue
            try:
                await member.send(message)
                success += 1
            except (discord.Forbidden, discord.HTTPException):
                failed += 1
            await asyncio.sleep(0.1)
        await ctx.send(f"✅ {success} members received the message.\n⚠️ {failed} members could not be contacted.")
        
    # -----------------------
    # dell all channel
    # -----------------------
        
    @commands.command(name="delchannels")
    async def delete_channels(self, ctx):
        # Check if user is the server owner
        if ctx.author != ctx.guild.owner:
            await ctx.send("❌ Only the SERVER OWNER can use this command.")
            return

        await ctx.send("⚠️ Deleting all channels...")

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except Exception:
                pass

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(Admin(bot))
