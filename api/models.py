from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entry"
    id = Column('id', Integer, primary_key=True)
    date = Column('date', String(8))
    title = Column('title', String(16))
    text_path = Column('text_path', String(50))

    def as_dict(self):
        with open(self.text_path) as file:
            return {
                'id': self.id,
                'date': self.date,
                'title': self.title,
                'text': file.read()
            }

    def save(self, session):
        session.add(self)
        session.commit()
