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

    def create_table(self, table_name, definition):
        query = "CREATE TABLE {} ({});".format(table_name, definition)
        self.cursor.execute(query)

    def check_existence(self, table: str, country_code: str):
        """
        check if a table has given country_code, to determine if database include the data of given country_code
        :param table:  the table to search
        :param country_code:  the specific country_code to look for
        :return:  True if given country_code exists, False otherwise
        """
        query = "SELECT COUNT(*) FROM {} WHERE country_code = ?".format(table)
        self.cursor.execute(query, (country_code,))
        result = self.cursor.fetchone()
        return result[0] != 0

    def update_cidr_git_repo(self, *data: str):
        """
        :param data:  data to be inserted to, data[0] country_code, data[1] data
        """
        select_query = "SELECT country_code, data FROM cidr_git_repo WHERE country_code = ?"
        self.cursor.execute(select_query, (data[0],))
        value = self.cursor.fetchone()  # if not None, value[0] = country_code, value[1] = data

        if value is None or len(value) == 0:
            insert_query = "INSERT INTO cidr_git_repo(country_code, data, last_updated) VALUES (?, ?, ?)"
            self.cursor.execute(insert_query, (data[0], data[1], Utils.get_current_time()))
            return True
        else:
            v = value[1]
            if v != data[1]:
                update_query = "UPDATE cidr_git_repo SET data = ?, last_updated = ? WHERE country_code = ?"
                self.cursor.execute(update_query, (data[1], Utils.get_current_time(), data[0],))
                return True
            return False

    def update_cidr_ip_mapper(self, newly_created_cidr2ip, *data):
        """
        :param newly_created_cidr2ip:  the newly created cidr2ip instance on runtime
        :param data: data[0]: country_code, data[1]: serialized and compressed object
        :return:  True if data is updated or new data is inserted, False otherwise
        """
        table_name = "cidr_ip_mapper"
        if not self.check_existence(table_name, data[0]):
            insert_query = "INSERT INTO cidr_ip_mapper(country_code, cidr_to_ip_obj) VALUES (?, ?)"
            self.cursor.execute(insert_query, (data[0], data[1]))
            return True
        else:
            search_query = "SELECT country_code, cidr_to_ip_obj FROM cidr_ip_mapper WHERE country_code = ?"
            self.cursor.execute(search_query, (data[0],))
            result = self.cursor.fetchone()
            # print(Utils.cal_hash(Utils.compress(Utils.serialize(new_calculated_data))))
            # print(Utils.cal_hash(result[1]))
            # print(Utils.deserialize(Utils.decompress(cidr2ip_obj_from_db)))
            # print(new_calculated_data)

            # using cal_hash to compare, since the newly created CIDR2IP instance and data from db have
            # different reference even if they hold exact the same value
            if Utils.compare_obj(Utils.compress(Utils.serialize(newly_created_cidr2ip)), result[1]):
                print("No cidr and/or ip addresses change for country {}".format(data[0]))
                return False
            update_query = "UPDATE cidr_ip_mapper SET cidr_to_ip_obj = ?, last_updated = ? WHERE country_code = ?"
            self.cursor.execute(update_query, (data[1], Utils.get_current_time(), data[0],))
            return True
