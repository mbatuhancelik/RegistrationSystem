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

def viewStudents(req):
    result = run_statement("""
    Select student.student_id, user.username, user.name, surname, email, department_id, completed_credits, gpa from 
    student inner join user on  student.username=user.username""")

    delete = forms.DeleteStudentForm()
    return render(req,'viewStudents.html',{"results":result,"form":delete})

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

def deleteInstructor(req):
    user_result = run_statement(f"delete from user where username = \"{req.POST['username']}\";" )
    
    #in successful execution, user and student result returns empty tuple
    return HttpResponseRedirect("./viewInstructors")

def viewInstructors(req):
    result = run_statement("""
    select user.username, name , surname, email, department_id, title from user inner join instructor on user.username = instructor.username""")

    delete = forms.DeleteInstructorForm()
    return render(req,'viewInstructors.html',{"results":result,"form":delete})