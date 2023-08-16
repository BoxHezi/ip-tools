#!/usr/local/bin/python3

import configparser
from Module.GitRepo import GitRepo
from Module.Cidr2Ip import CIDR2IP

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.conf")

    # repo = GitRepo(config["GITREPO"])
    # repo.check_update()
    # del repo
    # cidr2ip = CIDR2IP()

# TODO
# [x] 1. cidr to ip
# [ ] 2. ip to asn, ref: https://ipapi.is/developers.html
# [ ] 3. ip lookups, for open ports and vulnerabilities, ref: https://internetdb.shodan.io/
# [ ] 4. result to json, database, etc
