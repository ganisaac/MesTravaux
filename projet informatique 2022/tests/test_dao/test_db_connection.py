from dao.db_connection import DBConnection
import unittest

class TestConnection(unittest.TestCase):

    def test_connection(self):
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                res = cursor.fetchone()
        self.assertEqual(1,res["test"])

if __name__ == "__main__":
    unittest.main()