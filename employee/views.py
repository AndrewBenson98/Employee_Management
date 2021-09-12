from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib.auth.models import User 
from .forms import EmpForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout 

# Create your views here.

def landing_page(request):
    return render(request,'employee/landing.html',{})

def employee_list(request):
    
    employees =  Employee.objects.all()
    return render(request,'employee/employee_list.html',{'employees':employees})


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


def user_profile(request):
    
    emp = get_object_or_404(Employee, username=request.user.username)
    #emp = Employee.objects.filter(username=request.user.username).first()
    #return render(request, 'employee/emp_profile.html', {'emp':emp})
    return redirect('emp_profile', emp.empID)
    #return render(request,'employee/test.html',{})

def emp_profile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    #emp = Employee.objects.filter(pk=pk).first()
    return render(request, 'employee/emp_profile.html', {'emp':emp})


def emp_remove(request,pk):
    emp = get_object_or_404(Employee, pk=pk)
    
    # TO DO: Delete user also
    try:
        u = User.objects.get(username=emp.username)
        u.delete()
        emp.delete()
        return redirect('employee_list')
    #messages.success(request, "The user is deleted")            

    # except User.DoesNotExist:
    #     messages.error(request, "User does not exist")    
    #     #return redirect('employeeList')

    except Exception as e: 
        messages.error(request, "There is an exception")
        return redirect('employee_list')
    
    
    

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            
            #TO DO Write function to check that username and password is right
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("employee_list")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="employee/login.html", context={"login_form":form})
    
def logout_request(request):
    #user= request.user
    logout(request)
    return redirect('login_request')