from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Profile
import random


# -------------------------------------------------
# SMS OTP PLACEHOLDER
# -------------------------------------------------
def send_sms_otp(phone, otp):
    print(f"[SMS OTP] Phone: {phone} | OTP: {otp}")
    return True


# ---------------------------
# LOGIN
# ---------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'accounts/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'accounts/login.html')


# ---------------------------
# SIGNUP WITH OTP
# ---------------------------
def signup_view(request):
    if request.method == 'POST':

        if 'send_otp' in request.POST:
            data = {
                'first_name': request.POST['first_name'],
                'middle_name': request.POST.get('middle_name', ''),
                'last_name': request.POST['last_name'],
                'username': request.POST['username'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'dob': request.POST['dob'],
                'password': request.POST['password'],
                'otp': random.randint(100000, 999999)
            }

            if User.objects.filter(username=data['username']).exists():
                return render(request, 'accounts/signup.html', {
                    'error': 'Username already exists'
                })

            request.session['signup_data'] = data

            from django.conf import settings

            send_mail(
                'OTP Verification - MS Construction',
                f"Your OTP is {data['otp']}",
                settings.DEFAULT_FROM_EMAIL,
                [data['email']],
                fail_silently=False,
            )

            send_sms_otp(data['phone'], data['otp'])

            return render(request, 'accounts/signup.html', {'otp_sent': True})

        if 'verify_otp' in request.POST:
            entered = request.POST['otp']
            data = request.session.get('signup_data')

            if data and str(data['otp']) == entered:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )

                Profile.objects.create(
                    user=user,
                    phone=data['phone'],
                    middle_name=data['middle_name'],
                    date_of_birth=data['dob']
                )

                del request.session['signup_data']
                return redirect('login')

            return render(request, 'accounts/signup.html', {
                'error': 'Invalid OTP',
                'otp_sent': True
            })

    return render(request, 'accounts/signup.html')


# ---------------------------
# RESET PASSWORD
# ---------------------------
def reset_password_view(request):
    if request.method == 'POST':

        if 'send_otp' in request.POST:
            try:
                user = User.objects.get(email=request.POST['email'])
            except User.DoesNotExist:
                return render(request, 'accounts/reset_password.html', {
                    'error': 'Email not registered'
                })

            otp = random.randint(100000, 999999)
            request.session['reset_data'] = {
                'user_id': user.id,
                'otp': otp
            }

            send_mail(
                'Password Reset OTP',
                f"Your OTP is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            return render(request, 'accounts/reset_password.html', {
                'otp_sent': True
            })

        if 'reset_password' in request.POST:
            entered = request.POST['otp']
            data = request.session.get('reset_data')

            if data and str(data['otp']) == entered:
                user = User.objects.get(id=data['user_id'])
                user.set_password(request.POST['new_password'])
                user.save()
                del request.session['reset_data']
                return redirect('login')

            return render(request, 'accounts/reset_password.html', {
                'error': 'Invalid OTP',
                'otp_sent': True
            })

    return render(request, 'accounts/reset_password.html')


# ---------------------------
# PROFILE VIEW / EDIT
# ---------------------------
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        profile.middle_name = request.POST.get('middle_name', '')
        profile.phone = request.POST['phone']
        profile.date_of_birth = request.POST['dob']

        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']

        request.user.save()
        profile.save()
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})


# ---------------------------
# DELETE ACCOUNT (SAFE)
# ---------------------------
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')

    return render(request, 'accounts/delete_account.html')
