#!/usr/local/bin/python3

import configparser
import argparse

from Module.SqliteDriver import DB
from Module.GitRepo import GitRepo
from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler
import Module.Utils as Utils

from Services import DatabaseInitService, GitRepoService, Cidr2IpService


def init_argparse():
    arg = argparse.ArgumentParser(description="IP Tools", formatter_class=argparse.RawTextHelpFormatter)
    arg.add_argument("-g", "--git", help="Clone git repo to local or check git local repo update", action="store_true")
    arg.add_argument("-gf", help="Force to run git repo check", action="store_true")
    arg.add_argument("-c", "--country",
                     help="country code for CIDR to IP function\n"
                          "support multiple country code, separate by space, e.g. -c au us nz, default set to au\n"
                          "use -c- for all country",
                     nargs="*")
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


if __name__ == '__main__':
    args = init_argparse().parse_args()  # init argparse
    config = init_configparser()  # init configparse

    DatabaseInitService.init_db_table(config["DATABASE"])

    if args.git or args.gf:
        # git local repo initialization
        repo = GitRepo(config["GITREPO"])
        updated_country = repo.find_updated_files()
        GitRepoService.git_repo_to_database(repo, DB("./data.db"),
                                            Utils.get_all_country_code() if args.gf else updated_country)
        del repo

    if args.country is not None:
        country_list = []
        if args.country != ["-"]:  # parse all country's cidr to ip if args.country is ["-"]
            country_list = ["au"] if len(args.country) == 0 else args.country
        else:
            country_list = Utils.get_all_country_code()
        Cidr2IpService.cidr_to_ip_mapper(DB("./data.db"), country_list)

    if args.ip:
        for i in args.ip:
            print(Utils.ip_query(str(i)))

    if args.asn:
        for a in args.asn:
            print(Utils.asn_query(str(a)))

    if args.internetdb:
        for inet in args.internetdb:
            print(Utils.internet_db_query(str(inet)))
