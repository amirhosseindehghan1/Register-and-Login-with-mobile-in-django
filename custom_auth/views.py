from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MyUser
from . import forms
from . import helper
from django.contrib import messages
# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    form = forms.RegisterForm()
    messages.error(request, 'Test error messages')
    if request.method == 'POST':
        try:
            if 'mobile' in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # send otp
                otp = helper.get_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify page
                return HttpResponseRedirect(reverse('verify'))
        except MyUser.DoesNotExist:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify page
                return HttpResponseRedirect(reverse('verify'))
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile = mobile)
        if request.method == 'POST':

            # Check OTP Expiration
            if not helper.check_otp_expiration(user.mobile):
                return HttpResponseRedirect(reverse('register_view'))
            if user.otp != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('register_view'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        context = {
            'mobile': mobile
        }
        return render(request, 'verify.html', context)
    except MyUser.DoesNotExist:
        return HttpResponseRedirect(reverse('register_view'))


# def mobile_login(request):
#     if request.method == 'POST':
#         if 'mobile' in request.POST:
#             mobile = request.POST.get('mobile')
#             user = MyUser.objects.get(mobile=mobile)
#             login(request, user)
#             return HttpResponseRedirect(reverse('dashboard'))
#     context = {
#
#     }
#     return render(request, 'mobile_login.html', context)

@login_required(login_url='/')
def dashboard(request):

    context = {

    }
    return render(request, 'dashboard.html', context)