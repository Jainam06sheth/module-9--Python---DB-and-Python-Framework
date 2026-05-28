from django.shortcuts import render, redirect
from patient.models import *
from accounts.models import checkLoggin, Appointment
from doctor.models import *
from datetime import date

@checkLoggin
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(
            user_id=request.session['user_id']
        )
    except Patient.DoesNotExist:
        return redirect('login')


    all_appointments = Appointment.objects.filter(
                                    patient=patient
                                ).select_related('doctor').order_by(
                                    'date',
                                    'time'
                                )

    today = date.today()

    upcoming = []

    past = []

    total_spend = 0

    for appt in all_appointments:

        if appt.date >= today and appt.status in (
            'Pending',
            'Approved'
        ):

            upcoming.append(appt)

        else:

            past.append(appt)

        if appt.status in (
            'Pending',
            'Approved',
            'Completed'
        ):

            total_spend += appt.doctor.fee

    doctors = Doctor.objects.all().order_by('name')

    context = {

        'patient': patient,

        'user_role': 'patient',

        'user_name': patient.name,

        'upcoming_appointments': upcoming,

        'past_appointments': past,

        'upcoming_count': len(upcoming),

        'past_count': len(past),

        'total_expenditure': total_spend,

        'doctors': doctors,
    }

    return render(
        request,
        'patient/patient_dashboard.html',
        context
    )


@checkLoggin
def book_appointment(request):

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor_id')

        appt_date = request.POST.get('date')

        appt_time = request.POST.get('time')

        try:

            patient = Patient.objects.get(
                user_id=request.session['user_id']
            )

        except Patient.DoesNotExist:

            e_msg = "Patient profile not found."

            return redirect('login')

        try:

            doctor = Doctor.objects.get(
                id=doctor_id
            )

        except Doctor.DoesNotExist:

            e_msg = "Doctor not found."

            return redirect('patient_dashboard')

        try:

            Appointment.objects.create(

                patient=patient,

                doctor=doctor,

                date=appt_date,

                time=appt_time,

                status='Pending',
            )

            s_msg = (
                f"Appointment requested with "
                f"{doctor.name}!"
            )

        except Exception as e:

            e_msg = f"Booking failed: {str(e)}"

    referer = request.META.get('HTTP_REFERER')

    if referer:

        return redirect(referer)

    return redirect('patient_dashboard')


@checkLoggin
def cancel_appointment(request, appointment_id):

    if request.method == 'POST':

        try:

            patient = Patient.objects.get(
                user_id=request.session['user_id']
            )

        except Exception as e:

            e_msg = "Patient profile not found."

            return redirect('login')

        try:

            appt = Appointment.objects.get(
                                                id=appointment_id,
                                                patient=patient
                                          )

        except Exception as e :

            e_msg = "Appointment not found."

            return redirect('patient_dashboard')

        try:

            appt.status = 'Cancelled'

            appt.save()

            s_msg = "Appointment cancelled successfully."

        except Exception as e:

            e_msg = f"Error cancelling: {str(e)}"

    return redirect('patient_dashboard')


@checkLoggin
def discover_view(request):

    try:

        patient = Patient.objects.get(user_id=request.session['user_id'])

    except Patient.DoesNotExist:

        e_msg = "Patient profile not found."

        return redirect('login')

    doctors = Doctor.objects.all().order_by('name')

    context = {

        'patient': patient,

        'user_role': 'patient',

        'user_name': patient.name,

        'doctors': doctors,
    }

    return render(request, 'patient/discover.html', context)


def index_view(request):

    doctors = Doctor.objects.all().order_by('name')

    user_name = ""

    is_logged_in = ('user_id' in request.session)

    user_role = request.session.get('user_role','')

    if is_logged_in:

        user_id = request.session.get('user_id')

        if user_role == 'doctor':

            doctor_obj = Doctor.objects.filter(user_id=user_id).first()

            if doctor_obj:

                user_name = doctor_obj.name

        elif user_role == 'patient':

            patient_obj = Patient.objects.filter(user_id=user_id).first()

            if patient_obj:

                user_name = patient_obj.name

    context = {

        'doctors': doctors,

        'is_logged_in': is_logged_in,

        'user_role': user_role,

        'user_name': user_name,
    }

    return render(request,'patient/index.html',context    )