import requests
import pprint
import json
import sqlite3

conn = sqlite3.connect('db/Culture.db')
cursor = conn.cursor()

for i in range(1, 148):
    if i == 1:
        start = 0
    finish = i * 1000
    url = f'https://opendata.mkrf.ru/v2/egrkn/$?s={start}&l={finish}'
    res = requests.get(f'https://opendata.mkrf.ru/v2/egrkn/$?s=0&l=1000',
                       headers={
                           'X-API-KEY': '772c6ef89b0ef87bededd6647107b4fd1b2586b157e0540405e917a789c5d581'}).text

    start = finish

    res = json.loads(res)['data']
    for el in res:
        el = el['changes'][0]['diff'][0]['value']['general']

        name = el['name']
        try:
            address_text = str(el.get('address').get('fullAddress'))
        except AttributeError:
            address_text = ''
        try:
            map_position = str(el['address']['mapPosition']['coordinates'])
        except (KeyError, AttributeError, TypeError):
            map_position = ''

        category = el['categoryType']['value']

        try:
            photo = el['photo']['url']
        except (KeyError, TypeError):
            photo = ''
        try:
            info = el['securityInfo']
        except KeyError:
            info = ''

        object_type = el['typologies'][0]['value']
        unesco_status = el['unesco']['value']

        cursor.execute(
            "Insert into objects (name, address_text, map_pos, category, photo, info, object_type, unesco_status) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            (name, address_text, map_position, category, photo, info, object_type, unesco_status))
        conn.commit()

cursor.close()
conn.close()
