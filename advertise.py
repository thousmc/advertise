#!/usr/bin/env python3

'''
made by thou for thousmc
made with lots of help from Captainjamason
started on december 31 2024
first working version completed on january 7 2025
'''

from pathlib import Path
import requests
import json
import subprocess
import time
import random
import argparse
import sys

CURRENT_TIME = time.strftime('%Y-%m-%d-%H-%M-%S')
SECRET_MESSAGE_CHANCE = 0.04  # added for readability
SCRIPT_DIR = Path(__file__).resolve().parent
MAP_AD = 'tellraw @a [{"text":"Check out the thousmc2 live interactive map! ","color":"gray"},{"text":"map.thousmc.xyz","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://map.thousmc.xyz"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://map.thousmc.xyz","color":"gray","italic":true}]}}]'
INVITE_AD = 'tellraw @a [{"text":"Join the thousmc2 Discord server! ","color":"gray"},{"text":"discord.gg/xr6umCvj8J","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://discord.gg/xr6umCvj8J"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://discord.gg/xr6umCvj8J","color":"gray","italic":true}]}}]'

def paths_create(path):
    path_expand = Path(path).expanduser()
    if not Path(path_expand).exists():
        Path(path_expand).mkdir(parents=True)
        print(f'Created path: "{path_expand}"')
        return path_expand
    else:
        return path_expand

def is_invite():
    is_invite_path = paths_create('~/.local/state/thousmc/advertise')
    global is_invite_file  # maybe i shouldnt do this
    is_invite_file = is_invite_path / 'is_invite.txt'
    opened = is_invite_file.open() if (is_invite_file.is_file()) else None
    if not is_invite_file.is_file():
        choice = str(random.randint(0, 1))
        is_invite_file.touch()
        is_invite_file.write_text(choice)
        return choice
    return '1' in opened.read()

def advertisement():
    if are_players('play.thousmc.xyz', save=True) == False:
        exit(1)
    # secret message functionality
    # small chance a non-discord, non-map message occurs
    secret_messages = open(f'{SCRIPT_DIR}/secret_messages.txt')
    secret_message_list = []
    for message in secret_messages:
        secret_message_list.append(message.strip())
    if random.random() < SECRET_MESSAGE_CHANCE:
        return 'tellraw @a [{"text":"' + random.choice(secret_message_list) + '","color":"gold"}]'
    # actual discord & map ad
    if is_invite() == True:
        is_invite_file.write_text('0')
        return INVITE_AD
    else:
        is_invite_file.write_text('1')
        return MAP_AD
        
def are_players(url, save=False):
    # thank you jamason
    link = 'https://api.mcsrvstat.us/3/' + url
    response = requests.get(link)
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        raise Exception(f"Error: {response.status_code}")
    are_players_cache_path = paths_create('~/.local/state/thousmc/serverinfocache')
    if save == True:
        dump_filename = f'{are_players_cache_path}/{url}-{CURRENT_TIME}.json'
        with open(dump_filename, 'w') as file:
            json.dump(data, file, indent=4)
    if data["online"] == True and data["players"]["online"] > 0:
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) == 1:
        subprocess.run(['tmux', 'send-keys', '-t', '0', f'{advertisement()}', 'Enter'])
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--areplayers', type=str, help='Return "True" if players are on the specified Minecraft server')
    parser.add_argument('-s', '--save', action='store_true', help='Optional flag to save the .json parsed by "-a"/"--areplayers"')

    args = parser.parse_args()
    if args.save and not args.areplayers:
        parser.error('The "--save" option requires the "-a"/"--areplayers" argument.')

    if args.areplayers:
        if args.save:
            print(are_players(args.areplayers, save=True))
        else:
            print(are_players(args.areplayers))