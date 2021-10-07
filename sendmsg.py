#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

SLEEP_TIME = 30
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
bl="\033[94m"
ye="\033[93m"
wi="\033[0m"

class main():
    def banner():
        os.system('clear')
        print(f"""
        {cy}|_  __|_{bl} _ .__.._ _
        {cy}|_)(_)|_{bl}(_||(_|| | |
        {cy}        {bl} _|{cy}by @Ivam3
        """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"(_>)─➤ run python setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(cy+'(_>)─➤ Enter the code: '+bl))
        
        os.system('clear')
        main.banner()
        try:
            input_file = sys.argv[1]
            users = []
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                next(rows, None)
                for row in rows:
                    user = {}
                    user['username'] = row[0]
                    user['id'] = int(row[1])
                    user['access_hash'] = int(row[2])
                    user['name'] = row[3]
                    users.append(user)
            print(cy+'(_>)─➤ Choose a method')
            print(cy+" ╰─["+bl+"1"+cy+"]─➤"+bl+" send message by user ID\n"+cy+" ╰─["+bl+"2"+cy+"]─➤"+bl+" send message by username ")
            mode = int(input(cy+"Input : "+bl))

            message = input("\n"+cy+"(_>)─➤ Enter Your Message : "+wi)

            for user in users:
                if mode == 2:
                    if user['username'] == "":
                        continue
                    receiver = client.get_input_entity(user['username'])
                elif mode == 1:
                    receiver = InputPeerUser(user['id'],user['access_hash'])
                else:
                    print(re+"(_>)─➤ Invalid Mode. Exiting.")
                    client.disconnect()
                    sys.exit()
                try:
                    print(cy+"(_>)─➤ Sending Message to"+bl+" :", user['name'])
                    client.send_message(receiver, message.format(user['name']))
                    print(ye+" ╰──➤ Waiting {} seconds".format(SLEEP_TIME))
                    time.sleep(SLEEP_TIME)
                except PeerFloodError:
                    print(re+"(_>)─➤ Getting Flood Error from telegram. \n ╰──➤ Script is stopping now. \n ╰──➤ Please try again after some time.")
                    client.disconnect()
                    sys.exit()
                except Exception as e:
                    print(re+"(_>)─➤ Error:", e)
                    print(re+" ╰──➤ Trying to continue...")
                    continue
                client.disconnect()
                print(gr+"Done. Message sent to all users.")

        except IndexError:
            print(re+"(_>)─➤ .csv file doesn't specified. \n ╰──➤ Aborting.")

main.send_sms()
