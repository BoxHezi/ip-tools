#!/usr/local/bin/python3
import ipaddress
from tqdm import tqdm

from Module.SqliteDriver import DB

# REF: https://github.com/herrbischoff/country-ip-blocks

BASE_PATH = "./country-ip-blocks/ipv4/"


class CIDR2IP:
    __IPv4_BASE_PATH = "./country-ip-blocks/ipv4/"
    __IPv6_BASE_PATH = "./country-ip-blocks/ipv6/"

    def __init__(self, country_code):
        """
        :param country_code: country code to get cidr file, default set to au
        """
        self.country_code = country_code
        self.ipv4_cidrs = []
        self.ipv4_ip_dict = {}
        self.ipv6_cidrs = []
        self.ipv6_ip_dict = {}
        self.read_cidr_file()

    def read_cidr_file(self):
        ipv4_path = self.__IPv4_BASE_PATH + self.country_code + ".cidr"
        ipv6_path = self.__IPv6_BASE_PATH + self.country_code + ".cidr"
        try:
            with open(ipv4_path, "r") as reader:
                self.ipv4_cidrs = [line.strip() for line in reader]
        except FileNotFoundError as e:
            print(e)

        try:
            with open(ipv6_path, "r") as reader:
                self.ipv6_cidrs = [line.strip() for line in reader]
        except FileNotFoundError as e:
            print(e)

    def map_ipv4(self):
        print("Start parsing IPv4 CIDR for country {}...".format(self.country_code.capitalize()))
        for cidr in tqdm(self.ipv4_cidrs):
            self.ipv4_ip_dict[cidr] = [str(ip) for ip in ipaddress.IPv4Network(cidr)]

    def map_ipv6(self):
        print("Start parsing IPv6 CIDR for country {}...".format(self.country_code.capitalize()))
        for cidr in tqdm(self.ipv6_cidrs):
            self.ipv4_ip_dict[cidr] = [str(ip) for ip in ipaddress.IPv6Network(cidr)]

    def store_data(self, data):
        print("Check database database for country {}".format(self.country_code.capitalize()))
        db = DB("./data.db")
        # TODO: check if there is database entry for corresponding country_code
        if not db.check_existence("cidr_ip_mapper", self.country_code):
            # TODO: insert data to database
            pass

        # if not db.check_table_existence(self.country_code):
        #     definition = """
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     cidr_to_ip_obj BLOB,
        #     last_updated INTEGER DEFAULT (datetime('now', 'localtime'))"""
        #     db.create_table(self.country_code, definition)  # create table
        # else:
        #     pass
