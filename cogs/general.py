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

        commands_list = (
            ("/ทดสอบ", "ตรวจสอบสถานะบอท"),
            ("/ช่วยเหลือ", "แสดงรายการคำสั่ง"),
            ("/ประกาศ", "สร้างประกาศแบบ Embed"),
            ("/ประชุม สร้าง", "สร้างประกาศนัดประชุม"),
            ("/ประชุม ล่าสุด", "ดูการประชุมล่าสุด"),
            ("/เช็กชื่อ เปิด", "เปิดรอบเช็กชื่อ"),
            ("/เช็กชื่อ ลงชื่อ", "เช็กชื่อเข้าร่วม"),
            ("/เช็กชื่อ รายชื่อ", "ดูรายชื่อผู้เช็กชื่อ"),
            ("/เช็กชื่อ ปิด", "ปิดรอบเช็กชื่อ"),
            ("/งาน เพิ่ม", "สร้างและมอบหมายงาน"),
            ("/งาน รายการ", "ดูงานที่ยังไม่เสร็จ"),
            ("/งาน เสร็จ", "ปิดงานเป็นเสร็จสิ้น"),
        )

        for command, description in commands_list:
            embed.add_field(
                name=command,
                value=description,
                inline=False,
            )

        embed.set_footer(text="AFT.SBTVC • Discord Bot")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
