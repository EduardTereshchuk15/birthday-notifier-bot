import json
from collections import defaultdict
from datetime import datetime, timedelta
from gsheet import get_birthdays, send_message

BIRTHDAY_MESSAGES = {
    "today": "🎉 Сьогодні святкують день народження! Привітаймо! 🥳\n",
    "week": "🎂 Цього тижня святкують день народження:\n"
}

def lambda_handler(event, context):
    mode = extract_mode(event)
    if not mode:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'mode' parameter. Use 'today' or 'week'."})
        }

    bdays = get_birthdays()
    grouped_bdays = group_birthdays_by_chat(bdays, mode)
    send_birthday_notifications(grouped_bdays, mode)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Success notified"})
    }


def extract_mode(event):
    body = event.get("body")
    if body:
        try:
            json_body = json.loads(body)
            if "mode" in json_body:
                return json_body["mode"]
        except json.JSONDecodeError:
            pass

    if event.get("queryStringParameters") and "mode" in event["queryStringParameters"]:
        return event["queryStringParameters"]["mode"]

    return None


def group_birthdays_by_chat(bdays, mode):
    today = datetime.now()
    result = defaultdict(list)

    if mode == "today":
        for b in bdays:
            if b["date"].day == today.day and b["date"].month == today.month:
                result[b["chat_id"]].append(b)

    elif mode == "week":
        start = today
        end = today + timedelta(days=6 - today.weekday())

        for b in bdays:
            bday_this_year = b["date"].replace(year=today.year)
            if start.date() <= bday_this_year.date() <= end.date():
                result[b["chat_id"]].append(b)

    return result

def build_message(mode, people):
    header = BIRTHDAY_MESSAGES.get(mode, "")
    body = "\n".join(f"• {p['name']} — {p['date'].strftime('%d.%m')}" for p in people)
    return header + body

def send_birthday_notifications(grouped_bdays, mode):
    for chat_id, people in grouped_bdays.items():
        if not people:
            continue
        msg = build_message(mode, people)
        send_message(chat_id, msg)
