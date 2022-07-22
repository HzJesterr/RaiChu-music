
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from RaiChu.config import BOT_NAME as bn
from Process.filters import other_filters2
from time import time
from datetime import datetime
from Process.decorators import authorized_users_only
from RaiChu.config import BOT_USERNAME, ASSISTANT_USERNAME

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 ** 2 * 24),
    ("hour", 60 ** 2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(other_filters2)
async def start(_, message: Message):
        await message.reply_text(
        f"""** Merhaba , ben Jester Music Bot ✋

              Telegram görüntülü sohbetinde müzik ve video hatta YouTube uzerinden canlı yayın oynatabilirim.😁😁
              Powered by ❤️ @zmonios**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "**Sahibim**", url="https://t.me/sarikola"
                    ),
                    InlineKeyboardButton(
                        "**Komutlar**", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "Beni nasıl eklersin ? 🤠", callback_data="cbhowtouse"
                    ),
                  ],[
                    InlineKeyboardButton(
                       " 𝐒𝐮𝐩𝐩𝐨𝐫𝐭👿", url="https://t.me/zmonios"
                    ),
                    InlineKeyboardButton(
                        "𝐔𝐩𝐝𝐚𝐭𝐞𝐬", url="https://t.me/zmonbots"
                    )
                ],[
                    InlineKeyboardButton(
                        "➕ **Gruba Ekle** ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )
