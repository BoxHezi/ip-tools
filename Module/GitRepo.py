import os
import git

import sqlalchemy
from sqlalchemy import String, Integer, JSON, DateTime
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import Module.Utils as Utils

# REF: https://github.com/herrbischoff/country-ip-blocks

Base = declarative_base()


class GitRepoData(Base):
    __tablename__ = "cidr_git_repo"
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    last_updated = Column(DateTime, default=Utils.get_now_datetime(), onupdate=Utils.get_now_datetime())

    def __init__(self, country_code, data, last_updated):
        self.country_code = country_code
        self.data = data
        self.last_updated = last_updated


def init(db_name: str, echo: bool = True):
    db_name = "sqlite:///" + db_name
    engine = create_engine(db_name, echo=echo)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def session_commit(session):
    session.commit()


def session_close(session: sqlalchemy.orm.session.Session):
    session.close()


def is_record_exists(session, country_code: str):
    record = session.query(GitRepoData).filter(GitRepoData.country_code == country_code)
    return session.query(record.exists()).scalar()


def add_record(session, obj: GitRepoData):
    session.add(obj)


class GitRepo:
    __IPv4_BASE_PATH = "./country-ip-blocks/ipv4/"
    __IPv6_BASE_PATH = "./country-ip-blocks/ipv6/"

    def __init__(self, config):
        self.local_repo = config["git_local_repo"]
        self.remote_repo = config["git_remote_url_ssh"]

        if not os.path.exists(self.local_repo):
            print("No local repo, cloning from remote {}".format(self.remote_repo))
            git.Repo.clone_from(self.remote_repo, self.local_repo)

        self.repo = git.Repo(self.local_repo)

    def __del__(self):
        self.repo.close()

    def get_local_repo(self):
        return git.Repo(self.local_repo)

    def find_updated_files(self, pull: bool = True):
        """
        check if the git repo contains new pushes
        :param pull: pull from remote if new pushes detected
        :return: list of updated files, return empty list if up-to-date
        """
        origin = self.repo.remotes.origin
        origin.fetch()

        local_hash = self.repo.head.commit.hexsha
        remote_hash = origin.refs.master.commit.hexsha

        updated_files = []
        if local_hash == remote_hash:
            print("Git repo is up-to-date")
        else:
            print("Git repo update detected")
            # find all files from new pushes
            for item in self.repo.index.diff(remote_hash):
                updated_country = item.a_path[5:7]
                if updated_country not in updated_files:
                    updated_files.append(updated_country)
            if pull:
                print("Pulling from remote...")
                origin.pull()

        return updated_files

    def read_content_and_cal_hash(self, country_code):
        file_suffix = ".cidr"
        result = {"country_code": country_code}
        ipv4_contents = Utils.read_file(self.__IPv4_BASE_PATH + country_code + file_suffix)
        ipv6_contents = Utils.read_file(self.__IPv6_BASE_PATH + country_code + file_suffix)
        ipv4_hashes = Utils.cal_hash(",".join(ipv4_contents).encode()) if ipv4_contents else None
        ipv6_hashes = Utils.cal_hash(",".join(ipv6_contents).encode()) if ipv6_contents else None
        result["ipv4_info"] = {"md5": ipv4_hashes[0], "sha256": ipv4_hashes[1]} if ipv4_hashes else None
        result["ipv6_info"] = {"md5": ipv6_hashes[0], "sha256": ipv6_hashes[1]} if ipv6_hashes else None
        return result
