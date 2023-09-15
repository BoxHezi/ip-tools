from Module.GitRepo import GitRepo
from Module.SqliteDriver import DB
from Module.DAO.DataAccess import GitRepoData

from sqlite3 import Error as sql_error


def git_repo_to_database(repo: GitRepo, db: DB, country_list: list):
    if len(country_list) == 0:
        return

    db.begin_transaction()
    for country in country_list:
        dao = GitRepoData(db, country)
        dao.data = repo.read_content_and_cal_hash(country)
        try:
            if dao.has_record:
                dao.update_db()
            else:
                dao.insert_into_db()
        except sql_error as e:
            print(e)
            db.perform_rollback()
            return
    db.perform_commit()
    del db
