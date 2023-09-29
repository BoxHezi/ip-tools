from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:

    def __init__(self, db_name: str, db_engine: str = "sqlite:///", echo: bool = True, model: any = None):
        db = db_engine + db_name
        self.__engine = create_engine(db, echo=echo)
        Session = sessionmaker(bind=self.__engine)
        model.metadata.create_all(self.__engine)
        self.__session = Session()

    def close(self):
        self.__session.close()

    def commit(self):
        self.__session.commit()

    def get_session(self):
        return self.__session
