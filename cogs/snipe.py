import discord
from discord.ext import commands
from discord import ui
import sqlite3
import json
from datetime import datetime

DB_NAME = "snipes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS snipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER,
            author_id INTEGER,
            author_name TEXT,
            avatar_url TEXT,
            content TEXT,
            attachments TEXT,
            deleted_at INTEGER
        )
    """)
    conn.commit()
    conn.close()

class SnipeView(ui.View):
    def __init__(self, snipes, author):
        super().__init__(timeout=60)
        self.snipes = snipes
        self.index = 0
        self.command_author = author

    def create_embed(self, data):
        embed = discord.Embed(
            description=data["content"] or "*No message content*",
            color=discord.Color.blurple(),
            timestamp=datetime.fromtimestamp(data["deleted_at"])
        )

        embed.set_author(
            name=f"{data['author_name']} ({data['author_id']})",
            icon_url=data["avatar_url"]
        )

        embed.add_field(
            name="Deleted At",
            value=f"<t:{data['deleted_at']}:F>",
            inline=False
        )

        attachments = json.loads(data["attachments"])
        files_text = []

        for att in attachments:
            if att["is_image"]:
                embed.set_image(url=att["url"])
            else:
                files_text.append(f"[{att['filename']}]({att['url']})")

        if files_text:
            embed.add_field(
                name="Attachments",
                value="\n".join(files_text),
                inline=False
            )

        embed.set_footer(text="Made By PhaseDev")
        return embed

    async def update(self, interaction):
        embed = self.create_embed(self.snipes[self.index])
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.command_author:
            return await interaction.response.send_message(
                "You can't control this menu.", ephemeral=True
            )

        self.index = (self.index - 1) % len(self.snipes)
        await self.update(interaction)

    @ui.button(label="Next ➡", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.command_author:
            return await interaction.response.send_message(
                "You can't control this menu.", ephemeral=True
            )

        self.index = (self.index + 1) % len(self.snipes)
        await self.update(interaction)


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        init_db()

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        attachments = []
        for att in message.attachments:
            attachments.append({
                "url": att.url,
                "filename": att.filename,
                "is_image": att.content_type and att.content_type.startswith("image")
            })

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
            INSERT INTO snipes (
                guild_id, channel_id, author_id, author_name,
                avatar_url, content, attachments, deleted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message.guild.id,
            message.channel.id,
            message.author.id,
            str(message.author),
            message.author.display_avatar.url,
            message.content,
            json.dumps(attachments),
            int(datetime.utcnow().timestamp())
        ))

        # Keep only last 10 per channel
        c.execute("""
            DELETE FROM snipes
            WHERE id NOT IN (
                SELECT id FROM snipes
                WHERE guild_id = ? AND channel_id = ?
                ORDER BY deleted_at DESC
                LIMIT 10
            )
            AND guild_id = ? AND channel_id = ?
        """, (
            message.guild.id,
            message.channel.id,
            message.guild.id,
            message.channel.id
        ))

        conn.commit()
        conn.close()

    @commands.command()
    async def snipe(self, ctx):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
            SELECT author_id, author_name, avatar_url,
                   content, attachments, deleted_at
            FROM snipes
            WHERE guild_id = ? AND channel_id = ?
            ORDER BY deleted_at DESC
        """, (ctx.guild.id, ctx.channel.id))

        rows = c.fetchall()
        conn.close()

        if not rows:
            return await ctx.send("There are no deleted messages to snipe.")

        snipes = []
        for row in rows:
            snipes.append({
                "author_id": row[0],
                "author_name": row[1],
                "avatar_url": row[2],
                "content": row[3],
                "attachments": row[4],
                "deleted_at": row[5]
            })

        view = SnipeView(snipes, ctx.author)
        embed = view.create_embed(snipes[0])

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Snipe(bot))