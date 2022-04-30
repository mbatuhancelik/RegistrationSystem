from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from runSQL import run_statement
from . import forms

def index(req):
    if req.session["type"] != "dbmanager":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False') 
    
    return render(req,'homepage.html')

def addStudentForm(req):

    if req.session["type"] != "dbmanager":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False')
    isFailed=req.GET.get("fail",False)
    student_form = forms.AddStudentForm()

    return render(req, "addStudent.html",{"student_form":student_form, "addFailed":isFailed,"path":"addStudent"} )

def addStudent(req):

    data = {}
    for field in forms.studentFormFields:
        data[field] =  f"\"{req.POST[field]}\""

    user_result = run_statement(f"INSERT INTO user VALUES({data['username']},{data['email']},sha2({data['password']},256),{data['name']},{data['surname']},{data['department']});" )
    student_result = run_statement(f"INSERT INTO student(username,student_id) VALUES({data['username']},{data['studentId']});" )
    
    #in successful execution, user and student result returns empty tuple
    return HttpResponseRedirect("./addStudentForm")

def deleteStudent(req):
    user_result = run_statement(f"delete from user where username in (select username from student where student.student_id = {req.POST['studentId']});" )
    
    #in successful execution, user and student result returns empty tuple
    return HttpResponseRedirect("./viewStudents")

def getStudent(req):
    return HttpResponseRedirect(f"./viewStudents?studentId={req.POST['studentId']}")

def viewStudents(req):
    result = run_statement("""
    Select student.student_id, user.username, user.name, surname, email, department_id, completed_credits, gpa from 
    student inner join user on  student.username=user.username order by  completed_credits ASC""")

    student=req.GET.get("studentId")
    grades = None
    if student:
        grades = run_statement(f"select course_id, course_id, grade from grades inner join student on grades.student_id = student.student_id where student.student_id = {student}" )
    delete = forms.GetStudentForm()
    return render(req,'viewStudents.html',{"results":result,"form":delete,"student":student,"grades":grades })

def addInstructorForm(req):
    
    if req.session["type"] != "dbmanager":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False')

    isFailed=req.GET.get("fail",False)
    instructor_form = forms.AddInstructorForm()

    return render(req, "addInstructor.html",{"form":instructor_form, "addFailed":isFailed} )

def addInstructor(req):

    data = {}
    for field in forms.instructorFormFields:
        data[field] =  f"\"{req.POST[field]}\""
    user_result = run_statement(f"INSERT INTO user VALUES({data['username']},{data['email']},sha2({data['password']},256),{data['name']},{data['surname']},{data['department']});")
    student_result = run_statement(f"INSERT INTO instructor VALUES({data['username']},{data['title']});")
    
    #in successful execution, user and student result returns empty tuple
    return HttpResponseRedirect("./addInstructorForm")

def updateInstructor(req):
    user_result = run_statement(f"update instructor set title = \"{req.POST['title']}\" where username = \"{req.POST['username']}\";" )
    
    #in successful execution, user and student result returns empty tuple
    return HttpResponseRedirect("./viewInstructors")

def viewInstructors(req):
    result = run_statement("""
    select user.username, name , surname, email, department_id, title from user inner join instructor on user.username = instructor.username""")

    update = forms.UpdateInstructorForm()
    return render(req,'viewInstructors.html',{"results":result,"form":update})

def getCoursesOfInstructor(req):
    return HttpResponseRedirect(f"./viewCoursesOfInstructor?instructor={req.POST['username']}")

def viewCoursesOfInstructor(req):

    instructor=req.GET.get("instructor")
    result = None
    if instructor: 
        result = run_statement(f"""
        select course_id,  name, l.classroom_id, campus, timeslot from classroom inner join 
        (select c.course_id,c.name,  location.timeslot, location.classroom_id from location  inner join
        (select * from course where lecturer = \"{instructor}\") as c on 
        c.course_id = location.course_id) as l 
        on l.classroom_id = classroom.classroom_id; """)

    form = forms.GetInstructorForm()
    return render(req,'coursesOfInstructor.html',{"courses":result,"form":form,"instructor":instructor })


def getGradeAverage(req):
    return HttpResponseRedirect(f"./viewGradeAverage?courseId={req.POST['courseId']}")

def viewGradeAverage(req):

    course=req.GET.get("courseId")
    result = None
    if course: 
        result = run_statement(f"""
        select c.course_id, name, avg   from course inner join (select course_id, avg(grade) as avg from grades 
        where course_id = \"{course}\") as c 
        on c.course_id = course.course_id; """)

    form = forms.GetCourseForm()
    return render(req,'gradeAverage.html',{"result":result,"form":form })