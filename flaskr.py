# coding: utf-8
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE   = '/tmp/flaskr.db'
DEBUG      = True
SECRET_KEY = 'development key'
USERNAME   = 'admin'
PASSWORD   = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db();

@app.after_request
def after_request(response):
    g.db.close()
    return response

# アプリの生成
# from_objectで指定したオブジェクト内の大文字の変数をすべて取得する
# 環境変数から設定を引継ぐことも可能
# 例）app.config.from_envver('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0')
    app.run()

