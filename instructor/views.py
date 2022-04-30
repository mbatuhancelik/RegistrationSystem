from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from runSQL import run_statement
from . import forms


def index(req):
    if req.session["type"] != "instructor":
        req.session.flush()
        return HttpResponseRedirect('../login?unAuth=False') 
    
    isFailed=req.GET.get("fail",False)
    print (isFailed)
    classroom = forms.classroomTimeFilterForm()
    return render(req,'homepage_instr.html',{"form":classroom,"action_fail":isFailed})

def viewClassrooms(req):

    ts = req.GET.get('timeslot')

    if ts != None:
        result = run_statement(f"""
        SELECT classroom.classroom_id, classroom.campus, classroom.capacity 
        FROM classroom where classroom_id not in (
        select classroom.classroom_id from classroom inner join location on classroom.classroom_id = location.classroom_id and location.timeslot= {ts} );""")
    else:
        # Get classrooms that are available, not reserved by a course

        #this shows all classrooms for now
        # we can modify this such that it only shows all available classrooms
        result = run_statement( """
        SELECT classroom.classroom_id, classroom.campus, classroom.capacity, timeslot 
        FROM classroom left join location on classroom.classroom_id = location.classroom_id ;""")

    return render(req,'viewClassrooms.html',{"results":result})

def filterClassrooms(req):
    print(req.POST['timeslot'])
    if req.POST['timeslot'] == '':
        ts = -1
    else:
        ts = int(req.POST['timeslot'])

    if ts < 1 or ts > 10:
        return HttpResponseRedirect('.?fail=true')
    else:

        return HttpResponseRedirect(f"./viewClassrooms?timeslot={ts}")