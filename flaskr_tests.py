# coding: utf-8
import os
from flaskr import flaskr
import unittest
import tempfile

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


# テスト実行
if __name__ == '__main__':
    unittest.main()

