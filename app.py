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

    teach_class = relationship('Class', back_populates='teachers')

    def add_class(self, session, class_title, start_time, end_time, stud_id=None):
        new_class = Class(class_title=class_title, teacher_id=self.teacher_id, start_time=start_time, end_time=end_time, stud_id=stud_id)
        session.add(new_class)
        session.commit()

    @classmethod
    def change_student_grade(self, session, student_id, new_grade):
        # Find the student by their ID
        student = session.query(Student).filter_by(stud_id=student_id).first()

        if student:
            # Update the student's grade
            student.grade = new_grade
            session.commit()
            return True  # Grade change successful
        else:
            return False 
        
    # @classmethod    
    # def add_student_to_class(self, session, student_id, class_id):
    #     # Check if the class with the given class_id exists
    #     class_entry = session.query(Class).filter_by(class_id=class_id).first()

    #     if class_entry:
    #         # Check if the student with the given student_id exists
    #         student = session.query(Student).filter_by(stud_id=student_id).first()

    #         if student:
    #             # Check if the student is not already enrolled in this class
    #             if student not in class_entry.students:
    #                 class_entry.students.append(student)
    #                 session.commit()
    #                 print(f"Student {student.stud_first_name} {student.stud_last_name} added to class: {class_entry.class_title}")
    #             else:
    #                 print("Student is already enrolled in this class.")
    #         else:
    #             print("Student not found.")
    #     else:
    #         print("Class not found.")        

class Student(Base):
    __tablename__ = 'student'
    stud_id = Column(Integer, Sequence('stud_id_seq'), primary_key=True)
    stud_first_name = Column(String)
    stud_last_name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    grade = Column(String)

    stud_class = relationship('Class', back_populates='students')

    def get_grade(self):
        return self.grade
    
    @classmethod
    def get_student_grades(cls,session):
        student_grades = []

        students = session.query(cls).all()

        for student in students:
            student_name = f"{student.stud_first_name} {student.stud_last_name}"
            student_grade = student.grade if student.grade is not None else "N/A"

            student_grades.append({"student name": student_name, "grade": student_grade})

        return student_grades
    
    @classmethod
    def get_available_classes(cls, session):
        available_classes = []

        classes = session.query(Class).all()

        for class_entry in classes:
            class_title = class_entry.class_title
            start_time = class_entry.start_time
            end_time = class_entry.end_time
            teacher_name = f"{class_entry.teachers.teacher_first_name} {class_entry.teachers.teacher_last_name}"

            available_classes.append({"class_title": class_title,
                                       "start_time": start_time, 
                                       "end_time": end_time, 
                                       "teacher": teacher_name})

        return available_classes
    
    # def enroll_in_class(self, session, class_title):
    #     class_entry = session.query(Class).filter_by(class_title=class_title).first()

    #     if class_entry:
    #         if self not in class_entry.students:
    #             class_entry.students.append(self)
    #             session.commit()
    #             print(f"Enrolled in class: {class_entry.class_title}")
    #         else:
    #             print("Already enrolled in this class.")
    #     else:
    #         print("Class not found.")

class Class(Base):
    __tablename__ = 'class'
    class_id = Column(Integer,Sequence('class_id_seq'), primary_key=True)
    class_title = Column(String)
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    stud_id = Column(Integer, ForeignKey('student.stud_id'))
    start_time = Column(String)
    end_time = Column(String)

    teachers = relationship('Teacher', back_populates='teach_class')
    students = relationship('Student', back_populates='stud_class')


    def get_timetable(cls,session,student_id=None, teacher_id=None):
        timetable = []
        query = session.query(Class)

        if student_id:
            query = query.filter_by(stud_id=student_id)

        if teacher_id:
            query = query.filter_by(teacher_id=teacher_id)

        classes = query.all()

        for class_entry in classes:
            class_title = class_entry.class_title
            start_time = class_entry.start_time
            end_time = class_entry.end_time

            timetable.append({"class_title": class_title, "start_time": start_time, "end_time": end_time})

        return timetable

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()






