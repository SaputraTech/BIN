from cybervpn import *
import requests
import subprocess
import time
@bot.on(events.CallbackQuery(data=b'create-vless'))
async def create_vless(event):
    async def create_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond('**Expiry In :**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text

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
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
      Xray/Vless Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks    : {user}
🌀Domain     : {DOMAIN}
🌀Port TLS   : 2087
🌀Port NTLS  : 2082
🌀NetWork    : (WS)
🌀User ID    : {uuid}
🌀Path NTLS  : /vless-ntls
🌀Path TLS   : /vless-tls
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀Link TLS : **
`{x[0]}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀Link NTLS :**
`{x[1].replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
{DOMAIN}:89/vless-{user}.txt
**📆Expiry : {later}**
"""
        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'cek-vless'))
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

        if level == 'admin':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

		
@bot.on(events.CallbackQuery(data=b'renew-vless1'))
async def ren_vless(event):
    async def ren_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text

        async with bot.conversation(chat) as exp:
            await event.respond('**Expiry In :**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text

        cmd = f'printf "%s\n" "{user}" "{exp}" | renew-vless'
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
            await ren_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


# CEK member VLESS
@bot.on(events.CallbackQuery(data=b'listvless'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'member-vless'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
```
-
{z}
```
""", buttons=[[Button.inline("‹ Main Menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'delete-vless2'))
async def delete_vless(event):
    async def delete_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text

        cmd = f'printf "%s\n" "{user}" | delete-vless'
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
            await delete_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'trial-vless3'))
async def trial_vless(event):
    async def trial_vless_(event):
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-vless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**✘ User Already Exist**")
        else:
            today = DT.date.today()
            later = today + DT.timedelta(days=int(1))
            x = [x.group() for x in re.finditer("vless://(.*)", a)]
            print(x)
            remarks = re.search("#(.*)", x[0]).group(1)
            # domain = re.search("@(.*?):", x[0]).group(1)
            uuid = re.search("vless://(.*?)@", x[0]).group(1)
            # path = re.search("path=(.*)&", x[0]).group(1)
            msg = f"""
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
      Xray/Vless Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks    : {remarks}
🌀Domain     : {DOMAIN}
🌀Port TLS   : 2087
🌀Port NTLS  : 2082
🌀NetWork    : (WS)
🌀User ID    : {uuid}
🌀Path NTLS  : /vless-ntls
🌀Path TLS   : /vless-tls
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀Link TLS : **
`{x[0]}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀Link NTLS :**
`{x[1].replace(" ","")}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
{DOMAIN}:89/vless-{remarks}.txt
**📆Expiry : 1 Days**
"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trial_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'vless'))
async def vless(event):
    async def vless_(event):
        inline = [
[Button.inline(" Trial ","trial-vless3"),
Button.inline(" Create ","create-vless")],
[Button.inline(" Renew ","renew-vless1"),
Button.inline(" Delete ","delete-vless2")],
[Button.inline(" Member ","listvless")],
[Button.inline("‹ Back Menu ›","menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**✅ MENU VLESS**
__- VLess None TLS__
__- VLess TLS__
__- Port 2087,2082__

**✅ SERVER INFO**
__- Domain: {DOMAIN}__
__- Region: {z["country"]}__
"""
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

