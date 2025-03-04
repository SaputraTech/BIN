from cybervpn import *
import requests
import subprocess
import time

#############################################################################
###                            VLESS CREATE (RESELLER)                    ###
#############################################################################	
@bot.on(events.CallbackQuery(data=b'create-vless-member'))
async def create_vless(event):
    async def create_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond("**Choose Expiry Day**", buttons=[
                [Button.inline(" 30 Hari ", "30")]
            ])
            exp = exp.wait_event(events.CallbackQuery)
            exp = (await exp).data.decode("ascii")
        
        await process_user_balance_vless(event, user_id)

        cmd = f'printf "%s\n" "{user}" "{exp}" | add-vless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"Terjadi kesalahan: {e}\nSubproses output: {a}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        x = [x.group() for x in re.finditer("vless://(.*)", a)]
        print(x)
        uuid = re.search("vless://(.*?)@", x[0]).group(1)
        msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐋𝐄𝐒𝐒 𝐓𝐑𝐈𝐀𝐋 🍀 
**━━━━━━━━━━━━━━━━━━━━━**
➱ Remarks   : {user}
➱ Domain    : {DOMAIN}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ User ID   : {uuid}
➱ Network   : ws
➱ Path WS   : /vless
➱ Path gRPC : vless-service
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS TLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[0]}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS NTLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[1].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS gRPC ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[2].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
** ➽ 𝐄𝐗𝐏𝐈𝐑𝐄𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 : {later}**
**━━━━━━━━━━━━━━━━━━━━━**
"""
        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await create_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'cek-vless-member'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'cek-vless'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
╔═╗─╔╗╔╗─╔╗───╔═╦═╗
║╔╬═╣╠╣╚╦╝╠╗╔═╣═╣═╣
║╚╣╩╣═╬╗║╔╣╚╣╩╬═╠═║
╚═╩═╩╩╝╚═╝╚═╩═╩═╩═╝
{z}

**Shows Logged In Users Vless**
""", buttons=[[Button.inline("‹ Main Menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


#############################################################################
###                              RENEW VLESS (RESELLER)                   ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'renew-vless-member'))
async def ren_vless(event):
    async def ren_vless_(event):
        # Meminta username pengguna
        async with bot.conversation(chat) as user_conv:
            await event.respond('**➥ Input Username :**')

            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text.strip()  # Hapus spasi ekstra
            print(f"User input: {user}")  # Debug log untuk melihat input

            if not user:
                await event.respond("**✘ Username tidak boleh kosong.**")
                return

        # Meminta pilihan expiry
        async with bot.conversation(chat) as exp_conv:
            await event.respond(
                "**❏ Choose Expiry Day ❏**",
                buttons=[ 
                    [Button.inline("15 Hari = 5000", b"15")],
                    [Button.inline("30 Hari = 10000", b"30")],
                    [Button.inline("60 Hari = 15000", b"60")],
                    [Button.inline("90 Hari = 25000", b"90")]
                ]
            )
            exp = await exp_conv.wait_event(events.CallbackQuery)
            expp = exp.data.decode("ascii").strip()  # Pastikan data diproses dengan benar
            print(f"Expiry chosen: {expp}")  # Debug log untuk melihat pilihan expiry

        # Validasi expiry
        harga_map = {
            "15": 5000,
            "30": 10000,
            "60": 15000,
            "90": 25000
        }

        harga = harga_map.get(expp)
        if not harga:
            await event.respond("**✘ Pilihan tidak valid.**")
            return

        # Memproses saldo pengguna
        saldo_tercukupi = await process_user_balance_vless(event, user_id, harga)
        if not saldo_tercukupi:
            return  # Jika saldo tidak cukup, keluar

        cmd = f'printf "%s\n" "{user}" "{expp}" | renew-vless'

        try:
            print(f"Executing command: {cmd}")  # Debug log untuk melihat perintah yang dijalankan
            a = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
            print(f"Command output: {a}")  # Debug log untuk melihat output dari perintah
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode("utf-8") if e.output else "No output"
            await event.respond(f"**✘ Error: {e}\nOutput: {error_message}**")
            return

        # Pastikan output berhasil
        if not a:
            await event.respond("**✘ Tidak ada output dari perintah.**")
            return

        msg = f"""**{a}**"""
        await event.respond(msg)

    # Mendapatkan user_id dan chat_id
    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        # Mengecek level pengguna dalam database
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await ren_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        await event.respond(f"**Terjadi kesalahan: {e}**")


#############################################################################
###                             VLESS CHECK (RESELLER)                    ###
#############################################################################	
# CEK member VLESS
@bot.on(events.CallbackQuery(data=b'cek-membervl-member'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'bash cek-mvs'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

{z}

**Shows Users from databases**
""", buttons=[[Button.inline("‹ Main Menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


#############################################################################
###                            VLESS DELETE (RESELLER)                    ###
#############################################################################	
@bot.on(events.CallbackQuery(data=b'delete-vless'))
async def delete_vless(event):
	async def delete_vless_(event):
		async with bot.conversation(chat) as user:
			await event.respond('**Username:**')
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		await event.edit("Processing.")
		await event.edit("Processing..")
		await event.edit("Processing...")
		await event.edit("Processing....")
		time.sleep(1)
		await event.edit("`Processing Crate Premium Account`")
		time.sleep(1)
		await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 84%\n█████████████████████▒▒▒▒ `")
		time.sleep(0)
		await event.edit("`Processing... 100%\n█████████████████████████ `")
		time.sleep(1)
		await event.edit("`Wait.. Setting up an Account`")
		cmd = f'printf "%s\n" "{user}" | del-vless'
		try:
			a = subprocess.check_output(cmd, shell=True).decode("utf-8")
		except:
			await event.respond("**User Not Found**")
		else:
			msg = f"""**Successfully Deleted**"""
			await event.respond(msg)
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

#############################################################################
###                            VLESS TRIAL (RESELLER)                     ###
#############################################################################	
@bot.on(events.CallbackQuery(data=b'trial-vless-member'))
async def trial_vless(event):
    async def trial_vless_(event):
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**✘ User Already Exist**")
        else:
            # Mengganti masa aktif menjadi 1 jam
            now = DT.datetime.now()
            later = now + DT.timedelta(hours=1)  # Masa aktif 1 jam
            x = [x.group() for x in re.finditer("vless://(.*)", a)]
            print(x)
            remarks = re.search("#(.*)", x[0]).group(1)
            uuid = re.search("vless://(.*?)@", x[0]).group(1)
            
            msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐋𝐄𝐒𝐒 𝐓𝐑𝐈𝐀𝐋 🍀 
**━━━━━━━━━━━━━━━━━━━━━**
➱ Remarks   : {remarks}
➱ Domain    : {DOMAIN}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ User ID   : {uuid}
➱ Network   : ws
➱ Path WS   : /vless
➱ Path gRPC : vless-service
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS TLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[0]}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS NTLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[1].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS gRPC ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[2].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
** ➽ 𝐄𝐗𝐏𝐈𝐑𝐄𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 : {later.strftime('%H:%M:%S')}**
**━━━━━━━━━━━━━━━━━━━━━**
        """
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await trial_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

#############################################################################
###                            VLESS TRIAL (RESELLER)                     ###
#############################################################################	
@bot.on(events.CallbackQuery(data=b'trial1-vless-member'))
async def trial_vless(event):
    async def trial_vless_(event):
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**✘ User Already Exist**")
        else:
            # Mengganti masa aktif menjadi 3 jam
            now = DT.datetime.now()
            later = now + DT.timedelta(hours=3)  # Masa aktif 3 jam
            x = [x.group() for x in re.finditer("vless://(.*)", a)]
            print(x)
            remarks = re.search("#(.*)", x[0]).group(1)
            uuid = re.search("vless://(.*?)@", x[0]).group(1)
            
            msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐋𝐄𝐒𝐒 𝐓𝐑𝐈𝐀𝐋 🍀 
**━━━━━━━━━━━━━━━━━━━━━**
➱ Remarks   : {remarks}
➱ Domain    : {DOMAIN}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ User ID   : {uuid}
➱ Network   : ws
➱ Path WS   : /vless
➱ Path gRPC : vless-service
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS TLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[0]}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS NTLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[1].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS gRPC ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{x[2].replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
** ➽ 𝐄𝐗𝐏𝐈𝐑𝐄𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 : {later.strftime('%H:%M:%S')}**
**━━━━━━━━━━━━━━━━━━━━━**
        """
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await trial_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        
#############################################################################
###                            VLESS MEMBER (RESELLER)                    ###
#############################################################################	
@bot.on(events.CallbackQuery(data=b'vless-member'))
async def vless(event):
    async def vless_(event):
        inline = [
            [Button.inline("Create VLess", "create-vless-member"),
            Button.inline("Renew VLess", "renew-vless-member")],
            [Button.inline("Trial 1 Jam", "trial-vless-member"),
            Button.inline("Trial 3 Jam", "trial1-vless-member")],
            [Button.inline("🔙 Back To Menu", "menu")],
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
𝚇𝚛𝚊𝚢 𝚅𝚕𝚎𝚜𝚜 𝙼𝚎𝚗𝚞
- Vless WS TLS
- Vless WS NTLS
- Vless gRPC TLS

𝚁𝚞𝚕𝚎𝚜:
- Max 2 Login
- Max 3x Peringatan (Penggantian UUID)
- Peringatan 4x Banned
"""
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

