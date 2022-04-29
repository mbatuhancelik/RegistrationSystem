from django.http import HttpResponseBadRequest, HttpResponseRedirect
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
    
    student_form = forms.AddStudentForm

    return render(req, "addUser.html",{"student_form":student_form} )

def addStudent(req):

    data = {}
    for field in forms.studentFormFields:
        data[field] =  req.POST[field]

    result = run_statement(f"INSERT user VALUES({data['Username']},{data['Email']},sha2({data['Password']},256),{data['Name']},{data['Surname']},{data['Department']});")
    print(result)