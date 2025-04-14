from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=True)

    def __repr__(self):
        return f"<Table(id={self.id}, name={self.name}, seats={self.seats}, location={self.location})>"
