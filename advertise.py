# made by thou for thousmc
# made with lots of help from Captainjamason
# started on december 31 2024

from pathlib import Path
import subprocess
import time

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

if __name__ == '__main__':
    #subprocess.run(['curl', 'https://api.mcsrvstat.us/3/', ''])
    print(is_invite(), '\n')
    paths_create(f'~/.local/share/thousmc/advertise/serverinfocache')
    print(CURRENT_TIME)