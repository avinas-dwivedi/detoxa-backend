import os
import csv
from celery import shared_task
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.utils import timezone
from detoxa_services.models.reports_models import UserLearnabilityReport, UserEyeSightReport,UserHandEyeCoordinationReport,UserGrowthReport
from detoxa_services.utils.generate_otp import generateMobileOTP

@shared_task
def new_tests_report():
    """
    This function generates a new registration report in csv and send to the admin's email.
    """
    # Get the list of all users
    learnability_tests = UserLearnabilityReport.objects.filter(report_date__date=timezone.now().today().date())
    eye_sight_tests = UserEyeSightReport.objects.filter(report_date__date=timezone.now().today().date())
    hand_eye_tests = UserHandEyeCoordinationReport.objects.filter(report_date__date=timezone.now().today().date())
    growth_tests = UserGrowthReport.objects.filter(report_date__date=timezone.now().today().date())
    
    # generateMobileOTP('7678689353')
    # generateMobileOTP('7678174860')
    # Create a csv file and write the header
    with open('new_test_report.csv', 'w') as csvfile:
        fieldnames = ['Full Name', 'Email', 'Phone', 'Date of Birth','Age','Gender','Report Name','Report','Report Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Write the data of each test
        # for test in learnability_tests:
        #     writer.writerow({'Full Name': test.child_user.full_name, 'Email': test.child_user.email, 'Phone': test.child_user.mobile, 'Date of Birth': test.child_user.dob,'Age': test.child_user.age,'Gender':test.gender,'Report Name':test.report_name,'Report':test.report,'Report Date':test.report_date})

        for test in eye_sight_tests:
            writer.writerow({'Full Name': test.child_user.full_name, 'Email': test.child_user.email, 'Phone': test.child_user.mobile, 'Date of Birth': test.child_user.dob,'Age': test.child_user.age,'Gender':test.gender,'Report Name':test.report_name,'Report':test.report,'Report Date':test.report_date})

        for test in hand_eye_tests:
            writer.writerow({'Full Name': test.child_user.full_name, 'Email': test.child_user.email, 'Phone': test.child_user.mobile, 'Date of Birth': test.child_user.dob,'Age': test.child_user.age,'Gender':test.gender,'Report Name':test.report_name,'Report':test.report,'Report Date':test.report_date})

        for test in growth_tests:
            writer.writerow({'Full Name': test.child_user.full_name, 'Email': test.child_user.email, 'Phone': test.child_user.mobile, 'Date of Birth': test.child_user.dob,'Age': test.child_user.age,'Gender':test.gender,'Report Name':test.report_name,'Report':test.report,'Report Date':test.report_date})
        
        for test in learnability_tests:
            writer.writerow({'Full Name': test.child_user.full_name, 'Email': test.child_user.email, 'Phone': test.child_user.mobile, 'Date of Birth': test.child_user.dob,'Age': test.child_user.age,'Gender':test.gender,'Report Name':test.report_name,'Report':test.report,'Report Date':test.report_date})

    # Send the csv file to the admin's email
    mail = EmailMessage('New Tests Report', 'Please find the attached new tests report.',settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    mail.attach_file('new_test_report.csv','text/csv')
    mail.send()
    # Delete the csv file
    os.remove('new_test_report.csv')
    return True

