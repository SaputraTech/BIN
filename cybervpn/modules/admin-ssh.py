import requests
from cybervpn import *

@bot.on(events.CallbackQuery(data=b'ssh'))
async def ssh(event):

#############################################################################
###                              PANEL SSH (RESELLER)                     ###
#############################################################################
    async def ssh_member_manager(event):
        inline = [
            [Button.inline("Create SSH", "create-ssh-member"),
            Button.inline("Renew SSH", "skt-renew-ssh-member")],
            [Button.inline("Trial 2 Jam", "skt-trial-ssh-member")],
            [Button.inline("🔙 Back To Menu", "menu")],
]
        
        z = requests.get("http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
𝚂𝚂𝙷/𝙳𝚛𝚘𝚙𝚋𝚎𝚊𝚛 𝙼𝚎𝚗𝚞
- UDP
- SSH
- SSH SSL
- SSH WS
- SSH WS-SSL
- HTTP ProxY
- BadVPN UDPgw

𝚁𝚞𝚕𝚎𝚜:
- Max 2 Login
- Max 3x Peringatan (Ganti Password)
- Peringatan 4x Banned
"""
        await event.edit(msg, buttons=inline)

#############################################################################
###                              PANEL SSH (ADMIN)                        ###
#############################################################################
    async def ssh_admin_manager(event):
        inline = [
[Button.inline(" Trial ","trial-ssh"),
Button.inline(" Create ","create-ssh")],
[Button.inline(" Delete ","delete-ssh"),
Button.inline(" Cek Login ","skt-login-ssh")],
[Button.inline(" Member ","show-ssh"),
Button.inline(" Renew ","renew-ssh")],
[Button.inline("🔙 Main Menu","menu")]]
        
        z = requests.get("http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
SSH/Dropbear Menu
- UDP
- SSH
- SSH SSL
- SSH WS
- SSH WS-SSL
- HTTP ProxY
- BadVPN UDPgw

Rules:
- Max 2 Login
- Max 3x Peringatan (Ganti Password)
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
            await ssh_admin_manager(event)
        else:
            await ssh_member_manager(event)
    except Exception as e:
        print(f'Error: {e}')

