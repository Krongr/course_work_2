import os
import sys
sys.path.append(os.getcwd())

import sqlalchemy as sq
from db.scheme import *
from utils import get_credentials_from_file


if __name__ == "__main__":
    db_password = get_credentials_from_file(
        'credentials/db_user_pass.txt'
    )
    db = f'postgresql://db_user:{db_password}@localhost:5432/netology_cw_2'
    engine = sq.create_engine(db)


    Base.metadata.create_all(engine)

    # Not required?
    # db_connection = engine.connect()
    # unwanted_relations = {
    #     2: 'есть друг/есть подруга',
    #     3: 'помолвлен/помолвлена',
    #     4: 'женат/замужем',
    #     7: 'влюблён/влюблена',
    #     8: 'в гражданском браке'
    # }
    # for id, relation in unwanted_relations.items():
    #     db_connection.execute(f"""
    #         INSERT INTO unwanted_relations(id, relation)
    #         VALUES({id}, '{relation}');
    #     """)