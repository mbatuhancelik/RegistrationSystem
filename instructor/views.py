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
    isValid_classroom=req.GET.get("classroom_fail",False)
    # Check if course input for student list is valid
    isValid_students=req.GET.get("students_fail",False)

    classroom_form = forms.classroomTimeFilterForm()
    student_form = forms.ViewStudentsOfForm()
    courseName_form = forms.CourseNameForm()
    return render(req,'homepage_instr.html',{"classroom_form":classroom_form, "student_form":student_form, "courseName_form":courseName_form,"classroom_fail":isValid_classroom, "students_fail":isValid_students})

def viewClassrooms(req):

    ts = req.GET.get('timeslot')

    # Select Available Classrooms for the given timeslot 
    result = run_statement(f"""
    SELECT classroom.classroom_id, classroom.campus, classroom.capacity 
    FROM classroom where classroom_id not in (
    select classroom.classroom_id from classroom inner join location on classroom.classroom_id = location.classroom_id and location.timeslot= {ts} );""")

    classroom_headers = ["Classroom ID", "Campus", "Classroom Capacity"]
    title = f"Available Classrooms for Timeslot {ts}"
    return render(req,'viewDataList.html',{"results":result, "header_list":classroom_headers, "title": title, "gotForm":False })

def filterClassrooms(req):

    if req.POST['timeslot'] == '':# Timeslot empty!
        ts = -1
    else:
        ts = int(req.POST['timeslot'])

    if ts < 1 or ts > 10:# Timeslot is invalid!
        return HttpResponseRedirect('.?classroom_fail=true')
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
    # Add course with given parameters
    course_result = run_statement(f"INSERT INTO course VALUES({data['courseID']},{data['name']},{data['credits']},{data['quota']},{lecturer});")
    location_result = run_statement(f"INSERT INTO location VALUES({data['courseID']},{data['classroomID']},{data['timeslot']});")
    
    return HttpResponseRedirect("./addCourseForm")

def addPreqForm(req):
    # TODO: This can be moved to the index instructor page
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
    # Add prerequisites for give course
    preq_result = run_statement(f"INSERT INTO prerequisite_of VALUES({data['courseID']},{data['preq_courseID']});")
    
    return HttpResponseRedirect("./addPreqForm")

def viewCourses(req):
    
    lecturer = f"\"{req.session['username']}\""

    # Select Courses given by session lecturer
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
        ON courses.course_id=preqs.main ORDER BY courses.course_id  ASC
    """)

    course_headers = ["CourseID", "Course Name", "ClassroomID", "Timeslot", "Quota", "Prerequisite List"]
    return render(req,'viewDataList.html',{"results":result, "header_list":course_headers, "gotForm":False})

def viewStudentsForCourse(req):
    # TODO: ADD GRADE FUNCTION IS WORKING BUT NOT ABLE TO SHOW GRADES ON TABLE

    course = req.GET.get('course')
    # Select students of given course 
    result = run_statement(f"""
        SELECT user.username, student.student_id, user.email, user.name, user.surname, "-" as grade FROM
        user INNER JOIN student
        ON user.username=student.username 
        WHERE student.student_id IN (SELECT student_id FROM enrolled_in WHERE course_id = '{course}');
    """)

    student_headers = ["Username", "studentID", "email", "Name", "Surname", "Grade"]
    title = f"Students Of {course}"
    addGradeForm = forms.addGradeForm
    return render(req,'viewDataList.html',{"results":result, "header_list":student_headers, "title": title, "gotForm":True, "addGradeForm":addGradeForm})


def viewStudentsForm(req):

    if req.POST['courseID'] == '':# courseID empty!
        course = None
    else:
        course = req.POST['courseID']

    # Checking if the course belongs to the session lecturer
    lecturer = f"\"{req.session['username']}\""
    lecturer_check = run_statement(f"select * from course where course_id = '{course}' and lecturer = {lecturer}")

    if len(lecturer_check) <= 0 or course == None:#   course doesn't belong to this lecturer or empty course name, invalid action
        return HttpResponseRedirect('.?students_fail=true')
    else:
        return HttpResponseRedirect(f"./viewStudentsForCourse?course={course}")

def updateCourseName(req):
    data = {}
    for field in forms.courseNameFields:
        data[field] =  f"\"{req.POST[field]}\""

    # Checking if the course belongs to the session lecturer
    lecturer = f"\"{req.session['username']}\""
    lecturer_check = run_statement(f"select * from course where course_id = {data['courseID']} and lecturer = {lecturer}")

    if len(lecturer_check) <= 0:#   course doesn't belong to this lecturer or empty course name, invalid action
        return HttpResponseRedirect('.?students_fail=true')
    else:
        # Update course name
        nameUpdate_result = run_statement(f"UPDATE course SET name = {data['name']} WHERE course.course_id={data['courseID']} ;")
        return HttpResponseRedirect(f"./")

def addGrade(req):
    # TODO: ADD GRADE FUNCTION IS WORKING BUT NOT ABLE TO SHOW GRADES ON TABLE

    # Checking if the course belongs to the session lecturer
    lecturer = f"\"{req.session['username']}\""
    lecturer_check = run_statement(f"select * from course where course_id = '{req.POST['courseID']}' and lecturer = {lecturer}")

    if len(lecturer_check) <= 0:#   course doesn't belong to this lecturer or empty course name, invalid action
        return HttpResponseRedirect('.?students_fail=true')
    else:
        # Add grade for the given student on given course
        addGrade_result = run_statement(f"INSERT INTO grades VALUES ({req.POST['studentID']},'{req.POST['courseID']}', {req.POST['grade']});")
        return HttpResponseRedirect(f"./viewStudentsForCourse?course={req.POST['courseID']}")
