from Module.SqliteDriver import DB
import Module.Utils as Utils


class InternetDBDAO:

    def __init__(self, db: DB, ip: str | int, data=None):
        self.db = db
        if isinstance(ip, str):
            self.ip = Utils.ip_int(ip)
        else:
            self.ip = ip
        if data is not None:
            self.data = data
