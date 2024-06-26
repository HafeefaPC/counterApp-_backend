from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Counter(Base):
    __tablename__ = 'counter'

    id = Column(Integer, primary_key=True, index=True)
    limit_value = Column(Integer, nullable=False, default=10)
