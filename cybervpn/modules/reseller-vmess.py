from cybervpn import *
import subprocess
import json
import re
import base64
import datetime as DT
import requests
import time
import sys
from telethon.sync import TelegramClient
import sqlite3

#############################################################################
###                             CREATE VMESS                              ###
#############################################################################

@bot.on(events.CallbackQuery(data=b'create-vmess-member'))
async def create_vmess(event):
    async def create_vmess_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**➽ Username :**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond("**❏ Choose Expiry Day ❏**", buttons=[
                    [Button.inline("15 Hari = 5000", b"15")],
                    [Button.inline("30 Hari = 10000", b"30")],
                    [Button.inline("60 Hari = 15000", b"60")],
                    [Button.inline("90 Hari = 25000", b"90")]
            ])
            exp = (await exp_conv.wait_event(events.CallbackQuery)).data.decode("ascii")

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
        saldo_tercukupi = await process_user_balance_vmess(event, user_id, harga)
        
        if not saldo_tercukupi:  # Jika saldo tidak mencukupi, hentikan proses
            return

        # Ambil informasi ISP dan kota dari API
        try:
            ip_info = requests.get(f"http://ip-api.com/json/?fields=isp,city").json()
            isp = ip_info.get("isp", "Unknown ISP")
            city = ip_info.get("city", "Unknown City")
        except Exception as e:
            isp = "Unknown ISP"
            city = "Unknown City"
            print(f"Error fetching ISP/CITY info: {e}")

        cmd = f'printf "%s\n" "{user}" "{exp}" | add-vmess'
        
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            await event.respond(f"An error occurred: {e}")
            return  # Stop execution if there's an error


        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        z2 = base64.b64decode(b[2].replace("vmess://", "")).decode("ascii")
        z2 = json.loads(z2)
        
        msg = f"""
——————————————————————————————
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐌𝐄𝐒𝐒 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🍀 
——————————————————————————————
➱ Remarks   : {z["ps"]}
➱ ISP       : {isp}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ UUID      : {z["id"]}
➱ Path WS   : /vmess
➱ Path gRPC : vmess-service
➱ Domain WS : {z["add"]}
➱ Domain WC : bug.com.{z["add"]}
——————————————————————————————
 ❒ VMESS WS TLS ↴
——————————————————————————————
```{b[0].strip("'").replace(" ","")}```
——————————————————————————————
 ❒ VMESS WS NTLS ↴
——————————————————————————————
```{b[1].strip("'").replace(" ","")}```
——————————————————————————————
 ❒ VMESS gRPC ↴
——————————————————————————————
```{b[2].strip("'").replace(" ","")}```
——————————————————————————————
** ➽ 𝐄𝐗𝐏𝐈𝐑𝐄𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 : {later}**
——————————————————————————————
"""
        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await create_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

#############################################################################
###                              TRIAL VMESS                              ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'trial-vmess-member'))
async def trial_vmess(event):
    async def trial_vmess_(event):

        # output cmd
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        later = DT.datetime.now() + DT.timedelta(hours=1)  # Masa aktif diubah menjadi 1 jam
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)
        
        z2 = base64.b64decode(b[2].replace("vmess://", "")).decode("ascii")
        z2 = json.loads(z2)
        
        msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐌𝐄𝐒𝐒 𝐓𝐑𝐈𝐀𝐋 🍀 
**━━━━━━━━━━━━━━━━━━━━━**
➱ Remarks   : {z["ps"]}
➱ Domain    : {z["add"]}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ User ID   : {z["id"]}
➱ Alter ID  : 0
➱ Security  : auto
➱ Path WS   : /vmess
➱ Path gRPC : vmess-service
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS TLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[0].strip("'").replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS NTLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[1].strip("'").replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS gRPC ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[2].strip("'").replace(" ","")}```
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
            await trial_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        
#############################################################################
###                              TRIAL VMESS                              ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'trial1-vmess-member'))
async def trial_vmess(event):
    async def trial_vmess_(event):

        # output cmd
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        later = DT.datetime.now() + DT.timedelta(hours=3)  # Masa aktif diubah menjadi 3 jam
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)
        
        z2 = base64.b64decode(b[2].replace("vmess://", "")).decode("ascii")
        z2 = json.loads(z2)
        
        msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
          🍀 𝐗𝐑𝐀𝐘 𝐕𝐌𝐄𝐒𝐒 𝐓𝐑𝐈𝐀𝐋 🍀 
**━━━━━━━━━━━━━━━━━━━━━**
➱ Remarks   : {z["ps"]}
➱ Domain    : {z["add"]}
➱ Port TLS  : 443
➱ Port NTLS : 80
➱ User ID   : {z["id"]}
➱ Alter ID  : 0
➱ Security  : auto
➱ Path WS   : /vmess
➱ Path gRPC : vmess-service
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS TLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[0].strip("'").replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS WS NTLS ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[1].strip("'").replace(" ","")}```
**━━━━━━━━━━━━━━━━━━━━━**
 ❒ VMESS gRPC ↴
