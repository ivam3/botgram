#!/usr/bin/python3
#Coded by : @Ivam3 on Oct 2021

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random

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
    """)

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
    print(re+"(_>)─➤ run python setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(cy+'(_>)─➤ Enter the code: '+bl))
 
os.system('clear')
banner()
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
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print(cy+'(_>)─➤ Choose a group to add members')
i=0
for group in groups:
    print(cy+' ╰─['+bl+str(i)+cy+']─➤'+bl+' - '+group.title)
    i+=1

g_index = input("\n"+cy+"(_>)─➤"+bl+" Enter a Number : "+wi)
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
print(cy+"(1)─➤ add member by user ID\n(2)─➤ add member by username ")
mode = int(input(bl+"Input : "+wi)) 
n = 0
 
for user in users:
    n += 1
    if n % 50 == 0:
	    time.sleep(1)
	    try:
	        print ("Adding {}".format(user['id']))
	        if mode == 1:
	            if user['username'] == "":
	                continue
	            user_to_add = client.get_input_entity(user['username'])
	        elif mode == 2:
	            user_to_add = InputPeerUser(user['id'], user['access_hash'])
	        else:
	            sys.exit(re+"(_>)─➤ Invalid Mode Selected. Please Try Again.")
	        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
	        print(cy+"(_>)─➤ Waiting for 5-10 Seconds...")
	        time.sleep(random.randrange(5, 10))
	    except PeerFloodError:
	        print(re+"(_>)─➤ Getting Flood Error from telegram. \n ╰──➤ Script is stopping now. \n ╰──➤ Please try again after some time.")
	    except UserPrivacyRestrictedError:
	        print(re+"(_>)─➤ The user's privacy settings do not allow you to do this. \n ╰──➤ Skipping.")
	    except:
	        traceback.print_exc()
	        print(re+"(_>)─➤ Unexpected Error")
	        continue
