#!/usr/local/bin/python3

import configparser
import argparse

from Module.GitRepo import GitRepo
from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler
import Module.Utils as Utils


def init_argparse():
    arg = argparse.ArgumentParser(description="IP Tools", formatter_class=argparse.RawTextHelpFormatter)
    arg.add_argument("-g", "--git", help="Clone git repo to local or check git local repo update", action="store_true")
    arg.add_argument("-c", "--country",
                     help="country code for CIDR to IP function\n"
                          "when providing country code, CIDR to IP function will be enabled\n"
                          "support multiple country code, separate by space, e.g. -c au us nz, default set to au\n"
                          "use -c- for all country",
                     nargs="*")
    # arg.add_argument("-i4", "--ipv4",
    #                  help="Enable CIDR to IP for ipv4 addresses, enabled by default",
    #                  action="store_true", default=True)
    arg.add_argument("-t6",
                     help="Enable CIDR to IP for ipv6 addresses, disabled by default",
                     action="store_true", default=False)
    arg.add_argument("-i", "--ip", help="Query ip information, using API from ipapi.is\n"
                                        "support multiple ip, separate using space, e.g. -i 8.8.8.8 51.83.59.99",
                     nargs="+")
    arg.add_argument("-a", "--asn", help="Query ASN information, using API from ipapi.is\n"
                                         "provide ASN without the prefix 'as'\n"
                                         "support multiple ASN query, separate using space, e.g. -a 23500 23501 23501",
                     nargs="+")
    arg.add_argument("-inet", "--internetdb", help="Query information from https://internetdb.shodan.io/\n"
                                                   "support multiple ip, separate using space, e.g. -inet 8.8.8.8 "
                                                   "51.83.59.99",
                     nargs="+")
    return arg


def init_configparser(conf_path: str = "config.conf"):
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    return conf


def map_cidr_to_ip(countries, ipv6: bool = False):
    cidr2ip_handler = Cidr2ipHandler()
    for country in countries:
        temp = CIDR2IP(country)
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6()
        cidr2ip_handler.add_record(country, temp)
        if temp.store_data(Utils.compress(Utils.serialize(temp))):
            cidr2ip_handler.add_updated_record(temp)

    if len(cidr2ip_handler.updated_list) != 0:
        print("Update detected for the following country(s):")
        for c in cidr2ip_handler.updated_list:
            print(c.country_code)
    return cidr2ip_handler


if __name__ == '__main__':
    args = init_argparse().parse_args()  # init argparse
    config = init_configparser()  # init configparse

    if args.git:
        # git local repo initialization
        repo = GitRepo(config["GITREPO"])
        # repo.check_updated_file()
        if repo.has_update():
            updated_country = repo.check_updated_file()
            print(updated_country)
        del repo

    if args.country is not None:
        country_list = []
        if args.country != ["-"]:  # parse all country's cidr to ip if args.country is ["-"]
            country_list = ["au"] if len(args.country) == 0 else args.country
        else:
            country_list = Utils.get_all_country_code()
        cidr_to_ip_handler = map_cidr_to_ip(country_list)

    if args.ip:
        for i in args.ip:
            print(Utils.ip_query(str(i)))

    if args.asn:
        for a in args.asn:
            print(Utils.asn_query(str(a)))

    if args.internetdb:
        for inet in args.internetdb:
            print(Utils.internet_db_query(str(inet)))
