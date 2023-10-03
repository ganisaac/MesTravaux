import os

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Classe technique permettant d'assurer une connecion unique à la base de données.
    """
    def __init__(self):
        dotenv.load_dotenv(override=True) 
        self.__connection =psycopg2.connect(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            database=os.environ["DATABASE"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            cursor_factory=RealDictCursor)

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection

if __name__ == "__main__":
    with DBConnection().connection as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            res = cursor.fetchone()
        print(1 == res["test"])
