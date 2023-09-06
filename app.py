from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey

DATABASE_URI = 'sqlite:///records.db'
engine = create_engine(DATABASE_URI, echo=True)

Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, Sequence('teacher_id_seq'), primary_key = True)
    teacher_first_name = Column(String)
    teacher_last_name = Column(String)
    salary = Column(Integer)