import sqlalchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from Module.DatabaseDriver import Database
import Module.Utils as Utils


class InternetDB(declarative_base()):
    __tablename__ = "internetdb"
    ip = Column(Integer, primary_key=True, index=True)
    ip_str = Column(String, nullable=False)
    hostnames = Column(String)
    ports = Column(String)
    cpes = Column(String)
    vulns = Column(String)
    tags = Column(String)
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())

    def __init__(self, data):
        self.ip = Utils.ip_int(data["ip"])
        self.ip_str = data["ip"]
        self.hostnames = Utils.list_2_str(data["hostnames"])
        self.ports = Utils.list_2_str(data["ports"])
        self.cpes = Utils.list_2_str(data["cpes"])
        self.vulns = Utils.list_2_str(data["vulns"])
        self.tags = Utils.list_2_str(data["tags"])

    def __repr__(self):
        out = f"IP: {self.ip_str}\n"
        out += f"Hostnames: {self.hostnames}\n"
        out += f"Ports: {self.ports}\n"
        out += f"vulns: {self.vulns}\n"
        return out


class InternetDBDAO:
    def __init__(self, db: Database):
        self.db = db

    def add_record(self, record: InternetDB):
        session = self.db.get_session()
        session.add(record)

    def update_record(self, new: InternetDB):
        session = self.db.get_session()
        record = session.query(InternetDB).filter(InternetDB.ip == new.ip).all()[0]
        record.hostnames = new.hostnames
        record.ports = new.ports
        record.cpes = new.cpes
        record.vulns = new.vulns
        record.tags = new.tags
        record.last_updated = Utils.get_now_datetime()

    def get_record_by_ip(self, ip: int | str):
        if isinstance(ip, str):
            ip = Utils.ip_int(ip)
        session = self.db.get_session()
        record = session.query(InternetDB).filter(InternetDB.ip == ip).all()
        if len(record) == 0:
            print(f"No record matched for {Utils.ip_str(ip)} founded")
        else:
            return record[0]

    def has_record_for_ip(self, ip: int | str):
        if isinstance(ip, str):
            ip = Utils.ip_int(ip)
        session = self.db.get_session()
        record = session.query(InternetDB).filter(InternetDB.ip == ip)
        return session.query(record.exists()).scalar()
