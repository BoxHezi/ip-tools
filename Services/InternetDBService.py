import Module.Utils as Utils
from Module.SqliteDriver import DB
from Module.DAO.InternetDBDAO import InternetDBDAO
from tqdm import tqdm


# ref: https://internetdb.shodan.io/

def db_init(db: DB):
    db.cursor.execute("""create table IF NOT EXISTS internetdb
(
    ip       integer not null
        constraint internetdb_pk
            primary key,
    ip_str TEXT not null,
    hostnames TEXT,
    ports    TEXT,
    cpes     TEXT,
    vulns    TEXT,
    tags     TEXT,
    last_updated TEXT default (datetime('now', 'localtime')) not null
);
""")
    db.cursor.execute("""create index IF NOT EXISTS internetdb_ip_index
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
    db_init(db)  # create table if not exists
    ips = ls_to_ips(ls, ipv6)
    for ip in tqdm(ips):
        result = Utils.internet_db_query(ip)  # type(result) => json/dict
        if "ip" not in result:
            continue
        dao = InternetDBDAO(db, ip, result)
        if dao.has_record():
            dao.update_db()
        else:
            dao.insert_into_db()
