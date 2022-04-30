from django.http import HttpResponseRedirect
from runSQL import run_statement
from django.shortcuts import render
from . import forms
# Create your views here.
def index(req):
    if req.session["type"] != "student":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False')
    return render(req,'studentHomepage.html')

def enrollCourse(req):
    
    run_statement(f"""
    insert into enrolled_in values({req.session['studentId']}, "{req.POST['courseId']}");
    """)

    return HttpResponseRedirect("./courses")


def courses(req):
    courses = list(run_statement("""select course_id, cl.name, surname, department_id, credits from user inner join 
                    (select * from course inner join instructor on course.lecturer = instructor.username) as cl
                    on user.username = cl.username"""))
    if len(courses) != 0:
        for i in range(len(courses)):
            courses[i] = list(courses[i])
            
            preqs = list(run_statement(f"""select prerequisite from prerequisite_of where main = "{courses[i][0]}";"""))

            preqs_string =  ""
            for p in preqs:
                preqs_string += p[0] + ","
            
            courses[i].append(preqs_string[:-1])
            courses[i] = tuple(courses[i])
    courses = tuple(courses)

    courseForm = forms.GetCourseForm()
    return render(req,'viewCourses.html',{"courses":courses,"form": courseForm})

def transcript(req):

    takenCourses = list(run_statement(f"""SELECT grades.course_id, name,  grade FROM 
    grades inner join course on grades.course_id = course.course_id
    where student_id = {req.session["studentId"]};"""))
    
    enrolledCourses = list(run_statement(f"""SELECT course.course_id, name FROM 
    enrolled_in inner join course on enrolled_in.course_id = course.course_id;
    where student_id = {req.session["studentId"]};"""))

    enrolledCourses += takenCourses

    return render(req,'transcript.html',{"courses":enrolledCourses})
