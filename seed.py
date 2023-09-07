from app import session
from app import Class
from app import Teacher
from app import Student

# --- teachers
teach1 = Teacher(teacher_first_name='George',teacher_last_name='West',salary= 708000)
teach2 = Teacher(teacher_first_name='Dennis',teacher_last_name='Kimaita',salary= 1600100)
teach3 = Teacher(teacher_first_name='Doris',teacher_last_name='Gitonga',salary= 2000000)
teach4 = Teacher(teacher_first_name='Sasha',teacher_last_name='Mbulumo',salary= 401000)

session.add_all([teach1,teach2,teach3,teach4])
session.commit()


stud1= Student(stud_first_name='Tinashe',stud_last_name='Kachingwe',age=20,gender='F',grade='B')
stud2 = Student(stud_first_name='Chilombo',stud_last_name='Efuru',age=22,gender='F',grade='C')
stud3 = Student(stud_first_name='Brent',stud_last_name='Faiyaz',age=19,gender='M',grade='B')
stud4 = Student(stud_first_name='Solange',stud_last_name='Knowles',age=20,gender='F',grade='A')
stud5 = Student(stud_first_name='Donald',stud_last_name='Glover',age=20,gender='M',grade='A')
stud6 = Student(stud_first_name='John',stud_last_name='Legend',age=25,gender='M',grade='D')
stud7 = Student(stud_first_name='Ella',stud_last_name='Mai',age=21,gender='F',grade='A')
stud8 = Student(stud_first_name='Daniel',stud_last_name='Ceaser',age=19,gender='M',grade='B')
stud9 = Student(stud_first_name='Teyana',stud_last_name='Taylor',age=20,gender='F',grade='B')

session.add_all([stud1,stud2,stud3,stud4,stud5,stud6,stud7,stud8,stud9])
session.commit()

class1 = Class(class_title='Pure Mathematics',teacher_id=teach1.teacher_id, stud_id=stud1.stud_id,start_time='9.00 AM',end_time='11.00AM')
class2 = Class(class_title='Thermodynamics',teacher_id=teach1.teacher_id, stud_id=stud1.stud_id,start_time='1.00 PM',end_time='3.00PM')
class3 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud1.stud_id,start_time='7.00 AM',end_time='10.00AM')
class4 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud2.stud_id,start_time='7.00 AM',end_time='10.00AM')
class5 = Class(class_title='Computer systems',teacher_id=teach2.teacher_id, stud_id=stud3.stud_id,start_time='7.00 AM',end_time='10.00AM')
class6 = Class(class_title='Literature',teacher_id=teach3.teacher_id, stud_id=stud5.stud_id,start_time='8.00 AM',end_time='10.00AM')


session.add_all([class1,class2,class3,class4,class5,class6])
session.commit()

session.close()

