import ssl
import certifi
import slack_sdk

import os

from dotenv import load_dotenv

# env load
load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())

slack_token = os.getenv("SLACK_BOT_TOKEN")
client = slack_sdk.WebClient(token=slack_token, ssl=ssl_context)

client.chat_postMessage(channel='#dev_alarm_bot',
                        text="API TEST4")