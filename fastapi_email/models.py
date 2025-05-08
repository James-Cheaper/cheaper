from sqlalchemy import Column, String, Boolean, DateTime
from fastapi_email.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    token = Column(String, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)