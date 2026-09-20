import discord
from discord import app_commands
from discord.ext import commands


class Announcements(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ประกาศ",
        description="สร้างประกาศของ AFT.SBTVC",
    )
    @app_commands.describe(
        หัวข้อ="หัวข้อของประกาศ",
        รายละเอียด="รายละเอียดของประกาศ",
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def announce(
        self,
        interaction: discord.Interaction,
        หัวข้อ: str,
        รายละเอียด: str,
    ) -> None:
        embed = discord.Embed(
            title=f"📢 {หัวข้อ}",
            description=รายละเอียด,
            timestamp=discord.utils.utcnow(),
        )

        embed.set_author(
            name="AFT.SBTVC",
            icon_url=interaction.guild.icon.url
            if interaction.guild and interaction.guild.icon
            else None,
        )
        embed.set_footer(
            text=f"ประกาศโดย {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url,
        )

        await interaction.response.send_message(embed=embed)

    @announce.error
    async def announce_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ คุณไม่มีสิทธิ์ใช้คำสั่ง /ประกาศ"
        else:
            message = "❌ เกิดข้อผิดพลาดในการสร้างประกาศ"
            print(f"/ประกาศ error: {error}")

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Announcements(bot))
