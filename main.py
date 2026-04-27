import discord
from discord.ext import commands
import asyncio
import random
import os

# Self-bot setup
bot = commands.Bot(command_prefix="!", self_bot=True)

# Danh sách quyền (Mặc định chỉ có mày dùng được)
# Self-bot sẽ tự nhận diện ID của mày khi online
whitelist = []
stop_nhay = False

DEFAULT_QUOTES = [
    "Ê {user}, sủa lên xem nào? Sao câm nín thế?",
    "Gõ nhanh cái tay lên {user}, chậm chạp thế này định dưỡng già à?",
    "Mẹ m s đó {user}, nhìn cái mặt là thấy không ưa rồi!",
    "Tầm này mà còn bơ à {user}, nhục thế ông cháu?",
    "Ngoi lên đây solo xem nào {user}, đừng có núp lùm nữa!",
    "Dậy mà rep đi {user}, nãy gáy to lắm mà giờ tắt đài rồi à?",
    "Nhìn {user} gõ phím mà tao tưởng rùa bò, chậm vcl!",
    "Tag cho cháy máy này {user}, tag cho nát cái điện thoại này!",
    "Sủa tiếp đi {user}, tao đang nghe đây, sủa hay tao cho cục xương!",
    "Cay không {user}? Cay thì làm gì đi chứ!",
    "Đừng có giả vờ ngoại tuyến nữa {user}, hèn thế?"
]

@bot.event
async def on_ready():
    if bot.user.id not in whitelist:
        whitelist.append(bot.user.id)
    print(f"Self-bot {bot.user} 123")

@bot.command()
async def add(ctx, member: discord.Member):
    if ctx.author.id == bot.user.id: # Chỉ mày mới được add người khác
        if member.id not in whitelist:
            whitelist.append(member.id)
            await ctx.send(f"Đã cấp quyền nhây cho {member.name}")
        else:
            await ctx.send("Đứa này có quyền sẵn rồi Nhi ơi!")

@bot.command()
async def remove(ctx, member: discord.Member):
    if ctx.author.id == bot.user.id:
        if member.id in whitelist and member.id != bot.user.id:
            whitelist.remove(member.id)
            await ctx.send(f"Đã thu hồi quyền của {member.name}")

@bot.command()
async def nhay(ctx, member: discord.Member):
    global stop_nhay
    if ctx.author.id not in whitelist:
        return # Không có quyền thì bot im re luôn
    
    stop_nhay = False
    try:
        await ctx.message.delete()
    except:
        pass
    
    quotes = DEFAULT_QUOTES.copy()
    if ctx.message.attachments:
        at = ctx.message.attachments[0]
        if at.filename.endswith(".txt"):
            content = await at.read()
            try:
                decoded = content.decode("utf-8")
            except:
                decoded = content.decode("latin-1")
            quotes = [line.strip() for line in decoded.split('\n') if line.strip()]

    while not stop_nhay:
        msg = random.choice(quotes).replace("{user}", member.mention)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.2, 1.8))
        await ctx.send(msg)
        await asyncio.sleep(random.uniform(1.5, 2.5))

@bot.command()
async def stop(ctx):
    if ctx.author.id in whitelist:
        global stop_nhay
        stop_nhay = True
        await ctx.send(".")

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
