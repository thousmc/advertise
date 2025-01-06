# made by thou for thousmc
# made with lots of help from Captainjamason
# this script works under the assumption that it runs every 30 minutes
# started on december 31 2024

from pathlib import Path
import subprocess
import time
import random

CURRENT_TIME = time.strftime('%Y-%m-%d-%H-%M-%S')

def paths_create(path):
    path_expand = Path(path).expanduser()
    if not Path(path_expand).exists():
        Path(path_expand).mkdir(parents=True)
        print(f'Created path: "{path_expand}"')
        return path_expand
    else:
        print(f'"{path_expand}" already exists. Skipping creation...')
        return path_expand

def is_invite():
    is_invite_path = paths_create('~/.local/share/thousmc/advertise')
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

    # secret message functionality
    # small chance a non-discord, non-map message occurs
    secret_messages = open('secret_messages.txt')
    secret_message_list = []
    for message in secret_messages:
        secret_message_list.append(message.strip())
    if random.random() < 0.04:
        choice = random.randrange(0, len(secret_message_list))
        return 'tellraw @a [{"text":"' + secret_message_list[choice] + '","color":"gold"}]'

    # actual discord & map ad
    if is_invite() == True:
        is_invite_file.write_text('0')
        return 'tellraw @a [{"text":"Join the thousmc2 Discord server! ","color":"gray"},{"text":"discord.gg/xr6umCvj8J","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://discord.gg/xr6umCvj8J"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://discord.gg/xr6umCvj8J","color":"gray","italic":true}]}}]\' Enter'
    else:
        is_invite_file.write_text('1')
        return 'tellraw @a [{"text":"Check out the thousmc2 live interactive map! ","color":"gray"},{"text":"map.thousmc.xyz","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://map.thousmc.xyz"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://map.thousmc.xyz","color":"gray","italic":true}]}}]\' Enter'
        

def is_online(url, save=False):
    pass

if __name__ == '__main__':
    paths_create('~/.local/share/thousmc/serverinfocache')
    print(advertisement())