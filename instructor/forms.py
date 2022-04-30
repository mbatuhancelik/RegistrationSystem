import string
from django import forms

courseFormFields = ["courseID", "name", "credits", "classroomID", "timeslot", "quota"]
courseFormFieldsType = [string, string, int, string, int, int]
preqFormFields = ["courseID", "preq_courseID"]

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