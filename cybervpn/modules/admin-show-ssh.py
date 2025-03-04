from cybervpn import *
import subprocess
@bot.on(events.CallbackQuery(data=b'show-ssh'))
async def show_ssh(event):
    user_id = str(event.sender_id)

    async def show_ssh_(event):
        a = 'bash /usr/bin/member-ssh'
        x = subprocess.check_output(a, shell=True).decode("utf-8")
        await event.respond(f"""
---------------------------------------------------
**LIST ALL USER SSH & OVPN**
---------------------------------------------------
{x}

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

