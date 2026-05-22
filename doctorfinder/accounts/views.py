from django.shortcuts import redirect
from functools import wraps

def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session or request.session.get('user_role') != 'patient':
            # Add an error message if you're using messages framework
            return redirect('login') # Replace 'login' with your actual login URL name
        return view_func(request, *args, **kwargs)
    return wrapper

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session or request.session.get('user_role') != 'doctor':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
