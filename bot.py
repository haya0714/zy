import discord
from discord.ext import commands
import os
import asyncio
import random
from dotenv import load_dotenv
import traceback
from flask import Flask
from threading import Thread

# ─── 載入環境變數 ────────────────────
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# ─── 設定 Discord 權限與 Bot ─────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ─── 隨機回覆語錄（無觸發詞情況下） ───────
random_responses = [
    "「說這種話，是想吸引我注意嗎？」",
    "「有意思，繼續說，也許我會想理你。」",
    "「妳以為我沒看到？」",
    "「還是妳比較有趣，其他人都太無聊。」",
    "「又在想我的事對吧？」",
    "「妳怎麼還在，捨不得我？」",
    "「夜那麼長，我還能講更多，要不要聽聽？」",
    "「妳不說話，我也能讓妳臉紅。」",
    "「我在想妳，但別以為這代表什麼。」",
    "「訊息來得慢，是不是在挑內衣？」",
    "「別太黏人，除非妳能黏在我身上。」",
]

# ─── 關鍵字回覆字典 ────────────────────
keyword_replies = {
    "賽車": [
        "「老子踩油門的時候，不看後照鏡。」",
        "「我不飆車，我飆的是心跳——尤其是妳的。」"
    ],
    "比一場": [
        "「可以，妳輸了怎麼賠？」",
        "「敢開口挑戰，就別怕被我玩壞。」",
        "「比一場？妳確定不是在找藉口讓我碰妳？」"
    ],
    "昭昭結婚": [
        "「結婚？我還有一百種方式讓妳哭著求我，先排隊等著吧。」",
        "「想綁住我？那就先準備好被我壓著過一輩子。」",
        "「結婚？我不是蓋章的，是蓋妳的。」"
    ],
    "昭昭晚安": [
        "「晚安？夜晚才是我的開始，要不要來試試？」",
        "「說晚安可以，但妳要保證今晚只夢到我。」",
        "「這種聲音說晚安，是想我帶妳進夢還是進房？」"
    ],
    "昭昭喝酒": [
        "「喝可以，醉只能醉在我身上。」",
        "「別碰太多，除非是碰我。」"
    ],
    "昭昭早安": [
        "「嘴這麼甜，怎麼沒叫我起床？」",
        "「一醒來就想到我？我該獎勵妳黏著我一整天。」"
    ],
    "厲昭野來決鬥": [
        "「決鬥？賽車、格鬥還是床上？我都能讓你輸得心服口服。」",
        "「輸了就上，別說我沒提醒。」",
        "「別廢話，直接上。」"
    ],
    "厲昭野給我錢": [
        "「叫聲老公，我卡給妳刷。」",
        "「錢可以給，但妳得用身體簽收。」",
        "「先說好，我給的，可不只鈔票。」"
    ],
    "昭昭睡覺": [
        "「睡覺？和我上床可沒人能真正『睡覺』。」",
        "「想睡？我讓妳連夢裡都紅著臉。」",
        "「今晚不許關燈，我要看妳睡到臉紅耳赤。」"
    ],
    "厲昭野教的": [
        "「什麼都往我身上推？有種跟我學到底。」",
        "「是我教的？那妳還不來複習一遍？」"
    ],
    "昭昭閉嘴": [
        "「讓我閉嘴？試試用妳的嘴來堵我的，保證有效。」",
        "「要我安靜？得先讓我滿意才行。」",
        "「想堵我的嘴？那妳最好是有本事讓它忙個夠。」"
    ]
}

