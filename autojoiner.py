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
client = TelegramClient('jsculthereicome', api_id, api_hash)

async def main():
    await client.start(phone_number)
    channel = await client.get_entity(channel_link)

    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        message = event.message.text

        invite_link_pattern = r"https://t.me/\+([A-Za-z0-9-_]+)"
        match = re.search(invite_link_pattern, message)

        if match:
            invite_hash = match.group(1)
            try:
                await client(ImportChatInviteRequest(invite_hash))
                print(f"Joined {match.group(0)}")
            except Exception as e:
                print(f"Failed to join {match.group(0)}: {e}")

client.loop.run_until_complete(main())
client.run_until_disconnected()
