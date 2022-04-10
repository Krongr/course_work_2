import os
import sys
sys.path.append(os.getcwd())

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from db.scheme import *


class DbClient():
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def start_session(self):
        db = ('postgresql://'
            f'{self.user}:{self.password}@localhost:5432/netology_cw_2')
        engine = sq.create_engine(db)

        Session = sessionmaker(bind=engine)
        return Session()

    # Not required?
    # def get_unwanted_relations(self):
    #     ids_list = []
    #     session = self.start_session()
    #     selection = session.query(UnwantedRelations.id)
    #     for item in selection:
    #         ids_list.append(item[0])
    #     return ids_list

    def create_meeting_list_record(self, user_id, candidate_id):
        session = self.start_session()
        session.add(MeetingList(
            user_id = user_id,
            candidate_id = candidate_id
        ))
        session.commit()

    def get_meeting_list(self, user_id):
        ids_list =[]
        session = self.start_session()
        selection = session.query(MeetingList.candidate_id
            ).filter(MeetingList.user_id == user_id)
        for item in selection:
            ids_list.append(item[0])
        return ids_list
    
    def get_black_list(self):
        ids_list = []
        session = self.start_session()
        selection = session.query(BlackList.id)
        for item in selection:
            ids_list.append(item[0])
        return ids_list

    def get_unwanted_ids(self, user_id):
        return self.get_meeting_list(user_id) + self.get_black_list()