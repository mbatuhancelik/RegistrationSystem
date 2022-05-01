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

def searchCourse(req):
    return HttpResponseRedirect(f"./courses?search={req.POST['keyword']}")

def coursesPage(req ,courses):
    return render(req,'viewCourses.html',{"courses":courses,
                                            "form": forms.GetCourseForm(),
                                            "searchForm":forms.SearchCourseForm(),
                                            "filterForm": forms.FilterCourseForm()
                                            }) 
def appendPrerequisites(courses):
    if len(courses) != 0:
        for i in range(len(courses)):
            courses[i] = list(courses[i])
            
            preqs = list(run_statement(f"""select prerequisite from prerequisite_of where main = "{courses[i][0]}";"""))

            preqs_string =  ""
            for p in preqs:
                preqs_string += p[0] + ","
            
            courses[i].append(preqs_string[:-1])
            courses[i] = tuple(courses[i])
    return tuple(courses)

def listCourses(req):
    query = """select course_id, cl.name, surname, department_id, credits from user inner join 
                    (select * from course inner join instructor on course.lecturer = instructor.username) as cl
                    on user.username = cl.username"""

    if req.GET.get("search"):
        query += f"  where cl.name LIKE '%{req.GET.get('search')}%'"
    courses = appendPrerequisites( list(run_statement(query)) )    

    return coursesPage(req, courses)


def transcript(req):

    takenCourses = list(run_statement(f"""SELECT grades.course_id, name,  grade FROM 
    grades inner join course on grades.course_id = course.course_id
    where student_id = {req.session["studentId"]};"""))
    
    enrolledCourses = list(run_statement(f"""SELECT course.course_id, name FROM 
    enrolled_in inner join course on enrolled_in.course_id = course.course_id;
    where student_id = {req.session["studentId"]};"""))

    enrolledCourses += takenCourses

    return render(req,'transcript.html',{"courses":enrolledCourses})

def filterCourses(req):
    department = req.POST['department']
    minCredits = req.POST['minCredits']
    maxCredits = req.POST['maxCredits']

    if not minCredits:
        minCredits = run_statement("select min(credits) from course;")[0][0]
    if not maxCredits:
        maxCredits = run_statement("select max(credits) from course;")[0][0]
    if not department:
        department = ''

    result = run_statement(f"call filterCourses('{department}', {minCredits}, {maxCredits});select min(credits) from course;")
    courses = appendPrerequisites( list(result))

    return coursesPage(req, courses)


