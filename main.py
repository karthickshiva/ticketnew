import http.client

import requests
import json
import logging
import configparser

config = configparser.ConfigParser()
config.read('keys.properties')

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logs.txt')

file_name = 'ref.json'
cinemas = []
bot_key = config.get('Keys', 'bot_key')
chat_id = config.get('Keys', 'chat_id')


def send_to_telegram_bot(text):
    telegram_url = f'https://api.telegram.org/bot{bot_key}/sendMessage'

    payload = json.dumps({
        "chat_id": chat_id,
        "text": text
    })
    headers = {
        'Content-Type': 'application/json'
    }

    telegram_response = requests.request("POST", telegram_url, headers=headers, data=payload)
    if telegram_response.status_code == 200:
        logger.info("Notification sent")
    else:
        logger.info("Notification failed")


def check_ticketnew():
    ref_cinemas = []
    try:
        with open(file_name, 'r') as json_file:
            ref_cinemas = json.load(json_file)
    except FileNotFoundError:
        logger.info("No reference file to compare.")

    url = (
        "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city=chennai&movieCode=rur_1kciu&version=3"
        "&site_id=6&channel=HTML5&child_site_id=370")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        current_cinemas = []
        for cinema in data['meta']['cinemas']:
            current_cinemas.append(cinema['name'])
        with open(file_name, 'w') as json_file:
            json.dump(current_cinemas, json_file)

        new_cinemas = [cinema for cinema in current_cinemas if cinema not in ref_cinemas]
        if len(new_cinemas) == 0:
            msg = 'No new cinemas added!'
        else:
            msg = 'New cinemas added: \n' + '\n'.join(new_cinemas)
            send_to_telegram_bot(msg)
        logger.info(msg)
    else:
        logger.info("Failed to retrieve the API data. Status code:", response.status_code)


def check_mayajaal():
    ref_file = ''
    try:
        with open("maya.txt", 'r') as f:
            ref_file = f.read()
    except FileNotFoundError:
        logger.info("No reference file to compare.")
    conn = http.client.HTTPSConnection("cinemas.bookmyshow.com")
    conn.request("GET", "https://cinemas.bookmyshow.com/api/getDEData?cmd=IBVGETSHOWTIMESBYEVENT&cc=MAYA&dc=20231019&ec=ET00351731&sr=CHEN&et=MT&f=json")
    res = conn.getresponse()
    msg = 'Mayajaal timings:\n'
    if res.status == 200:
        data = json.loads(res.read().decode("utf-8"))
        for show_times in data['BookMyShow']['arrShowTimes']:
            msg += show_times['ShowTimeDisplay'] + '\n'
        #logger.info(msg)
        if ref_file != msg:
            with open('maya.txt', 'w') as f:
                f.write(msg)
            print(msg)
            send_to_telegram_bot(msg)
    else:
        print(res.read().decode("utf-8"))
        logger.info("Failed to retrieve the API data. Status code:", res.status)


while True:
    check_mayajaal()
