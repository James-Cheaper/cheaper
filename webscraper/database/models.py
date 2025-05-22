from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class EbayItem(Base):
    __tablename__ = 'ebay_items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    currency = Column(String)
    url = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # if linked to a user


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Assume it's already hashed