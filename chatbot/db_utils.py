import psycopg2

class DBUtils:

    cur = None

    def __init__(self):
        conn = psycopg2.connect("dbname=innovation user=postgres password=postgres")
        self.cur = conn.cursor()

    def query(self, query=None):
        self.cur.execute(query)
        return self.cur.fetchall()
