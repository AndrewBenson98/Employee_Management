from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField
from employee.utils import create_new_ref_number, generateTempPassword
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
    deptID = models.CharField(primary_key=True, max_length=4)
    deptName = models.CharField("name",max_length=25, unique=True, null=True)
    
    def __str__(self):
        return self.deptName

class Employee(models.Model):

    empID = models.CharField("Employee ID",primary_key=True, max_length=8, unique=True, default=create_new_ref_number)
    fName = models.CharField("first name",max_length=25, null=True, blank=True) 
    lName = models.CharField("last name",max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    hireDate = models.DateField("Date joined",auto_now_add=True, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    deptID = models.ForeignKey( Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="department")
    user = models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True, unique=True)
    username = models.CharField("username",max_length=50, null=True, blank=True) 
    description = models.TextField(max_length=255, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        #Create new user
        #Check if user exists
        if not User.objects.filter(username=self.username).exists():
            self.username = self.fName + self.lName +self.empID[4:]
            #Uncomment for prod
            #self.email = self.fName+'.'+self.lName+''+self.empID[4:]+'@gmail.com'
            self.email = 'andrew.benson.testmail+'+self.fName+''+self.lName+'@gmail.com'
            User.objects.create_user(username=self.username,email=self.email, password=generateTempPassword())
            #Set the user
            self.user = User.objects.get(username=self.username)
        
        super(Employee, self).save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.fName} {self.lName}"
    


