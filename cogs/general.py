import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ทดสอบ",
        description="ตรวจสอบว่าบอท AFT.SBTVC ทำงานหรือไม่",
    )
    async def test(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            f"✅ AFT.SBTVC BOT ทำงานปกติ\n📡 Ping: {latency_ms} ms",
            ephemeral=True,
        )

    @app_commands.command(
        name="ช่วยเหลือ",
        description="แสดงรายการคำสั่งของ AFT.SBTVC BOT",
    )
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="🤖 AFT.SBTVC BOT",
            description="ระบบช่วยจัดการเซิร์ฟเวอร์ อวท. AFT.SBTVC",
        )

        embed.add_field(
            name="/ทดสอบ",
            value="ตรวจสอบสถานะการทำงานของบอท",
            inline=False,
        )
        embed.add_field(
            name="/ช่วยเหลือ",
            value="แสดงรายการคำสั่งที่ใช้งานได้",
            inline=False,
        )
        embed.add_field(
            name="/ประกาศ",
            value="สร้างประกาศแบบ Embed สำหรับผู้ที่มีสิทธิ์จัดการข้อความ",
            inline=False,
        )

        embed.set_footer(text="AFT.SBTVC • Discord Bot")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
