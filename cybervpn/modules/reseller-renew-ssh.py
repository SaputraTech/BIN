import subprocess
from datetime import datetime, timedelta
from cybervpn import *

@bot.on(events.CallbackQuery(data=b'skt-renew-ssh-member'))
async def renew_ssh_member(event):
    async def renew_ssh_member_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**➽ Username :**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).message.message.strip()

        async with bot.conversation(chat) as exp_conv:
            await event.respond("**❏ Choose Expiry Day ❏**", buttons=[
                [Button.inline("15 Hari = 5000", b"15")],
                [Button.inline("30 Hari = 10000", b"30")],
                [Button.inline("60 Hari = 15000", b"60")],
                [Button.inline("90 Hari = 25000", b"90")]
            ])
            exp_msg = await exp_conv.wait_event(events.CallbackQuery)
            days = exp_msg.data.decode("ascii")

            # Menentukan harga berdasarkan pilihan user
            if days == "15":
                harga = 5000
            elif days == "30":
                harga = 10000
            elif days == "60":
                harga = 15000
            elif days == "90":
                harga = 25000
            else:
                await event.respond("**✘ Pilihan tidak valid.**")
                return

        # Panggil fungsi untuk memproses saldo pengguna
        saldo_tercukupi = await process_user_balance_ssh(event, user_id, harga)

        try:
            # Periksa masa kedaluwarsa saat ini
            current_exp_output = subprocess.check_output(f'chage -l {user} | grep "Account expires"', shell=True).decode().strip()
            current_exp_str = current_exp_output.split(":")[-1].strip()

            if current_exp_str == 'never':  # Jika tidak ada kedaluwarsa
                current_exp_date = datetime.utcnow()
            else:
                current_exp_date = datetime.strptime(current_exp_str, "%b %d, %Y")

            # Tentukan tanggal kedaluwarsa baru
            if current_exp_date < datetime.utcnow():
                current_exp_date = datetime.utcnow()

            new_expiration_date = current_exp_date + timedelta(days=int(days))
            expiration = new_expiration_date.strftime("%Y-%m-%d")

            # Perbarui akun
            subprocess.check_output(
                f'''
                passwd -u {user}
                usermod -e {expiration} {user}
                ''',
                shell=True
            )

            # New formatted message
            msg = f"""
**━━━━━━━━━━━━━━━━━━━━━**
❏ 𝐑𝐞𝐧𝐞𝐰 𝗦𝗦𝗛 𝐀𝐜𝐜𝐨𝐮𝐧𝐭
❏ 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖱𝖾𝗇𝖾𝗐𝖾id 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒
**━━━━━━━━━━━━━━━━━━━━━**
❖ Username   : {user}
❖ Expired On : {expiration}
**━━━━━━━━━━━━━━━━━━━━━**
"""
            await event.respond(msg)

        except subprocess.CalledProcessError as e:
            await event.respond(f"Error: {e.stderr}")
        except Exception as e:
            await event.respond(f"Error: {e}")

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await renew_ssh_member_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
