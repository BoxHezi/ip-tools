from Module.DAO.Cidr2IpDAO import Cidr2IpData
from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler

import Module.Utils as Utils


def dao_2_obj(dao: Cidr2IpData) -> CIDR2IP:
    # TODO: convert Cidr2IpData to CIDR2IP object
    pass


def obj_2_dao(cidr2ip) -> Cidr2IpData:
    # TODO: convert CIDR2IP instance to Cidr2IpData in order to store in database
    pass


def cidr_2_ip_to_database(db, cidr2ip_obj: CIDR2IP):
    # TODO: insert/update cidr2ip_obj to database
    return True


def cidr_to_ip_mapper(countries: list, ipv6: bool = False):
    cidr2ip_handler = Cidr2ipHandler()
    for country in countries:
        temp = CIDR2IP(country)
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6()
        cidr2ip_handler.add_record(country, temp)
        # TODO: add data to database
        has_update = cidr_2_ip_to_database(None, temp)
        if has_update:
            # TODO: add to cidr2ip_handler.updated_list
            cidr2ip_handler.add_updated_record(temp)
            pass
