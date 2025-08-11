#!/usr/bin/env python3
import json
import datetime
import sys

# stop output after jan 1
if datetime.datetime.now() >= datetime.datetime(2026, 1, 1):
    sys.exit(0)

def ordinal(n: int) -> str:
    if 10 <= (n % 100) <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

expiry_date = datetime.datetime(2026, 1, 1)
now = datetime.datetime.now()
delta = expiry_date - now
days_until_expiry = max(delta.days, 0)

months = (expiry_date.year - now.year) * 12 + (expiry_date.month - now.month)
if expiry_date.day < now.day:
    months -= 1
months = max(months, 0)

weeks = days_until_expiry // 7

if days_until_expiry <= 0:
    hover_main = "Expired"
elif months >= 1:
    hover_main = f"{months} month{'s' if months != 1 else ''} left"
elif weeks >= 1:
    hover_main = f"{weeks} week{'s' if weeks != 1 else ''} left"
else:
    hover_main = f"{days_until_expiry} day{'s' if days_until_expiry != 1 else ''} left"

if days_until_expiry == 1:
    prefix_text = 'ATTENTION: '
elif days_until_expiry <= 7:
    prefix_text = 'WARNING: '
elif days_until_expiry <= 30:
    prefix_text = 'Notice: '
else:
    prefix_text = 'Remember! '

date_display = expiry_date.strftime("%B ") + ordinal(expiry_date.day) + expiry_date.strftime(", %Y")
pre_text = f'{prefix_text}The "play.thousmc.xyz" IP will stop working on '
post_text = '. Please switch to "thousmc.net" before then!'

tellraw_data = [
    {
        "text": pre_text,
        "color": "red"
    },
    {
        "text": date_display,
        "underlined": True,
        "hover_event": {
            "action": "show_text",
            "value": [
                {"text": hover_main, "color": "gray", "italic": True},
                {"text": f" ({days_until_expiry} days total)", "color": "gray"}
            ]
        }
    },
    {
        "text": post_text,
        "color": "red"
    }
]

print('/tellraw @a ' + json.dumps(tellraw_data, separators=(",", ":")))