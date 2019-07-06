# coding: utf-8
import os
from flaskr import flaskr
import unittest
import tempfile

'''
定数
'''

USERNAME = 'admin'
PASSWORD = 'default'

class FlaskrTestCase(unittest.TestCase):

    # テストの準備
    def setUp(self):
        # テスト用DBを作成
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    # テストの後始末
    def tearDown(self):
        # テスト用DBを削除
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    # 空DBのテスト
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    # テスト用ログイン関数
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    # テスト用ログアウト関数
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # ログイン、ログアウトのテスト
    def test_login_logout(self):
        # 正常ログイン
        rv = self.login(USERNAME, PASSWORD)
        assert b'You were logged in' in rv.data
        # 正常ログアウト
        rv = self.logout()
        assert b'You were logged out' in rv.data
        # 異常ログイン　ユーザー名違い
        rv = self.login('adminx', PASSWORD)
        assert b'Invalid username' in rv.data
        # 異常ログイン　パスワード違い
        rv = self.login(USERNAME, 'defaultx')
        assert b'Invalid password' in rv.data

    # メッセージ追加テスト
    def test_messages(self):
        sample_txt='<strong>HTML</strong> allowed here'
        self.login(USERNAME, PASSWORD)
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text=sample_txt,
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

# テスト実行
if __name__ == '__main__':
    unittest.main()

