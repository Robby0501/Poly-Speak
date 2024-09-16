from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(LargeBinary, nullable=False)  # Ensure it's LargeBinary
    language_to_learn = Column(String, nullable=False)
    proficiency_level = Column(String, nullable=False)
    daily_goal = Column(Integer, nullable=False)
    start_option = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
        except Exception as e:
            print(f"Error checking password: {str(e)}")
            return False

