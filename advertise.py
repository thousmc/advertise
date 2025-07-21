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

def format_ads():
    ads_dir = Path('ads')
    ad_files = list(ads_dir.glob('*.json'))

    formatted_ads = []
    for i in ad_files:
        ad = i.open()
        loaded_ad = json.load(ad)
        formatted_ad = json.dumps(loaded_ad, separators=(',', ':'))
        formatted_ads.append(formatted_ad)
    return formatted_ads

def paths_create(path):
    path_expand = Path(path).expanduser()
    if not Path(path_expand).exists():
        Path(path_expand).mkdir(parents=True)
        print(f'Created path: "{path_expand}"')
        return path_expand
    else:
        return path_expand

def ad_decision(formatted_ads):
    if not formatted_ads:
        return None
    ad_decision_path = paths_create('~/.local/state/thousmc/advertise')
    ad_decision_file = ad_decision_path / 'ad_decision.txt'
    current_index = 0
    if ad_decision_file.is_file():
        try:
            current_index = int(ad_decision_file.read_text())
        except ValueError:
            current_index = 0
    if current_index >= len(formatted_ads):
        current_index = 0
    next_index = current_index + 1
    if next_index >= len(formatted_ads):
        next_index = 0
    ad_decision_file.write_text(str(next_index))
    return current_index

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
    all_ads = format_ads()
    ad_index = ad_decision(all_ads)
    if ad_index is not None:
        chosen_ad_json = all_ads[ad_index]
        return f'tellraw @a {chosen_ad_json}'
    exit(1)
        
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