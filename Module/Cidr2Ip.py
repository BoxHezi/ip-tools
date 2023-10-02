from tqdm import tqdm

from sqlalchemy import Integer, String, DateTime, PickleType
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base

from Module.DatabaseDriver import Database
import Module.utils as Utils


# REF: https://github.com/herrbischoff/country-ip-blocks


class Cidr2Ip(declarative_base()):
    __tablename__ = "cidr_ip_mapper"

    id = Column(Integer, primary_key=True)
    country_code = Column(String, nullable=False)
    data = Column(PickleType, nullable=False)  # pickled CIDR2IP instance
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())

    __IPv4_BASE_PATH = "./country-ip-blocks/ipv4/"
    __IPv6_BASE_PATH = "./country-ip-blocks/ipv6/"

    def __init__(self, country_code):
        self.country_code = country_code
        self.ipv4_cidrs = []
        self.ipv4_ip_dict = {}
        self.ipv6_cidrs = []
        self.ipv6_ip_dict = {}

    def read_cidr_file(self):
        ipv4_path = self.__IPv4_BASE_PATH + self.country_code + ".cidr"
        ipv6_path = self.__IPv6_BASE_PATH + self.country_code + ".cidr"

        try:
            with open(ipv4_path, "r") as reader:
                self.ipv4_cidrs = [line.strip() for line in reader]
            with open(ipv6_path, "r") as reader:
                self.ipv6_cidrs = [line.strip() for line in reader]
        except FileNotFoundError as e:
            print(f"File Not Found Error: {e}")

    def map_ipv4(self):
        print("Start parsing IPv4 CIDR for country {}...".format(self.country_code))
        for cidr in tqdm(self.ipv4_cidrs):
            self.ipv4_ip_dict[cidr] = Utils.cidr2ip(cidr)

    def map_ipv6(self):
        print("Start parsing IPv6 CIDR for country {}...".format(self.country_code))
        for cidr in tqdm(self.ipv6_cidrs):
            self.ipv6_ip_dict[cidr] = Utils.cidr2ip(cidr, True)


class Cidr2IpDAO:
    def __init__(self, db: Database):
        self.db = db

    def add_record(self, c2i: Cidr2Ip):
        c2i.data = Utils.compress(Utils.serialize(c2i))
        session = self.db.get_session()
        session.add(c2i)

    def update_record(self, new: Cidr2Ip):
        session = self.db.get_session()
        record = session.query(Cidr2Ip).filter(Cidr2Ip.country_code == new.country_code).all()[0]
        record.data = Utils.compress(Utils.serialize(new))
        record.last_updated = Utils.get_now_datetime()

    def get_record_by_country_code(self, country_code):
        session = self.db.get_session()
        record = session.query(Cidr2Ip).filter(Cidr2Ip.country_code == country_code).all()
        if len(record) == 0:
            print(f"No record matched for {country_code} founded")
        else:
            return record[0]

    def has_record_for_country_code(self, country_code):
        session = self.db.get_session()
        record = session.query(Cidr2Ip).filter(Cidr2Ip.country_code == country_code)
        return session.query(record.exists()).scalar()
