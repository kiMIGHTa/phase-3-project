from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URI = 'sqlite:///records.db'
engine = create_engine(DATABASE_URI, echo=True)

Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer, Sequence('teacher_id_seq'), primary_key = True)
    teacher_first_name = Column(String)
    teacher_last_name = Column(String)
    salary = Column(Integer)

    classes = relationship('Class', back_populates='teachers')

class Student(Base):
    __tablename__ = 'student'
    stud_id = Column(Integer, Sequence('stud_id_seq'), primary_key=True)
    stud_first_name = Column(String)
    stud_last_name = Column(String)
    gender = Column(String)
    grade = Column(String)

class Class(Base):
    __tablename__ = 'class'
    class_id = Column(Integer,Sequence('class_id_seq'), primary_key=True)
    class_title = Column(String)
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    stud_id = Column(Integer, ForeignKey('student.stud_id'))

    teachers = relationship('Teacher', back_populates='classes')


