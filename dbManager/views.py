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