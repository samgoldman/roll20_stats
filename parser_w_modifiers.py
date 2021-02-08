from bs4 import BeautifulSoup
import sys
import re
from statistics import mean

with open(sys.argv[1]) as f:
    soup = BeautifulSoup(f, 'html.parser')

rolls = {}
names = None

if len(sys.argv) > 2:
    with open(sys.argv[2]) as f:
        names = {}
        for line in f:
            line_names = line.split(',')
            for name in line_names:
                names[name.strip()] = line_names[0]

messages = soup.find_all('div', {'class': 'message'})

most_recent_by = None

for message in messages:
    by = message.find('span', {'class': 'by'})
    
    if not by is None:
        most_recent_by = by.text[:-1]
        if names is not None:
            if most_recent_by in names:
                most_recent_by = names[most_recent_by]

    if not most_recent_by in rolls:
        rolls[most_recent_by] = []

    roll_divs = message.find_all('div', {'class': 'didroll'})
    formulas = message.find_all('div', {'class': 'formula'})

    is_plain_d20 = False

    for formula in formulas:
        if formula.text.startswith('rolling d20') or formula.text.startswith('rolling 1d20'):
            is_plain_d20 = True

    if is_plain_d20:
        for roll_div in roll_divs:
            try:
                rolls[most_recent_by].append(int(roll_div.text))
            except:
                pass

    roll_divs = message.find_all('span', {'class': 'inlinerollresult'})
    for roll_div in roll_divs:
        title = roll_div['title']
        if title.startswith('Rolling 1d20') or title.startswith('Rolling d20'):
            result = roll_div.text
            try:
                rolls[most_recent_by].append(int(result))
            except:
                pass

for key in list(rolls):
    if len(rolls[key]) == 0:
        del rolls[key]

for key, l in sorted(rolls.items(), key=lambda item: mean(item[1]), reverse=True):
    try:
        print('{}\t{:.2f} ({} rolls)'.format(key, mean(l), len(l)))

    except:
        pass
