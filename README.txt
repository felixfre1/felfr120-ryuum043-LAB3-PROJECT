Before you work on your project, activate the corresponding environment:
. venv/bin/activate
We can know how to use flask from below link
https://amateur-engineer-blog.com/flask-api/

{% comment %} we can press this command for formatting SQL {% endcomment %}
{% comment %} Cmd + p →>SQL Format →Enter {% endcomment %}

to open live server
command+shift+p

1. close collab-live session,
2. press "join"
3. add link in vs.code from live share.


sqlite3 database.db < schema.sql

sqlite3 database.db


schema.sqlのコードをコピペして、database_helperにペースト。そうすることで、テーブルの作成が可能になる。


通信処理を成功させるための環境構築 3/2/14:22
server.pyのport番号を5500に設定する。
server.pyをrun(実行)する。
http://127.0.0.1:5500/static/client.html
にアクセスする。

maybe
表示された画面からstatic/client.htmlを選択する。


rm -rf /Users/ryutaro/.anyenv/envs/nodenv/shims/yarn

to use gunicorn in this app, we should use below command
gunicorn server:app -b 127.0.0.1:5500

to search port number info
sudo lsof -i:5500
