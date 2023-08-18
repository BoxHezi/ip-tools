import os
import git


class GitRepo:

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

    def check_update(self, pull: bool = True):
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

        return local_hash == remote_hash

    def check_updated_file(self):
        """
        check which files are updated
        """
        pass
