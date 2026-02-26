import discord
from discord.ext import commands

# Store detected words per guild: {guild_id: {word: response}}
detect_words = {}

# Store role words per guild: {guild_id: {word: role_id}}
role_words = {}

class World(commands.Cog):
    """Word detection and role assignment commands"""

    def __init__(self, bot):
        self.bot = bot

    # -----------------------
    # HELPERS
    # -----------------------
    def get_guild_detect_words(self, guild_id):
        """Get detect words for a specific guild"""
        if guild_id not in detect_words:
            detect_words[guild_id] = {}
        return detect_words[guild_id]

    def get_guild_role_words(self, guild_id):
        """Get role words for a specific guild"""
        if guild_id not in role_words:
            role_words[guild_id] = {}
        return role_words[guild_id]

    # -----------------------
    # DETECT WORDS
    # -----------------------
    @commands.hybrid_command(name="setdetect", description="Add a word to detect with a response")
    async def set_detect(self, ctx, word: str, *, response: str):
        guild_detect = self.get_guild_detect_words(ctx.guild.id)
        guild_detect[word.lower()] = response
        await ctx.send(f"✅ Word '{word}' added with response '{response}' on this server")

    @commands.hybrid_command(name="deldetect", description="Remove a word from detection")
    async def del_detect(self, ctx, word: str):
        guild_detect = self.get_guild_detect_words(ctx.guild.id)
        removed = guild_detect.pop(word.lower(), None)
        if removed:
            await ctx.send(f"✅ Word '{word}' removed from detection")
        else:
            await ctx.send(f"⚠️ Word '{word}' was not in the detection list")

    @commands.hybrid_command(name="listdetect", description="List all detected words and responses")
    async def list_detect(self, ctx):
        guild_detect = self.get_guild_detect_words(ctx.guild.id)
        if not guild_detect:
            await ctx.send("⚠️ No words are currently detected on this server")
            return
        lines = [f"**{word}** → {resp}" for word, resp in guild_detect.items()]
        await ctx.send("\n".join(lines))

    @commands.hybrid_command(name="cleardetects", description="Clear all detected words")
    async def clear_detects(self, ctx):
        guild_detect = self.get_guild_detect_words(ctx.guild.id)
        guild_detect.clear()
        await ctx.send("✅ All detected words have been cleared on this server")

    # -----------------------
    # ROLE WORDS
    # -----------------------
    @commands.hybrid_command(name="setroleword", description="Assign a role if a word is said")
    async def set_role_word(self, ctx, word: str, role: discord.Role):
        guild_role = self.get_guild_role_words(ctx.guild.id)
        guild_role[word.lower()] = role.id
        await ctx.send(f"✅ If someone says '{word}', they will get the role '{role.name}'")

    @commands.hybrid_command(name="delroleword", description="Remove a word-role configuration")
    async def del_role_word(self, ctx, word: str):
        guild_role = self.get_guild_role_words(ctx.guild.id)
        removed = guild_role.pop(word.lower(), None)
        if removed:
            await ctx.send(f"✅ Configuration for '{word}' removed")
        else:
            await ctx.send(f"⚠️ No role configured for '{word}'")

    @commands.hybrid_command(name="listrolewords", description="List all role-word configurations")
    async def list_role_words(self, ctx):
        guild_role = self.get_guild_role_words(ctx.guild.id)
        if not guild_role:
            await ctx.send("⚠️ No role words set on this server")
            return
        lines = []
        for word, role_id in guild_role.items():
            role = ctx.guild.get_role(role_id)
            role_name = role.name if role else "❌ (role missing)"
            lines.append(f"**{word}** → {role_name}")
        await ctx.send("\n".join(lines))

    @commands.hybrid_command(name="clearrolewords", description="Clear all role word configurations")
    async def clear_rolewords(self, ctx):
        guild_role = self.get_guild_role_words(ctx.guild.id)
        guild_role.clear()
        await ctx.send("✅ All role-word configurations cleared")

    # -----------------------
    # MESSAGE LISTENER
    # -----------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_detect = self.get_guild_detect_words(message.guild.id)
        guild_role = self.get_guild_role_words(message.guild.id)

        # Check for detected words
        for word, response in guild_detect.items():
            if word in message.content.lower():
                await message.channel.send(response)
                break

        # Check for role words
        for word, role_id in guild_role.items():
            if word in message.content.lower():
                role = message.guild.get_role(role_id)
                if role and role not in message.author.roles:
                    try:
                        await message.author.add_roles(role)
                        await message.channel.send(f"✅ {message.author.mention} has been given the role {role.name}!")
                    except discord.Forbidden:
                        await message.channel.send(f"❌ I don't have permission to assign roles.")
                break

# -----------------------
# SETUP
# -----------------------
async def setup(bot):
    await bot.add_cog(World(bot))