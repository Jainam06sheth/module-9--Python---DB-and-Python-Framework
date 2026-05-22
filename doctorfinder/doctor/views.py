from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctor

# Create your views here 

def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'home.html', {'doctors': doctors})


def profile(request):
    return render(request, 'doctor.html')


def contact(request):
    return HttpResponse('Contact Page')


def payment(request):
    return HttpResponse('Paytm Payment Gateway Integrated')