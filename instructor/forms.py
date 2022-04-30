from django import forms

instructorFormFields = ["username", "email", "password", "name", "surname", "department","title"]
studentFormFields = ["username", "email", "password", "name", "surname", "department","studentId"]
classroomFormFields = ["classroom_id", "campus", "capacity"]

class classroomTimeFilterForm(forms.Form):
    # classroom_id = forms.CharField(widget=forms.TextInput())
    # campus = forms.CharField(widget=forms.TextInput())
    # capacity = forms.IntegerField()
    timeslot = forms.IntegerField()