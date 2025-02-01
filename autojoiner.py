import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import FloodWaitError
from dotenv import load_dotenv
import os
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if os.path.exists('.env'):
    load_dotenv('.env')
else:
    load_dotenv('.env.example') 

invite_link_pattern = r"https://t.me/\+([A-Za-z0-9-_]+)"

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
phone_number = os.getenv('PHONE_NUMBER')
channel_link = os.getenv('CHANNEL_LINK')
notification_channel_link = os.getenv('NOTIFICATION_CHANNEL_LINK')
notification_channel_admin_user = os.getenv('NOTIFICATION_CHANNEL_ADMIN_USER')

client = TelegramClient(f"{phone_number.replace('+', '')}", api_id, api_hash)
notifier_client = TelegramClient('notification', api_id, api_hash)

def get_invite_hash(event):
    message = event.message.text
    match = re.search(invite_link_pattern, message)
    if match:
        return match.group(1)
    return None

async def join_group(client, invite_hash):
    try:
        await client(ImportChatInviteRequest(invite_hash))
        logging.info(f"Successfully joined group with invite link {invite_hash}.")
        return True
    except Exception as e:
        logging.error(f"Failed to join group with invite link {invite_hash}: {e}")
        return False

async def notify_channel(notifier_client, notification_channel, username, invite_hash):
    try:
        await notifier_client.send_message(notification_channel, f"{username} joined using {invite_hash}!")
        return True
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        return False

async def start_client():
    listening = True
    while listening:
        try:
            await client.start(phone_number)
            await notifier_client.start(notification_channel_admin_user)

            listening_channel = await client.get_entity(channel_link)
            notifying_channel = await notifier_client.get_entity(notification_channel_link)

            logging.info(f"Started listening for messages in {listening_channel.title}...")

            @client.on(events.NewMessage(chats=listening_channel))
            async def handle(event):
                nonlocal listening
                invite_hash = get_invite_hash(event)
                if invite_hash is None:
                    # no invite link found in message, continue listening
                    return

                joined_successfully = await join_group(client, invite_hash)
                if not joined_successfully:
                    # failed to join group, continue listening
                    return
                
                # stop listening after successfully joining group, regardless of whether notification was sent
                listening = False

                logging.info(f"Stopping soon. Notifying channel about successful join...")
                
                me = await client.get_me()
                username = me.username if me.username else phone_number
                await notify_channel(notifier_client, notifying_channel, username, invite_hash)
                try:
                    await client.disconnect()
                except Exception as e:
                    logging.error(f"Error occurred while disconnecting: {e}")
            await client.run_until_disconnected()
        except FloodWaitError as e:
            logging.error(f"Flood wait error occurred. Waiting for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            logging.error(f"Error occurred while connecting: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

async def main():
    await start_client()

if __name__ == "__main__":
    logging.info("Autojoiner started.")
    client.loop.run_until_complete(main())
    logging.info("Autojoiner stopped.")
