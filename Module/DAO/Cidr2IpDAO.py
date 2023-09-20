import Module.Utils as Utils
import hashlib


class Cidr2IpData:
    __TABLE_NAME = "cidr_ip_mapper"

    def __init__(self, db, country_code, obj=None, last_updated=None):
        self.db = db
        self.country_code = country_code
        self.has_record = self.__conatin_record()
        if not obj:
            self.retrieve_data_by_country_code()
        else:
            self.cidr_to_ip_obj = obj
            self.last_updated = last_updated
            self.id = None

    def __repr__(self):
        return """Country code: {}\nHash of Obj: {}\nLast Updated: {}\n""".format(self.country_code,
                                                                                  hashlib.md5(
                                                                                      self.cidr_to_ip_obj).hexdigest(),
                                                                                  self.last_updated)

    def __conatin_record(self):
        query = "SELECT * FROM cidr_ip_mapper WHERE country_code = ?"
        self.db.cursor.execute(query, (self.country_code,))
        result = self.db.cursor.fetchone()
        return False if result is None or len(result) == 0 else True

    def has_update(self):
        # 1. query from database using country_code
        # 2. compare data in database with self
        # 3. return result

        # True if 1. no record 2. record has changes
        query = "SELECT * FROM cidr_ip_mapper WHERE country_code = ?"
        self.db.cursor.execute(query, (self.country_code,))
        result = self.db.cursor.fetchone()
        if result is not None:
            data_in_db = result[2]
            if Utils.compare_obj(self.cidr_to_ip_obj, data_in_db):
                return False
        return True

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

    def insert_into_db(self):
        query = "INSERT INTO cidr_ip_mapper(country_code, cidr_to_ip_obj, last_updated) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (self.country_code, self.cidr_to_ip_obj, Utils.get_current_time()))

    def update_db(self):
        query = "UPDATE cidr_ip_mapper SET cidr_to_ip_obj = ?, last_updated = ? WHERE country_code = ?"
        self.db.cursor.execute(query, (self.cidr_to_ip_obj, Utils.get_current_time(), self.country_code))
