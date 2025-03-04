from cybervpn import *
import subprocess
import datetime as DT
import random

@bot.on(events.CallbackQuery(data=b'skt-trial-ssh-member'))
async def trial_ssh(event):
    user_id = str(event.sender_id)
    async def trial_ssh_(event):
        user = "Tested" + str(random.randint(100, 1000))
        pw = "1"
        exp = "2 hours"  # Masa aktif 2 jam

        # Format tanggal dengan waktu untuk masa aktif 2 jam
        exp_time = (DT.datetime.now() + DT.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        cmd = f'useradd -e "{exp_time}" -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'

        try:
            # Logging perintah untuk debugging
            print(f"Running command: {cmd}")
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            print(f"Command output: {result.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode('utf-8')
            print(f"Error: {error_msg}")
            await event.respond(f"**Failed to create user:**\n{error_msg}")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")
            await event.respond(f"**Unexpected error occurred:** {e}")
            return
        else:
            now = DT.datetime.now()
            later = now + DT.timedelta(hours=2)
            msg = f"""
**━━━━━━━━━━━━━━━━━━━**
    __Accounts Trial Created __ 
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
```GET / HTTP/1.1[crlf]Host: [host][crlf]Upgrade: Websocket[crlf]Connection: Keep-Alive[crlf]Connection: Keep-Alive[crlf]User-Agent: [ua][crlf]Ping: clients3.google.com[crlf]Sec-WebSocket-Extensions: superspeed[crlf][crlf]```
**━━━━━━━━━━━━━━━━━━━**
**➽ Expiry:** `{later.strftime('%H:%M:%S')}`
**━━━━━━━━━━━━━━━━━━━**
"""
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await trial_ssh_(event)
        else:
            await event.answer(f"Akses Ditolak...!!", alert=True)
    except Exception as e:
        print(f"Error: {e}")
