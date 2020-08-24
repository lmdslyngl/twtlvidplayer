# twtlvidplayer
- Twitterのタイムラインに流れてきた動画を収集して連続再生するWebアプリ

## 動かし方
1. docker/data/token_template.jsonにTwitterトークンを設定し，token.jsonにリネーム
2. ``` # docker-compose up -d ```
3. ``` http://{立てたサーバ}:5000/index.html ```にアクセス
