import re
import asyncio

from RaiChu.config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, IMG_6
from RaiChu.inline import stream_markup
from Process.design.thumbnail import thumb
from Process.design.chatname import CHAT_TITLE
from Process.filters import command, other_filters
from Process.queues import QUEUE, add_to_queue
from Process.main import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch
IMAGE_THUMBNAIL = "https://telegra.ph/file/519b6bc739756cb822039.png"


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("__Anonim__ bir Yöneticisiniz!\n\n» yönetici haklarından kullanıcı hesabına geri dönün.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için aşağıdaki **izinlere** sahip bir **Yönetici** olmam gerekiyor:\n\n» ❌ __Mesajları sil__\n» ❌ __Kullanıcıları davet et__\n» ❌ __Görüntülü sohbeti yönet__\n\nBittiğinde, /reload yazın"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Görüntülü sohbeti yönetin__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Mesajları sil__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Kullanıcı ekle__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot **\n\n**neden katılamadı**: `{e}`"
            )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **video indiriliyor...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __yalnızca 720, 480, 360'a izin verilir__ \n💡 **şimdi 720p'de video akışı**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=thumbnail,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🗂 **İsim:** [{songname}]({link}) | `video`\n💭 **Chat:** `{chat_id}`\n🧸 **Talep eden:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("🔄 **vc'ye katılıyor...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=thumbnail,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🗂 **İsim:** [{songname}]({link}) | `video`\n💭 **Chat:** `{chat_id}`\n🧸 **Talep eden:** {requester}",
                )
        else:
            if len(m.command) < 2:
                await m.reply_photo(
                     photo=f"{IMG_6}",
                    caption= "💬**Kullanım: /play Müzik Çalmak İçin Bir Başlık Şarkısı Verin veya Video Oynatmak için /vplay**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 Channel", url=f"https://t.me/zmonbots"),
                            InlineKeyboardButton("💭 Support", url=f"https://t.me/zmonios")
                        ],
                        [
                            InlineKeyboardButton("🗑 Kapat", callback_data="cls")
                        ]
                    ]
                )
            )
            else:
                loser = await c.send_message(chat_id, f"**indiriliyor**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                      )
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **Sonuç bulunamadı.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    shub, ytlink = await ytdl(url)
                    if shub == 0:
                        await loser.edit(f"❌ yt-dl sorunlar tespit edildi\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🗂 **İsim:** [{songname}]({url}) | `video`\n⏱ **Süre:** `{duration}`\n🧸 **Talep eden:** {requester}",
                            )
                        else:
                            try:
                                await loser.edit(
                            f"**Panthora İndirici**\n\n**Başlık**: {title[:22]}\n\n100% ████████████100%\n\n**Geçen süre**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🎵 **İsim:** [{songname}]({url}) | `video`\n⏱ **Süre:** `{duration}`\n🧸 **Talep eden:** {requester}",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply_photo(
                     photo=f"{IMG_6}",
                    caption="💫**Kullanım: /play Müzik Çalmak İçin Bir Başlık Şarkısı Verin veya Video Oynatma için /vplay**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 Channel", url=f"https://t.me/zmonbots"),
                            InlineKeyboardButton("💭 Support", url=f"https://t.me/zmonios")
                        ],
                        [
                            InlineKeyboardButton("🗑 Kapat", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            loser = await c.send_message(chat_id, f"**indiriliyor**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **Sonuç bulunamadı.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                shub, ytlink = await ytdl(url)
                if shub == 0:
                    await loser.edit(f"❌ yt-dl sorunlar tespit edildi\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🗂 **İsim:** [{songname}]({url}) | `video`\n⏱ **Süre:** `{duration}`\n🧸 **Talep eden:** {requester}",
                        )
                    else:
                        try:
                            await loser.edit(
                            f"**Panthora İndirici**\n\n**Baslık**: {title[:22]}\n\n100% ████████████100%\n\n**Geçen süre**: 00:00 Seconds\n\n**Ses Dönüştürme[FFmpeg Process]**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **İsim:** [{songname}]({url}) |`video`\n⏱ **Süre:** `{duration}`\n🧸 **Talep eden:** {requester}",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("__Anonim__ bir Yöneticisiniz!\n\n» yönetici haklarından kullanıcı hesabına geri dönün.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için aşağıdaki **izinlere** sahip bir **Yönetici** olmam gerekiyor:\n\n» ❌ __Mesajları sil__\n» ❌ __Kullanıcıları davet et__\n» ❌ __Görüntülü sohbeti yönet__\n\nBittiğinde , /reload yazın"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Görüntülü sohbeti yönetin__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Mesajları sil__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 Beni kullanmak için, aşağıda bana aşağıdaki izni verin:"
        + "\n\n» ❌ __Kullanıcı ekle__\n\nİşiniz bittiğinde tekrar deneyin.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot katılamadı**\n\n**sebep**: `{e}`"
            )

    if len(m.command) < 2:
        await m.reply("» akış için bana bir canlı bağlantı/m3u8 url/youtube bağlantısı verin.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **Yayın işleniyor...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **şimdi 720p'de video akışı yapıyor**"
                )
            loser = await c.send_message(chat_id, "🔄 **Yayın işleniyor...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            null, livelink = await ytdl(link)
        else:
            livelink = link
            null = 1

        if null == 0:
            await loser.edit(f"❌ yt-dl sorunları algılandı\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🧸 **Talep eden:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **vc'ye katılıyor...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"💡 **[Video Live]({link}) akış başladı.**\n\n💭 **Chat:** `{chat_id}`\n🧸 **Talep eden:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
