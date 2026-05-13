from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Date

# Create database engine
engine = create_engine("sqlite:///clients.db")

# Create base class
Base = declarative_base()

# Create session
SessionLocal = sessionmaker(bind=engine)


# Client Table
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    status = Column(String)
    last_contact = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)