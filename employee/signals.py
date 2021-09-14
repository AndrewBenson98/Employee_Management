from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Employee, Profile
from employee.utils import generateTempPassword

@receiver(post_save, sender=Employee)
def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(employee=instance)
        new_user = User.objects.create_user(username=instance.username,email=instance.email, password=generateTempPassword())
        instance.user = new_user
        instance.save()
        
        
        
        
@receiver(post_save, sender=Employee)
def create_user(sender, instance, **kwargs):
    if instance:
        instance.profile.save()
