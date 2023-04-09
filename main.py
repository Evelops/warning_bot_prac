import ssl
import certifi
import slack_sdk
import pymysql

from config.conn_db import connect_to_db

import os
from dotenv import load_dotenv

# env load
load_dotenv()
# get DB NAME
db_name = os.getenv("DB_NAME")


# connection to db
try:
    connect_to_db()
    cur = connect_to_db().cursor()
except Exception:
    print("error")

# RDS 테이블의 정보 조회
check_db_status = f"SHOW TABLE STATUS FROM {db_name} LIKE 'selection';"

ssl_context = ssl.create_default_context(cafile=certifi.where())

slack_token = os.getenv("SLACK_BOT_TOKEN")
client = slack_sdk.WebClient(token=slack_token, ssl=ssl_context)

client.chat_postMessage(channel='#dev_alarm_bot',
                        text=now_date)
