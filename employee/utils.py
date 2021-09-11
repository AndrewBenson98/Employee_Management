import random


def create_new_ref_number():
    empNum = random.randint(10000000, 99999999)
    return str(empNum)


def generateTempPassword():
    return 'testpassword'