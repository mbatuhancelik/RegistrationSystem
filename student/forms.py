from django import forms


class GetCourseForm(forms.Form):
    courseId = forms.CharField(widget=forms.TextInput())

class SearchCourseForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput())

class FilterCourseForm(forms.Form):
    department = forms.CharField(widget=forms.TextInput() , required=False)
    minCredits = forms.IntegerField(required=False)
    maxCredits = forms.IntegerField(required=False)