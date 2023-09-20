#!/usr/local/bin/python3
from tqdm import tqdm

from Module.Utils import cidr2ip

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
        print("Start parsing IPv4 CIDR for country {}...".format(self.country_code))
        for cidr in tqdm(self.ipv4_cidrs):
            self.ipv4_ip_dict[cidr] = cidr2ip(cidr)

    def map_ipv6(self):
        print("Start parsing IPv6 CIDR for country {}...".format(self.country_code))
        for cidr in tqdm(self.ipv6_cidrs):
            self.ipv6_ip_dict[cidr] = cidr2ip(cidr, True)


class Cidr2ipHandler:

    def __init__(self):
        self.cidr2ips = {}
        self.updated_list: list[CIDR2IP] = []

    def add_record(self, country_code, record: CIDR2IP):
        self.cidr2ips[country_code] = record

    def get_all_record(self):
        return self.cidr2ips

    def get_record_by_country_code(self, country_code):
        return self.cidr2ips[country_code]

    def add_updated_record(self, record: CIDR2IP):
        self.updated_list.append(record)

    def clear_updated_list(self):
        self.updated_list = []
