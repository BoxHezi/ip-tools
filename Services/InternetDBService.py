import Module.Utils as Utils
from tqdm import tqdm

from Module import InternetDB


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


def start_query(db_name: str, ls: list, ipv6: bool=False):
    session = InternetDB.init(db_name)
    ips = list_to_ips(ls, ipv6)
    results = []
    for ip in tqdm(ips):
        try:
            result = Utils.internet_db_query(ip)  # type(result) => json/dict
            if "ip" not in result:
                continue
            temp = InternetDB.InternetDB(ip=Utils.ip_int(ip), ip_str=ip, hostnames=Utils.list_2_str(result["hostnames"]),
                                        ports=Utils.list_2_str(result["ports"]), cpes=Utils.list_2_str(result["cpes"]),
                                        vulns=Utils.list_2_str(result["vulns"]), tags=Utils.list_2_str(result["tags"]))
            results.append(temp)
        except Exception as e:
            print(f"Exception: {e}")
    InternetDB.add_records(session, results)
    InternetDB.session_close(session)
