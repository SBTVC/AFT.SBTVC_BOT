import discord
from discord import app_commands
from discord.ext import commands

import database


class MeetingGroup(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="ประชุม", description="จัดการการประชุมของ AFT.SBTVC")

    @app_commands.command(name="สร้าง", description="สร้างประกาศการประชุม")
    @app_commands.describe(
        หัวข้อ="หัวข้อการประชุม",
        วันที่="วันที่ เช่น 22/09/2569",
        เวลา="เวลา เช่น 16:30",
        สถานที่="สถานที่ประชุม",
        รายละเอียด="รายละเอียดเพิ่มเติม (ถ้ามี)",
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def create(
        self,
        interaction: discord.Interaction,
        หัวข้อ: str,
        วันที่: str,
        เวลา: str,
        สถานที่: str,
        รายละเอียด: str | None = None,
    ) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        meeting_id = database.execute(
            """
            INSERT INTO meetings (
                guild_id, title, meeting_date, meeting_time,
                location, details, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                interaction.guild.id,
                หัวข้อ,
                วันที่,
                เวลา,
                สถานที่,
                รายละเอียด,
                interaction.user.id,
            ),
        )

        embed = discord.Embed(
            title="📅 นัดประชุม AFT.SBTVC",
            description=f"**{หัวข้อ}**",
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="📆 วันที่", value=วันที่, inline=True)
        embed.add_field(name="🕒 เวลา", value=เวลา, inline=True)
        embed.add_field(name="📍 สถานที่", value=สถานที่, inline=False)

        if รายละเอียด:
            embed.add_field(name="📝 รายละเอียด", value=รายละเอียด, inline=False)

        embed.set_footer(
            text=f"รหัสการประชุม #{meeting_id} • สร้างโดย {interaction.user.display_name}"
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ล่าสุด", description="ดูการประชุมล่าสุด")
    async def latest(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        row = database.fetchone(
            """
            SELECT * FROM meetings
            WHERE guild_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (interaction.guild.id,),
        )

        if row is None:
            await interaction.response.send_message(
                "ยังไม่มีการประชุมที่บันทึกไว้",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"📅 การประชุม #{row['id']}",
            description=f"**{row['title']}**",
        )
        embed.add_field(name="📆 วันที่", value=row["meeting_date"], inline=True)
        embed.add_field(name="🕒 เวลา", value=row["meeting_time"], inline=True)
        embed.add_field(name="📍 สถานที่", value=row["location"], inline=False)
        if row["details"]:
            embed.add_field(name="📝 รายละเอียด", value=row["details"], inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class Meetings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.group = MeetingGroup()
        self.bot.tree.add_command(self.group)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.group.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meetings(bot))
