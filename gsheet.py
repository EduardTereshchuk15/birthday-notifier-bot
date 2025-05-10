import os
import requests

from datetime import datetime
from gspread import Client, service_account
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]
ERROR_GROUP_CHAT_ID = os.environ["ERROR_GROUP_CHAT_ID"]

def client_init_json() -> Client:
    return service_account(filename='credentials.json')

def get_birthdays():
    try:
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
            except Exception as e:
                error_message = f"Error parsing row {row}: {str(e)}"
                send_message(ERROR_GROUP_CHAT_ID, error_message)
                print(error_message)
                continue
        return bdays

    except Exception as e:
        error_message = f"An error occurred in get_birthdays(): {str(e)}"
        send_message(ERROR_GROUP_CHAT_ID, error_message)
        raise

def send_message(group_chat_id, message):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": group_chat_id,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(response.json())
