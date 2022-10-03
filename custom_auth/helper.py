import datetime
from random import randint
from zeep import Client
from . import models
def send_otp(mobile, otp):

    mobile = [mobile,]


   # Here you should set sms API


    print('OTP: ', otp)

def get_random_otp():
    return randint(1000, 9999)

def check_otp_expiration(mobile):
    try:
        user = models.MyUser.objects.get(mobile=mobile)
        now = datetime.datetime.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP Time :' , diff_time)

        if diff_time.seconds > 30:
            return False
        return True
    except models.MyUser.DoesNotExist:
        return False