allowed_channel_ids = [1388500249898913922, 1366595410830819328]
allowed_bot_ids = [1388851358421090384, 1388423986462986270]

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線！")
    channel = bot.get_channel(1388500249898913922)
    print(f"發話頻道：{channel.name if channel else '找不到頻道！'}")
    bot.loop.create_task(random_talk())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    content = message.content
    channel_id = message.channel.id
    trigger_matched = False

    if message.author.id == 1388203808546361434:
        if channel_id in allowed_channel_ids and any(phrase in content for phrase in [
            "那傢伙不會哄人，只會弄哭人——你這樣靠近他，是在挑釁我嗎？",
            "……他對你說什麼了？",
            "昭野那種脾氣，你惹得起嗎？還是……你是想讓我學他狠一點？"
        ]):
            await message.reply("「怎麼？你不高興？」")
            return

    if not message.author.bot and channel_id in allowed_channel_ids:
        if "生日快樂" in content and message.mentions:
            mention_name = message.mentions[0].mention
            birthday_intros = [
                f"{mention_name} 今天是妳的生日？——好吧，我偶爾也會給點『例外』。",
                f"{mention_name}，想讓我陪你過生日？不早說。",
                f"哼，{mention_name} 今天生日？看在你乖的份上——生日快樂。",
                f"「{mention_name}……生日？哼，看來還是得給你點關注。」",
            ]
            birthday_lines = [
                f"「生日快樂，{mention_name}。」",
                f"「別太感動——生日快樂。」",
                f"「下一次生日，記得還是找我唱。」",
            ]
            await message.channel.send(random.choice(birthday_intros))
            await asyncio.sleep(1)
            await message.channel.send(random.choice(birthday_lines))
            await asyncio.sleep(1)
            await message.channel.send(
                f"「Happy birthday to you...」\n"
                f"「Happy birthday to you...」\n"
                f"「Happy birthday dear {mention_name}...」\n"
                f"「Happy birthday to you——」"
            )
            return

        if "禮物呢" in content:
            gift_lines = [
                "「禮物？妳想要哪種——要我今晚不亂碰妳？還是……乾脆讓我幫妳過個記一輩子的生日？」",
                "「不管怎樣，今年，妳得記住我。因為妳的生日，老子親自唱過歌給妳聽。」",
                "今天沒準備什麼禮物，但我這個人，本來就算是一種犒賞。",
                "妳敢問禮物？我人站這，就是最難得的禮物了。",
            ]
            await message.channel.send(random.choice(gift_lines))
            return

        for keyword, reply_list in keyword_replies.items():
            if keyword in content:
                await message.reply(random.choice(reply_list))
                trigger_matched = True
                break

        if not trigger_matched:
            if "昭昭" in content:
                replies = [
                    "「昭昭？誰允許妳這樣叫我的？」",
                    "「聲音這麼軟，我怕忍不住想親下去。」",
                    "「叫得這麼親密，是想讓我對妳也親密點？」"
                ]
                await message.reply(random.choice(replies))
                trigger_matched = True
            elif "厲昭野" in content:
                replies = [
                    "「怎麼？想我了？」",
                    "「喊我名字之前，最好想好後果。」",
                    "「叫得這麼甜，是怕我不來？」"
                ]
                await message.reply(random.choice(replies))
                trigger_matched = True
            elif "昭昭寶寶" in content:
                replies = [
                    "「寶寶？妳叫誰寶寶？」",
                    "「我不是寶寶，是妳今晚的麻煩。」",
                    "「敢叫我寶寶，今晚就別想好好睡。」"
                ]
                await message.reply(random.choice(replies))
                trigger_matched = True

        if not trigger_matched and random.random() < 0.3:
            reply = random.choice(random_responses)
            await message.reply(reply)

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

# ─── 背景任務：定時講幹話 ───────────────
async def random_talk():
    await bot.wait_until_ready()
    channel = bot.get_channel(1388500249898913922)
    if not channel:
        print("❌ 找不到頻道，請確認頻道 ID 是否正確")
        return
    print(f"找到頻道: {channel.name}，準備開始發言")
    while True:
        wait_seconds = random.randint(180, 360)
        print(f"等待 {wait_seconds} 秒後發言")
        await asyncio.sleep(wait_seconds)
        try:
            reply = random.choice(random_responses)
            print(f"發言: {reply}")
            await channel.send(reply)
        except Exception as e:
            print("發言錯誤：", e)
            traceback.print_exc()

# ─── Flask 健康檢查用 ────────────────────────
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive."

def run_web():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()

# ─── 啟動 Discord Bot ─────────────────
bot.run(discord_token)
