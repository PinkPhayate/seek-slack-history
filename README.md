# seek-slack-history

## outline
slackのAPIを使って、特定のチャンネルの記録を取得するスクリプト

フリープランではprivateなレポジトリとダイレクトメッセージをSlack UIからexportする方法がなかったのでAPIで取得できるようにする

## Usage
1. slackのAPI実行をする時に必要なトークンを取得する
2. tokenを使ったAPIでアクセスできるスコープを決める

以下のスコープにアクセスできると大体のチャンネルの履歴は取れる
  - channels:history
  - groups:history
  - im:history

3. 2で取得したトークンを環境変数で登録
```
export SLACK_BOT_TOKEN=xoxp-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
4. 過去のトークを取得したいチャンネルのキーをUIから取得
slackの画面でチャンネルを右クリックした時に取得できる。
5. スクリプト実行
CSVで履歴が取得できる
```
# キーがGJVGEUEP8になっているチャンネルの過去のメッセージを全件取得
python seek-history.py GJVGEUEP8
```

## Requirement
- requests
- python 3

```
pip install -r requirements.txt
```
