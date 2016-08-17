from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
import datetime


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def query_one():
    """1. Query all of the puppies and return the results in ascending alphabetical order"""
    puppies = session.query(Puppy.name).order_by(Puppy.name.asc()).all()

    for puppy in puppies:
        print puppy.name

def query_two():
    """2. Query all of the puppies that are less than 6 months old organized by the youngest first"""
    today = datetime.date.today()
    max_days_old = 180
    max_birthday = today - datetime.timedelta(days = max_days_old)
    puppies = session.query(Puppy.name, Puppy.dateOfBirth).filter(Puppy.dateOfBirth >= max_birthday).order_by(Puppy.dateOfBirth.desc()).all()
    
    for puppy in puppies:
        print "{puppy_name}: {dob}".format(puppy_name= puppy[0], dob=puppy[1])
        
        
def query_three():
    """3. Query all puppies by ascending weight."""
    
    puppies = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()
    
    for puppy in puppies:
        print "{puppy_name}: {weight}".format(puppy_name=puppy[0], weight=puppy[1])
        
def query_four():
    """4. Query all puppies grouped by the shelter in which they are staying. Show count of puppies at each shelter"""
    puppies = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    
    for shelter_puppy in puppies:
    
        print "{shelter_name}: {puppy}".format(shelter_name=shelter_puppy[0].name, puppy=shelter_puppy[1])



query_one()
query_two()
query_three()
query_four()