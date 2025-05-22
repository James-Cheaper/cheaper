# webscraper/database/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webscraper.database.models import Base
from webscraper.database.models import User, EbayItem  


DATABASE_URL = "postgresql://postgres:cheaper@localhost/cheaper_local"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
