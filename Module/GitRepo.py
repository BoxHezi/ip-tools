import os
from sqlite3 import Error as sql_error

import git
import json

import Module.Utils as Utils
from Module.SqliteDriver import DB
from Module.DAO import DataAccess


# REF: https://github.com/herrbischoff/country-ip-blocks

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

    def has_update(self, pull: bool = True):
        origin = self.repo.remotes.origin
        origin.fetch()

        local_hash = self.repo.head.commit.hexsha
        remote_hash = origin.refs.master.commit.hexsha

        if local_hash == remote_hash:
            print("Git repo is up-to-date")
        else:
            print("Git repo update detected")
            if pull:
                print("Pulling from remote...")
                origin.pull()

        return local_hash != remote_hash

    def check_updated_file(self):
        """
        check which files are updated
        store hash in database
        """
        country_set = Utils.get_all_country_code()

        file_suffix = ".cidr"
        data = {}
        for c in country_set:
            temp = {"country_code": c}
            ipv4_contents = Utils.read_file(self.__IPv4_BASE_PATH + c + file_suffix)
            ipv6_contents = Utils.read_file(self.__IPv6_BASE_PATH + c + file_suffix)
            ipv4_hashes = Utils.cal_hash(",".join(ipv4_contents).encode()) if ipv4_contents is not None else None
            ipv6_hashes = Utils.cal_hash(",".join(ipv6_contents).encode()) if ipv6_contents is not None else None
            temp["ipv4_info"] = {"md5": ipv4_hashes[0], "sha256": ipv4_hashes[1]} if ipv4_hashes is not None else None
            temp["ipv6_info"] = {"md5": ipv6_hashes[0], "sha256": ipv6_hashes[1]} if ipv6_hashes is not None else None
            data[c] = temp

            # temp = DataAccess.GitRepoData("./data.db", c, None, None)
            # # print(temp)
            # temp.retrieve_data_by_country_code()
            # print(temp)

        return self.store_data(data)

    @staticmethod
    def store_data(data: dict) -> list:
        updated_list = []  # a list to store updated CIDR information
        db = DB("./data.db")
        db.begin_transaction()
        try:
            for k, v in data.items():  # k: country_code, v: data
                json_data = json.dumps(v)
                if db.update_cidr_git_repo(k, json_data):
                    updated_list.append(k)
            db.perform_commit()
        except sql_error as e:
            db.perform_rollback()
            updated_list = []
            print("Transaction rollback due to error {}".format(e))
        finally:
            del db
            return updated_list
