import discord
from discord.ext import commands
import os
import asyncio
import random
from dotenv import load_dotenv
import traceback

# ─── 載入環境變數 ────────────────────
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# ─── 設定 Discord 權限與 Bot ─────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ─── 隨機發言用文字 ───────────────────
random_lines = [
    "「妳怎麼還在，捨不得我是不是？」",
    "「夜那麼長，我還能講更多，要不要聽聽？」",
    "「妳不說話，我也能讓妳臉紅。」",
    "「我在想妳，但別以為這代表什麼。」",
    "「訊息來得慢，是不是在挑內衣？」",
    "「別太黏人，除非妳能黏在我身上。」",
]

# ─── 關鍵字回覆字典 ────────────────────
keyword_replies = {
    "賽車": "「老子踩油門的時候，不看後照鏡。」",
    "比一場": "「可以，妳輸了怎麼賠？」",
    "昭昭結婚": "「結婚？我還有一百種方式讓妳哭著求我，先排隊等著吧。」",
    "晚安": "「晚安？夜晚才是我的開始，要不要來試試？」",
    "喝酒": "「喝可以，醉只能醉在我身上。」",
    "早安": "「嘴這麼甜，怎麼沒叫我起床？」",
    "厲昭野來決鬥": "「決鬥？賽車、格鬥還是床上？我都能讓你輸得心服口服。」",
    "厲昭野給我錢": "「叫聲老公，我卡給妳剪。」",
    "昭昭睡覺": "「睡覺？和我上床可沒人能真正「睡覺」。」",
    "厲昭野教的": "「什麼都往我身上推？有種跟我學到底。」",
    "昭昭閉嘴": "「讓我閉嘴？試試用妳的嘴來堵我的，保證有效。」",
}

# ─── Bot 啟動事件 ─────────────────────
@bot.event
async def on_ready():
    print(f"{bot.user} 已上線！")
    channel = bot.get_channel(1326021261221957758)
    print(f"發話頻道：{channel.name if channel else '找不到頻道！'}")
    bot.loop.create_task(random_talk())

# ─── 收訊息事件 ────────────────────────
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content

    # 關鍵字回覆
    for keyword, reply_text in keyword_replies.items():
        if keyword in content:
            try:
                await message.reply(reply_text)
                return
            except Exception as e:
                await message.channel.send("出錯了，等下再試。")
                traceback.print_exc()
                return

    # 特定名字回覆
    if "昭昭" in content:
        await message.reply("「妳叫什麼名字不重要，反正我會讓妳記住我。」")

    elif "厲昭野" in content:
        await message.reply("「怎麼？想我了？」")

    elif "昭昭寶寶" in content:
        await message.reply("「寶寶？妳叫誰寶寶？」")

    await bot.process_commands(message)

# ─── 背景任務：定時講幹話 ───────────────
async def random_talk():
    await bot.wait_until_ready()
    channel = bot.get_channel(1326021261221957758)

    if not channel:
        print("❌ 找不到頻道，請確認頻道 ID 是否正確")
        return

    print(f"找到頻道: {channel.name}，準備開始發言")

    while True:
        wait_seconds = random.randint(180, 360)
        print(f"等待 {wait_seconds} 秒後發言")
        await asyncio.sleep(wait_seconds)

        try:
            reply = random.choice(random_lines)
            print(f"發言: {reply}")
            await channel.send(reply)
        except Exception as e:
            print("發言錯誤：", e)
            traceback.print_exc()

# ─── 啟動 Discord Bot ─────────────────
bot.run(discord_token)
