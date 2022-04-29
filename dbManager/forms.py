from django import forms


studentFormFields = ["Username", "Email", "Password", "Name", "Surname", "Department"]

class AddStudentForm(forms.Form):
     class Meta:
        fields = ["Username", "Email", "Password", "Name", "Surname", "Department"]
    # def __init__(self, *args, **kwargs):

    #     extra_fields = kwargs.pop('extra', 0)

    #     super(self).__init__(*args, **kwargs)
    #     for i in studentFormFields:
    #         self.fields[i] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': i }))