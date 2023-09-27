from Module.Cidr2Ip import CIDR2IP, Cidr2ipHandler, Cidr2IpData
import Module.Cidr2Ip as c2i

import Module.Utils as Utils


def start(db_name, countries: list, ipv6: bool = False):
    session = c2i.init(db_name)

    cidr2ip_handler = Cidr2ipHandler()
    for country in countries:
        temp = CIDR2IP(country)
        temp.map_ipv4()
        if ipv6:
            temp.map_ipv6()
        cidr2ip_handler.add_record(country, temp)

        # create Cidr2IpData instance
        to_store = Cidr2IpData(country, Utils.compress(Utils.serialize(temp)))

        # add to database
        if c2i.is_record_exists(session, country):
            record = session.query(Cidr2IpData).filter(Cidr2IpData.country_code == country).all()[0]
            record.data = to_store.data
            record.last_updated = Utils.get_now_datetime()
        else:
            c2i.add_record(session, to_store)
        c2i.session_commit(session)
    c2i.session_close(session)
