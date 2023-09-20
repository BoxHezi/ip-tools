from Module.DAO.Cidr2IpDAO import Cidr2IpData
from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler
from Module.SqliteDriver import DB

import Module.Utils as Utils


def dao_2_obj(dao: Cidr2IpData) -> CIDR2IP:
    """
    convert Cidr2IpData (DAO) back to CIDR2IP instance
    :param dao: Cidr2IpData instance
    :return: CIDR2IP instance
    """
    return Utils.deserialize(Utils.decompress(dao.cidr_to_ip_obj))


def obj_2_dao(db: DB, cidr2ip: CIDR2IP) -> Cidr2IpData:
    """
    convert CIDR2IP instance in Cidr2IpData
    :param db: database connection reference
    :param cidr2ip:  CIDR2IP instance
    :return: Cidr2IpData instance
    """
    return Cidr2IpData(db, cidr2ip.country_code, Utils.compress(Utils.serialize(cidr2ip)), Utils.get_current_time())


def cidr_2_ip_to_database(db: DB, cidr2ip_obj: CIDR2IP):
    """
    insert cidr_2_ip information into database
    :param db: database connection reference
    :param cidr2ip_obj: CIDR2IP instance
    :return: Cidr2IpData instance if there is update (new record or updated record); None otherwise
    """
    dao = obj_2_dao(db, cidr2ip_obj)
    # print(dao)
    # print(dao.has_record)
    # print("Has Update:", dao.has_update())
    updated = dao.has_update()
    if dao.has_record:
        if updated:
            dao.update_db()
    else:
        dao.insert_into_db()
    return dao if updated else None


def cidr_to_ip_mapper(db: DB, countries: list, ipv6: bool = False):
    cidr2ip_handler = Cidr2ipHandler()
    db.begin_transaction()
    for country in countries:
        temp = CIDR2IP(country)
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6()
        cidr2ip_handler.add_record(country, temp)
        result = cidr_2_ip_to_database(db, temp)
        if result is not None:
            cidr2ip_handler.add_updated_record(temp)  # add to updated_record list if there is update
    db.perform_commit()
