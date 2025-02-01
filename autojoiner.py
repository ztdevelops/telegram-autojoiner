from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from dotenv import load_dotenv
import os
import re

if os.path.exists('.env'):
    load_dotenv('.env')
else:
    load_dotenv('.env.example')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
channel_link = os.getenv('CHANNEL_LINK')
notification_channel_link = os.getenv('NOTIFICATION_CHANNEL_LINK')

client = TelegramClient(f"{phone_number.replace("+", "")}", api_id, api_hash)

async def main():
    await client.start(phone_number)
    me = await client.get_me()
    username = me.username if me.username else phone_number
    target_channel = await client.get_entity(channel_link)
    print(f"{username} is currently listening to messages in channel {target_channel.title}")

    @client.on(events.NewMessage(chats=target_channel))
    async def handler(event):
        message = event.message.text

        invite_link_pattern = r"https://t.me/\+([A-Za-z0-9-_]+)"
        match = re.search(invite_link_pattern, message)

        if match:
            invite_hash = match.group(1)
            try:
                await client(ImportChatInviteRequest(invite_hash))
                print(f"{username} successfully joined the group, sending notification to channel.")
                await client.send_message(notification_channel_link, f"{username} joined using {match.group(1)}!")
                print("Group joined successfully. Terminating the session.")
                await client.disconnect()
            except Exception as e:
                print(f"Failed to join {match.group(0)}: {e}")

client.loop.run_until_complete(main())
client.run_until_disconnected()
