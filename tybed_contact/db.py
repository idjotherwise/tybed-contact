# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_db.ipynb.

# %% auto 0
__all__ = ['sqlite_file_name', 'sqlite_url', 'engine', 'create_db_and_tables', 'get_session', 'create_persons', 'create_person',
           'read_persons']

# %% ../01_db.ipynb 2
from fastcore.utils import *
from sqlmodel import Session, select, create_engine
from .models import Person, PersonCreate, PersonRead, PersonUpdate

# %% ../01_db.ipynb 4
sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    create_persons()
    
def get_session():
    with Session(engine) as session:
        yield session
        
def create_persons(session: Session = get_session()):
    person_ifan = Person(first_name="ifan", last_name="johnston", occupation="dev")
    session.add(person_ifan)
    session.commit()
    session.refresh(person_ifan)

# %% ../01_db.ipynb 5
def create_person(
               session: Session, # A SQLModel session
               person: PersonCreate # An SQLModel for creating a `Person`
              )-> PersonRead:
    "Add a person to the database"
    db_person = Person.from_orm(person)
    session.add(person)
    session.commit()
    session.refresh(db_person)
    return db_person

def read_persons(
                session: Session, # A SQLModel session.
                offset: int = 0, # Offset to read from.
                limit: int = 100 # Maximum index to read to.
                ) -> List[Person]:
    persons = session.exec(select(Person).offset(offset).limit(limit)).all()
    return persons