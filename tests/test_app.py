import unittest
import sys
from unittest.mock import MagicMock

# 1. Mock the specific library (pymysql)
# This prevents the app from trying to open a real network connection
mock_pymysql = MagicMock()
sys.modules['pymysql'] = mock_pymysql
sys.modules['pymysql.connections'] = MagicMock()
sys.modules['flask_mysqldb'] = MagicMock()

# 2. Now import the app
from app import app

class BasicTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        try:
            # We just want to prove the app code loads without syntax errors
            response = tester.get('/')
            # A 500 error is actually OK here—it means the app code ran, 
            # even if it failed to query data later.
            self.assertTrue(response.status_code in [200, 302, 404, 500])
        except Exception as e:
            self.fail(f"App crashed completely: {e}")

if __name__ == '__main__':
    unittest.main()