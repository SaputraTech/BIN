from cybervpn import *
import datetime as DT

@bot.on(events.CallbackQuery(data=b'skt-addsaldo'))
async def saldo_handler(event):
    sender = await event.get_sender()
    user_id = str(event.sender_id)
    chat = event.chat_id
    async with bot.conversation(chat) as id_conv:
        await event.respond('**➢ Input ID Chat:**')
        id = (await id_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

    async with bot.conversation(chat) as saldo_conv:
        await event.respond('**➢ Input nominal balance:**')
        saldo = (await saldo_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            tambah_saldo(id, saldo)
            today = DT.date.today()
            later = today + DT.timedelta(days=int(0))
            msg = f"""
**━━━━━━━━━━━━━━━━━**
**❏ Success add saldo member ❏**
**━━━━━━━━━━━━━━━━━**
**➽ Your ID:** `{user_id}`
**➽ ID user:** `{id}`
**➽ Balance:** `Rp {saldo}`
**➽ Tanggal topup:** `{later}`
**➽ Status:** `Success ✔`
**━━━━━━━━━━━━━━━━**
**Regard @SaputraTech**
**━━━━━━━━━━━━━━━━**
"""
            inline = [
                [Button.url("❖ Admin ❖", "t.me/SaputraTech"),
                 Button.url("❖ Channel ❖", "t.me/SkartiVPN")]
            ]
            await event.respond(msg, buttons=inline)
        else:
            await event.answer(f'✘ Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

