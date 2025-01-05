# made by thou for thousmc
# made with lots of help from Captainjamason
# this script works under the assumption that it runs every 30 minutes
# started on december 31 2024

from pathlib import Path
import subprocess
import time
import random

CURRENT_TIME = time.strftime('%Y-%m-%d-%H-%M-%S')

def is_invite():
    # sees if it should run invitation or map advertisement
    # 0 = invite
    # else (30) = map
    minute = time.strftime('%M')
    if minute == 0:
        return True
    else:
        return False

def paths_create(path):
    path_expand = Path(path).expanduser()
    if not Path(path_expand).exists():
        Path(path_expand).mkdir(parents=True)
        print(f'Created path: "{path_expand}"')
    else:
        print(f'"{path_expand}" already exists. Skipping creation...')

def advertisement():
    secret_messages = open('secret_messages.txt')
    secret_message_list = []
    for message in secret_messages:
        secret_message_list.append(message.strip())
    if random.random() < 0.05:
        choice = random.randrange(0, len(secret_message_list))
        return 'tellraw @a [{"text":"' + secret_message_list[choice] + '","color":"gold"}]'
    if is_invite() == True:
        return 'tellraw @a [{"text":"Join the thousmc2 Discord server! ","color":"gray"},{"text":"discord.gg/xr6umCvj8J","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://discord.gg/xr6umCvj8J"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://discord.gg/xr6umCvj8J","color":"gray","italic":true}]}}]\' Enter'
    else:
        return 'tellraw @a [{"text":"Check out the thousmc2 live interactive map! ","color":"gray"},{"text":"map.thousmc.xyz","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://map.thousmc.xyz"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://map.thousmc.xyz","color":"gray","italic":true}]}}]\' Enter'


if __name__ == '__main__':
    print(is_invite(), '\n')
    paths_create(f'~/.local/share/thousmc/advertise/serverinfocache')
    print(advertisement())