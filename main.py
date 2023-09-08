from app import session
from app import Student
from app import Class
from app import Teacher

def teacher_actions(session):
    while True:
        print("Teacher Actions:")
        print("1. Change Student Grade")
        print("2. Check timetable")
        print("3. Add class (an student)")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            student_id = int(input("Enter the student's ID: "))
            new_grade = input("Enter the new grade: ")
            Teacher.change_student_grade(session, student_id, new_grade)
            print("Grade changed")
        

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
            stud_id = input("Enter student ID: ")
            start_time = input("Enter start time: ")
            end_time = input("Enter end time: ")

            teacher = session.query(Teacher).filter_by(teacher_first_name=teacher_name.split()[0], teacher_last_name=teacher_name.split()[1]).first()
            student = session.query(Student).filter_by(stud_id=stud_id).first()
            

            if teacher and student:
                teacher.add_class(session, class_title, start_time, end_time, stud_id)
                print("Class and student added successfully.")
            elif teacher:
                teacher.add_class(session, class_title, start_time, end_time)
                print("Class added successfully.")                    
            else:
                print("Teacher not found.")

        
        # elif choice == "4":
        #     teacher_name = input("Enter teacher's full name (e.g., 'George West'): ")
        #     class_id = int(input("Enter the class ID: "))
        #     student_id = int(input("Enter the student's ID: "))

        #     teacher = session.query(Teacher).filter_by(teacher_first_name=teacher_name.split()[0], teacher_last_name=teacher_name.split()[1]).first()

        #     teacher.add_student_to_class(session, student_id, class_id)

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid input.")


def student_actions(session):
    while True:
        print("Student Actions:")
        print("1. Check my Grade")
        print("2. Check availabe classes")
        print("3. Check timetable")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            student_name = input("Enter student's full name: ")
            student = session.query(Student).filter_by(stud_first_name=student_name.split()[0], stud_last_name=student_name.split()[1]).first()
            if student:
                my_grade= student.grade
                print(f"Name:{student_name} Grade:{my_grade}")
        elif choice == "2":
            student_name = input("Enter student's full name: ")
            student = session.query(Student).filter_by(stud_first_name=student_name.split()[0], stud_last_name=student_name.split()[1]).first()
            if student:
                available_classes = student.get_available_classes(session)  
                for available_class in available_classes:
                    print(available_class)

        elif choice == "3":
            student_input_id = input("Enter student's id: ")
            # Retrieve the teacher based on the input name
            student = session.query(Class).filter_by(stud_id=student_input_id).first()

            if student:
                timetable = student.get_timetable(session)
                if timetable:
                    print("Timetable:")
                    for entry in timetable:
                        print(f"Class Title: {entry['class_title']}")
                        print(f"Start Time: {entry['start_time']}")
                        print(f"End Time: {entry['end_time']}")
                        print()
                else:
                    print("No classes found for this student.")
            else:
                print("Student not found.")
        
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid input.")



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
            break
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter '1' for Teacher, '2' for Student, or '3' to quit.")

    session.close()


if __name__ == "__main__":
    main(session)