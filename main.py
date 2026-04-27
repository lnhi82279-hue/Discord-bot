import discord
from discord.ext import commands
import asyncio
import random
import os

# Cấu hình Intent để bot có quyền đọc tin nhắn
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ID của Nhi (Chủ bot)
ADMIN_ID = 1373258875549126687

# Danh sách những người được phép dùng lệnh
whitelist = [ADMIN_ID]

DEFAULT_QUOTES = [“mẹ m s đó {user}”, “cn đĩ lồn sủa lẹ {user}”, “cn chó mẹ m {user}”, “cn đĩ cặc {user}”, “địt mẹ m {user}”, “con lồn ei {user}”, “thấy bố chat nhah cái sợ à 😹😹 {user}”, “địt mẹ m kkkk {user}”, “thk chó súc vật {user}”, “thấy bố kẹp chữ bot là tưởng bố bot à cn đĩ {user}”, “đĩ mẹ m cn đĩ sv {user}”, “sủa lẹ đê m ei😹 {user}”, “m s đó em ei {user}”, “m nhah k cn đĩ ngu {user}”, “m thik soạn k cn chó lồn {user}”, “tới mốt cn chó lồn {user}”, “cái cn gái mẹ m {user}”, “bố chat dòg nào dòg nấy st vcl {user}”, “địt mẹ m nhah k cn chó {user}”, “lẹ ei m {user}”, “cn đĩ mẹ m cn chó ei {user}”, “cn lồn lẹ m {user}”]
stop_nhay = False

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã sẵn sàng hoạt động!')

@bot.command()
async def add(ctx, member: discord.Member):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("❌ Tuổi gì cấp quyền?")
    if member.id not in whitelist:
        whitelist.append(member.id)
        await ctx.send(f"✅ Đã cấp quyền cho {member.mention}")
    else:
        await ctx.send("Người này có quyền rồi má!")

@bot.command()
async def remove(ctx, member: discord.Member):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("❌ Không có quyền tước!")
    if member.id in whitelist:
        if member.id == ADMIN_ID:
            return await ctx.send("Định tự tước quyền mình luôn hả?")
        whitelist.remove(member.id)
        await ctx.send(f"🚫 Đã tước quyền của {member.mention}")

@bot.command()
async def nhay(ctx, member: discord.Member):
    global stop_nhay
    if ctx.author.id not in whitelist:
        return await ctx.send("⚠️ Bạn không có quyền dùng lệnh này!")

    # QUAN TRỌNG: Reset lại stop_nhay để có thể chạy nhiều lần
    stop_nhay = False 
    
    quotes = DEFAULT_QUOTES
    
    # Kiểm tra nếu Nhi gửi kèm file .txt để lấy câu chửi riêng
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.txt'):
            try:
                content = await attachment.read()
                decoded_content = content.decode('utf-8')
                quotes = [line.strip() for line in decoded_content.split('\n') if line.strip()]
                await ctx.send(f"✅ Đã nhận kịch bản nhây từ file!")
            except Exception as e:
                await ctx.send(f"❌ Lỗi đọc file rồi Nhi ơi!")

    await ctx.send(f"🚀 Bắt đầu nhây {member.mention}!")

    while not stop_nhay:
        async with ctx.typing():
            await await asyncio.sleep(random.randint(3, 5))
        
        raw_quote = random.choice(quotes)
        final_message = raw_quote.replace("{user}", member.mention)
        
        await ctx.send(final_message)
        # Thời gian chờ giữa các lần nhây (từ 1 đến 3 giây)
        await asyncio.sleep(random.randint(1, 3))

@bot.command()
async def stop(ctx):
    global stop_nhay
    if ctx.author.id not in whitelist:
        return
    stop_nhay = True
    await ctx.send("🛑 Đã dừng nhây!")

# Lấy Token từ biến môi trường trên Render (Không dán mã thật vào đây)
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("Lỗi: Không tìm thấy DISCORD_TOKEN trong Environment!")
