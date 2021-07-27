import sqlite3


class DB:
    def __init__(self, dbn):
        self._conn = sqlite3.connect(dbn, check_same_thread=False)
        self._cur = self._conn.cursor()

    def insert(self, sql, values=()):
        self._cur.execute(sql, values)
        self._conn.commit()

    def get(self, sql, values=()):
        try:
            return self._cur.execute(sql, values).fetchall()
        except Exception as e:
            print(e)
            return None

    def insert_many(self, sql, values_list=(())):
        self._cur.executemany(sql, values_list)
        self._conn.commit()

    '''def get_many(self, sql, values_list=(())):
            try:
                return self._cur.executemany(sql, values_list).fetchall()
            except:
                return None'''