import functions_framework
from datetime import datetime, timedelta
from dotenv import load_dotenv
from gsheet import get_birthdays, send_message

load_dotenv()

@functions_framework.http
def publish_birthdays(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    mode = None
    if request_json and "mode" in request_json:
        mode = request_json["mode"]
    elif request_args and "mode" in request_args:
        mode = request_args["mode"]

    if not mode:
        return {"error": "Missing 'mode' parameter. Use 'today' or 'week'."}, 400

    bdays = get_birthdays()
    today = datetime.now()

    if mode == "week":
        end = today + timedelta(days=6 - today.weekday())
        upcoming = [
            b for b in bdays
            if b["date"].month == today.month and today.day <= b["date"].day <= end.day
        ]

        if not upcoming:
            return {"message": "No birthdays this week"}, 200

        if upcoming:
            msg = "🎂 Цього тижня святкують:\n" + "\n".join(
                f"• {b['name']} — {b['date'].strftime('%d.%m')}" for b in upcoming
            )
        send_message(msg)
        return {"message": msg}, 200

    elif mode == "today":
        today_birthdays = [
            b for b in bdays if b["date"].day == today.day and b["date"].month == today.month
        ]

        if not today_birthdays:
            return {"message": "No birthdays today"}, 200

        names = [b["name"] for b in today_birthdays]
        names_str = ", ".join(names)
        msg = f"🎉 Сьогодні день народження у {names_str}! Привітаймо! 🥳"
        send_message(msg)
        return {"message": msg}, 200
    return None
