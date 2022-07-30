import requests
import datetime
import os
import re
import csv
import sys

def get_conversation_history(ch_name, cursor=None):
    """
    APIをリクエストして過去の会話を取得する
    """
    url = "https://slack.com/api/conversations.history?cursor={}".format(cursor) if cursor is not None else "https://slack.com/api/conversations.history"
    token = os.environ["SLACK_BOT_TOKEN"]


    header={
        "Authorization": "Bearer {}".format(token),
    }

    payload  = {
        "channel" : ch_name
        }

    res = requests.get(url, headers=header, params=payload)
    return res.json()


def main(ch_name, output_file, cursor=None):
    """
    APIで取得できるメッセージ数の上限があるため、再帰関数として作っている
    """
    # 以下の2行のコメントアウトを外すと、Slack APIへのリクエストは1回しか送られなくなる
    # if cursor is not None:
    #     return

    res = get_conversation_history(ch_name, cursor)
    # APIが正しく実行できなかった場合は異常終了する
    if res['ok'] is not True:
        print(res)
        sys.exit(1)

    if res['has_more']:
        main(ch_name, output_file, res['response_metadata']['next_cursor'])
    messages = res['messages']

    output_array = []
    # APIの結果が新しい記録から表示されるので、逆順にソートする
    for message in messages[::-1]:
        # 時間の取得
        ts = message['ts'].split('.')[0]
        dt = datetime.datetime.fromtimestamp(int(ts))

        msg_date = dt.strftime("%Y-%m-%d %H:%M:%S")

        # 日付, 記録内容で配列作成
        output_array.append([msg_date, message['text']])

    # CSVファイル保存
    with open(output_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(output_array)

# 保存したいチャンネル
args = sys.argv
ch_name = args[1]

# アウトプットするファイル名
now_time = datetime.datetime.now()
output_file = "{}-{}.csv".format(ch_name, now_time.strftime('-%Y%m%d%H%M%S'))

main(ch_name=ch_name, output_file=output_file)
