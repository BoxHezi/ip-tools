from sqlalchemy import String, Integer, JSON, DateTime
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base

from Module.DatabaseDriver import Database
import Module.Utils as Utils


# REF: https://github.com/herrbischoff/country-ip-blocks


class CountryCidr(declarative_base()):
    __tablename__ = "country_cidr_info"
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())

    __IPv4_BASE_PATH = "./country-ip-blocks/ipv4/"
    __IPv6_BASE_PATH = "./country-ip-blocks/ipv6/"

    def __init__(self, country_code):
        self.country_code = country_code

    def read_content_and_cal_hash(self):
        file_suffix = ".cidr"
        result = {"country_code": self.country_code}
        ipv4_contents = Utils.read_file(self.__IPv4_BASE_PATH + self.country_code + file_suffix)
        ipv6_contents = Utils.read_file(self.__IPv6_BASE_PATH + self.country_code + file_suffix)
        ipv4_hashes = Utils.cal_hash(",".join(ipv4_contents).encode()) if ipv4_contents else None
        ipv6_hashes = Utils.cal_hash(",".join(ipv6_contents).encode()) if ipv6_contents else None
        result["ipv4_info"] = {"md5": ipv4_hashes[0], "sha256": ipv4_hashes[1]} if ipv4_hashes else None
        result["ipv6_info"] = {"md5": ipv6_hashes[0], "sha256": ipv6_hashes[1]} if ipv6_hashes else None
        return result


class CountryCidrDAO:
    def __init__(self, db: Database):
        self.db = db

    def add_record(self, git_repo: CountryCidr):
        session = self.db.get_session()
        session.add(git_repo)

    def update_record(self, new: CountryCidr):
        session = self.db.get_session()
        record = session.query(CountryCidr).filter(CountryCidr.country_code == new.country_code).all()[0]
        record.data = new.data
        record.last_updated = Utils.get_now_datetime()

    def get_record_by_country_code(self, country_code):
        session = self.db.get_session()
        record = session.query(CountryCidr).filter(CountryCidr.country_code == country_code).all()
        if len(record) == 0:
            print(f"No record matched for {country_code} founded")
        else:
            return record[0]

    def has_record_for_country_code(self, country_code):
        session = self.db.get_session()
        record = session.query(CountryCidr).filter(CountryCidr.country_code == country_code)
        return session.query(record.exists()).scalar()
