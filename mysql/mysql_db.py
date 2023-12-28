import re
import sys
sys.path.append('/code/Langchain-Chatchat')
from configs import MYSQL_HOST
import pymysql
from queue import Queue

HOST = MYSQL_HOST
USER ='selector'
PWD ='gicselector'
DB ='gemology'

class ConnectionPool:
    def __init__(self, size, *args, **kwargs):
        self._size = size
        self._pool = Queue(size)
        self._args = args
        self._kwargs = kwargs
        self._initialize_pool()

    def _initialize_pool(self):
        for _ in range(self._size):
            conn = pymysql.connect(*self._args, **self._kwargs)
            self._pool.put(conn)

    def get_connection(self):
        try:
            return self._pool.get(block=False)
        except Queue.Empty:
            print("No connection available, creating a new one.")
            conn = pymysql.connect(*self._args, **self._kwargs)
            return conn

    def release_connection(self, conn):
        self._pool.put(conn)

    def close_all(self):
        while not self._pool.empty():
            conn = self._pool.get()
            conn.close()

pool = ConnectionPool(5, host=HOST, user=USER, password=PWD, db=DB)