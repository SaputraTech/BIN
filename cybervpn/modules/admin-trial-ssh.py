from cybervpn import *
import subprocess
import datetime as DT
import random

@bot.on(events.CallbackQuery(data=b'trial-ssh'))
async def trial_ssh(event):
    user_id = str(event.sender_id)
    async def trial_ssh_(event):
        user = "trialX" + str(random.randint(100, 1000))
        pw = "1"
        exp = "1"
        
        cmd = f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            await event.respond("**✘ User Already Exist**")
        else:
            today = DT.date.today()
            later = today + DT.timedelta(days=int(exp))
            msg = f"""
__Accounts Created Successfully__ 
**×━━━━━━━━━━━━━━━━━━━━━×**
**🔰Host/IP:** `{DOMAIN}`
**🔰Username:** `{user.strip()}`
**🔰Password:** `{pw.strip()}`
**×━━━━━━━━━━━━━━━━━━━━━×**
**🌀OpenSSH:** `22`
**🌀SSL/TLS:** `445`, `777`, `443`
**🌀Ssh Udp:** `1-65535`
**🌀Dropbear:** `109`,`143`
**🌀WS SSL:** `443`
**🌀WS HTTP:** `80`
**🌀Squid:** `8080`, `3128`
**🌀UDPGW :** `7100-7300`
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀Payload Ssh Ws🍀**
`GET / HTTP/1.1 [crlf]Host: {DOMAIN}[crlf]Upgrade: websocket[crlf][crlf]`
**×━━━━━━━━━━━━━━━━━━━━━×**
**🍀File OpenVPN🍀**
__{DOMAIN}:89/udp.ovpn__
__{DOMAIN}:89/ssl.ovpn__
__{DOMAIN}:89/tcp.ovpn__
**×━━━━━━━━━━━━━━━━━━━━━×**
**🗓Expiry:** `{later}`
**×━━━━━━━━━━━━━━━━━━━━━×**
"""
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trial_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak...!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

