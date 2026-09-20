import discord
from discord import app_commands
from discord.ext import commands

import database


class TaskGroup(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="งาน", description="ระบบมอบหมายและติดตามงาน")

    @app_commands.command(name="เพิ่ม", description="เพิ่มงานใหม่")
    @app_commands.describe(
        ชื่องาน="ชื่อของงาน",
        ผู้รับผิดชอบ="สมาชิกที่รับผิดชอบ",
        กำหนดส่ง="วันกำหนดส่ง เช่น 25/09/2569",
        รายละเอียด="รายละเอียดเพิ่มเติม (ถ้ามี)",
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_task(
        self,
        interaction: discord.Interaction,
        ชื่องาน: str,
        ผู้รับผิดชอบ: discord.Member,
        กำหนดส่ง: str | None = None,
        รายละเอียด: str | None = None,
    ) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        task_id = database.execute(
            """
            INSERT INTO tasks (
                guild_id, title, details, assignee_id,
                assignee_name, due_date, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                interaction.guild.id,
                ชื่องาน,
                รายละเอียด,
                ผู้รับผิดชอบ.id,
                ผู้รับผิดชอบ.display_name,
                กำหนดส่ง,
                interaction.user.id,
            ),
        )

        embed = discord.Embed(
            title=f"📋 งานใหม่ #{task_id}",
            description=f"**{ชื่องาน}**",
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="👤 ผู้รับผิดชอบ",
            value=ผู้รับผิดชอบ.mention,
            inline=False,
        )
        embed.add_field(
            name="📅 กำหนดส่ง",
            value=กำหนดส่ง or "ไม่ได้กำหนด",
            inline=True,
        )
        embed.add_field(
            name="🟡 สถานะ",
            value="กำลังดำเนินการ",
            inline=True,
        )
        if รายละเอียด:
            embed.add_field(name="📝 รายละเอียด", value=รายละเอียด, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="รายการ", description="ดูงานที่ยังไม่เสร็จ")
    async def list_tasks(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        rows = database.fetchall(
            """
            SELECT * FROM tasks
            WHERE guild_id = ? AND status != 'เสร็จสิ้น'
            ORDER BY id DESC
            LIMIT 20
            """,
            (interaction.guild.id,),
        )

        if not rows:
            await interaction.response.send_message(
                "✅ ตอนนี้ไม่มีงานค้าง",
                ephemeral=True,
            )
            return

        lines = []
        for row in rows:
            due = row["due_date"] or "ไม่กำหนด"
            lines.append(
                f"**#{row['id']} {row['title']}**\n"
                f"ผู้รับผิดชอบ: {row['assignee_name'] or '-'} • "
                f"กำหนดส่ง: {due}"
            )

        embed = discord.Embed(
            title="📋 งานที่กำลังดำเนินการ",
            description="\n\n".join(lines),
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="เสร็จ", description="ปิดงานเป็นเสร็จสิ้น")
    @app_commands.describe(รหัสงาน="หมายเลขงาน เช่น 3")
    async def complete_task(
        self,
        interaction: discord.Interaction,
        รหัสงาน: int,
    ) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์",
                ephemeral=True,
            )
            return

        row = database.fetchone(
            """
            SELECT * FROM tasks
            WHERE id = ? AND guild_id = ?
            """,
            (รหัสงาน, interaction.guild.id),
        )

        if row is None:
            await interaction.response.send_message(
                "❌ ไม่พบงานรหัสนี้",
                ephemeral=True,
            )
            return

        can_manage = (
            isinstance(interaction.user, discord.Member)
            and interaction.user.guild_permissions.manage_messages
        )

        if row["assignee_id"] != interaction.user.id and not can_manage:
            await interaction.response.send_message(
                "❌ เฉพาะผู้รับผิดชอบงานหรือผู้ดูแลเท่านั้นที่ปิดงานนี้ได้",
                ephemeral=True,
            )
            return

        database.execute(
            """
            UPDATE tasks
            SET status = 'เสร็จสิ้น', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (รหัสงาน,),
        )

        await interaction.response.send_message(
            f"✅ งาน **#{รหัสงาน} {row['title']}** เสร็จสิ้นแล้ว"
        )


class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.group = TaskGroup()
        self.bot.tree.add_command(self.group)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.group.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tasks(bot))
