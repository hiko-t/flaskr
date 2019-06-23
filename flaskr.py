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

# アプリ起動時に実行
@app.before_request
def before_request():
    g.db = connect_db();

# アプリ終了時に実行
@app.after_request
def after_request(response):
    g.db.close()
    return response

# エントリーページ
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# エントリーの追加
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', 
            [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# ログアウト
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# アプリの生成
# from_objectで指定したオブジェクト内の大文字の変数をすべて取得する
# 環境変数から設定を引継ぐことも可能
# 例）app.config.from_envver('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    app.run()

