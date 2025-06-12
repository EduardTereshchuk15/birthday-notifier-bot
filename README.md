# Birthday Notifier Bot

This project is a Google Cloud Function that automates notifying a Telegram group about upcoming birthdays. The script reads birthday information from a Google Sheet and sends messages about today's or next week's birthdays to a specified Telegram group chat using a Telegram bot. The function is triggered on a schedule using Google Cloud Scheduler.

## Features
* Reads birthday data from a Google Sheet
* Sends notifications to a Telegram group about:
   - Today's birthdays
   - This week's birthdays (upcoming birthdays for the week)
* Handles errors gracefully and sends error notifications to a separate Telegram group
* Fully automated and scheduled via Google Cloud Scheduler

## Folder Structure
```
birthday-notifier-bot/
├── main.py               # Main script for the Cloud Function
├── gsheet.py             # Helper functions for interacting with Google Sheets
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (local testing only)
├── credentials.json      # Service account credentials for Google Sheets API
```

## How It Works
  **1. Google Sheet:** 
   - Stores the list of people and their birthdays in the following format:

| Name          | Birthday   |
|---------------|------------|
| John Doe      | 15.10      |
| Jane Smith    | 20.10      |

   - The script fetches this data using the Google Sheets API.

**2. Telegram Notifications:**

  - A Telegram bot sends messages to a group chat with a list of people who have birthdays today or in the upcoming week.
  - If an error occurs (e.g., Google Sheets API issues), the bot sends an error notification to a separate Telegram group.
    
**3. Google Cloud Function:**

- The script runs as a Google Cloud Function (Gen2) and is triggered via HTTP.
- Cloud Scheduler runs the function daily or weekly based on the configured schedule.

## Prerequisites
Before deploying and running the script, make sure you have the following:

**1. Google Cloud Project:**
* Google Cloud project with billing enabled
* APIs enabled:
  - Cloud Functions API
  - Cloud Scheduler API
  - Google Sheets API
    
**2. Google Service Account:**
* A service account with access to the Google Sheet containing birthday data
* A `credentials.json` file for authenticating the service account
  
**3. Telegram Bot:**
- Telegram bot created via @BotFather.
- The bot token and group chat IDs for:
  - The main group (for birthday notifications).
  - The error group (for error notifications).
  
**4. Environment Variables:**
- **TELEGRAM_TOKEN**: The token for your Telegram bot.
- **GROUP_CHAT_ID**: The chat ID of the main Telegram group.
- **ERROR_GROUP_CHAT_ID**: The chat ID of the error notification Telegram group.
- **TABLE_URL**: The URL of the Google Sheet containing birthday data.

## Setup and Deployment
**1. Clone the Repository**
```
git clone https://github.com/EduardTereshchuk15/birthday-notifier-bot.git
cd birthday-notifier-bot
```
**2. Install Dependencies**

Install the required Python libraries:
```
pip install -r requirements.txt
```
**3. Configure Environment Variables**

Create a .env file in the project directory with the following variables:
```
TELEGRAM_TOKEN=your_telegram_bot_token
GROUP_CHAT_ID=your_main_group_chat_id
ERROR_GROUP_CHAT_ID=your_error_group_chat_id
TABLE_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
```
**4. Deploy to Google Cloud Functions**

Deploy the function using the gcloud CLI:

```
gcloud functions deploy publish_birthdays \
    --gen2 \
    --runtime python310 \
    --region us-central1 \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars TELEGRAM_TOKEN=your_telegram_bot_token,GROUP_CHAT_ID=your_main_group_chat_id,ERROR_GROUP_CHAT_ID=your_error_group_chat_id,TABLE_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
```
**5. Configure Cloud Scheduler**

Create a Cloud Scheduler job to trigger the function on a schedule (e.g., every day at 9:00 AM):
```
gcloud scheduler jobs create http birthday-notifier \
    --schedule "0 9 * * *" \
    --uri https://REGION-PROJECT_ID.cloudfunctions.net/publish_birthdays \
    --http-method POST \
    --time-zone "UTC" \
    --message-body '{"mode": "today"}'
```

## Development and Testing
**Local Testing**
1. Run the function locally using the Functions Framework:
```
functions-framework --target=publish_birthdays
```
2. Send a test HTTP request:
```
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"mode": "today"}'
```
**Simulating Errors**

To test error handling, temporarily use an invalid TABLE_URL or remove the credentials.json file.

