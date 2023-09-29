import os

import git


# REF: https://github.com/herrbischoff/country-ip-blocks


class GitRepo:
    def __init__(self, config):
        self.local_repo = config["git_local_repo"]
        self.remote_repo = config["git_remote_url_ssh"]
        if not os.path.exists(self.local_repo):
            print("No local repo, cloning from remote {}".format(self.remote_repo))
            git.Repo.clone_from(self.remote_repo, self.local_repo)
        self.repo = git.Repo(self.local_repo)

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
            return []
        print("Git repo update detected")
        # find all files from new pushes
        for item in self.repo.index.diff(remote_hash):
            updated_country = item.a_path[5:7]
            updated_country not in updated_files and updated_files.append(updated_country)
        if pull:
            print("Pulling from remote...")
            self.pull_from_remote()
        return updated_files

    def pull_from_remote(self):
        origin = self.repo.remotes.origin
        origin.pull()