**━━━━━━━━━━━━━━━━━━━━━**
```{b[2].strip("'").replace(" ","")}```
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
            await trial_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


#############################################################################
###                              CHECK VMESS (ADMIN)                      ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'cek-vmess-member'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'cek-ws'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
   ___ ___ _  __ __   ____  __ ___ ___ ___ 
  / __| __| |/ / \ \ / /  \/  | __/ __/ __|
 | (__| _|| ' <   \ V /| |\/| | _|\__ \__ \
  \___|___|_|\_\   \_/ |_|  |_|___|___/___/
                                           
{z}

**Shows Logged In Users Vmess**
""", buttons=[[Button.inline("‹ Main Menu ›", "vmess-member")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


#############################################################################
###                              CHECK VMESS (RESELLER)                   ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'cek-member-member'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'bash cek-mws'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
   ___ ___ _  __ __   ____  __ ___ ___ ___ 
  / __| __| |/ / \ \ / /  \/  | __/ __/ __|
 | (__| _|| ' <   \ V /| |\/| | _|\__ \__ \
  \___|___|_|\_\   \_/ |_|  |_|___|___/___/
                                           
{z}

**Shows Users from databases**
""", buttons=[[Button.inline("‹ Main Menu ›", "vmess-member")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

#############################################################################
###                             DELETE VMESS (ADMIN)                      ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'delete-vmess'))
async def delete_vmess(event):
	async def delete_vmess_(event):
		async with bot.conversation(chat) as user:
			await event.respond('**Username:**')
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		cmd = f'printf "%s\n" "{user}" | delws'
		try:
			a = subprocess.check_output(cmd, shell=True).decode("utf-8")
		except:
			await event.respond("**User Not Found**")
		else:
			msg = f"""**Successfully Deleted {user} **"""
			await event.respond(msg)
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_vmess_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

#############################################################################
###                              RENEW VMESS (RESELLER)                   ###
#############################################################################
@bot.on(events.CallbackQuery(data=b'renew-vmess-member'))
async def ren_vmess(event):
    async def ren_vmess_(event):

        # Meminta username pengguna
        async with bot.conversation(chat) as user_conv:
            await event.respond('**➥ Input Username :**')

            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text

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
            expp = exp.data.decode("ascii")


        # Validasi input username
        if not user:
            await event.respond("**✘ Username tidak boleh kosong.**")
            return

        # Menentukan harga berdasarkan pilihan
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
        saldo_tercukupi = await process_user_balance_vmess(event, user_id, harga)
        if not saldo_tercukupi:
            return

        cmd = f'printf "%s\n" "{user}" "{expp}" | renew-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**✘ User Not Found**")
        else:
            msg = f"""**{a}**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await ren_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


#############################################################################
###                            VMESS MEMBER (RESELLER)                    ###
#############################################################################		
@bot.on(events.CallbackQuery(data=b'vmess-member'))
async def vmess(event):
    async def vmess_(event):
        inline = [
            [Button.inline("Create VMess", "create-vmess-member"),
            Button.inline("Renew VMess", "renew-vmess-member")],
            [Button.inline("Trial 1 Jam", "trial-vmess-member"),
            Button.inline("Trial 3 Jam", "trial1-vmess-member")],
            [Button.inline("🔙 Back To Menu", "menu")],
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
𝚇𝚛𝚊𝚢 𝚅𝙼𝚎𝚜𝚜 𝙼𝚎𝚗𝚞
- VMess WS TLS
- VMess WS NTLS
- VMess gRPC TLS

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
            await vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
