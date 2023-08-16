#!/usr/local/bin/python3

import ipaddress
import os
from tqdm import tqdm

from Module.GitRepo import GitRepo

BASE_PATH = "./country-ip-blocks/ipv4/"


class CIDR2IP:
    IP4_BASE_PATH = "./country-ip-blocks/ipv4"
    IP6_BASE_PATH = "./country-ip-blocks/ipv6"

    def __init__(self):
        print(os.path.exists(self.IP4_BASE_PATH))


def check_ipv4(code):
    path = BASE_PATH + code + ".cidr"
    cidrs = {}
    with open(path, "r") as reader:
        print("Start parsing IPv4 cidr for country code {}...".format(code.replace(".cidr", "").capitalize()))
        lines = [line.strip() for line in reader]
        for cidr in tqdm(lines):
            cidrs[cidr] = [str(ip) for ip in ipaddress.IPv4Network(cidr)]

    return cidrs


def check_ipv6(code):
    path = BASE_PATH + code + ".cidr"
    cidrs = {}
    with open(path, "r") as reader:
        print("Start parsing IPv6 cidr for country code {}...".format(code.replace(".cidr", "").capitalize()))
        lines = [line.strip() for line in reader]
        for cidr in tqdm(lines):
            cidrs[cidr] = [str(ip) for ip in ipaddress.IPv6Network(cidr)]

    return cidrs


def main():
    pass


if __name__ == "__main__":
    main()
