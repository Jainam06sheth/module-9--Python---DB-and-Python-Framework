from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from datetime import date

def login_view(request):
    if 'user_id' in request.session:
        if request.session.get('user_role') == 'doctor':
            return redirect('doctor_dashboard')
        return redirect('patient_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'accounts/login.html',{'error': 'Invalid username or password.'})
        if Doctor.objects.filter(user_id=user.id).exists():
            role = 'doctor'
        elif Patient.objects.filter(user_id=user.id).exists():
            role = 'patient'
        else:
            return render(request, 'accounts/login.html',
                          {'error': 'No profile found for this account.'})
        request.session['user_id']   = user.id
        request.session['user_role'] = role
        if role == 'doctor':
            return redirect('doctor_dashboard')
        return redirect('patient_dashboard')
    return render(request, 'accounts/login.html')
def logout_view(request):
    request.session.flush()
    return redirect('login')
def register_view(request):
    if request.method == 'POST':
        name       = request.POST.get('name', '').strip()
        email      = request.POST.get('email', '').strip()
        username   = request.POST.get('username', '').strip()
        password   = request.POST.get('password', '')
        role       = request.POST.get('role', 'patient')
        speciality = request.POST.get('speciality', '').strip()
        experience = request.POST.get('experience', 0)
        fee        = request.POST.get('fee', 0)
        if not username or not password or not name or not email:
            return render(request, 'accounts/register.html',
                          {'error': 'All fields are required.'})
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html',
                          {'error': 'Username already taken.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html',
                          {'error': 'Email already registered.'})
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            if role == 'doctor':
                Doctor.objects.create(
                    user_id    = user.id,
                    name       = name,
                    speciality = speciality,
                    experience = int(experience) if experience else 0,
                    fee        = float(fee) if fee else 0,
                )
            else:
                Patient.objects.create(
                    user_id = user.id,
                    name    = name,
                )
            return render(request, 'accounts/register.html',{'success': 'Account created! You can now log in.'})
        except Exception as err:
            return render(request, 'accounts/register.html',{'error': f'Registration failed: {err}'})
    return render(request, 'accounts/register.html')

# ------------------------------------------------------------------
# Forgot password view
# ------------------------------------------------------------------

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'No account associated with that email.',
            })
        
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(f"/accounts/reset/{user.id}/{token}/")
        
        # Render HTML email
        html_message = render_to_string('accounts/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'current_year': date.today().year,
        })
        plain_message = strip_tags(html_message)
        
        # Send email (settings must define EMAIL_HOST, etc.)
        send_mail(
            subject='DoctorFinder Password Reset',
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return render(request, 'accounts/forgot_password.html', {
            's_msg': 'Password reset email sent. Please check your inbox.',
        })
    return render(request, 'accounts/forgot_password.html')

# ------------------------------------------------------------------
# Reset password confirmation view
# ------------------------------------------------------------------

def password_reset_confirm_view(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'accounts/password_reset_confirm.html', {
            'error': 'Invalid reset link.'
        })

    if not default_token_generator.check_token(user, token):
        return render(request, 'accounts/password_reset_confirm.html', {
            'error': 'The reset link is invalid or has expired.'
        })

    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if not password:
            return render(request, 'accounts/password_reset_confirm.html', {
                'error': 'Password is required.',
                'user_id': user_id,
                'token': token
            })
        if password != confirm_password:
            return render(request, 'accounts/password_reset_confirm.html', {
                'error': 'Passwords do not match.',
                'user_id': user_id,
                'token': token
            })
        user.set_password(password)
        user.save()
        return render(request, 'accounts/login.html', {
            'success': 'Password reset successful! You can now log in.'
        })

    return render(request, 'accounts/password_reset_confirm.html', {
        'user_id': user_id,
        'token': token
    })
