from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Engine
engine = create_engine("sqlite:///clients.db")

# Base Class
Base = declarative_base()

# Session
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
    next_follow_up = Column(String)

    notes = Column(String)

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)

    client_name = Column(String)

    action = Column(String)

    timestamp = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)