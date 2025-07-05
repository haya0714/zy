import discord
from discord.ext import commands
import os
import asyncio
import random
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from utils import get_ai_reply

# ─── 載入環境變數 ────────────────────
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# ─── 設定 Discord 權限與 Bot ─────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ─── 可允許對話的頻道 ID ─────────────
allowed_channel_ids = [1388500249898913922, 1366595410830819328]

# ─── 啟動事件 ────────────────────────
@bot.event
async def on_ready():
    print(f"{bot.user} 已上線！")
    channel = bot.get_channel(allowed_channel_ids[0])
    print(f"發話頻道：{channel.name if channel else '找不到頻道！'}")

# ─── 訊息處理事件 ────────────────────
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    content = message.content
    channel_id = message.channel.id

    if not message.author.bot and channel_id in allowed_channel_ids:
        try:
            loop = asyncio.get_event_loop()
            reply = await loop.run_in_executor(None, get_ai_reply, content)
            await message.reply(reply or "……我懶得回你了。")
        except Exception as e:
            print("❌ 語言模型回覆錯誤：", e)
            await message.reply("……我懶得回你了。")

    # ─── 隨機加入表情反應 ──────────────
    if random.random() < 0.4:
        try:
            custom_emoji_ids = [
                1378737101549605056,
                1378725433138479135,
                1380212271925690448,
                1380208782843314196,
                1378732359167250574,
            ]
            unicode_emojis = ["😏", "🔥", "😎", "🤔", "😘", "🙄", "💋", "❤️"]

            if random.random() < 0.4:
                emoji = bot.get_emoji(random.choice(custom_emoji_ids))
                if emoji:
                    await message.add_reaction(emoji)
            else:
                await message.add_reaction(random.choice(unicode_emojis))
        except Exception as e:
            print("⚠️ 加表情出錯：", e)

# ─── 背景任務：健康檢查 ────────────────
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive."

def run_web():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()

# ─── 啟動 Discord Bot ─────────────────
bot.run(discord_token)
