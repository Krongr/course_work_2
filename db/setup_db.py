import os
import sys
sys.path.append(os.getcwd())

import sqlalchemy as sq
from db.scheme import Base
from utils import get_credentials_from_file


if __name__ == "__main__":
    db_password = get_credentials_from_file(
        'credentials/db_user_pass.txt'
    )
    db = f'postgresql://db_user:{db_password}@localhost:5432/netology_cw_2'
    engine = sq.create_engine(db)

    Base.metadata.create_all(engine)
