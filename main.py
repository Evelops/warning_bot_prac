import ssl
import certifi
import slack_sdk
import pymysql
import time
import json

import boto3

from config.conn_db import connect_to_db
from s3_Info import s3_info

import os
from dotenv import load_dotenv

# env load
load_dotenv()
# S3 연결 객체 생성
s3 = boto3.resource('s3')

# get env file load
db_name = os.getenv("DB_NAME")
slack_token = os.getenv("SLACK_BOT_TOKEN")

# define ssl certi
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = slack_sdk.WebClient(token=slack_token, ssl=ssl_context)

# date
now_date = time.strftime('%Y-%m-%d %H:%M:%S')
# connection to db
try:
    conn = connect_to_db()
    cur = conn.cursor()
except Exception as e:
    print(f"error => {type(e).__name__} - {str(e)}")

# RDS 테이블의 index, date 사이즈 총 사용량
check_db_status = "SELECT SUM(data_length + index_length) FROM information_schema.tables;"

cur.execute(check_db_status)
db_usage = cur.fetchone()[0]

# RDS 사용량 체크 후 byte to gigabyte
total_usage = f'{round(db_usage/(1024 * 1024 * 1024), 4)}GB'

print(db_usage)
print(round(db_usage/(1024 * 1024 * 1024), 4))

cur.close()
# RDS, S3 에 대한 기본정보를 json 타입으로 Slack Msg 전송
message = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{now_date}*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*S3 사용량:*\n{s3_info()['bucket_size']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*저장된 S3 파일 수:*\n{s3_info()['file_count']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*RDS 사용량:*\n {total_usage}"
            }
        },

    ]
}

# msg 전송 함수
def send_slack_msg(msg):
    print(msg)
    try:
        client.chat_postMessage(channel='#dev_alarm_bot',
                                blocks=msg["blocks"],
                                text="DEV Alarm Bot"
                                )
    except Exception as e:
        print(f"send slack msg error:{e}")


send_slack_msg(message)

