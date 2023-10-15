import requests
import json

file_name = 'ref.json'
cinemas = []
bot_key = '6565753430:AAEVdg3dBuEkdEfQzZF_njdUDmLx6V3j-Vo'
chat_id = 1191000872


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
        print("Notification sent")
    else:
        print("Notification failed")


try:
    with open(file_name, 'r') as json_file:
        cinemas = json.load(json_file)
except FileNotFoundError:
    print("No reference file to compare.")

url = ("https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city=chennai&movieCode=rur_1kciu&version=3"
       "&site_id=6&channel=HTML5&child_site_id=370")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    current_cinemas = []
    for cinema in data['meta']['cinemas']:
        current_cinemas.append(cinema['name'])
    with open(file_name, 'w') as json_file:
        json.dump(current_cinemas, json_file)

    new_cinemas = [cinema for cinema in current_cinemas if cinema not in cinemas]
    msg = ''
    if len(new_cinemas) == 0:
        msg = 'No new cinemas added!'
    else:
        msg = 'New cinemas added: \n' + '\n'.join(new_cinemas)
    print(msg)
    send_to_telegram_bot(msg)

else:
    print("Failed to retrieve the API data. Status code:", response.status_code)
