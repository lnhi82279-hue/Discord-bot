import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Danh sách dự phòng nếu không có file
DEFAULT_QUOTES = ["Alo {user}!", "Hiện hồn đi {user}."]
stop_nhay = False

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã sẵn sàng!')

@bot.command()
async def nhay(ctx, member: discord.Member):
    global stop_nhay
    stop_nhay = False
    
    quotes = DEFAULT_QUOTES
    
    # Kiểm tra xem người dùng có gửi kèm file không
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.txt'):
            try:
                # Tải file về bộ nhớ tạm
                content = await attachment.read()
                # Giải mã và tách thành các dòng, loại bỏ dòng trống
                decoded_content = content.decode('utf-8').splitlines()
                quotes = [line.strip() for line in decoded_content if line.strip()]
                await ctx.send(f"✅ Đã nhận kịch bản từ file `{attachment.filename}`!")
            except Exception as e:
                await ctx.send(f"❌ Lỗi đọc file: {e}")
        else:
            await ctx.send("⚠️ File gửi kèm phải là định dạng .txt nha!")

    await ctx.send(f"Bắt đầu 'tấn công' {member.mention}...")

    while not stop_nhay:
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 2.5))
        
        # Chọn câu nhây và thay thế {user} bằng tag người đó
        raw_quote = random.choice(quotes)
        # Nếu trong file bạn viết chữ {user}, bot sẽ tự thay bằng tag
        final_message = raw_quote.replace("{user}", member.mention) if "{user}" in raw_quote else f"{raw_quote} {member.mention}"
        
        await ctx.send(final_message)
        await asyncio.sleep(random.randint(3, 6))

@bot.command()
async def stop(ctx):
    global stop_nhay
    stop_nhay = True
    await ctx.send("Đã dừng nhây!")

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
