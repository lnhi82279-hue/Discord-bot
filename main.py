# main.py
import os
import asyncio
import random
import threading
from flask import Flask
import discord
from discord.ext import commands

# ====== CONFIG ======
TOKEN = os.getenv("token")  # set trong Railway variables
ADMIN_ID_RAW = os.getenv("1373258875549126687")  # set trong Railway variables (chỉ số)
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN chưa được đặt (env var).")

try:
    ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW else None
except Exception:
    ADMIN_ID = None

# ====== Keep-alive web server (Railway expects a web service) ======
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    # Note: debug=False to avoid reloader threads
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

# ====== Discord bot setup ======
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# troll replies (vui, không chửi nặng)
troll_replies = [
    "réo con đĩ mẹ m😏",
    "@ không con đĩ chó 🤨",
    "con gái mẹ m 😤",
    "@ thì gửi đơn xin trước 😂",
    "Ê ê réo lồn mẹ m 😎",
]

spam_tasks = {}  # channel_id -> asyncio.Task

def is_admin_check():
    async def predicate(ctx):
        if ADMIN_ID is None:
            return False
        return ctx.author.id == ADMIN_ID
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user} (ID {bot.user.id})")
    await bot.change_presence(activity=discord.Game("Đang troll server"))

@bot.event
async def on_message(message):
    # ignore bots
    if message.author.bot:
        return

    # If someone mentions admin
    if ADMIN_ID and any(u.id == ADMIN_ID for u in message.mentions):
        reply = random.choice(troll_replies)
        # Try delete original message (requires Manage Messages permission)
        try:
            await message.delete()
        except Exception as e:
            print("Không xóa được tin nhắn (thiếu permission?)", e)
        # Reply/troll the user
        try:
            await message.channel.send(f"<@{message.author.id}> {reply}")
        except Exception as e:
            print("đéo cb:", e)

        # DM admin a log (best-effort)
        try:
            admin_user = await bot.fetch_user(ADMIN_ID)
            dm_text = (
                f"Người dùng {message.author} đã mention bạn trong #{message.channel}.\n"
                f"Nội dung: {message.content} mày thích @ bố không"
                f"Link (nếu có): {getattr(message, 'jump_url', 'không có')}"
            )
            await admin_user.send(dm_text)
        except Exception as e:
            print("bố cho gửi chưa", e)

    # If someone mentions the bot
    if bot.user in message.mentions:
        reply = random.choice(troll_replies)
        try:
            await message.channel.send(f"<@{message.author.id}> {reply}")
        except Exception as e:
            print("Lỗi khi bot trả lời mention:", e)

    await bot.process_commands(message)

# ---- Commands (admin-only where appropriate) ----

@bot.command(name="troll")
@is_admin_check()
async def cmd_troll(ctx, member: discord.Member):
    """Admin troll 1 người."""
    reply = random.choice(troll_replies)
    await ctx.send(f"<@{member.id}> {reply}")

@bot.command(name="addreply")
@is_admin_check()
async def cmd_addreply(ctx, *, new_reply: str):
    """Admin thêm câu troll."""
    troll_replies.append(new_reply)
    await ctx.send("✅ Đã thêm câu troll.")

@bot.command(name="listreplies")
@is_admin_check()
async def cmd_listreplies(ctx):
    msg = "\n".join([f"{i+1}. {r}" for i, r in enumerate(troll_replies)])
    await ctx.send(f"📜 Danh sách reply:\n{msg}")

@bot.command(name="spam")
@is_admin_check()
async def cmd_spam(ctx, member: discord.Member, interval: float =.0, *, text: str = None):
    """
    Admin bắt bot spam mention:
    Usage: !spam @user 2.0 Nội dung...
    - interval: giây giữa 2 tin nhắn (mặc định 2s)
    - text: nếu không cung cấp sẽ dùng random troll
    Dừng bằng: !stop
    """
    channel_id = ctx.channel.id
    if channel_id in spam_tasks:
        await ctx.send("⚠️ Đang có spam trong kênh này rồi, dùng !stop để dừng trước.")
        return

    async def spam_loop():
        try:
            while channel_id in spam_tasks:
                msg = text or random.choice(troll_replies)
                await ctx.send(f"<@{member.id}> {msg}")
                await asyncio.sleep(max(0.5, float(interval)))
        except asyncio.CancelledError:
            return
        except Exception as e:
            print("Lỗi spam loop:", e)

    task = asyncio.create_task(spam_loop())
    spam_tasks[channel_id] = task
    await ctx.send(f"🚀 Bắt đầu spam {member.mention} (interval={interval}s).")

@bot.command(name="stop")
@is_admin_check()
async def cmd_stop(ctx):
    channel_id = ctx.channel.id
    task = spam_tasks.pop(channel_id, None)
    if task:
        task.cancel()
        await ctx.send("🛑 Đã dừng spam.")
    else:
        await ctx.send("❌ Không có spam nào đang chạy trong kênh này.")

@bot.command(name="ping")
async def cmd_ping(ctx):
    await ctx.send("Pong!")

# ---- START ----
if __name__ == "__main__":
    # Start web server thread for Railway
    keep_alive()
    # Run the bot
    bot.run(token)
