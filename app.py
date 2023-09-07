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

    def add_class(self, session, class_title, start_time, end_time):
        new_class = Class(class_title=class_title, teacher_id=self.teacher_id, start_time=start_time, end_time=end_time)
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

            available_classes.append({"class_title": class_title, "start_time": start_time, "end_time": end_time, "teacher": teacher_name})

        return available_classes
    
    # def enroll_in_class(self, session, class_title):
    #     # Check if the class with the given class_id exists
    #     class_entry = session.query(Class).filter_by(class_title=class_title).first()

    #     if class_entry:
    #         # Check if the student is not already enrolled in this class
    #         if self not in class_entry.students:
    #             class_entry.students.append(self)
    #             session.commit()
    #             print("Enrollment successful")
    #             return True  # Enrollment successful
    #         else:
    #             print("already enrolled")
    #             return False  # Student is already enrolled in this class
    #     else:
    #         print("failed")
    #         return False 


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

def teacher_actions(session):
    while True:
        print("Teacher Actions:")
        print("1. Change Student Grade")
        print("2. Check timetable")
        print("3. Add class")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            student_id = int(input("Enter the student's ID: "))
            new_grade = input("Enter the new grade: ")
            Teacher.change_student_grade(session, student_id, new_grade)
        

        elif choice == "2":
            teacher_input_id = input("Enter teacher's id: ")
            # Retrieve the teacher based on the input name
            teacher = session.query(Class).filter_by(teacher_id=teacher_input_id).first()

            if teacher:
                timetable = teacher.get_timetable(session)
                if timetable:
                    print("Timetable:")
                    for entry in timetable:
                        print(f"Class Title: {entry['class_title']}")
                        print(f"Start Time: {entry['start_time']}")
                        print(f"End Time: {entry['end_time']}")
                        print()
                else:
                    print("No classes found for this teacher.")
            else:
                print("Teacher not found.")

        elif choice == "3":
            teacher_name = input("Enter teacher's full name (e.g., 'George West'): ")
            class_title = input("Enter class title: ")
            start_time = input("Enter start time: ")
            end_time = input("Enter end time: ")

            teacher = session.query(Teacher).filter_by(teacher_first_name=teacher_name.split()[0], teacher_last_name=teacher_name.split()[1]).first()

            if teacher:
                teacher.add_class(session, class_title, start_time, end_time)
                print("Class added successfully.")
            else:
                print("Teacher not found.")

        elif choice == "4":
            print("Exiting...")
            break
        # elif choice == "2":
        #     break
        else:
            print("Invalid input.")

def student_actions():
    while True:
        print("Student Actions:")
        print("1. Check my Grades")
        print("2. Check timetable")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

    pass            


Session = sessionmaker(bind=engine)
session = Session()



# --- teachers
teach1 = Teacher(teacher_first_name='George',teacher_last_name='West',salary= 708000)
teach2 = Teacher(teacher_first_name='Dennis',teacher_last_name='Kimaita',salary= 1600100)
teach3 = Teacher(teacher_first_name='Doris',teacher_last_name='Gitonga',salary= 2000000)
teach4 = Teacher(teacher_first_name='Sasha',teacher_last_name='Mbulumo',salary= 401000)

# session.add_all([teach1,teach2,teach3,teach4])
# session.commit()


stud1= Student(stud_first_name='Tinashe',stud_last_name='Kachingwe',age=20,gender='F',grade='B')
stud2 = Student(stud_first_name='Chilombo',stud_last_name='Efuru',age=22,gender='F',grade='C')
stud3 = Student(stud_first_name='Brent',stud_last_name='Faiyaz',age=19,gender='M',grade='B')
stud4 = Student(stud_first_name='Solange',stud_last_name='Knowles',age=20,gender='F',grade='A')
stud5 = Student(stud_first_name='Donald',stud_last_name='Glover',age=20,gender='M',grade='A')
stud6 = Student(stud_first_name='John',stud_last_name='Legend',age=25,gender='M',grade='D')
stud7 = Student(stud_first_name='Ella',stud_last_name='Mai',age=21,gender='F',grade='A')
stud8 = Student(stud_first_name='Daniel',stud_last_name='Ceaser',age=19,gender='M',grade='B')
stud9 = Student(stud_first_name='Teyana',stud_last_name='Taylor',age=20,gender='F',grade='B')

# session.add_all([stud1,stud2,stud3,stud4,stud5,stud6,stud7,stud8,stud9])
# session.commit()

class1 = Class(class_title='Pure Mathematics',teacher_id=teach1.teacher_id, stud_id=stud1.stud_id,start_time='9.00 AM',end_time='11.00AM')
class2 = Class(class_title='Thermodynamics',teacher_id=teach1.teacher_id, stud_id=stud1.stud_id,start_time='1.00 PM',end_time='3.00PM')
class3 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud1.stud_id,start_time='7.00 AM',end_time='10.00AM')
class4 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud2.stud_id,start_time='7.00 AM',end_time='10.00AM')
class5 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud3.stud_id,start_time='7.00 AM',end_time='10.00AM')
class6 = Class(class_title='Literature',teacher_id=teach3.teacher_id, stud_id=stud5.stud_id,start_time='8.00 AM',end_time='10.00AM')


# session.add_all([class1,class2,class3,class4,class5,class6])
# session.commit()

    
def main(session):
    

    print("Welcome to the School Management System")

    while True:
        print("Choose your role:")
        print("1. Teacher")
        print("2. Student")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print("You are logged in as a Teacher.")
            teacher_actions(session)
            break
        elif choice == "2":
            print("You are logged in as a Student.")
            student_actions(session)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter '1' for Teacher, '2' for Student, or '3' to quit.")

    session.close()
# session.close()

# if __name__ == "__main__":
#     # Example usage for a specific student or teacher

# print(class1.get_timetable(session,student_id=1))
# print(stud1.get_student_grades(session))
# print(Student.get_available_classes(session))
# # stud5.enroll_in_class(session,class_title='Computer Systems')
# teach1.change_student_grade(session,student_id=1,new_grade='A')

if __name__ == "__main__":
    main(session)




