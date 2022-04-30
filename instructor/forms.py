import string
from django import forms

courseFormFields = ["courseID", "name", "credits", "classroomID", "timeslot", "quota"]
courseFormFieldsType = [string, string, int, string, int, int]
preqFormFields = ["courseID", "preq_courseID"]
courseNameFields = ["courseID", "name"]
addGradeFields = ["courseID", "studentID","grade"]

class classroomTimeFilterForm(forms.Form):
    timeslot = forms.IntegerField()

class AddCourseForm(forms.Form):
    courseID = forms.CharField(widget=forms.TextInput())
    name = forms.CharField(widget=forms.TextInput())
    credits = forms.IntegerField()
    classroomID = forms.CharField(widget=forms.TextInput())
    timeslot = forms.IntegerField()
    quota = forms.IntegerField()

class AddPreqForm(forms.Form):
    courseID = forms.CharField(widget=forms.TextInput())
    preq_courseID = forms.CharField(widget=forms.TextInput())

class ViewStudentsOfForm(forms.Form):
    courseID = forms.CharField(widget=forms.TextInput())

class CourseNameForm(forms.Form):
    courseID = forms.CharField(widget=forms.TextInput())
    name = forms.CharField(widget=forms.TextInput())

class addGradeForm(forms.Form):
    courseID = forms.CharField(widget=forms.TextInput())
    studentID = forms.IntegerField()
    grade = forms.FloatField()
