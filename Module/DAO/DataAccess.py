from Module.SqliteDriver import DB
import Module.Utils as Utils


class GitRepoData(DB):
    __TABLE_NAME = "cidr_git_repo"

    def __init__(self, db_path, country_code, data=None, last_updated=None):
        super().__init__(db_path)
        self.country_code = country_code
        self.data = data
        self.last_updated = last_updated
        self.id = None

    def __repr__(self):
        display = """Country Code: {}\nHash Info: {}\nLast Updated: {}\n""".format(self.country_code, self.data,
                                                                                   self.last_updated)
        display += "=" * 20
        return display

    def __del__(self):
        self.connection.close()

    def retrieve_data_by_country_code(self):
        query = "SELECT * FROM cidr_git_repo WHERE country_code = ?"
        self.cursor.execute(query, (self.country_code,))
        result = self.cursor.fetchone()
        if result is not None:
            self.id = result[0]
            self.data = result[2]
            self.last_updated = result[3]

    def insert_into_db(self):
        query = "INSERT INTO cidr_git_repo(country_code, data, last_updated) VALUES (?, ?, ?)"
        self.cursor.execute(query, (self.country_code, self.data, Utils.get_current_time(),))

    def update_db(self):
        query = "UPDATE cidr_git_repo SET data = ?, last_updated = ? WHERE country_code = ?"
        self.cursor.execute(query, (self.data, Utils.get_current_time(), self.country_code,))

    def has_update(self, data):
        return self.data == data
