from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

engine = create_engine("sqlite:///./fitcheck.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ClothingItem(Base):
    __tablename__ = "clothing_items"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    category = Column(String, nullable=True)
    colour = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)