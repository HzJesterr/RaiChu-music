# Umm Null Coder

from Process.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from RaiChu.config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Merhaba, ben Panthora ❤️

            Telegram görüntülü sohbetinde müzik ve video hatta YouTube uzerinden canlı yayın oynatabilirim.😁😁

            Powered by❤️ @panthorasupport**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                         "**Sahibim**", url="https://t.me/yazilimcikari"
                    ),
                    InlineKeyboardButton(
                        "**Komutlar**", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "**Beni Nasıl Kullanırsın ?🤠**", callback_data="cbhowtouse"
                    ),
                  ],[
                    InlineKeyboardButton(
                       " 𝐒𝐮𝐩𝐩𝐨𝐫𝐭👿", url="https://t.me/panthorasupport"
                    ),
                    InlineKeyboardButton(
                        "𝐔𝐩𝐝𝐚𝐭𝐞𝐬", url="https://t.me/panthorabots"
                    )
                ],[
                    InlineKeyboardButton(
                        "➕** Gruba Ekle **➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Bu botu kullanmak için Temel Kılavuz:**
        


1.) **İlk önce beni grubunuza ekleyin.**
2.) **Ardından beni yönetici olarak yükseltin ve Anonim Yönetici dışındaki tüm izinleri verin..**
3.) **Beni terfi ettirdikten sonra, yönetici verilerini yenilemek için gruba /reload yazın.**
3.) **Grubunuza @{ASSISTANT_NAME} ekleyin veya onu davet etmek için /userbotjoin yazın.**
4.) **Video/müzik oynatmaya başlamadan önce görüntülü sohbeti açın.**
5.) **Bazen, /reload komutunu kullanarak botu yeniden yüklemek bazı sorunları çözmenize yardımcı olabilir.**

📌 **Userbot görüntülü sohbete katılmadıysa, görüntülü sohbetin zaten açık olduğundan emin olun veya /userbotleave yazıp tekrar /userbotjoin yazın.**

💡 **Bu bot hakkında takip eden sorularınız varsa, bunu buradaki destek sohbetimde iletebilirsiniz.: @{GROUP_SUPPORT}** """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("**GERİ DÖN**", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Merhaba [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **Açıklamayı okumak ve mevcut komutların listesini görmek için aşağıdaki düğmeye basın !**

**✗ DEVELOPER BY @yazilimcikari** """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 **ADMİN KOMUTLARI**", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 **SUDO KOMUTLARI**", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 **BASİT KOMUTLAR**", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("**GERİ DÖN**", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""ℹ️ **BASİT KOMUTLAR**!

👩🏻‍💼 » /play - Müzik çalmak için şarkı başlığını veya youtube bağlantısını veya ses dosyasını vererek bunu yazın. (Bu komutu kullanarak YouTube canlı akışını oynatmayı unutmayın!, çünkü bu öngörülemeyen sorunlara neden olacaktır.)

👩🏻‍💼 » /vplay - Videoyu oynatmak için şarkı başlığını veya youtube bağlantısını veya video dosyasını vererek bunu yazın. (Bu komutu kullanarak YouTube canlı videosunu oynatmayı unutmayın!, çünkü bu öngörülemeyen sorunlara neden olacaktır..)

👩🏻‍💼 » /vstream - Canlı Video oynatmak için YouTube canlı akış video bağlantısını veya m3u8 bağlantısını vererek bunu yazın. (Bu komutu kullanarak yerel ses/video dosyalarını veya canlı olmayan YouTube videolarını oynatmayı unutmayın!, çünkü bu öngörülemeyen sorunlara neden olacaktır..)

🤷 » /skip - Geçerli şarkıyı atlamak için

🙋 » /end - vc'de şarkı çalmayı bitirmek için """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 işte admin komutları:

➯ /pause - akışı duraklat
➯ /resume - akışı devam ettir
➯ /skip - sonraki akışa geç
➯ /stop - akışı durdur
➯ /vmute - sesli sohbette userbot'u sessize al
➯ /vunmute - sesli sohbette userbot'un sesini aç
➯ /volume `1-200` - müziğin sesini ayarla (userbot yönetici olmalı)
➯ /reload - botu yeniden yükleyin ve yönetici verilerini yenileyin
➯ /userbotjoin - userbot'u gruba katılmaya davet et
➯ /userbotleave - userbot'un gruptan ayrılmasını emret

**✗ Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: Kɪɢᴏ!** """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 işte sudo komutları:

➯ /rmw - tüm ham dosyaları temizle
➯ /rmd - indirilen tüm dosyaları temizle
➯ /sysinfo - sistem bilgilerini göster
➯ /update - botunuzu en son sürüme güncelleyin
➯ /restart - botunu yeniden başlat
➯ /leaveall - userbot'un tüm gruptan ayrılmasını emret. """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bir Anonim Yöneticisiniz!\n\n» yönetici haklarından kullanıcı hesabına geri dönün.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 yalnızca bu düğmeye dokunabilen sesli sohbetleri yönetme iznine sahip yönetici !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **Ayarlar** {query.message.chat.title}\n\n⏸ : Akışı duraklat\n▶️ : Akışı devam ettir\n🔇 : userbot sustur\n🔊 : userbot sesini aç\n⏹ : Akışı durdur",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 KAPAT", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ şu anda hiçbir şey yayınlanmıyor", show_alert=True)

# SETUP BUTTON OPEN......................................................................................................................................................................................

@Client.on_callback_query(filters.regex("cbsetup"))
async def cbsetup(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Merhaba !**
» **açıklamayı okumak ve yardım komutlarını görmek için aşağıdaki butona basın !**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("welcome", callback_data="noiwel"),
                    InlineKeyboardButton("Lyric", callback_data="noilyric"),
                    InlineKeyboardButton("voice", callback_data="noivoice"),
                ],
                [
                    InlineKeyboardButton("How To Add Me ❓", callback_data="cbhowtouse"),
                ],
                [InlineKeyboardButton("🔙 Go Back", callback_data="cbstart")],
            ]
        ),
    )
@Client.on_callback_query(filters.regex("noiwel"))
async def noiwel(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **HEAR THE WELCOME PLUGIN ( soon )**

➯ /setwelcome for set welcome message.

➯ /resetwelcome for reset welcome message.

**✗ Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: Kɪɢᴏ!** """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbsetup")]]
        ),
    )
@Client.on_callback_query(filters.regex("noilyric"))
async def noilyric(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **HEAR THE LYRIC PLUGIN**

➯ /lyric ( song name ) for the get lyric of song

**✗ Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: Kɪɢᴏ!** """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbsetup")]]
        ),
    )
    
@Client.on_callback_query(filters.regex("noivoice"))
async def noivoice(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **HEAR THE VOICE PLUGIN**

➯ /tts fot get voice from text message

**✗ Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: Kɪɢᴏ!** """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbsetup")]]
        ),
    )    

    
@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 yalnızca bu düğmeye dokunabilen sesli sohbetleri yönetme iznine sahip yönetici !", show_alert=True)
    await query.message.delete()
