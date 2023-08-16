#!/usr/local/bin/python3

import configparser
import argparse
from Module.GitRepo import GitRepo
from Module.Cidr2Ip import CIDR2IP
import Module.IPUtils as IPUtils


def init_argparse():
    arg = argparse.ArgumentParser(description="IP Tools", formatter_class=argparse.RawTextHelpFormatter)
    arg.add_argument("-g", "--git", help="Clone git repo to local or check git local repo update", action="store_true")
    arg.add_argument("-c2i", help="CIDR to IP function", action="store_true")
    arg.add_argument("-c", "--country",
                     help="country code for CIDR to IP function\n"
                          "support multiple country code, separate by space, e.g. -c au us nz, default set to au\n"
                          "when providing country code, CIDR to IP function will be enabled",
                     nargs="+")
    return arg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = init_argparse()
    args = args.parse_args()
    if args.country:
        # enable CIDR to IP function
        args.c2i = True

    config = configparser.ConfigParser()
    config.read("config.conf")

    if args.git:
        # git local repo initialization
        repo = GitRepo(config["GITREPO"])
        repo.check_update()
        del repo

    if args.c2i:
        # create CIDR2IP instance
        cidr2ip_handler = {}
        if args.country:
            for c in args.country:
                cidr2ip = CIDR2IP(c)
                cidr2ip_handler[cidr2ip.country_code] = cidr2ip
        else:
            cidr2ip = CIDR2IP()
            cidr2ip_handler[cidr2ip.country_code] = cidr2ip

    # print(IPUtils.ip_query("51.83.59.99"))
    # print(IPUtils.asn_query("50673"))
    # print(IPUtils.internet_db_query("116.240.173.168"))
