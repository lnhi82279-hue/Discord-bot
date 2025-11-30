# main.py
import discord
from discord.ext import commands
from discord.utils import format_dt

intents = discord.Intents.default()
intents.members = True  # Bật event khi có thành viên mới
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel  # hoặc set channel khác bằng ID

    if channel:
        embed = discord.Embed(
            title="🎉 Thành viên mới vừa tham gia!",
            description=f"Chào mừng {member.mention} đến với server!",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📌 Hồ sơ người mới",
            value=(
                f"**Tên:** {member.name}\n"
                f"**ID:** {member.id}\n"
                f"**Ngày tạo tài khoản:** {format_dt(member.created_at, 'R')}\n"
            ),
            inline=False
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        await channel.send(embed=embed)

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
