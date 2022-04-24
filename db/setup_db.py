import os
import sys
sys.path.append(os.getcwd())

import configparser
import sqlalchemy as sq
from db.scheme import Base


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings.ini")
    db_password = config['db']['password']
    db = f'postgresql://db_user:{db_password}@localhost:5432/netology_cw_2'
    engine = sq.create_engine(db)

    Base.metadata.create_all(engine)
