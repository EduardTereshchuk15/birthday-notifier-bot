import os
import requests

from datetime import datetime
from gspread import Client, service_account
from dotenv import load_dotenv

load_dotenv()

def client_init_json() -> Client:
    return service_account(filename='credentials.json')

def get_birthdays():
    client = client_init_json()

    table_url = os.environ["TABLE_URL"]
    sheet = client.open_by_url(table_url).sheet1
    rows = sheet.get("A1:C")

    bdays = []
    for row in rows:
        try:
            name, date_str = row
            bday = datetime.strptime(date_str.strip(), "%d.%m")
            bdays.append({"name": name, "date": bday})
        except:
            continue
    return bdays

def send_message(message):
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(response.json())
