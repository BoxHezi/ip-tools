import os
import git
import Module.Utils as Utils


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
            for item in self.repo.index.diff(origin.refs.master.commit.hexsha):
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

    # @staticmethod
    # def store_data(db: DB, dao: DataAccess.GitRepoData):
    #     if dao.contains_record():
    #         dao.update_db(db)
    #     else:
    #         dao.insert_into_db(db)

    # @staticmethod
    # def store_data(data: dict) -> list:
    #     updated_list = []  # a list to store updated CIDR information
    #     db = DB("./data.db")
    #     db.begin_transaction()
    #     try:
    #         for k, v in data.items():  # k: country_code, v: data
    #             json_data = json.dumps(v)
    #             if db.update_cidr_git_repo(k, json_data):
    #                 updated_list.append(k)
    #         db.perform_commit()
    #     except sql_error as e:
    #         db.perform_rollback()
    #         updated_list = []
    #         print("Transaction rollback due to error {}".format(e))
    #     finally:
    #         del db
    #         return updated_list
