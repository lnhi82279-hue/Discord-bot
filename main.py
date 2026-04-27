import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ADMIN_ID = 1373258875549126687 # Đã lấy từ ID của bạn
whitelist = [ADMIN_ID]
DEFAULT_QUOTES = ["Alo {user}!", "Hiện hồn đi {user}."]
stop_nhay = False

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã sẵn sàng!')

@bot.command()
async def add(ctx, member: discord.Member):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("❌ Tuổi gì?")
    if member.id not in whitelist:
        whitelist.append(member.id)
        await ctx.send(f"✅ Đã cấp quyền cho {member.mention}")
    else:
        await ctx.send("Người này có quyền rồi!")

@bot.command()
async def nhay(ctx, member: discord.Member):
    if ctx.author.id not in whitelist:
        return await ctx.send("⚠️ Bạn không có quyền!")
    
    global stop_nhay
    stop_nhay = False
    quotes = DEFAULT_QUOTES
    
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.txt'):
            try:
                content = await attachment.read()
                decoded_content = content.decode('utf-8').splitlines()
                quotes = [line.strip() for line in decoded_content if line.strip()]
                await ctx.send(f"✅ Nhận kịch bản từ file!")
            except Exception as e:
                await ctx.send(f"❌ Lỗi file: {e}")

    await ctx.send(f"Bắt đầu nhây {member.mention}...")
    while not stop_nhay:
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1, 2))
        final_message = random.choice(quotes).replace("{user}", member.mention)
        await ctx.send(final_message)
        await asyncio.sleep(random.randint(3, 6))

@bot.command()
async def stop(ctx):
    if ctx.author.id in whitelist:
        global stop_nhay
        stop_nhay = True
        await ctx.send("Đã dừng nhây!")

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
