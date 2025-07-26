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
    json_files = list(ads_dir.glob('*.json'))
    py_files = list(ads_dir.glob('*.py'))

    formatted_ads = []
    for i in json_files:
        ad = i.open()
        loaded_ad = json.load(ad)
        formatted_ad = json.dumps(loaded_ad, separators=(',', ':'))
        formatted_ads.append(('json', formatted_ad))

    for py_file in py_files:
        formatted_ads.append(('python', str(py_file)))
    return formatted_ads

def execute_python_ad(py_file_path):
    try:
        result = subprocess.run([sys.executable, py_file_path], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Python ad error: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Python ad timed out: {py_file_path}")
        return None
    except Exception as e:
        print(f"Error executing Python ad: {e}")
        return None

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
        ad_type, ad_content = all_ads[ad_index]
        if ad_type == 'json':
            return f'tellraw @a {ad_content}'
        elif ad_type == 'python':
            python_result = execute_python_ad(ad_content)
            if python_result:
                return python_result
            else:
                # fallback to next json ad if Python execution fails
                json_ads = [ad for ad in all_ads if ad[0] == 'json']
                if json_ads:
                    return f'tellraw @a {json_ads[0][1]}'
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
        return True

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