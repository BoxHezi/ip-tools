import Module.Utils as Utils
from Module.SqliteDriver import DB


class BaseDAO:
    def __init__(self, db: DB):
        self.db = db

    def __del__(self):
        self.db.connection.close()

    def __repr__(self):
        return "Database connection: {}".format(self.db)


class GitRepoData(BaseDAO):
    __TABLE_NAME = "cidr_git_repo"

    def __init__(self, db: DB, country_code, data=None, last_updated=None):
        super().__init__(db)
        self.country_code = country_code
        self.has_record = False
        if not data:
            self.retrieve_data_by_country_code()
        else:
            self.data = data
            self.last_updated = last_updated
            self.id = None

    def __repr__(self):
        display = """Country Code: {}\nHash Info: {}\nLast Updated: {}\n""".format(self.country_code, self.data,
                                                                                   self.last_updated)
        display += "=" * 20
        return display

    def retrieve_data_by_country_code(self):
        query = "SELECT * FROM cidr_git_repo WHERE country_code = ?"
        self.db.cursor.execute(query, (self.country_code,))
        result = self.db.cursor.fetchone()
        if result is not None:
            self.id = result[0]
            self.data = Utils.to_json(result[2])  # str to dict (json)
            self.last_updated = result[3]
            self.has_record = True
        else:
            self.id, self.data, self.last_updated = None, None, None

    def insert_into_db(self):
        query = "INSERT INTO cidr_git_repo(country_code, data, last_updated) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (self.country_code, Utils.to_str(self.data), Utils.get_current_time(),))

    def update_db(self):
        query = "UPDATE cidr_git_repo SET data = ?, last_updated = ? WHERE country_code = ?"
        self.db.cursor.execute(query, (Utils.to_str(self.data), Utils.get_current_time(), self.country_code,))

    def has_update(self, data):
        return self.data != data


class Cidr2IpData(BaseDAO):
    __TABLE_NAME = "cidr_ip_mapper"

    def __init__(self, db: DB, country_code, obj=None, last_updated=None):
        super().__init__(db)
        self.country_code = country_code
        if not obj:
            self.retrieve_data_by_country_code()
        else:
            self.cidr_to_ip_obj = obj
            self.last_updated = last_updated
            self.id = None

    def retrieve_data_by_country_code(self):
        query = "SELECT * FROM cidr_ip_mapper WHERE country_code = ?"
        self.db.cursor.execute(query, (self.country_code,))
        result = self.db.cursor.fetchone()
        if result is not None:
            self.id = result[0]
            self.cidr_to_ip_obj = result[2]
            self.last_updated = result[3]
        else:
            self.id, self.cidr_to_ip_obj, self.last_updated = None, None, None
