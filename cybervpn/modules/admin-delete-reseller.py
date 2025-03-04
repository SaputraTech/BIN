from cybervpn import *
import subprocess
import datetime as DT
import asyncio

@bot.on(events.CallbackQuery(data=b'skt-delete-member'))
async def delete_handler(event):
    chat = event.chat_id
    sender = await event.get_sender()
    user_id = str(event.sender_id)

    async def delete_member(telegram_id):
        hapus_user(telegram_id)
        today = DT.date.today()
        later = today + DT.timedelta(days=int(0))
        msg = f"""
───────────────────────
    𝐀𝐜𝐭𝐢𝐨𝐧 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲
**User Reseller Berhasil Dihapus**
───────────────────────
 👤Reseller ID : {telegram_id}
───────────────────────
 📝Remove Date : {later}
"""
        await event.respond(msg)

    async with bot.conversation(chat) as conv:
        try:
            # Input Telegram ID
            await conv.send_message('**masukan id reseller :**')
            id_msg = await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            telegram_id = id_msg.raw_text

            await delete_member(telegram_id)

            user_level = get_level_from_db(user_id)
            print(f'Retrieved level from database: {user_level}')

            if user_level == 'admin':
                await delete_handler(event)
            else:
                await event.answer(f'Akses Ditolak..!!', alert=True)

        except asyncio.TimeoutError:
            print("Timeout occurred during conversation.")
            await event.respond("Percakapan timeout. Silakan coba lagi.")
        except Exception as e:
            print(f'Error: {e}')

