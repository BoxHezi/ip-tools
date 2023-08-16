#!/usr/local/bin/python3

import ipaddress
from tqdm import tqdm
from Module.GitRepo import GitRepo

# REF: https://github.com/herrbischoff/country-ip-blocks

BASE_PATH = "./country-ip-blocks/ipv4/"


class CIDR2IP:
    IP4_BASE_PATH = "./country-ip-blocks/ipv4/"
    IP6_BASE_PATH = "./country-ip-blocks/ipv6/"

    def __init__(self, country_code: str = "au"):
        """
        :param country_code: country code to get cidr file, default set to au
        """
        self.country_code = country_code
        self.ipv4_cidrs = []
        self.ipv4_ip_dict = {}
        self.ipv6_cidrs = []
        self.ipv6_ip_dict = {}

    def check_ipv4(self):
        path = self.IP4_BASE_PATH + self.country_code + ".cidr"
        with open(path, "r") as reader:
            print("Start parsing IPv4 CIDR for country {}...".format(self.country_code.capitalize()))
            self.ipv4_cidrs = [line.strip() for line in reader]
            for cidr in tqdm(self.ipv4_cidrs):
                self.ipv4_ip_dict[cidr] = [str(ip) for ip in ipaddress.IPv4Network(cidr)]

    def check_ip6(self):
        path = self.IP6_BASE_PATH + self.country_code + ".cidr"
        with open(path, "r") as reader:
            print("Start parsing IPv6 CIDR for country {}...".format(self.country_code.capitalize()))
            self.ipv6_cidrs = [line.strip() for line in reader]
            for cidr in tqdm(self.ipv6_cidrs):
                self.ipv6_ip_dict[cidr] = [str(ip) for ip in ipaddress.IPv6Network(cidr)]
