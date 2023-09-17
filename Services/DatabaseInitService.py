from Module.SqliteDriver import DB


def init_db_table(config):
    db_path = config["PATH"]

    db = DB(db_path)
    db.cursor.execute("""create table IF NOT EXISTS cidr_git_repo
(
    id           integer                                     not null
        constraint cidr_git_repo_pk
            primary key autoincrement,
    country_code TEXT(2)                                     not null,
    data         TEXT                                        not null,
    last_updated TEXT default (datetime('now', 'localtime')) not null
);""")

    db.cursor.execute("""create table  IF NOT EXISTS cidr_ip_mapper
(
    id             INTEGER
        primary key autoincrement,
    country_code   TEXT(2),
    cidr_to_ip_obj BLOB,
    last_updated   TEXT default (datetime('now', 'localtime'))
);""")
