import os
import csv
from celery.schedules import crontab
from celery import shared_task
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.utils import timezone
from detoxa_services.models.appointments_models import Appointment
from detoxa_services.utils.generate_otp import generateMobileOTP

@shared_task

def new_appointments_report():
    """
    This function generates a new appointments report in csv and send to the admin's email.
    """
    # Get the list of all users
    appointments = Appointment.objects.filter(booked_at__date=timezone.now().today().date())
    # print(appointments)
    # generateMobileOTP('7678689353')
    # generateMobileOTP('7678174860')
    # Create a csv file and write the header
    with open('appointments_report.csv', 'w') as csvfile:
        fieldnames = ['Parent Full Name','Child Full Name', 'Parent Email', 'Parent Phone','Doctor Full Name','Doctor Email','Doctor Phone', 'Date of Birth','Age','Gender','Address','Appointment Date','Appointment Slot','Fees','Created At Date','Created AT Time','Promocode Applied','Promocode']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Write the data of each user
        for appointment in appointments:
            writer.writerow({'Parent Full Name': appointment.user.full_name, 'Child Full Name': appointment.child.full_name, 'Parent Email': appointment.user.email, 'Parent Phone': appointment.user.mobile,'Doctor Full Name':appointment.doctor.user.full_name,'Doctor Email':appointment.doctor.user.email,'Doctor Phone':appointment.doctor.user.mobile, 'Date of Birth': appointment.child.dob,'Age': appointment.child.age,'Gender':appointment.child.gender,'Address':appointment.child.address,'Appointment Date':appointment.date,'Appointment Slot':appointment.slot,'Fees':appointment.fees,'Created At Date':appointment.booked_at.date(),'Created At Time':appointment.booked_at.time(),'Promocode Applied':appointment.is_promocode_applied,'Promocode':appointment.promocode})
    # Send the csv file to the admin's email
    mail = EmailMessage('New Appointments Report', 'Please find the attached new registration report.',settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    mail.attach_file('appointments_report.csv','text/csv')
    mail.send()
    # Delete the csv file
    os.remove('appointments_report.csv')
    return True
