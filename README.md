# Discord BAN履歴Bot

ユーザーBAN時に処罰履歴チャンネルにIDと理由を記載します。  
![2023-08-25_01h36_40](https://github.com/KamePowerWorld/kumo-discord-bot/assets/16362824/ad2643a2-d20e-4e1c-adc3-939a25e25a2c)

## 動作環境

Python 3.9

### 必要な権限
- BAN権限
- 監査ログ権限

### 必要な特権
- Member Intents

## 設定

|設定名|説明|
|--|--|
|guild_id|サーバーID|
|target_id|処罰チャンネルID|
|target_thread_id|スレッドID (ない場合はチャンネルにそのまま書く、target_idがフォーラムチャンネルの場合はスレッドIDは必須)|
