import discord
from discord.ext import commands, tasks
from discord.ui import View, Select
import itertools

# -------------------------------
# Animated embed colors
# -------------------------------
COLORS = [
    discord.Color.blue(),
    discord.Color.green(),
    discord.Color.gold(),
    discord.Color.purple(),
    discord.Color.orange(),
    discord.Color.red()
]

class DropdownHelp(commands.Cog):
    """Interactive dropdown help with animated embed colors"""

    def __init__(self, bot):
        self.bot = bot
        self.color_cycle = itertools.cycle(COLORS)
        self.embed_color = next(self.color_cycle)
        self.animate_colors.start()

    @tasks.loop(seconds=1.5)
    async def animate_colors(self):
        """Animate the embed color every 1.5 seconds"""
        self.embed_color = next(self.color_cycle)

    @commands.command(name="helpv2")
    async def help_command(self, ctx):
        """Send interactive dropdown help menu"""
        categories = {
            "Admin": [
                "!kick - Kick a member",
                "!ban - Ban a member",
                "!unban - unBan a member",
                "!mute - Mute a member",
                "!unmute - Unmute a member",
                "!warn - Warn a member",
                "!clearwarns - Clear member warnings",
                "!lock - Lock a channel",
                "!unlock - Unlock a channel",
                "!setnick - Change a nickname",
                "!announce - Make announcement",
                "!slowmode - Set slowmode",
                "!purge - Delete messages",
                "!roleadd - Add role",
                "!roleremove - Remove role",
                "!clear - Clear a channel",
                "!nickname - Change your nickname",
                "!serverban - Ban via ID",
                "!forcekick - Kick via ID",
                "!dm - DM a user",
                "!muteall - Mute all in voice",
                "!delchannels - only use it server got nuke"
            ],
            "Fun": [
                "!8ball <question> - Ask the magic ball",
                "!dice - Roll a dice",
                "!joke - Get a joke",
                "!meme - Display meme (in work)"
            ],
            "Utility": [
                "!say <msg> - Repeat message",
                "!randomnumber [min] [max] - Random number",
                "!time - UTC time",
                "!date - UTC date",
                "!avatar [member] - Member avatar",
                "!servericon - Server icon",
                "!uptime - Bot uptime",
                "!ping - Bot latency",
                "!pick <opt1> <opt2> [opt3] - Random choice",
                "!emoji <emoji> - Show emoji",
                "!reverse <text> - Reversed text",
                "!upper <text> - Uppercase text",
                "!lower <text> - Lowercase text",
                "!mock <text> - Mock text",
                "!repeat <text> [times] - Repeat text",
                "!shrug - ¯\\_(ツ)_/¯",
                "!tableflip - (╯°□°)╯︵ ┻━┻",
                "!unflip - ┬─┬ ノ( ゜-゜ノ)",
                "!countdown <number> - Countdown",
                "!add <a> <b> - Add",
                "!subtract <a> <b> - Subtract",
                "!multiply <a> <b> - Multiply",
                "!divide <a> <b> - Divide",
                "!color - Random color",
                "!rolldice [sides] - Roll dice",
                "!invite-bot - your not that dumb :skull:"
            ],
            "Info": [
                "!userinfo [member] - Member info",
                "!roleinfo <role> - Role info",
                "!channelinfo [channel] - Channel info"
            ],
            "World": [
                "!setdetect <word> <response> - Add word detection",
                "!deldetect <word> - Remove detect word",
                "!listdetect - List detected words",
                "!cleardetects - Clear detected words",
                "!setroleword <word> <role> - Auto role word",
                "!delroleword <word> - Remove role word",
                "!listrolewords - List role words",
                "!clearrolewords - Clear all role words"
            ]
        }

        # -----------------------
        # Dropdown for categories
        # -----------------------
        options = [discord.SelectOption(label=name, description=f"Show {name} commands") for name in categories.keys()]

        class HelpDropdown(Select):
            def __init__(self, parent_cog):
                super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
                self.parent_cog = parent_cog  # reference the cog to get color

            async def callback(self, interaction: discord.Interaction):
                cat = self.values[0]
                embed = discord.Embed(
                    title=f"📚 {cat} Commands",
                    description="\n".join(categories[cat]),
                    color=self.parent_cog.embed_color
                )
                embed.set_footer(text="Made By PhaseDev And Hosted By PhaseDev")
                await interaction.response.edit_message(embed=embed)

        class HelpView(View):
            def __init__(self, parent_cog):
                super().__init__(timeout=None)
                self.add_item(HelpDropdown(parent_cog))

        # Send the help embed with dropdown view
        await ctx.send(
            embed=discord.Embed(
                title="📚 Help Menu",
                description="Select a category from the dropdown below!",
                color=self.embed_color
            ),
            view=HelpView(self)
        )

async def setup(bot):
    await bot.add_cog(DropdownHelp(bot))