from Module.Cidr2Ip import Cidr2Ip, Cidr2IpDAO
from Module.DatabaseDriver import Database


def start(db_path, countries: list, ipv6: bool = False):
    db = Database(db_path, model=Cidr2Ip)
    for c in countries:
        temp = Cidr2Ip(c)
        temp.read_cidr_file()
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6
        dao = Cidr2IpDAO(db)
        dao.update_record(temp) if dao.has_record_for_country_code(c) else dao.add_record(temp)
    db.commit()
    db.close()
