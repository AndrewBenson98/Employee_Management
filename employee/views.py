from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib.auth.models import User 
from .forms import EmpForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import login, authenticate 

# Create your views here.
def employeeList(request):
    
    employees =  Employee.objects.all()
    return render(request,'employee/employeeList.html',{'employees':employees})


def emp_new(request):
    if request.method == "POST":
        form = EmpForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.save()
            return redirect('emp_profile', emp.empID)
        
    else:
        form = EmpForm()
    return render(request, 'employee/emp_edit.html', {'form': form})

def emp_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmpForm(request.POST, instance=emp)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.save()
            return redirect('emp_profile', pk)
    else:
        form = EmpForm(instance=emp)
    return render(request, 'employee/emp_edit.html', {'form': form})


def emp_profile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    #emp = Employee.objects.filter(pk=pk).first()
    return render(request, 'employee/emp_profile.html', {'emp':emp})

def emp_remove(request,pk):
    emp = get_object_or_404(Employee, pk=pk)
    emp.delete()
    return redirect('employeeList')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("employeeList")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="employee/login.html", context={"login_form":form})