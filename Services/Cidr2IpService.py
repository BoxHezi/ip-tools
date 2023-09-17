from Module.DAO.Cidr2IpDAO import Cidr2IpData
from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler
from Module.SqliteDriver import DB

import Module.Utils as Utils


def dao_2_obj(dao: Cidr2IpData) -> CIDR2IP:
    # TODO: convert Cidr2IpData to CIDR2IP object
    pass


def obj_2_dao(db: DB, cidr2ip: CIDR2IP) -> Cidr2IpData:
    """
    convert CIDR2IP instance in Cidr2IpData
    :param db: database connection reference
    :param cidr2ip:  CIDR2IP instance
    :return: Cidr2IpData instance
    """
    # TODO: convert CIDR2IP instance to Cidr2IpData in order to store in database
    return Cidr2IpData(db, cidr2ip.country_code, Utils.compress(Utils.serialize(cidr2ip)), Utils.get_current_time())


def cidr_2_ip_to_database(db: DB, cidr2ip_obj: CIDR2IP):
    # TODO: insert/update cidr2ip_obj to database
    # dao = Cidr2IpData(db, Utils.compress(Utils.serialize(cidr2ip_obj)))
    dao = obj_2_dao(db, cidr2ip_obj)
    if dao.has_record:
        dao.update_db()
    else:
        dao.insert_into_db()


def cidr_to_ip_mapper(db: DB, countries: list, ipv6: bool = False):
    cidr2ip_handler = Cidr2ipHandler()
    for country in countries:
        temp = CIDR2IP(country)
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6()
        cidr2ip_handler.add_record(country, temp)
        # TODO: add data to database
        cidr_2_ip_to_database(db, temp)
        # if has_update:
        #     # TODO: add to cidr2ip_handler.updated_list
        #     cidr2ip_handler.add_updated_record(temp)
        #     pass
