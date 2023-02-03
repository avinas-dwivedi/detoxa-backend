import io
import os
import boto3
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
import requests
from detoxa_services.models.organizations_models import Organizations
from detoxa_services.models.reports_models import UserMedicalReport


@shared_task
def send_report(email,logged_in_user,user_class,user_section,report_id):
    if email:
        try:
            report = UserMedicalReport.objects.get(id=report_id)
            file_path = requests.get(report.report_url)
            file_name = 'medical_report{}.pdf'.format(report.id)
            with open (file_name, 'wb') as output:
                output.write(file_path.content)
            file_location = (os.path.abspath(file_name))
            mail = EmailMessage(f'Email for Medical report', 'Hi,<br> Please find below the attached Medical report for your refernce.', settings.FROM_EMAIL, [email])
            mail.content_subtype = "html"  
            mail.attach_file(file_name)
            mail.send()
            if os.path.exists(file_location):
                os.remove(file_location)
        except Exception as e:
            print('Exception:',e)
    if user_class and user_section:
        organization_obj = Organizations.objects.get(user__id=logged_in_user)
        reports = UserMedicalReport.objects.filter(organization=organization_obj,user_class=user_class,user_section=user_section)
        for report in reports:
            try:
                report = UserMedicalReport.objects.get(id=report.id)
                file_path = requests.get(report.report_url)
                file_name = 'medical_report{}.pdf'.format(report.id)
                with open (file_name, 'wb') as output:
                    output.write(file_path.content)
                file_location = (os.path.abspath(file_name))
                mail = EmailMessage(f'Email for Medical report', 'Hi,<br> Please find below the attached Medical report for your refernce.', settings.FROM_EMAIL, [report.user.email])
                mail.content_subtype = "html"  
                mail.attach_file(file_name)
                mail.send()
                if os.path.exists(file_location):
                    os.remove(file_location)
            except Exception as e:
                print('Exception:',e)
    return 'report sent'
