from cybervpn import *
import requests
import subprocess
import time
import os
@bot.on(events.CallbackQuery(data=b'reboot'))
async def reboot(event):
    user_id = str(event.sender_id)
    async def reboot_(event):
        cmd = 'reboot'
        subprocess.check_output(cmd, shell=True)
        await event.edit("""
**𝓡𝓔𝓑𝓞𝓞𝓣 𝓢𝓔𝓡𝓥𝓔𝓡 𝓑𝓔𝓡𝓗𝓐𝓢𝓘𝓛...**
""", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await reboot_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'resx'))
async def resx(event):
    user_id = str(event.sender_id)
    async def resx_(event):
        cmd = f'systemctl restart nginx | systemctl restart xray | systemctl restart rc-local | systemctl restart client | systemctl restart server | systemctl restart dropbear | systemctl restart ws | systemctl restart openvpn | systemctl restart cron | systemctl restart haproxy | systemctl restart netfilter-persistent | systemctl restart squid | systemctl restart udp-custom'
        subprocess.check_output(cmd, shell=True)
        await event.edit("""
**↻ 𝖲𝖾𝗋𝗏𝗂𝖼𝖾 𝖡𝖾𝗋𝗁𝖺𝗌𝗂𝗅 𝖣𝗂 𝖱𝖾𝗌𝗍𝖺𝗋𝗍...**
""", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await resx_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'service-status'))
async def show_ssh(event):
    user_id = str(event.sender_id)

    async def show_ssh_(event):
        a = 'bash /usr/bin/status-service'
        x = subprocess.check_output(a, shell=True).decode("utf-8")
        await event.respond(f"""
```{x}```

""", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await show_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)

    except Exception as e:
        print(f'Error: {e}')

	

@bot.on(events.CallbackQuery(data=b'traffic'))
async def show_ssh(event):
    user_id = str(event.sender_id)

    async def show_ssh_(event):
        a = 'bash /usr/bin/traffic-server'
        x = subprocess.check_output(a, shell=True).decode("utf-8")
        await event.respond(f"""
```{x}```

""", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await show_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)

    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'backup'))
async def backup(event):
    user_id = str(event.sender_id)
    async def backup_(event):
        cmd = 'printf "%s\n" | backup-bot'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Not Exist**")
        else:
            msg = f"```\nbackup data server berhasil...\n```"
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await backup_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'rest'))
async def upload(event):
    user_id = str(event.sender_id)
    async def upload_(event):
        me = await bot.get_me()
        async with bot.conversation(event.chat_id) as con:
            await event.reply('**(Reply This Chat) Upload File :**')
            file = con.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            file = await file
            file = file.message.media
            file = await event.client.download_media(file, "/media/")
            path = file
            sex = "restore-bot"
            ox = subprocess.check_output(sex, shell=True).decode("utf-8")
            msg = f"{ox}"

        await event.respond("`Please Wait Proccess Restored`".format(os.path.basename(file)))
        await event.respond(msg, buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await upload_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.NewMessage(pattern="(?:.restore|/restore)"))
