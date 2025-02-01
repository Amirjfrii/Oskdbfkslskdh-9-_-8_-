from telethon import *
import time
import asyncio

api_id = 22051826
api_hash = "713ee0c13c60e46ecf2f9c3af4a7694b"
phone = "+79957352366"  you prone namber
client = TelegramClient("sendstars", api_id, api_hash)
client.session.set_dc(2, "149.154.167.40", 443)

async def send_stars(event, peer, msid, cnt):
    sended = 0
    message = await event.reply(f"sented: {sended}/{cnt} stars. ")
    
    for _ in range(round(cnt / 2500)):
        if sended < cnt:
            rid = int(time.time()) << 32
            sended += 2500
            ch = await client.get_input_entity(peer)
            await client(functions.messages.SendPaidReactionRequest(peer=ch, msg_id=msid, count=2500, random_id=rid, private=False))
            
            new_message = f"sented: {sended}/{cnt}  stars."
            await message.edit(new_message)

    new_message = f"sented: {sended}/{cnt}  stars. Done"
    await message.edit(new_message)

@client.on(events.NewMessage(pattern=r'\.stars_add'))
async def stars_handler(event):
    try:
        command = event.text.split()
        if len(command) != 4:
            await event.reply("Invalid command format. Используйте: .stars_add <username> <message_id> <count>")
            return

        username = command[1]
        message_id = int(command[2])
        count = int(command[3])

        peer = await client.get_input_entity(username)

        await send_stars(event, peer, message_id, count)
    
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")

async def main():
    await client.start(phone)
    print("Client Working")

client.loop.run_until_complete(main())
client.run_until_disconnected()
