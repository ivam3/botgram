from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time

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
 
print(cy+'(_>)─➤ Choose a group to scrape members :'+bl)
i=0
for g in groups:
    print(cy+' ╰─['+bl+str(i)+cy+']─➤ '+bl+ g.title)
    i+=1
 
print('')
g_index = input(cy+"(_>)─➤"+bl+" Enter a Number : "+wi)
target_group=groups[int(g_index)]
 
print(cy+'(_>)─➤ Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
 
print(cy+'(_>)─➤ Saving In file...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(gr+'(_>)─➤ Members scraped successfully.')
