from django import forms

instructorFormFields = ["username", "email", "password", "name", "surname", "department","title"]
studentFormFields = ["username", "email", "password", "name", "surname", "department","studentId"]
classroomFormFields = ["classroom_id", "campus", "capacity"]

class classroomTimeFilterForm(forms.Form):
    timeslot = forms.IntegerField()