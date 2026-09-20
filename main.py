import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import database


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not TOKEN:
    raise RuntimeError(
        "ไม่พบ DISCORD_TOKEN กรุณาสร้างไฟล์ .env และกำหนด Token ของบอทก่อน"
    )


class AFTBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        database.init_db()

        extensions = (
            "cogs.general",
            "cogs.announcements",
            "cogs.meetings",
            "cogs.attendance",
            "cogs.tasks",
        )

        for extension in extensions:
            await self.load_extension(extension)
            print(f"โหลด {extension} แล้ว")

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"ซิงก์คำสั่งในเซิร์ฟเวอร์แล้ว {len(synced)} คำสั่ง")
        else:
            synced = await self.tree.sync()
            print(f"ซิงก์คำสั่งแบบ Global แล้ว {len(synced)} คำสั่ง")


bot = AFTBot()


@bot.event
async def on_ready() -> None:
    if bot.user is None:
        return

    print(f"เข้าสู่ระบบเป็น {bot.user} ({bot.user.id})")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="ดูแลเซิร์ฟเวอร์ AFT.SBTVC",
        ),
    )


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
) -> None:
    if isinstance(error, app_commands.MissingPermissions):
        message = "❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้"
    elif isinstance(error, app_commands.CommandOnCooldown):
        message = f"⏳ กรุณารอ {error.retry_after:.1f} วินาทีแล้วลองใหม่"
    else:
        message = "❌ เกิดข้อผิดพลาดในการทำงานของคำสั่ง"
        print(f"Application command error: {error}")

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


bot.run(TOKEN)
