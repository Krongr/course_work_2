import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# Not required?
# class UnwantedRelations(Base):
#     __tablename__ = 'unwanted_relations'
#     id = sq.Column(sq.Integer, primary_key=True)
#     relation = sq.Column(sq.String, nullable=False, unique=True)

class MeetingList(Base):
    __tablename__ = 'meeting_list'
    user_id = sq.Column(sq.Integer, primary_key=True)
    candidate_id = sq.Column(sq.Integer, primary_key=True)
    sq.PrimaryKeyConstraint('user_id', 'candidate_id', name='matchings_pk')

class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True)
    reason = sq.Column(sq.String, nullable=False)