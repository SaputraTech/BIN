from cybervpn import *
from telethon import events, Button
import requests

@bot.on(events.NewMessage(pattern=r"(?:.menu|/start|/menu)$"))
@bot.on(events.CallbackQuery(data=b'menu'))
async def start_menu(event):
    sender = await event.get_sender()
    user_id = str(event.sender_id)
    sender_username = sender.username

    if check_user_registration(user_id):
        try:
            s = 'bash /usr/bin/menu-reseller'
            m = subprocess.check_output(s, shell=True).decode("utf-8")
            o = 'bash /usr/bin/menu-admin'
            z = subprocess.check_output(o, shell=True).decode("utf-8")
            skt_saldo_admin, level = get_saldo_and_level_from_db(user_id)

            if level == "user":
                member_inline = [
                    [Button.inline("𝗦𝗦𝗛 𝗪𝗦", "ssh"),
                    Button.inline("𝗩𝗠𝗘𝗦𝗦", "vmess-member")],
                    [Button.inline("𝗩𝗟𝗘𝗦𝗦", "vless-member"),
                    Button.inline("𝗧𝗥𝗢𝗝𝗔𝗡", "trojan-member")],
                    [Button.inline("➕ TopUp Saldo ➕", "topup")],
                ]

                member_msg = f"""
**{m}**
```👤 Username  : @{sender_username}
🧙‍♂️ User ID    : {user_id}
👾 Saldo Saya : Rp {skt_saldo_admin}```
"""
                x = await event.edit(member_msg, buttons=member_inline)
                if not x:
                    await event.reply(member_msg, buttons=member_inline)


            elif level == "admin":
                admin_inline = [
               [Button.inline(" 𝗦𝗦𝗛 𝗪𝗦 ","ssh"),
Button.inline(" 𝗩𝗠𝗘𝗦𝗦 ","vmess")],
[Button.inline(" 𝗧𝗥𝗢𝗝𝗔𝗡 ","trojan"),
Button.inline(" 𝗩𝗟𝗘𝗦𝗦 ","vless")],
[Button.inline(" 𝗙𝗘𝗔𝗧𝗨𝗥𝗘 𝗠𝗔𝗡𝗔𝗚𝗘 ","setting")]]	

                admin_msg = f"""
{z}
```💰 𝕊𝕚𝕤𝕒 𝕊𝕒𝕝𝕕𝕠  : Rp {skt_saldo_admin}
🧾 𝕋𝕠𝕥𝕒𝕝 ℝ𝕖𝕤𝕖𝕝𝕝𝕖𝕣  : {get_user_count()} Orang```
"""
                x = await event.edit(admin_msg, buttons=admin_inline)
                if not x:
                    await event.reply(admin_msg, buttons=admin_inline)

        except Exception as e:
            print(f"Error: {e}")

    else:
        await event.reply(
            f'```🗿 Sorry, Anda belum terdaftar, silahkan register```',
            buttons=[[(Button.inline("Registrasi", "https://t.me/SaputraTech"))]]
        )

