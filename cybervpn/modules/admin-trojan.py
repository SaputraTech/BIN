from cybervpn import *
import requests
import subprocess
@bot.on(events.CallbackQuery(data=b'create-trojan'))
async def create_trojan(event):
    async def create_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond('**Expiry In :**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text

        cmd = f'printf "%s\n" "{user}" "{exp}" | add-trojan'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"Terjadi kesalahan: {e}\nSubproses output: {a}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        b = [x.group() for x in re.finditer("trojan://(.*)", a)]
        print(b)
        domain = re.search("@(.*?):", b[0]).group(1)
        uuid = re.search("trojan://(.*?)@", b[0]).group(1)
        msg = f"""
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
    Trojan Ws Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks    : {user}
🌀Domain     : {DOMAIN}
🌀Port       : 2097
🌀Password   : {user}
🌀Encryption : none
🌀Path       : /directpath
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link Trojan Ws : 
`trojan://{user}@{DOMAIN}:2097/?sni={DOMAIN}&type=ws&host={DOMAIN}&path=/directpath&encryption=none#{user}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
__{DOMAIN}:89/trojanGO-{user}.txt__
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
            await create_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'cek-tr'))
async def cek_trojan(event):
    async def cek_trojan_(event):
        cmd = 'cek-tr'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

╔═╗─╔╗╔╗
║╔╬═╣╠╣╚╦╦╦═╦╦═╗╔═╦╗
║╚╣╩╣═╣╔╣╔╣╬╠╣╬╚╣║║║
╚═╩═╩╩╩═╩╝╚╦╝╠══╩╩═╝
───────────╚═╝
{z}

**Shows Logged In Users Trojan**
""", buttons=[[Button.inline("‹ Main Menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'trial-trojan'))
async def trial_trojan(event):
    async def trial_trojan_(event):
        cmd = f'printf "%s\n" "trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | add-trojan'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**✘ User Already Exist**")
        else:
            today = DT.date.today()
            later = today + DT.timedelta(days=int(1))
            b = [x.group() for x in re.finditer("trojan://(.*)", a)]
            print(b)
            remarks = re.search("#(.*)", b[0]).group(1)
            domain = re.search("@(.*?):", b[0]).group(1)
            uuid = re.search("trojan://(.*?)@", b[0]).group(1)
            msg = f"""
__Accounts Created Suuccessfuly__
**×━━━━━━━━━━━━━━━━━━━━━×**
    Trojan Ws Accounts
**×━━━━━━━━━━━━━━━━━━━━━×**
🌀Remarks    : {user}
🌀Domain     : {DOMAIN}
🌀Port       : 2097
🌀Password   : {user}
🌀Encryption : none
🌀Path       : /directpath
**×━━━━━━━━━━━━━━━━━━━━━×**
🍀Link Trojan Ws : 
`trojan://{remarks}@{DOMAIN}:2097/?sni={DOMAIN}&type=ws&host={DOMAIN}&path=/directpath&encryption=none#{remarks}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**✅Format OpenClash✅**
__{DOMAIN}:89/trojanGO-{remarks}.txt__
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
            await trial_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'renew-trojan'))
async def ren_trojan(event):
    async def ren_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond('**Expiry In :**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text
        
        cmd = f'printf "%s\n" "{user}" "{exp}" | renew-trojan'
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
            await ren_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak...!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')



# CEK member tr
@bot.on(events.CallbackQuery(data=b'showtr'))
async def cek_tr(event):
    async def cek_tr_(event):
        cmd = 'bash member-trojan'.strip()
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
            await cek_tr_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


		
@bot.on(events.CallbackQuery(data=b'delete-trojan'))
async def delete_trojan(event):
    async def delete_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username :**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        cmd = f'printf "%s\n" "{user}" | delete-trojan'
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
            await delete_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'trojan'))
async def trojan(event):
    async def trojan_(event):
        inline = [
[Button.inline(" Create ","create-trojan"),
Button.inline(" Delete ","delete-trojan")],
[Button.inline(" Renew ","renew-trojan"),
Button.inline(" Member ","showtr")],
[Button.inline("‹ Back Menu ›","menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**✅ MENU TROJAN**
__- Trojan Ws__
__- Trojan Go__
__- Port 2097__

**✅ SERVER INFO**
__- Domain: {DOMAIN}
__- Region: {z["country"]}
        """
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trojan_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

