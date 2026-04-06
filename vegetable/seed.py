from faker import Faker
fake=Faker()
import random
from .models import *
from django.db.models import Sum

def create_subject_marks():
    try:
        stu_name=Student.objects.all()
        for stu in stu_name:
            subjects=Subject.objects.all()
            for sub in subjects:
                SubjectMarks.objects.create(
                    subject=sub,
                    student=stu,
                    marks=random.randint(0,100)
                    )
    except Exception as e:
        print(e)

def seed_db(n=10)->None:
    try:
        for i in range(0,n):
            departments_objs=Department.objects.all()
            random_index=random.randint(0,len(departments_objs)-1)
            department=departments_objs[random_index]
            student_id=f"Stu{random.randint(4,100)}"
            name=fake.name()
            email=fake.email()
            age=random.randint(15,25)
            address=fake.address()

            student_id_obj=StudentID.objects.create(student_id=student_id)
            Student.objects.create(
                department=department,
                student_id=student_id_obj,

                name=name,
                email=email,
                age=age,
                address=address,
            )
    except Exception as e:
        print(e)

def generate_reportcard():
    current_rank=-1
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-age')
    i=1
    for rank in ranks:
        Reportcard.objects.create( student=rank,
                student_rank=i)
        i+=1