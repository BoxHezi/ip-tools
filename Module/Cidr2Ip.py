from tqdm import tqdm

from sqlalchemy import Integer, String, DateTime, PickleType
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base

from Module.Utils import cidr2ip
import Module.Utils as Utils

from Module.DatabaseDriver import Database

# REF: https://github.com/herrbischoff/country-ip-blocks

# BASE_PATH = "./country-ip-blocks/ipv4/"

# Base = declarative_base()

# class Cidr2IpDAO(Base):
#     __tablename__ = "cidr_ip_mapper"

#     id = Column(Integer, primary_key=True)
#     country_code = Column(String, nullable=False)
#     data = Column(PickleType, nullable=False)  # pickled CIDR2IP instance
#     last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())

#     def __init__(self, country_code, data):
#         self.country_code = country_code
#         self.data = data
#         self.last_updated = Utils.get_now_datetime()


# def init(db_name: str, echo: bool = True):
#     db_name = "sqlite:///" + db_name
#     engine = create_engine(db_name, echo=echo)
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     return Session()


# def session_commit(session: sqlalchemy.orm.session.Session):
#     session.commit()


# def session_close(session: sqlalchemy.orm.session.Session):
#     session.close()


# def is_record_exists(session, country_code: str):
#     record = session.query(Cidr2IpDAO).filter(Cidr2IpDAO.country_code == country_code)
#     return session.query(record.exists()).scalar()


# def add_record(session, obj: Cidr2IpDAO):
#     session.add(obj)


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
            self.ipv4_ip_dict[cidr] = cidr2ip(cidr)

    def map_ipv6(self):
        print("Start parsing IPv6 CIDR for country {}...".format(self.country_code))
        for cidr in tqdm(self.ipv6_cidrs):
            self.ipv6_ip_dict[cidr] = cidr2ip(cidr, True)


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
        #     self.c2i = record[0]
        # return self.c2i

    def has_record_for_country_code(self, country_code):
        session = self.db.get_session()
        record = session.query(Cidr2Ip).filter(Cidr2Ip.country_code == country_code)
        return session.query(record.exists()).scalar()


# class CIDR2IP:
#     __IPv4_BASE_PATH = "./country-ip-blocks/ipv4/"
#     __IPv6_BASE_PATH = "./country-ip-blocks/ipv6/"

#     def __init__(self, country_code):
#         """
#         :param country_code: country code to get cidr file, default set to au
#         """
#         self.country_code = country_code
#         self.ipv4_cidrs = []
#         self.ipv4_ip_dict = {}
#         self.ipv6_cidrs = []
#         self.ipv6_ip_dict = {}
#         self.read_cidr_file()

#     def read_cidr_file(self):
#         ipv4_path = self.__IPv4_BASE_PATH + self.country_code + ".cidr"
#         ipv6_path = self.__IPv6_BASE_PATH + self.country_code + ".cidr"
#         try:
#             with open(ipv4_path, "r") as reader:
#                 self.ipv4_cidrs = [line.strip() for line in reader]
#         except FileNotFoundError as e:
#             print(e)

#         try:
#             with open(ipv6_path, "r") as reader:
#                 self.ipv6_cidrs = [line.strip() for line in reader]
#         except FileNotFoundError as e:
#             print(e)

#     def map_ipv4(self):
#         print("Start parsing IPv4 CIDR for country {}...".format(self.country_code))
#         for cidr in tqdm(self.ipv4_cidrs):
#             self.ipv4_ip_dict[cidr] = cidr2ip(cidr)

#     def map_ipv6(self):
#         print("Start parsing IPv6 CIDR for country {}...".format(self.country_code))
#         for cidr in tqdm(self.ipv6_cidrs):
#             self.ipv6_ip_dict[cidr] = cidr2ip(cidr, True)


# class Cidr2ipHandler:

#     def __init__(self):
#         self.cidr2ips = {}
#         self.updated_list: list[CIDR2IP] = []

#     def add_record(self, country_code, record: CIDR2IP):
#         self.cidr2ips[country_code] = record

#     def get_all_record(self):
#         return self.cidr2ips

#     def get_record_by_country_code(self, country_code):
#         return self.cidr2ips[country_code]

#     def add_updated_record(self, record: CIDR2IP):
#         self.updated_list.append(record)

#     def clear_updated_list(self):
#         self.updated_list = []
