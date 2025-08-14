from telethon.sync import TelegramClient
import os, sys
import configparser
import argparse
import csv
from datetime import datetime

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
bl="\033[94m"
ye="\033[93m"
wi="\033[0m"

def banner():
      os.system('clear')
      print(f"""
    {cy}|_  __|_{bl} _ .__.._ _
    {cy}|_)(_)|_{bl}(_||(_|| | |
    {cy}        {bl} _|{cy}by @Ivam3
    {cy}Scraping comments from a specific user...{wi}
    """)

# --- Argumentos de línea de comandos ---
parser = argparse.ArgumentParser(description='Scrape comments from a specific user in a group.')
parser.add_argument('group_username', type=str, help='The username of the group (e.g., "telegramgroup").')
parser.add_argument('target_username', type=str, help='The username of the target user (e.g., "telegramuser").')
args = parser.parse_args()

# --- Cargar configuración (copiado de getdata.py) ---
cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"(_>)-➤ Please run python setup.py first!\n")
    sys.exit(1)

async def main():
    banner()
    print(f"{cy}(_>)-➤ Connecting to Telegram...{wi}")
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        os.system('clear')
        banner()
        try:
            await client.sign_in(phone, input(cy+'(_>)-➤ Enter the 2FA code: '+bl))
        except Exception as e:
            print(f"{re}Error: {e}")
            sys.exit(1)

    os.system('clear')
    banner()
    
    group = args.group_username
    target_user = args.target_username
    
    print(f"{cy}(_>)-➤ Searching for group '{bl}{group}{cy}' and user '{bl}{target_user}{cy}'...{wi}")

    try:
        entity = await client.get_entity(group)
        target = await client.get_entity(target_user)
    except Exception as e:
        print(f"{re}Error: Could not find group or user. Details: {e}{wi}")
        sys.exit(1)

    print(f"{gr}(_>)─➤ Found! Starting to fetch messages...{wi}")

    output_file = 'comments.csv'
    with open(output_file, "w", encoding='UTF-8', newline='') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(['date', 'message_id', 'comment_text'])

        async for message in client.iter_messages(entity, from_user=target):
            if message.text:
                date_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{bl}[{date_str}]{wi} {message.text}\n")
                writer.writerow([date_str, message.id, message.text])

    print(f"\n{gr}(_>)-➤ Scraping complete. Comments saved to {output_file}{wi}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
