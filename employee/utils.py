import random
from django.core.mail import send_mail


def create_new_ref_number():
    empNum = random.randint(10000000, 99999999)
    return str(empNum)


def generateTempPassword():
    return 'testpassword'


def send_email( subject, message, recipients):
    
    
    from_email = "andrew.benson.testmail+admin@gmail.com"
    # subject = "Requesting Time Off"
    # message = "This person is requesting time off"
    
    # mail_list =[]
    # for recipient in recipients:
    #     mail_list += recipient.email    
    
    send_mail(
        subject,
        message,
        from_email,
        recipients,
        fail_silently=False,
    )
    
    