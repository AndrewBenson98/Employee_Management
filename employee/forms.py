from django import forms
from .models import Employee, Leave_Request

class EmpForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ('fName','lName','title', 'salary','manager','deptID')


class DateInput(forms.DateInput):
    input_type='date'

class Leave_Request_Form(forms.ModelForm):
    
    class Meta:
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        model = Leave_Request
        fields = ('start_date', 'end_date')