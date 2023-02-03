import os
import csv
from celery import shared_task
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.utils import timezone
from detoxa_services.models.users import Users
from detoxa_services.models.organizations_models import OrganizationUser
from detoxa_services.utils.generate_otp import generateMobileOTP

@shared_task
def new_registration_report():
    """
    This function generates a new registration report in csv and send to the admin's email.
    """
    # Get the list of all users
    users = Users.objects.filter(created__date=timezone.now().today().date())
    print(users)

    # generateMobileOTP('7678689353')
    # generateMobileOTP('7678174860')
    # Create a csv file and write the header
    with open('new_registration_report.csv', 'w') as csvfile:
        fieldnames = ['Full Name', 'Email', 'Phone','Address','is_doctor','is_school_admin','is_society_admin','is_company_admin','School Name','Society Name','Company Name','Created_at Date','Created_at Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Write the data of each user
        for user in users:
            try:
                # Get the organization user of the user
                organization_user = OrganizationUser.objects.get(user=user)
                if organization_user.organization.type == 'School':
                    writer.writerow({'Full Name': organization_user.user.full_name, 'Email': organization_user.user.email, 'Phone': organization_user.user.mobile, 'Address':organization_user.user.address,'is_doctor':organization_user.user.is_doctor,'is_school_admin':organization_user.user.is_school_admin,'is_society_admin':organization_user.user.is_society_admin,'is_company_admin':organization_user.user.is_company_admin,'School Name':organization_user.organization.name,'Society Name':'','Company Name':'','Created_at Date':organization_user.user.created.date(),'Created_at Time':organization_user.user.created.time()})
                if organization_user.organization.type == 'Society':
                        writer.writerow({'Full Name': organization_user.user.full_name, 'Email': organization_user.user.email, 'Phone': organization_user.user.mobile, 'Address':organization_user.user.address,'is_doctor':organization_user.user.is_doctor,'is_school_admin':organization_user.user.is_school_admin,'is_society_admin':organization_user.user.is_society_admin,'is_company_admin':organization_user.user.is_company_admin,'School Name':'','Society Name':organization_user.organization.name,'Company Name':'','Created_at Date':organization_user.user.created.date(),'Created_at Time':organization_user.user.created.time()})
                if organization_user.organization.type == 'Company':
                        writer.writerow({'Full Name': organization_user.user.full_name, 'Email': organization_user.user.email, 'Phone': organization_user.user.mobile, 'Address':organization_user.user.address,'is_doctor':organization_user.user.is_doctor,'is_school_admin':organization_user.user.is_school_admin,'is_society_admin':organization_user.user.is_society_admin,'is_company_admin':organization_user.user.is_company_admin,'School Name':'','Society Name':'','Company Name':organization_user.organization.name,'Created_at Date':organization_user.user.created.date(),'Created_at Time':organization_user.user.created.time()})
            except Exception as e:
                print(e)
                writer.writerow({'Full Name': user.full_name, 'Email': user.email, 'Phone': user.mobile,'Address':user.address,'is_doctor':user.is_doctor,'is_school_admin':user.is_school_admin,'is_society_admin':user.is_society_admin,'is_company_admin':user.is_company_admin,'School Name':'','Society Name':'','Company Name':'','Created_at Date':user.created.date(),'Created_at Time':user.created.time()})
    # Send the csv file to the admin's email
    mail = EmailMessage('New Registration Report', 'Please find the attached new registration report.',settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    mail.attach_file('new_registration_report.csv','text/csv')
    mail.send()
    # Delete the csv file
    os.remove('new_registration_report.csv')
    return True