async def rest(event):
    user_id = str(event.sender_id)
    db = get_db()

    async def rest_(event):
        if event.is_reply:
            try:
                restore = await event.client.download_media(
                    await event.get_reply_message(),
                    "cybervpn/",
                )

                if "(" not in restore:
                    path1 = Path(restore)
                    await event.respond(
                        "Uploaded To Server `{}`".format(
                            os.path.basename(restore)
                        )
                    )
                    owe = subprocess.check_output(restorebot, shell=True)
                    await event.respond(f"{owe}", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])
                else:
                    os.remove(restore)
                    await event.respond("Restore Data Failed")
            except Exception as e:
                await event.respond(str(e))
                os.remove(restore)

        await asyncio.sleep(DELETE_TIMEOUT)
        await event.delete()

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await rest_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'topup'))
async def show_ssh(event):
    user_id = str(event.sender_id)

    async def show_ssh_(event):
        await event.respond(f"""
🧿 𝙼𝚎𝚗𝚞 𝚃𝙾𝙿𝚄𝙿
- 𝔸𝕦𝕥𝕙𝕠𝕣: @SaputraTech
━━━━━━━━━━━━━━━━━━━━━━
- 𝐌𝐢𝐧𝐢𝐦𝐚𝐥 𝐓𝐎𝐏𝐔𝐏 𝐑𝐩. 25000
- ᴘᴀꜱᴛɪᴋᴀɴ ꜱᴜᴅᴀʜ ᴍᴇɴᴄᴏʙᴀ ᴛʀɪᴀʟ ᴅᴀɴ ᴛᴇʟᴀʜ,
ᴍᴇᴍʙᴀᴄᴀ ᴄᴀᴛᴀᴛᴀɴ #FAQ ᴅᴀɴ #TOS ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.

👑 𝙼𝚎𝚗𝚞 𝙱𝙾𝙽𝚄𝚂
- ℙ𝕄: @SaputraTech
━━━━━━━━━━━━━━━━━━━━━━
𝑻𝒐𝒑𝒖𝒑 𝑹𝒑 25.000 𝒃𝒐𝒏𝒖𝒔 𝑹𝒑 2.000
𝑻𝒐𝒑𝒖𝒑 𝑹𝒑 40.000 𝒃𝒐𝒏𝒖𝒔 𝑹𝒑 4.000
𝑻𝒐𝒑𝒖𝒑 𝑹𝒑 50.000 𝒃𝒐𝒏𝒖𝒔 𝑹𝒑 5.000
𝑻𝒐𝒑𝒖𝒑 𝑹𝒑 100.000 𝒃𝒐𝒏𝒖𝒔 𝑹𝒑 15.000
━━━━━━━━━━━━━━━━━━━━━━
""", buttons=[[Button.inline(" 🔙 Main Menu", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await show_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)

    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'panel'))
async def backers(event):
    user_id = str(event.sender_id)
    async def backers_(event):
        inline = [
            [Button.inline(" Tambah Reseller", "registrasi-member"), Button.inline(" Hapus Reseller", "skt-delete-member")],
            [Button.inline(" List Member Reseller", "skt-show-user")],
            [Button.inline(" ➕ 𝕋𝕒𝕞𝕓𝕒𝕙 𝕊𝕒𝕝𝕕𝕠 ➕", "skt-addsaldo")],
            [Button.inline(" Kembali", "menu")]
        ]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
━━━━━━━━━━━━━━━━━━━━━━━━
 ❐ 𝓗𝓪𝓵𝓵𝓸 𝓑𝓸𝓼 👋, 𝚂𝙰𝙻𝙰𝙼 𝙲𝚄𝙰𝙽 ❐
━━━━━━━━━━━━━━━━━━━━━━━━
        ⇲ 𝗠𝗘𝗡𝗨 𝗥𝗘𝗦𝗘𝗟𝗟𝗘𝗥 ⇱
━━━━━━━━━━━━━━━━━━━━━━━━
 ⚡ 𝙲𝚛𝚎𝚊𝚝𝚎 𝚂𝚂𝙷 𝚆𝙴𝙱𝚂𝙾𝙲𝙺𝙴𝚃
 ⚡ 𝙲𝚛𝚎𝚊𝚝𝚎 𝚇𝚛𝚊𝚢 𝚅𝚖𝚎𝚜𝚜
 ⚡ 𝙲𝚛𝚎𝚊𝚝𝚎 𝚇𝚛𝚊𝚢 𝚅𝚕𝚎𝚜𝚜
 ⚡ 𝙲𝚛𝚎𝚊𝚝𝚎 𝚇𝚛𝚊𝚢 𝚃𝚛𝚘𝚓𝚊𝚗

━━━━━━━━━━━━━━━━━━━━━━━━
 **✦ Regards : 𝖩𝖺𝗇𝗀𝖺𝗇 𝖫𝗎𝗉𝖺 𝖲𝗁𝖺𝗅𝖺𝗍**
━━━━━━━━━━━━━━━━━━━━━━━━
"""
        await event.edit(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await backers_(event)
        else:
            await event.answer('Semvak, Akses mu Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'setting'))
async def settings(event):
    user_id = str(event.sender_id)
    async def settings_(event):
        inline = [
            [Button.inline(" 𝐂𝐇𝐄𝐂𝐊 𝐒𝐄𝐑𝐕𝐈𝐂𝐄", "service-status"), Button.inline("𝐑𝐄𝐒𝐓𝐀𝐑𝐓 𝐒𝐄𝐑𝐕𝐈𝐂𝐄", "resx")],
            [Button.inline(" 𝐓𝐑𝐀𝐅𝐅𝐈𝐂 𝐒𝐄𝐑𝐕𝐄𝐑", "traffic"), Button.inline(" 𝐑𝐄𝐁𝐎𝐎𝐓 𝐒𝐄𝐑𝐕𝐄𝐑", "reboot")],
            [Button.inline(" 𝐁𝐀𝐂𝐊𝐔𝐏 𝐃𝐀𝐓𝐀", "backup"), Button.inline("𝐑𝐄𝐒𝐓𝐎𝐑𝐄 𝐃𝐀𝐓𝐀", "rest")],
            [Button.inline(" 💻 𝐏𝐀𝐍𝐄𝐋 𝐑𝐄𝐒𝐄𝐋𝐋𝐄𝐑 💻", "panel")],
            [Button.inline(" 🔙 𝐁𝐚𝐜𝐤 𝐓𝐨 𝐌𝐞𝐧𝐮", "menu")]
        ]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**
❏━━━━━━━━━━━━━━━━━❏
🌟 𝕊𝕆𝕌ℝℂ𝔼 𝕍𝔼ℝ𝕊𝕀𝕆ℕ 1.0.23
❏━━━━━━━━━━━━━━━━━❏
👑 𝗗𝗘𝗩 @SaputraTech
❏━━━━━━━━━━━━━━━━━❏
**
"""
        await event.edit(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await settings_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

