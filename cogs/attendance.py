import discord
from discord import app_commands
from discord.ext import commands

import database


class AttendanceGroup(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="เช็กชื่อ", description="ระบบเช็กชื่อกิจกรรมและการประชุม")

    @app_commands.command(name="เปิด", description="เปิดรอบเช็กชื่อใหม่")
    @app_commands.describe(หัวข้อ="ชื่อกิจกรรมหรือการประชุม")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def open_session(
        self,
        interaction: discord.Interaction,
        หัวข้อ: str,
    ) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        active = database.fetchone(
            """
            SELECT id, title FROM attendance_sessions
            WHERE guild_id = ? AND is_open = 1
            ORDER BY id DESC
            LIMIT 1
            """,
            (interaction.guild.id,),
        )
        if active:
            await interaction.response.send_message(
                f"⚠️ มีรอบเช็กชื่อที่ยังเปิดอยู่: #{active['id']} {active['title']}",
                ephemeral=True,
            )
            return

        session_id = database.execute(
            """
            INSERT INTO attendance_sessions (guild_id, title, created_by)
            VALUES (?, ?, ?)
            """,
            (interaction.guild.id, หัวข้อ, interaction.user.id),
        )

        embed = discord.Embed(
            title="✅ เปิดเช็กชื่อ",
            description=f"**{หัวข้อ}**\nใช้คำสั่ง `/เช็กชื่อ ลงชื่อ` เพื่อเช็กชื่อ",
            timestamp=discord.utils.utcnow(),
        )
        embed.set_footer(text=f"รอบเช็กชื่อ #{session_id}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ลงชื่อ", description="เช็กชื่อในรอบที่กำลังเปิด")
    async def check_in(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        session = database.fetchone(
            """
            SELECT id, title FROM attendance_sessions
            WHERE guild_id = ? AND is_open = 1
            ORDER BY id DESC
            LIMIT 1
            """,
            (interaction.guild.id,),
        )

        if session is None:
            await interaction.response.send_message(
                "❌ ตอนนี้ไม่มีรอบเช็กชื่อที่เปิดอยู่",
                ephemeral=True,
            )
            return

        existing = database.fetchone(
            """
            SELECT id FROM attendance_records
            WHERE session_id = ? AND user_id = ?
            """,
            (session["id"], interaction.user.id),
        )

        if existing:
            await interaction.response.send_message(
                "ℹ️ คุณเช็กชื่อในรอบนี้แล้ว",
                ephemeral=True,
            )
            return

        database.execute(
            """
            INSERT INTO attendance_records (
                session_id, user_id, display_name
            ) VALUES (?, ?, ?)
            """,
            (session["id"], interaction.user.id, interaction.user.display_name),
        )

        await interaction.response.send_message(
            f"✅ เช็กชื่อ **{session['title']}** เรียบร้อยแล้ว",
            ephemeral=True,
        )

    @app_commands.command(name="รายชื่อ", description="ดูรายชื่อผู้ที่เช็กชื่อแล้ว")
    async def list_attendance(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        session = database.fetchone(
            """
            SELECT id, title, is_open FROM attendance_sessions
            WHERE guild_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (interaction.guild.id,),
        )

        if session is None:
            await interaction.response.send_message(
                "ยังไม่มีข้อมูลเช็กชื่อ",
                ephemeral=True,
            )
            return

        rows = database.fetchall(
            """
            SELECT display_name, checked_in_at
            FROM attendance_records
            WHERE session_id = ?
            ORDER BY checked_in_at ASC
            """,
            (session["id"],),
        )

        if rows:
            lines = [
                f"{index}. {row['display_name']}"
                for index, row in enumerate(rows, start=1)
            ]
            body = "\n".join(lines)
        else:
            body = "ยังไม่มีผู้เช็กชื่อ"

        status = "🟢 เปิดอยู่" if session["is_open"] else "🔴 ปิดแล้ว"
        embed = discord.Embed(
            title=f"📋 รายชื่อเช็กชื่อ #{session['id']}",
            description=f"**{session['title']}**\nสถานะ: {status}\n\n{body}",
        )
        embed.set_footer(text=f"รวม {len(rows)} คน")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ปิด", description="ปิดรอบเช็กชื่อที่กำลังเปิด")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def close_session(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        session = database.fetchone(
            """
            SELECT id, title FROM attendance_sessions
            WHERE guild_id = ? AND is_open = 1
            ORDER BY id DESC
            LIMIT 1
            """,
            (interaction.guild.id,),
        )

        if session is None:
            await interaction.response.send_message(
                "❌ ไม่มีรอบเช็กชื่อที่เปิดอยู่",
                ephemeral=True,
            )
            return

        database.execute(
            """
            UPDATE attendance_sessions
            SET is_open = 0, closed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (session["id"],),
        )

        count = database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM attendance_records
            WHERE session_id = ?
            """,
            (session["id"],),
        )

        await interaction.response.send_message(
            f"🔒 ปิดเช็กชื่อ **{session['title']}** แล้ว\nรวม {count['total']} คน"
        )


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.group = AttendanceGroup()
        self.bot.tree.add_command(self.group)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.group.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Attendance(bot))
