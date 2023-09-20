import Module.Utils as Utils
from Module.SqliteDriver import DB


# ref: https://internetdb.shodan.io/

def db_init(db: DB):
    db.cursor.execute("""create table IF NOT EXISTS internetdb
(
    ip       integer not null
        constraint internetdb_pk
            primary key,
    hostname TEXT,
    ports    TEXT,
    cpes     TEXT,
    vulns    TEXT,
    tags     TEXT
);
""")
    db.cursor.execute("""create index internetdb_ip_index
    on internetdb (ip);
""")
    db.perform_commit()


def ls_to_ips(ls, ipv6: bool = False) -> list:
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


def start_query(db: DB, ls: list, ipv6: bool = False):
    """
    start send query to get information from internetdb: https://internetdb.shodan.io/
    :param db: database connection reference
    :param ls: list of IP or CIDR, or both
    :param ipv6: use IPv6 if True. Default set to False
    :return:
    """
    db_init(db)
    ips = ls_to_ips(ls)
    for ip in ips:
        result = Utils.internet_db_query(ip)  # type json/dict
