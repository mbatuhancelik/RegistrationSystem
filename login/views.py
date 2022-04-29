from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)

from django.db import connection

def run_statement(statement):
    cursor= connection.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def index(req):
    if req.session:
        req.session.flush()
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'loginIndex.html',{"login_form":loginForm,"action_fail":isFailed})

def databaseManagerLogin(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM databasemanager WHERE username='{username}' and password= sha2('{password}',256);") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"] = username
        req.session["type"] = "dbmanager"
        return HttpResponseRedirect('../login') #TODO:Redirect user to home page
    else:
        return HttpResponseRedirect('../login?fail=true')

def lecturerLogin(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM user WHERE username='{username}' and  password=sha2('{password}',256) and username in (Select username from instructor);") #Run the query in DB
    if result: #If a result is retrieved
        req.session["username"] = username
        req.session["type"] = "instructor"
        return HttpResponseRedirect('../login') #TODO:Redirect user to home page
    else:
        return HttpResponseRedirect('../login?fail=true')

def studentLogin(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM user WHERE username='{username}' and  password=sha2('{password}',256) and username in (Select username from student);") #Run the query in DB
    if result: #If a result is retrieved
        req.session["username"] = username
        req.session["type"] = "student"
        return HttpResponseRedirect('../login') #TODO:Redirect user to home page
    else:
        return HttpResponseRedirect('../login?fail=true')
