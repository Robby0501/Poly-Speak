from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    language_to_learn = Column(String)
    proficiency_level = Column(String)
    daily_goal = Column(Integer)
    start_option = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)