import Module.Utils as Utils


class Cidr2IpData:
    __TABLE_NAME = "cidr_ip_mapper"

    def __init__(self, db, country_code, obj=None, last_updated=None):
        self.db = db
        self.country_code = country_code
        self.has_record = False
        if not obj:
            self.retrieve_data_by_country_code()
        else:
            self.cidr_to_ip_obj = obj
            self.last_updated = last_updated
            self.id = None

    def __repr__(self):
        return """Country code: {}\nSize of Obj: {} bytes\nLast Updated: {}\n""".format(self.country_code,
                                                                                        len(self.cidr_to_ip_obj) / 1024,
                                                                                        self.last_updated)

    def retrieve_data_by_country_code(self):
        query = "SELECT * FROM cidr_ip_mapper WHERE country_code = ?"
        self.db.cursor.execute(query, (self.country_code,))
        result = self.db.cursor.fetchone()
        if result is not None:
            self.id = result[0]
            self.cidr_to_ip_obj = result[2]
            self.last_updated = result[3]
            self.has_record = True
        else:
            self.id, self.cidr_to_ip_obj, self.last_updated = None, None, None

    def insert_into_db(self):
        query = "INSERT INTO cidr_ip_mapper(country_code, cidr_to_ip_obj, last_updated) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (self.country_code, self.cidr_to_ip_obj, Utils.get_current_time()))

    def update_db(self):
        query = "UPDATE cidr_ip_mapper SET cidr_to_ip_obj = ?, last_updated = ? WHERE country_code = ?"
        self.db.cursor.execute(query, (self.cidr_to_ip_obj, Utils.get_current_time(), self.country_code))
