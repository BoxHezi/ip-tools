from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Module.utils import debug_mode


class Database:
    def __init__(self, db_name: str, db_engine: str = "sqlite:///", model: any = None):
        db = db_engine + db_name
        self.__engine = create_engine(db, echo=debug_mode())
        Session = sessionmaker(bind=self.__engine)
        model.metadata.create_all(self.__engine)
        self.__session = Session()

    def close(self):
        self.__session.close()

    def commit(self):
        self.__session.commit()

    def get_session(self):
        return self.__session

    def get_record_by_attribute(self, obj, attribute, val):
        records = self.__session.query(obj).filter(getattr(obj, attribute) == val).all()
        return records
