from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Leave_Request, Profile
from django.contrib.auth.models import User 
from .forms import EmpForm, Leave_Request_Form, Update_Profile_Form
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from employee.utils import send_email
from django.http import HttpResponseForbidden
#from django.contrib.sites.models import Site

# Create your views here.

def landing_page(request):
    return render(request,'employee/landing.html',{})


def employee_list(request):
    
    employees =  Employee.objects.all()
    return render(request,'employee/employee_list.html',{'employees':employees})
    #return render(request,'employee/employee_list.html',{})

def about(request):
    return render(request, 'employee/about.html',{})


@login_required
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

@login_required
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


@login_required
def profile_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    profile = get_object_or_404(Profile,employee=emp)
    if request.method == "POST":
        form = Update_Profile_Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('emp_profile', pk)
    else:
        form = Update_Profile_Form(instance=profile)
    return render(request, 'employee/profile_edit.html', {'form': form, 'emp':emp})




def user_profile(request):
    
    emp = get_object_or_404(Employee, username=request.user.username)
    #emp = Employee.objects.filter(username=request.user.username).first()
    #return render(request, 'employee/emp_profile.html', {'emp':emp})
    return redirect('emp_profile', emp.empID)
    #return render(request,'employee/test.html',{})


def emp_profile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    leave_requests = Leave_Request.objects.filter(employee=emp)
    employees = Employee.objects.filter(manager=emp)
    #emp = Employee.objects.filter(pk=pk).first()
    return render(request, 'employee/emp_profile.html', {'emp':emp, 'leave_requests':leave_requests, 'employees':employees})


def emp_remove(request,pk):
    
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    else:
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
                return redirect("landing_page")
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

@login_required
def leave_request(request):
    if request.method == "POST":
            form = Leave_Request_Form(request.POST)
            if form.is_valid():
                leave_request = form.save(commit=False)
                emp = get_object_or_404(Employee, username=request.user.username)
                leave_request.employee = emp
                leave_request.status = 'Pending'
                leave_request.save()
                
                #Send email to manager with leave request
                subject =f"{emp.fName} {emp.lName} Is Requesting Time Off (Request#{leave_request.pk}"
                message = f"{emp.fName} {emp.lName} has requested time off for {leave_request.start_date} to {leave_request.end_date}. Go to this link to approve or reject \n" +str(request.get_host())+"/leave/detail/"+str(leave_request.pk)
                manager= emp.manager
                send_email(subject,message, [manager.email])
                messages.info(request, f"Request has been sent to {manager.fName} {manager.lName}.")
                
                return redirect('leave_list')
    else:
        form = Leave_Request_Form()
    return render(request, 'employee/leave_request.html', {'form': form})


def leave_list(request):
    leave_requests =  Leave_Request.objects.all()
    return render(request,'employee/leave_list.html',{'leave_requests':leave_requests})


def leave_detail(request, pk):
    leave_request = get_object_or_404(Leave_Request, pk=pk)
    return render(request, 'employee/leave_detail.html', {'leave_request':leave_request})

def leave_approve(request, pk):
    leave_request = get_object_or_404(Leave_Request, pk=pk)
    leave_request.status = 'Approved'
    leave_request.save()
    
    emp = leave_request.employee
    
    subject =f"Time off has been Approved (Request#{leave_request.pk})"
    message = f"Time off for {leave_request.start_date} to {leave_request.end_date} has been Approved \nClick here to view leave request: \n" +str(request.get_host())+"/leave/detail/"+str(leave_request.pk)
    
    send_email(subject,message, [emp.email])
    
    
    messages.success(request, "Time off has been Approved")
    return redirect('leave_detail', pk=pk)


def leave_reject(request, pk):
    leave_request = get_object_or_404(Leave_Request, pk=pk)
    leave_request.status = 'Rejected'
    leave_request.save()
    
    emp = leave_request.employee
    
    subject =f"Time off has been Rejected (Request#{leave_request.pk})"
    message = f"Time off for {leave_request.start_date} to {leave_request.end_date} has been Rejected \nClick here to view leave request: \n" +str(request.get_host())+"/leave/detail/"+str(leave_request.pk)
    
    send_email(subject,message, [emp.email])
    
    messages.success(request, "Time off has been Rejected")
    return redirect('leave_detail', pk=pk)


def leave_delete(request,pk):
    leave_request = get_object_or_404(Leave_Request, pk=pk)
    if leave_request.employee != request.user.employee:
        return HttpResponseForbidden()
    
    leave_request.delete()
    return redirect('leave_list')