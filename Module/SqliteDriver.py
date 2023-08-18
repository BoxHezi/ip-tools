import sqlite3
from time import strftime


class DB:

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = self.connect()
        self.cursor = self.connection.cursor() if self.connection is not None else None

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def connect(self):
        try:
            connection = sqlite3.connect(self.db_path)
            return connection
        except Exception as e:
            print(e)
            return None

    def get_cursor(self):
        return self.cursor if self.cursor is not None else None

    def update_data(self, table: str, *data: str):
        """
        :param table: table name to be inserted to
        :param data:  data to be inserted to, data[0] country_code, data[1] data
        """
        last_updated = strftime("%Y-%m-%d %H:%M:%S")
        select_query = "SELECT country_code, data FROM {} WHERE country_code = ?".format(table)
        self.cursor.execute(select_query, (data[0],))
        value = self.cursor.fetchone()  # if not None, value[0] = country_code, value[1] = data

        if value is None or len(value) == 0:
            insert_query = "INSERT INTO {}(country_code, data, last_updated) VALUES (?, ?, ?)".format(table)
            self.cursor.execute(insert_query, (data[0], data[1], last_updated))
        else:
            v = value[1]
            if v != data[1]:
                update_query = "UPDATE {} SET data = ?, last_updated = ? WHERE country_code = ?".format(table)
                self.cursor.execute(update_query, (data[1], last_updated, data[0],))