#!/usr/local/bin/python3

import configparser
import argparse
from Module.GitRepo import GitRepo
from Module.Cidr2Ip import CIDR2IP
import Module.IPUtils as IPUtils


def init_argparse():
    arg = argparse.ArgumentParser(description="IP Tools", formatter_class=argparse.RawTextHelpFormatter)
    arg.add_argument("-g", "--git", help="Clone git repo to local or check git local repo update", action="store_true")
    arg.add_argument("-c", "--country",
                     help="country code for CIDR to IP function\n"
                          "support multiple country code, separate by space, e.g. -c au us nz, default set to au\n"
                          "when providing country code, CIDR to IP function will be enabled",
                     nargs="*")
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = init_argparse().parse_args()  # init argparse
    config = init_configparser()  # init configparse

    if args.git:
        # git local repo initialization
        repo = GitRepo(config["GITREPO"])
        repo.check_update()
        del repo

    if args.country is not None:
        country_list = ["au"] if len(args.country) == 0 else args.country
        # create CIDR2IP instance
        cidr2ip_handler = {}
        for c in country_list:
            cidr2ip = CIDR2IP(c)
            cidr2ip_handler[cidr2ip.country_code] = cidr2ip

    if args.ip:
        for i in args.ip:
            print(IPUtils.ip_query(str(i)))

    if args.asn:
        for a in args.asn:
            print(IPUtils.asn_query(str(a)))

    if args.internetdb:
        for inet in args.internetdb:
            print(IPUtils.internet_db_query(str(inet)))
