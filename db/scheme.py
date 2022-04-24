import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MeetingList(Base):
    __tablename__ = 'meeting_list'
    user_id = sq.Column(sq.Integer, primary_key=True)
    candidate_id = sq.Column(sq.Integer, primary_key=True)
    sq.PrimaryKeyConstraint('user_id', 'candidate_id', name='matchings_pk')


class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True)
    reason = sq.Column(sq.String, nullable=False)
