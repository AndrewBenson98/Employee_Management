from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField, NullBooleanField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.http import request
from employee.utils import create_new_ref_number, generateTempPassword
from django.contrib.auth.models import User
from PIL import Image
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

    
    
    def save(self, *args, **kwargs):
        self.username = self.fName + self.lName +self.empID[4:]
        self.email = 'andrew.benson.testmail+'+self.fName+''+self.lName+'@gmail.com'
        super(Employee, self).save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.fName} {self.lName}"
    

class Profile(models.Model):
    employee = OneToOneField(Employee, on_delete=CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):

        super(Profile, self).save(*args,**kwargs)
        
        #Resize profile picture if too big
        img = Image.open(self.image.path)
        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.employee}"


class Leave_Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved','Approved'),
        ('Rejected', 'Rejected'),        
    ]
    
    employee = models.ForeignKey(Employee, on_delete=CASCADE)
    start_date =  models.DateField("Start Date",auto_now_add=False, null=True )
    end_date =  models.DateField("End Date",auto_now_add=False, null=True)
    status = models.CharField("Status", max_length=25, choices=STATUS_CHOICES, default='Pending') 
    
    def __str__(self):
        return f"{self.employee} {self.status}"