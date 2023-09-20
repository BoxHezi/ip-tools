from Module.SqliteDriver import DB
import Module.Utils as Utils


class InternetDBDAO:

    def __init__(self, db: DB, ip_str: str, data: dict):
        self.db = db
        self.ip = Utils.ip_int(ip_str)
        self.ip_str = ip_str
        self.hostnames = data["hostnames"]
        self.ports = data["ports"]
        self.cpes = data["cpes"]
        self.vulns = data["vulns"]
        self.tags = data["tags"]
        self.last_updated = None

    def __repr__(self):
        out = f"IP: {Utils.ip_str(self.ip)} "
        out += f"Hostnames: {'[]' if len(self.hostnames) == 0 else ','.join(self.hostnames)}\n"
        out += f"Open ports: {'[]' if len(self.ports) == 0 else ','.join(str(p) for p in self.ports)}\n"
        out += f"CPEs: {'[]' if len(self.cpes) == 0 else ','.join(self.cpes)}\n"
        out += f"Vulns: {'[]' if len(self.vulns) == 0 else ','.join(self.vulns)}\n"
        out += f"Tags: {'[]' if len(self.tags) == 0 else ','.join(self.tags)}\n"
        return out

    def has_record(self):
        """
        check if database contains entry for the IP address
        :return: True when has record, False otherwise
        """
        query = "SELECT * FROM internetdb WHERE ip = ?"
        self.db.cursor.execute(query, (self.ip,))
        result = self.db.cursor.fetchone()
        return False if result is None or len(result) == 0 else True

    def insert_into_db(self):
        query = "INSERT INTO internetdb(ip, ip_str, hostnames, ports, cpes, vulns, tags) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.db.cursor.execute(query, (
            self.ip, self.ip_str, Utils.list_2_str(self.hostnames), Utils.list_2_str(self.ports),
            Utils.list_2_str(self.cpes), Utils.list_2_str(self.vulns), Utils.list_2_str(self.tags),))
        self.db.perform_commit()

    def update_db(self):
        query = """UPDATE internetdb SET hostnames = ?, ports = ?, cpes = ?, vulns = ?, tags = ?, last_updated = ? 
                WHERE ip = ?"""
        self.db.cursor.execute(query, (
            Utils.list_2_str(self.hostnames), Utils.list_2_str(self.ports), Utils.list_2_str(self.cpes),
            Utils.list_2_str(self.vulns), Utils.list_2_str(self.tags), Utils.get_current_time(), self.ip,))
        self.db.perform_commit()
