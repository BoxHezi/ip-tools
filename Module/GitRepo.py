import os
import sqlite3

import git
import hashlib
import json

import Module.Utils as Utils
from Module.SqliteDriver import DB


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
            ipv4_info = self.cal_file_hash(self.__IPv4_BASE_PATH + c + file_suffix)
            ipv6_info = self.cal_file_hash(self.__IPv6_BASE_PATH + c + file_suffix)
            temp["ipv4_info"] = {"md5": ipv4_info[0], "sha256": ipv4_info[1]} if ipv4_info is not None else None
            temp["ipv6_info"] = {"md5": ipv6_info[0], "sha256": ipv6_info[1]} if ipv6_info is not None else None
            data[c[0:2]] = temp

        return self.store_data(data)

    @staticmethod
    def store_data(data: dict) -> list:
        updated_list = []  # a list to store updated CIDR information
        db = DB("./data.db")
        db.connection.execute("BEGIN;")
        try:
            for k, v in data.items():  # k: country_code, v: data
                json_data = json.dumps(v)
                if db.update_cidr_git_repo(k, json_data):
                    updated_list.append(k)
            db.connection.commit()
        except sqlite3.Error as e:
            db.connection.rollback()
            print("Transaction rollback due to error {}".format(e))
        finally:
            del db
            return updated_list

    @staticmethod
    def cal_file_hash(file_path) -> tuple | None:
        try:
            with open(file_path, "r") as reader:
                temp = [line.strip() for line in reader]
                md5 = hashlib.md5(",".join(temp).encode()).hexdigest()
                sha256 = hashlib.sha256(",".join(temp).encode()).hexdigest()
                return md5, sha256
        except FileNotFoundError:
            print("File {} not found".format(file_path))
            return None
