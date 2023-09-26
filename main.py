#!/usr/local/bin/python3

import configparser
import argparse

from Module.SqliteDriver import DB
from Module.GitRepo import GitRepo
import Module.Utils as Utils

from Services import CVEService, DatabaseInitService, GitRepoService, Cidr2IpService, InternetDBService


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
                                                   "support multiple ip and cidr, separate using space, "
                                                   ":e.g. -inet 8.8.8.8 51.83.59.99 192.168.0.0/24\n"
                                                   "if no database if specified, use ./databases/internetdb.db",
                     nargs="+")
    arg.add_argument("-cve", "--cve", help="get cve information from database\n"
                                           "require to use -db for specificing a database",
                                    action="store_true")
    arg.add_argument("-db", "--database", help="Specify database will be used to stored/retrieve data")
    arg.add_argument("--downloaddb", help="download CAPEC and CWE databaes, csv file, store in ./databases directory", action="store_true")
    return arg


def init_configparser(conf_path: str = "config.conf"):
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    return conf


if __name__ == '__main__':
    args = init_argparse().parse_args()  # init argparse
    config = init_configparser()  # init configparse

    # DatabaseInitService.init_db_table(config["DATABASE"])

    if args.git or args.gf:
        # git local repo initialization
        repo = GitRepo(config["GITREPO"])
        GitRepoService.start(args.database, repo, Utils.get_all_country_code() if args.gf else repo.find_updated_files())


    if args.country is not None:
        country_list = []
        if args.country != ["-"]:  # parse all country's cidr to ip if args.country is ["-"]
            country_list = ["au"] if len(args.country) == 0 else args.country
        else:
            country_list = Utils.get_all_country_code()
        Cidr2IpService.cidr_to_ip_mapper(DB(config["DATABASE"]), country_list)

    if args.ip:
        for i in args.ip:
            print(Utils.ip_query(str(i)))

    if args.asn:
        for a in args.asn:
            print(Utils.asn_query(str(a)))

    if args.internetdb:  # type(internetdb) => list
        db = "./databases/internetdb.db"
        if args.database:
            db = args.database
        print(f"Data will be stored into database: {db}")
        InternetDBService.start_query(db, args.internetdb)

    if args.downloaddb:
        CVEService.download_local_db()

    if args.cve:
        if not args.database:
            raise("Database required")
        db = args.database
        targets = CVEService.start_cve_search(DB(db))
        print(targets)

    # if args.cpe:
    #     print(args.cpe)
