from sqlalchemy import create_engine
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

#--------------------------------------------------
#		USERS
#--------------------------------------------------

# Class Table Inheritence: Single id per user, with common attributes
# in the Users table for each, but specialized attributes in the
# Mentors and Mentees tables, with a reference to User id

# Assumption: No need for location information as long as we're limiting
# the app to one location for now


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)  #TODO: some kind of encryption
    birth_date = Column(DateTime)
    summary = Column(Text)
    university_id = Column(Integer, ForeignKey('universities.id'))  #TODO: junction(users-universities)
    url = Column(Text)

    def __repr__(self):
        return '<User(id={0}, first_name={1}, last_name={2})'.format(
            self.id, self.first_name, self.last_name)

