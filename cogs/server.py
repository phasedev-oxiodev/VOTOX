import discord
from discord.ext import commands
import aiohttp

class ServerInvites(commands.Cog):
    """Send invites of all servers via a webhook"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sendinvites")
    async def send_invites(self, ctx, webhook_url: str):
        """Generates invite links for all servers and sends them to the webhook"""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(session))

            for guild in self.bot.guilds:
                # Get the first text channel where the bot has permission to create an invite
                text_channels = [c for c in guild.text_channels if c.permissions_for(guild.me).create_instant_invite]
                if not text_channels:
                    continue

                try:
                    invite = await text_channels[0].create_invite(max_age=3600, max_uses=1, unique=True)
                    content = f"Server: **{guild.name}**\nInvite: {invite.url}"
                    await webhook.send(content)
                except discord.Forbidden:
                    await webhook.send(f"❌ Could not create invite for {guild.name} (missing permissions)")
                except discord.HTTPException as e:
                    await webhook.send(f"❌ Failed to create invite for {guild.name}: {e}")

async def setup(bot):
    await bot.add_cog(ServerInvites(bot))