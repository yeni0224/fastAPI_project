from sqlalchemy import Column, Integer, String, Text
from fast_api_db.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)