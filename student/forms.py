from django import forms


class GetCourseForm(forms.Form):
    courseId = forms.CharField(widget=forms.TextInput())