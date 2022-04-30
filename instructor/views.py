from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from mysqlx import Session
from runSQL import run_statement
from . import forms
import string

def index(req):
    try:
        req.session["type"]
    except:# No active session exists 
        req.session["type"] = "Guest"

    if req.session["type"] != "instructor":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False') 
    
    # Check if timeslot input is valid
    isValid=req.GET.get("fail",False)

    classroom_form = forms.classroomTimeFilterForm()
    return render(req,'homepage_instr.html',{"form":classroom_form,"action_fail":isValid})

def viewClassrooms(req):

    ts = req.GET.get('timeslot')

    # Select Available Classrooms for the given timeslot 
    result = run_statement(f"""
    SELECT classroom.classroom_id, classroom.campus, classroom.capacity 
    FROM classroom where classroom_id not in (
    select classroom.classroom_id from classroom inner join location on classroom.classroom_id = location.classroom_id and location.timeslot= {ts} );""")

    classroom_headers = ["Classroom ID", "Campus", "Classroom Capacity"]
    return render(req,'viewDataList.html',{"results":result, "header_list":classroom_headers})

def filterClassrooms(req):

    if req.POST['timeslot'] == '':# Timeslot empty!
        ts = -1
    else:
        ts = int(req.POST['timeslot'])

    if ts < 1 or ts > 10:# Timeslot is invalid!
        return HttpResponseRedirect('.?fail=true')
    else:

        return HttpResponseRedirect(f"./viewClassrooms?timeslot={ts}")

def addCourseForm(req):
    
    if req.session["type"] != "instructor":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False')

    isFailed=req.GET.get("fail",False)

    # """ TODO: success alert
    # {% if addSuccess %}
    # <div class="alert alert-success" role="alert">
    #     <h4 class="alert-heading">Login Failed</h4>
    #     <p>Your username or password is not correct</p>
    # </div>
    # {% endif %}
    # """
    course_form = forms.AddCourseForm()

    return render(req, "addCourseForm.html",{"form":course_form, "fail":isFailed} )

def addCourse(req):
    data = {}
    for i in range(len(forms.courseFormFields)):
        if forms.courseFormFieldsType[i] == string:
            data[forms.courseFormFields[i]] =  f"\"{req.POST[forms.courseFormFields[i]]}\""
        else:
            data[forms.courseFormFields[i]] =  f"{req.POST[forms.courseFormFields[i]]}"

    lecturer = f"\"{req.session['username']}\""

    course_result = run_statement(f"INSERT INTO course VALUES({data['courseID']},{data['name']},{data['credits']},{data['quota']},{lecturer});")
    location_result = run_statement(f"INSERT INTO location VALUES({data['courseID']},{data['classroomID']},{data['timeslot']});")
    
    return HttpResponseRedirect("./addCourseForm")

def addPreqForm(req):
    
    if req.session["type"] != "instructor":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False')

    isFailed=req.GET.get("fail",False)
    preq_form = forms.AddPreqForm()

    return render(req, "addPreqForm.html",{"form":preq_form, "fail":isFailed } )

def addPreq(req):
    data = {}
    for field in forms.preqFormFields:
        data[field] =  f"\"{req.POST[field]}\""


    preq_result = run_statement(f"INSERT INTO prerequisite_of VALUES({data['courseID']},{data['preq_courseID']});")
    
    return HttpResponseRedirect("./addPreqForm")

def viewCourses(req):
    
    lecturer = f"\"{req.session['username']}\""
    # Select Courses given by  
    result = run_statement(f"""
    SELECT courses.course_id, courses.name, courses.classroom_id, courses.timeslot, courses.quota, preqs.preq_list FROM
    (
        SELECT  course.course_id, course.name, location.classroom_id, location.timeslot, course.quota FROM 
        course INNER JOIN location 
        on course.course_id=location.course_id where lecturer = {lecturer}
    ) AS courses
    LEFT JOIN
    (
        SELECT main,group_concat(prerequisite)as preq_list FROM 
        prerequisite_of INNER JOIN course
        on course.course_id=prerequisite_of.main GROUP BY main
    ) AS preqs
    ON courses.course_id=preqs.main 
    """)

    course_headers = ["CourseID", "Course Name", "ClassroomID", "Timeslot", "Quota", "Prerequisite List"]
    return render(req,'viewDataList.html',{"results":result, "header_list":course_headers})