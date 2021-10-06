#!/usr/bin/python3
#Coded by : @Ivam3 on Oct 2021

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
bl="\033[94m"
ye="\033[93m"
wi="\033[0m"

import os, sys
import time

def banner():
	os.system('clear')
	print(f"""
    {cy}|_  __|_{bl} _ .__.._ _
    {cy}|_)(_)|_{bl}(_||(_|| | |
    {cy}        {bl} _|{cy}by @Ivam3""")

def requirements():
	def csv_lib():
		banner()
		print(cy+'(_>)─➤'+bl+' it could take a while ...')
		os.system("python -m pip install cython numpy pandas")
	banner()
	print(cy+'(_>)─➤'+bl+' installing csv merge. It will take a long long time ...'+wi)
	input_csv = input(cy+'(_>)─➤'+bl+' do you want to enable csv merge (y/n) : '+wi).lower()
	if input_csv == "y":
		csv_lib()
	else:
		pass
	print(cy+'(_>)─➤'+bl+' installing requierments ...'+wi)
	os.system("""
		python -m pip install numpy telethon requests configparser
		touch config.data
		""")
	banner()
	print('\n'+cy+'(_>)─➤'+bl+" requierments Installed.\n")

def config_setup():
    import configparser
    banner()
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(cy+"(_>)─➤"+bl+" enter api ID : "+wi)
    cpass.set('cred', 'id', xid)
    xhash = input(cy+"(_>)─➤"+bl+"enter hash ID : "+wi)
    cpass.set('cred', 'hash', xhash)
    xphone = input(cy+"(_>)─➤"+bl+" enter phone number : "+wi)
    cpass.set('cred', 'phone', xphone)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    print(cy+"(_>)─➤"+bl+" setup complete !")

def merge_csv():
    import pandas as pd
    import sys
    banner()
    file1 = pd.read_csv(sys.argv[2])
    file2 = pd.read_csv(sys.argv[3])
    print(cy+'(_>)─➤'+bl+' merging '+sys.argv[2]+' & '+sys.argv[3]+' ...')
    print(cy+'(_>)─➤'+bl+' big files can take some time ... ')
    merge = file1.merge(file2, on='username')
    merge.to_csv("output.csv", index=False)
    print(cy+'(_>)─➤'+bl+' saved file as "output.csv"\n')

try:
	if any ([sys.argv[1] == '--config', sys.argv[1] == '-c']):
		print(cy+'(_>)─➤'+bl+' selected module : '+re+sys.argv[1])
		config_setup()
	elif any ([sys.argv[1] == '--merge', sys.argv[1] == '-m']):
		print(cy+'(_>)─➤'+bl+' selected module : '+re+sys.argv[1])
		merge_csv()
	elif any ([sys.argv[1] == '--install', sys.argv[1] == '-i']):
		requirements()
	elif any ([sys.argv[1] == '--help', sys.argv[1] == '-h']):
		banner()
		print(wi+"""$ python setup.py -m file1.csv file2.csv

	( --config  / -c ) setup api configration
	( --merge   / -m ) merge 2 .csv files in one 
	( --install / -i ) install requirements
	( --help    / -h ) show this msg 
			""")
	else:
		print('\n'+cy+'(_>)─➤'+bl+' unknown argument : '+ sys.argv[1])
		print(cy+' ╰───➤'+bl+' for help use : python setup.py -h'+'\n')

except IndexError:
    banner()
    print(f"""
{cy}(_>)─➤{re} no argument given
{cy} ╰───➤ for help run :{bl} python setup.py -h
{cy} ╰───➤ or join to   :{bl} https://t.me/Ivam3_Bot
""")
