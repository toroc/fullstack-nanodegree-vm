import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	address = Column(String(200))
	city = Column(String(80))
	state = Column(String(20))
	zipCode = Column(String(10))
	website = Column(String)
	

"""Model for MVC"""
class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	gender = Column(String(6), nullable = False)
	dateOfBirth = Column(Date)
	weight = Column(Numeric(10))
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	picture = Column(String)


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)