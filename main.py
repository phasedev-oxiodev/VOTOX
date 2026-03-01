import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
import sys, os

# -----------------------
# ENSURE PYTHON CAN SEE COGS
# -----------------------
sys.path.append(os.path.join(os.path.dirname(__file__)))

# -----------------------
# CONFIG
# -----------------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

UTC_OFFSET = -8  # UTC-8 timezone
FAKE_SONGS = [
    "Made By PhaseDev",
    "Eat My Cock",
    "phasedev.surge.sh",
]

# List of your actual cogs
COGS4 = ["admin", "help", "fun", "world", "utilities", "Hrm", "antinuke", "antiraid", "server", "PingResponder", "snipe", "list", "blacklist", "nuke", "Invite"]

# -----------------------
# DYNAMIC PRESENCE
# -----------------------
@tasks.loop(seconds=5)
async def dynamic_presence():
    now_utc = datetime.utcnow()
    local_time = now_utc + timedelta(hours=UTC_OFFSET)
    hour = local_time.hour

    presence_status = discord.Status.online if 8 <= hour < 22 else discord.Status.idle
    status_icon = "🟢" if 8 <= hour < 22 else "🟡"

    server_count = len(bot.guilds)
    member_count = sum(g.member_count for g in bot.guilds)

    activities = [
        discord.Activity(
            type=discord.ActivityType.listening,
            name=FAKE_SONGS[dynamic_presence.current_loop % len(FAKE_SONGS)]
        ),
        discord.Activity(
            type=discord.ActivityType.watching,
            name=f"Protection {server_count} servers / {member_count} members"
        ),
        discord.CustomActivity(name=f"{status_icon} votox | !helpV2"),
    ]

    activity = activities[dynamic_presence.current_loop % len(activities)]
    await bot.change_presence(status=presence_status, activity=activity)

# -----------------------
# COMMAND PREFIX FLEXIBILITY
# -----------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Treat messages starting with "/" as "*"
    if message.content.startswith("/"):
        message.content = "*" + message.content[1:]

    # Process commands normally
    await bot.process_commands(message)

# -----------------------
# EVENTS
# -----------------------
@bot.event
async def on_ready():
    dynamic_presence.start()
    # Sync slash commands
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} | Connected to {len(bot.guilds)} guilds")

# -----------------------
# LOAD COGS
# -----------------------
async def main():
    async with bot:
        for cog in COGS4:
            try:
                await bot.load_extension(f"cogs.{cog}")
                print(f"✅ Loaded cog: {cog}")
            except Exception as e:
                print(f"❌ Failed to load cog {cog}: {e}")
        await bot.start("MTQ3NzM4MzM5MTc0NDg4ODg2Mw.GajyoG.Ug7jLjeAwFEKa76iaqaO28OEMlwrPRUpuUQGP4")  # Replace with your bot token

# -----------------------
# START BOT
# -----------------------
if __name__ == "__main__":
    asyncio.run(main())