from cybervpn import *
import subprocess
import json
import re
import base64
import datetime as DT
import requests
import time

# ... (kode lainnya)

@bot.on(events.CallbackQuery(data=b'create-vmess'))
async def create_vmess(event):
    async def create_vmess_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username :**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text
 
        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expiry In :**')
            exp = (await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text
        cmd = f'printf "%s\n" "{user}" "{exp}" | add-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        msg = f"""
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
    Xray/Vmess Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks     : {z["ps"]}
🌀Domain      : {z["add"]}
🌀Port TLS    : 8443
🌀Port HTTP   : 8880
🌀User ID     : {z["id"]}
🌀Alter ID    : 0
🌀Security    : auto
🌀Network     : ws
🌀Path        : /v2ray
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link TLS  : 
`{b[0].strip("'").replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link None TLS : 
`{b[1].strip("'").replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
__{z["add"]}:89/vmess-{z["ps"]}.txt__
**📆Expiry      : {later}**

        """

        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')





# TRIAL VMESS
@bot.on(events.CallbackQuery(data=b'trial-vmess'))
async def trial_vmess(event):
    async def trial_vmess_(event):
        # loading animasi
        await event.edit("Processing.")
        await event.edit("Processing..")
        await event.edit("Processing...")
        await event.edit("Processing....")
        await event.edit("akun trial berhasil dibuat")
        # output cmd
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=1)  # You may need to adjust this, as "exp" is not defined in the scope
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        msg = f"""
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
    Xray/Vmess Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks     : {z["ps"]}
🌀Domain      : {z["add"]}
🌀Port TLS    : 8443
🌀Port HTTP   : 8880
🌀User ID     : {z["id"]}
🌀Alter ID    : 0
🌀Security    : auto
🌀Network     : ws
🌀Path        : /v2ray
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link TLS  : 
`{b[0].strip("'").replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link None TLS : 
`{b[1].strip("'").replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
__{z["add"]}:89/vmess-{z["ps"]}.txt__
**📆Expiry      : 1 Days**
        """
        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trial_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

#CEK VMESS
@bot.on(events.CallbackQuery(data=b'cek-vmess'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'cek-ws'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
╔═╗─╔╗──────────╔═╦═╗
║╔╬═╣╠╗╔═╦═╦══╦═╣═╣═╣
║╚╣╩╣═╣╚╗║╔╣║║║╩╬═╠═║
╚═╩═╩╩╝─╚═╝╚╩╩╩═╩═╩═╝
{z}

**Shows Logged In Users Vmess**
""", buttons=[[Button.inline(" 🔙 Main Menu", "vmess")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



## CEK member VMESS
@bot.on(events.CallbackQuery(data=b'cek-member'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'member-vmess'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
```
-
{z}
```
""", buttons=[[Button.inline(" 🔙 Main Menu", "vmess")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')





@bot.on(events.CallbackQuery(data=b'delete-vmess'))
async def delete_vmess(event):
    async def delete_vmess_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        cmd = f'printf "%s\n" "{user}" | delete-vmess'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**User Not Found**")
        else:
            msg = f"""**{a}**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await delete_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        

@bot.on(events.CallbackQuery(data=b'renew-vmess'))
async def ren_vmess(event):
    async def ren_vmess_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username :**')
            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expiry In :**')
            exp = await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = exp.raw_text

        cmd = f'printf "%s\n" "{user}" "{exp}" | renew-vmess'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**User Not Found**")
        else:
            msg = f"""**{a}**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await ren_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')








		
@bot.on(events.CallbackQuery(data=b'vmess'))
async def vmess(event):
    async def vmess_(event):
        inline = [
[Button.inline(" Trial ","trial-vmess"),
Button.inline(" Create ","create-vmess")],
[Button.inline(" Delete ","delete-vmess"),
Button.inline(" Renew ","renew-vmess")],
[Button.inline(" Member ","cek-member")],
[Button.inline("🔙 Back To Menu","menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
𝚇𝚛𝚊𝚢 𝚅𝙼𝚎𝚜𝚜 𝙼𝚎𝚗𝚞
- VMess gRPC TLS
- VMess WS Non-TLS
- VMess WS TLS

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

        if level == 'admin':
            await vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



