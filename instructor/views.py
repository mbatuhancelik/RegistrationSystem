from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from runSQL import run_statement
from . import forms


def index(req):
    if req.session["type"] != "instructor":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False') 
    
    # Check if timeslot input is valid
    isValid=req.GET.get("fail",False)

    classroom = forms.classroomTimeFilterForm()
    return render(req,'homepage_instr.html',{"form":classroom,"action_fail":isValid})

def viewClassrooms(req):

    ts = req.GET.get('timeslot')

    # Select Available Classrooms for the given timeslot 
    result = run_statement(f"""
    SELECT classroom.classroom_id, classroom.campus, classroom.capacity 
    FROM classroom where classroom_id not in (
    select classroom.classroom_id from classroom inner join location on classroom.classroom_id = location.classroom_id and location.timeslot= {ts} );""")

    return render(req,'viewClassrooms.html',{"results":result})

def filterClassrooms(req):

    if req.POST['timeslot'] == '':# Timeslot empty!
        ts = -1
    else:
        ts = int(req.POST['timeslot'])

    if ts < 1 or ts > 10:# Timeslot is invalid!
        return HttpResponseRedirect('.?fail=true')
    else:

        return HttpResponseRedirect(f"./viewClassrooms?timeslot={ts}")