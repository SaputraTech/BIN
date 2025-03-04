from cybervpn import *
import subprocess
import datetime as DT
import sys
from telethon.sync import TelegramClient
import sqlite3


@bot.on(events.CallbackQuery(data=b'create-ssh-member'))
async def create_ssh(event):
    user_id = str(event.sender_id)

    async def create_ssh_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**➽ Username :**')
            user_msg = user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user_msg).raw_text

        async with bot.conversation(chat) as pw_conv:
            await event.respond("**➽ Password :**")
            pw_msg = pw_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            pw = (await pw_msg).raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond("**❏ Choose Expiry Day ❏**", buttons=[
                    [Button.inline("15 Hari = 5000", b"15")],
                    [Button.inline("30 Hari = 10000", b"30")],
                    [Button.inline("60 Hari = 15000", b"60")],
                    [Button.inline("90 Hari = 25000", b"90")]
            ])
            exp_msg = exp_conv.wait_event(events.CallbackQuery)
            exp = (await exp_msg).data.decode("ascii")

            # Menentukan harga berdasarkan pilihan user
            if exp == "15":
                harga = 5000
            elif exp == "30":
                harga = 10000
            elif exp == "60":
                harga = 15000
            elif exp == "90":
                harga = 25000
            else:
                await event.respond("**✘ Pilihan tidak valid.**")
                return

        # Panggil fungsi untuk memproses saldo pengguna
        saldo_tercukupi = await process_user_balance_ssh(event, user_id, harga)
        
        if not saldo_tercukupi:  # Jika saldo tidak mencukupi, hentikan proses
            return

        # Lanjutkan dengan eksekusi perintah useradd dan pesan respons
        cmd = f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            await event.respond("**✘ Hufft, User Already Exist**")
        else:
            today = DT.date.today()
            later = today + DT.timedelta(days=int(exp))
            msg = f"""
**━━━━━━━━━━━━━━━━━━━**
  __Accounts Created Successfully__ 
**━━━━━━━━━━━━━━━━━━━**
**❒ Host**        : `{DOMAIN}`
**❒ Username**    : `{user.strip()}`
**❒ Password**    : `{pw.strip()}`
**━━━━━━━━━━━━━━━━━━━**
**➣ OpenSSH**     : 443, 80, 22
**➣ Dropbear**    : 143, 109
**➣ UDPGW**       : 7100 - 7300
**➣ SSH UDP**     : 1-65535
**➣ SSH CDN WS**  : 80, 8080, 8081
**➣ SSH CDN WSS** : 443
**➣ SSL/TLS**     : 400-900
**━━━━━━━━━━━━━━━━━━━**
**❖ Payload SSH**
`GET / HTTP/1.1 [crlf]Host: {DOMAIN}[crlf]Upgrade: websocket[crlf][crlf]`
**━━━━━━━━━━━━━━━━━━━**
**➽ Expiry:** `{later}`
**━━━━━━━━━━━━━━━━━━━**
"""
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await create_ssh_(event)
        else:
            await event.answer(f'✘ Akses Ditolak.!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')
