#!/usr/bin/env python3

from pathlib import Path
import json

MAP_AD = Path('map.json')
MAP_AD_ORG = '[{"text":"Check out the thousmc2 live interactive map! ","color":"gray"},{"text":"map.thousmc.xyz","color":"gold","underlined":true,"clickEvent":{"action":"open_url","value":"https://map.thousmc.xyz"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://map.thousmc.xyz","color":"gray","italic":true}]}}]'

if __name__  == '__main__':
    ad = MAP_AD.open()
    data = json.load(ad)
    compact = json.dumps(data, separators=(',', ':'))

    if compact == MAP_AD_ORG:
        identical = True
    else:
        identical = False

    print('Converted version:\n', compact)
    print('Original string:\n', MAP_AD_ORG)
    print('Are they identical?:', identical)