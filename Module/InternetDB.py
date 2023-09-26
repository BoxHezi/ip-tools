import sqlalchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import Module.Utils as Utils

Base = declarative_base()


class InternetDB(Base):
    __tablename__ = "internetdb"
    ip = Column(Integer, primary_key=True, nullable=False, index=True)
    ip_str = Column(String, nullable=False)
    hostnames = Column(String)
    ports = Column(String)
    cpes = Column(String)
    vulns = Column(String)
    tags = Column(String)
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())


def init(db_name: str="./databases/test.db", echo: bool=True):
    db_name = "sqlite:///" + db_name
    engine = create_engine(db_name, echo=echo)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def session_commit(session):
    session.commit()


def session_close(session: sqlalchemy.orm.session.Session):
    session.close()


def is_record_exists(session, ip: int):
    record = session.query(InternetDB).filter(InternetDB.ip==ip)
    return session.query(record.exists()).scalar()


def add_records(session: sqlalchemy.orm.session.Session, obj: InternetDB | list[InternetDB]):
    """
    add or update record.
    if no exist record, insert into database; update record if exists
    """
    if isinstance(obj, list):
        for item in obj:
            if is_record_exists(session, item.ip):  # if record exists
                info = session.query(InternetDB).filter(InternetDB.ip==item.ip).all()[0]
                info.hostnames = item.hostnames
                info.ports = item.ports
                info.cpes = item.cpes
                info.vulns = item.vulns
                info.tags = item.tags
                info.last_updated = Utils.get_now_datetime()
            else:
                session.add(item)
    else:
        session.add(obj)
    session_commit(session)


# engine = db_init()
# session = session_init(engine)
# contains_ip(session, "192.168.1.1")
# # add_records(session, InternetDB(ip=Utils.ip_int("192.168.1.1"), ip_str="192.168.1.1"))
# add_records(session, [
#     InternetDB(ip=Utils.ip_int("192.168.1.1"), ip_str="192.168.1.1"),
#     InternetDB(ip=Utils.ip_int("192.168.1.2"), ip_str="192.168.1.2"),
#     InternetDB(ip=Utils.ip_int("192.168.1.3"), ip_str="192.168.1.3")
# ])
# contains_ip(session, "192.168.1.1")
# session_close(session)

# engine = create_engine("sqlite:///./databases/test.db", echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# q = session.query(InternetDB.ip).filter(InternetDB.ip_str=="192.168.1.1")
# print("===" * 10)
# print(session.query(q.exists()).scalar())

# # session.add_all(
# #     [InternetDB(ip=Utils.ip_int("192.168.1.1"), ip_str="192.168.1.1"),
# #      InternetDB(ip=Utils.ip_int("192.168.1.2"), ip_str="192.168.1.2")]
# # )
# # session.commit()

# # for record in session.query(InternetDB).all():
# #     print("==" * 10)
# #     print(record)

# print(type(session))
# session.close()
