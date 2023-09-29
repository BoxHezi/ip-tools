import Module.Utils as Utils
from tqdm import tqdm

from Module.InternetDB import InternetDB, InternetDBDAO
from Module.DatabaseDriver import Database


# ref: https://internetdb.shodan.io/


def list_to_ips(ls, ipv6: bool = False) -> list:
    """
    convert input list (either IPs or cidr, or both) to list of ip
    :param ls: list to convert
    :param ipv6: use IPv6 if True. Default set to False
    :return:
    """
    output = []
    for i in ls:
        if Utils.is_cidr(i):
            output += Utils.cidr2ip(i, ipv6)
        else:
            output.append(i)
    return output


def start(db_path: str, ip_list: list, ipv6: bool = False):
    db = Database(db_path, model=InternetDB)
    ips = list_to_ips(ip_list, ipv6)
    for ip in tqdm(ips):
        try:
            result = Utils.internet_db_query(ip)  # type(result) => json/dict
            if "ip" not in result:
                continue
            temp = InternetDB(result)
            dao = InternetDBDAO(db)
            dao.update_record(temp) if dao.has_record_for_ip(ip) else dao.add_record(temp)
        except Exception as e:
            print(f"Exception: {e} while querying {ip}")
    db.commit()
    db.close()
