from django import forms
from .models import Employee

class EmpForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ('fName','lName','title', 'salary','manager','deptID')
