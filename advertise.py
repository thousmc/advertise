# made by thou for thousmc
# made with lots of help from Captainjamason
# started on december 31 2024

import subprocess
import json
import requests
import os
import time

HOME = os.environ['HOME']
LOCALSHARE = f'{HOME}/.local/share'

def is_invite():
    # sees if it should run invitation or map advertisement
    # 0 = invite
    # else (30) = map
    now = time.strftime('%M')
    if now == 0:
        return True
    else:
        return False

def paths_create():
    if os.path.exists(LOCALSHARE):

        perfect = f'{LOCALSHARE}/thousmc/advertise/grabcache'
        perfect_list = perfect[1:].split('/')

        i = 0
        new = ''
        while i < len(perfect_list):  # final file tree: $HOME/.local/share/thousmc/advertise/grabcache
            old = new
            new = new + '/' + perfect_list[i]
            if perfect_list[i] in LOCALSHARE:
                pass
            else:
                if os.path.exists(f'{new}'):
                    print(f'"{perfect_list[i]}" already exists.')
                else:
                    os.makedirs(f'{new}', exist_ok=True)
                    print(f'Created "{perfect_list[i]}" directory in "{old}"')
            i = i + 1

    else:
        raise ValueError(f"{LOCALSHARE} doesn't exist")

if __name__ == '__main__':

    #subprocess.run(['curl', 'https://api.mcsrvstat.us/3/', ''])
    print(is_invite(), '\n')
    paths_create()