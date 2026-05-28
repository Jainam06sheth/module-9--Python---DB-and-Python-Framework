from django.shortcuts import render, redirect
from accounts.models import Appointment, checkLoggin
from patient.models import Patient
from doctor.models import Doctor
from datetime import date

@checkLoggin
def doctor_dashboard(request):
    user_id = request.session['user_id']
    try:
        doctor = Doctor.objects.get(user_id=user_id)
    except Doctor.DoesNotExist:
        return redirect('login')

    all_appointments = Appointment.objects.filter(doctor=doctor)
    
    pending_appointments = all_appointments.filter(status='Pending').order_by('date', 'time')
    upcoming_appointments = all_appointments.filter(status='Approved').order_by('date', 'time')
    past_appointments = all_appointments.exclude(status__in=['Pending', 'Approved']).order_by('-date', '-time')

    context = {
        'doctor': doctor,
        'user_role': 'doctor',
        'user_name': doctor.name,
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'pending_count': pending_appointments.count(),
        'upcoming_count': upcoming_appointments.count(),
        'past_count': past_appointments.count(),
    }

    return render(request, "doctor/doctor_dashboard.html", context)

@checkLoggin
def approve_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            appt = Appointment.objects.get(id=appointment_id)
            new_time = request.POST.get('time')
            if new_time:
                appt.time = new_time
            appt.status = 'Approved'
            appt.save()
        except Appointment.DoesNotExist:
            pass
    return redirect('doctor_dashboard')

@checkLoggin
def reject_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            appt = Appointment.objects.get(id=appointment_id)
            appt.status = 'Rejected'
            appt.save()
        except Appointment.DoesNotExist:
            pass
    return redirect('doctor_dashboard')

@checkLoggin
def payment(request):
    user_id = request.session['user_id']
    try:
        doctor = Doctor.objects.get(user_id=user_id)
    except Doctor.DoesNotExist:
        return redirect('login')

    # Get completed/approved appointments to compute total earnings
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='Approved')
    total_earnings = sum(appt.doctor.fee for appt in completed_appointments)

    context = {
        'doctor': doctor,
        'user_role': 'doctor',
        'user_name': doctor.name,
        'completed_appointments': completed_appointments,
        'total_earnings': total_earnings,
    }
    return render(request, "doctor/payment.html", context)
