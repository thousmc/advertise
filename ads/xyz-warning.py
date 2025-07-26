#!/usr/bin/env python3

import json
import datetime

# Example: Warning about IP expiration
expiry_date = datetime.datetime(2026, 1, 1)  # August 15, 2025
current_date = datetime.datetime.now()
days_until_expiry = (expiry_date - current_date).days

if days_until_expiry == 1:
    message_text = f'ATTENTION: ".xyz" thousmc domains (e.g. play.thousmc.xyz) will stop working in {days_until_expiry} day on January 1st 2026! Please switch to "thousmc.net" or "play.thousmc.net!"'
elif days_until_expiry <= 7:
    message_text = f'WARNING: ".xyz" thousmc domains (e.g. play.thousmc.xyz) will stop working in {days_until_expiry} days on January 1st 2026! Please switch to "thousmc.net" or "play.thousmc.net!"'
elif days_until_expiry <= 30:
    message_text = f'Notice: ".xyz" thousmc domains (e.g. play.thousmc.xyz) will stop working in {days_until_expiry} days on January 1st 2026! Please switch to "thousmc.net" or "play.thousmc.net!"'
else:
    message_text = f'Remember! ".xyz" thousmc domains (e.g. play.thousmc.xyz) will stop working in {days_until_expiry} days on January 1st 2026! Please switch to "thousmc.net" or "play.thousmc.net!"'

# Generate tellraw JSON
tellraw_data = [
    {
        "text": message_text,
        "color": "red",
        "bold": days_until_expiry <= 7
    }
]

print(f'tellraw @a {json.dumps(tellraw_data, separators=(",", ":"))}')