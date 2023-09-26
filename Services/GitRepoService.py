from Module.GitRepo import GitRepo, GitRepoData
import Module.GitRepo as gp
import Module.Utils as Utils


def start(db_name, repo: GitRepo, country_list: list):
    if len(country_list) == 0:
        return

    if not db_name or db_name == "":
        db_name = "./data.db"
    session = gp.init(db_name, False)
    for country in country_list:
        temp = GitRepoData(country, None, Utils.get_now_datetime())
        temp.data = repo.read_content_and_cal_hash(country)
        if gp.is_record_exists(session, country):
            record = session.query(GitRepoData).filter(GitRepoData.country_code==country).all()[0]
            record.data = temp.data
            record.last_updated = Utils.get_now_datetime()
        else:
            gp.add_record(session, temp)
    gp.session_commit(session)
