from Module.CidrInfo import CountryCidr, CountryCidrDAO
from Module.DatabaseDriver import Database


def start(db_path, country_list: list):
    db = Database(db_path, model=CountryCidr)
    for c in country_list:
        temp = CountryCidr(c)
        temp.data = temp.read_content_and_cal_hash()
        dao = CountryCidrDAO(db)
        dao.update_record(temp) if dao.has_record_for_country_code(temp.country_code) else dao.add_record(temp)
    db.commit()
    db.close()
