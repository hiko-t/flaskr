import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
    
    # テストの準備
    def setUp(self):
        # テスト用DBを作成
        self.db_fd, flaskr.DATABASE = tempfile.mkstemp()
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    # テストの後始末
    def tearDown(self):
        # テスト用DBを削除
        os.close(self.db_fd)
        os.unlink(flaskr.DATABASE)

    if __name__ == '__main__':
        unittest.main()

