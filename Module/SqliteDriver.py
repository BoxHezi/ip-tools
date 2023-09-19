import sqlite3
import Module.Utils as Utils


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

    def begin_transaction(self):
        self.connection.execute("BEGIN;")

    def perform_commit(self):
        self.connection.commit()

    def perform_rollback(self):
        self.connection.rollback()

    # def check_existence(self, table: str, country_code: str):
    #     """
    #     check if a table has given country_code, to determine if database include the data of given country_code
    #     :param table:  the table to search
    #     :param country_code:  the specific country_code to look for
    #     :return:  True if given country_code exists, False otherwise
    #     """
    #     query = "SELECT COUNT(*) FROM {} WHERE country_code = ?".format(table)
    #     self.cursor.execute(query, (country_code,))
    #     result = self.cursor.fetchone()
    #     return result[0] != 0

    # def update_cidr_ip_mapper(self, newly_created_cidr2ip, *data):
    #     """
    #     :param newly_created_cidr2ip:  the newly created cidr2ip instance on runtime
    #     :param data: data[0]: country_code, data[1]: serialized and compressed object
    #     :return:  True if data is updated or new data is inserted, False otherwise
    #     """
    #     table_name = "cidr_ip_mapper"
    #     if not self.check_existence(table_name, data[0]):
    #         insert_query = "INSERT INTO cidr_ip_mapper(country_code, cidr_to_ip_obj) VALUES (?, ?)"
    #         self.cursor.execute(insert_query, (data[0], data[1]))
    #         return True
    #     else:
    #         search_query = "SELECT country_code, cidr_to_ip_obj FROM cidr_ip_mapper WHERE country_code = ?"
    #         self.cursor.execute(search_query, (data[0],))
    #         result = self.cursor.fetchone()

    #         if Utils.compare_obj(Utils.compress(Utils.serialize(newly_created_cidr2ip)), result[1]):
    #             print("No cidr and/or ip addresses change for country {}".format(data[0]))
    #             return False
    #         update_query = "UPDATE cidr_ip_mapper SET cidr_to_ip_obj = ?, last_updated = ? WHERE country_code = ?"
    #         self.cursor.execute(update_query, (data[1], Utils.get_current_time(), data[0],))
    #         return True
