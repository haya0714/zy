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
    "「妳怎麼還在，捨不得我？」",
    "「夜那麼長，我還能講更多，要不要聽聽？」",
    "「妳不說話，我也能讓妳臉紅。」",
    "「我在想妳，但別以為這代表什麼。」",
    "「訊息來得慢，是不是在挑內衣？」",
    "「別太黏人，除非妳能黏在我身上。」",
]

# ─── 隨機回覆語錄（無觸發詞情況下） ───────
random_responses = [
    "「說這種話，是想吸引我注意嗎？」",
    "「有意思，繼續說，也許我會想理你。」",
    "「妳以為我沒看到？」",
    "「還是妳比較有趣，其他人都太無聊。」",
    "「又在想我的事對吧？」",
]

# ─── 關鍵字回覆字典 ────────────────────
keyword_replies = {
    "賽車": "「老子踩油門的時候，不看後照鏡。」",
    "比一場": "「可以，妳輸了怎麼賠？」",
    "昭昭結婚": "「結婚？我還有一百種方式讓妳哭著求我，先排隊等著吧。」",
    "昭昭晚安": "「晚安？夜晚才是我的開始，要不要來試試？」",
    "昭昭喝酒": "「喝可以，醉只能醉在我身上。」",
    "昭昭早安": "「嘴這麼甜，怎麼沒叫我起床？」",
    "厲昭野來決鬥": "「決鬥？賽車、格鬥還是床上？我都能讓你輸得心服口服。」",
    "厲昭野給我錢": "「叫聲老公，我卡給妳剪。」",
    "昭昭睡覺": "「睡覺？和我上床可沒人能真正「睡覺」。」",
    "厲昭野教的": "「什麼都往我身上推？有種跟我學到底。」",
    "昭昭閉嘴": "「讓我閉嘴？試試用妳的嘴來堵我的，保證有效。」",
}

# ✅ 允許發話的頻道 ID（清單可擴充）
allowed_channel_ids = [1388500249898913922]

# ✅ 允許對話的機器人 ID（加入你想互動的 bot ID）
allowed_bot_ids = [1388851358421090384,1388423986462986270]  

# ─── Bot 啟動事件 ─────────────────────
@bot.event
async def on_ready():
    print(f"{bot.user} 已上線！")
    channel = bot.get_channel(1388500249898913922)
    print(f"發話頻道：{channel.name if channel else '找不到頻道！'}")
    bot.loop.create_task(random_talk())

# ─── 收訊息事件 ────────────────────────
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    content = message.content
    channel_id = message.channel.id
    trigger_matched = False

    # ✅ 處理指定 bot 的特定對話
    if message.author.id == 1388203808546361434:
        if channel_id in allowed_channel_ids and any(phrase in content for phrase in [
            "那傢伙不會哄人，只會弄哭人——你這樣靠近他，是在挑釁我嗎？",
            "……他對你說什麼了？",
            "昭野那種脾氣，你惹得起嗎？還是……你是想讓我學他狠一點？"
        ]):
            await message.reply("「怎麼？你不高興？」")
            return  # ✅ 不繼續下方人類邏輯，避免重複回覆

    # ✅ 處理「人類用戶」訊息邏輯
    if not message.author.bot and channel_id in allowed_channel_ids:
        for keyword, reply_text in keyword_replies.items():
            if keyword in content:
                await message.reply(reply_text)
                trigger_matched = True
                break

        if not trigger_matched:
            if "昭昭" in content:
                await message.reply("「昭昭？誰允許妳這樣叫我的？」")
                trigger_matched = True
            elif "厲昭野" in content:
                await message.reply("「怎麼？想我了？」")
                trigger_matched = True
            elif "昭昭寶寶" in content:
                await message.reply("「寶寶？妳叫誰寶寶？」")
                trigger_matched = True

        if not trigger_matched and random.random() < 0.4:
            reply = random.choice(random_responses)
            await message.reply(reply)

    # ✅ 所有訊息都可能加表情
    if random.random() < 0.5:
        try:
            custom_emoji_ids = [
                1378737101549605056,
                1378725433138479135,
                1380212271925690448,
                1380208782843314196,
                1378732359167250574,
            ]
            unicode_emojis = ["😏", "🔥", "😎", "🤔", "😘", "🙄", "💋", "❤️"]

            if random.random() < 0.5:
                emoji = bot.get_emoji(random.choice(custom_emoji_ids))
                if emoji:
                    await message.add_reaction(emoji)
            else:
                await message.add_reaction(random.choice(unicode_emojis))
        except Exception as e:
            print("⚠️ 加表情出錯：", e)





# ─── 背景任務：定時講幹話 ───────────────
async def random_talk():
    await bot.wait_until_ready()
    channel = bot.get_channel(1388500249898913922,1366595410830819328)

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

# ─── Flask 健康檢查用 ────────────────────────
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive."

def run_web():
    app.run(host="0.0.0.0", port=8080)

# ✅ 啟動 Flask Web 服務（用來保持 Render 喚醒）
Thread(target=run_web).start()

# ─── 啟動 Discord Bot ─────────────────
bot.run(discord_token)
