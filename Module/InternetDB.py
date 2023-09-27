import sqlalchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import Module.Utils as Utils

Base = declarative_base()


class InternetDBDAO(Base):
    __tablename__ = "internetdb"
    ip = Column(Integer, primary_key=True, nullable=False, index=True)
    ip_str = Column(String, nullable=False)
    hostnames = Column(String)
    ports = Column(String)
    cpes = Column(String)
    vulns = Column(String)
    tags = Column(String)
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())


def init(db_name: str = "./databases/test.db", echo: bool = True):
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
    record = session.query(InternetDBDAO).filter(InternetDBDAO.ip == ip)
    return session.query(record.exists()).scalar()


def add_records(session: sqlalchemy.orm.session.Session, obj: InternetDBDAO | list[InternetDBDAO]):
    """
    add or update record.
    if no exist record, insert into database; update record if exists
    """
    if isinstance(obj, list):
        for item in obj:
            if is_record_exists(session, item.ip):  # if record exists
                update_record(session.query(InternetDBDAO).filter(InternetDBDAO.ip == item.ip).all()[0], item)
            else:
                session.add(item)
    else:
        if is_record_exists(session, obj.ip):
            update_record(session.query(InternetDBDAO).filter(InternetDBDAO.ip == obj.ip).all()[0], obj)
        else:
            session.add(obj)
    session_commit(session)


def update_record(record, new_record):
    record.hostnames = new_record.hostnames
    record.ports = new_record.ports
    record.cpes = new_record.cpes
    record.vulns = new_record.vulns
    record.tags = new_record.tags
    record.last_updated = Utils.get_now_datetime()
