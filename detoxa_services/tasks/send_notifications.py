import base64
import pandas as pd
from celery import shared_task
from detoxa_backend import settings
from detoxa_services.models.hospitals_models import Hospital, HospitalUser
from detoxa_services.models.notification_models import Notifications
from detoxa_services.models.organizations_models import OrganizationUser, Organizations
from detoxa_services.models.users import Users
from django.core.mail import send_mail



@shared_task
def send_notifications(notification_id,user_type):
    print(notification_id,user_type)
    notification = Notifications.objects.get(id=notification_id)
    if notification.notification_type == 'Email':
        if user_type == 'School User':
            organizations = Organizations.objects.filter(type='School')
            for organization in organizations:
                for user in OrganizationUser.objects.filter(organization=organization):
                    send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Society User':
                organizations = Organizations.objects.filter(type='Society')
                for organization in organizations:
                    for user in OrganizationUser.objects.filter(organization=organization):
                        send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Company User':
                organizations = Organizations.objects.filter(type='Company')
                for organization in organizations:
                    for user in OrganizationUser.objects.filter(organization=organization):
                        send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Hospital User':
            hospitals = Hospital.objects.all()
            for hospital in hospitals:
                for user in HospitalUser.objects.filter(hospital=hospital):
                    send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'School Admin':
            # organizations = Organizations.objects.filter(type='School')
            # for organization in organizations:
            for user in Users.objects.filter(is_school_admin=True):
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Society Admin':
                # organizations = Organizations.objects.filter(type='Society')
                # for organization in organizations:
                for user in Users.objects.filter(is_society_admin=True):
                    send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Company Admin':
                # organizations = Organizations.objects.filter(type='Company')
                # for organization in organizations:
                for user in Users.objects.filter(is_company_admin=True):
                    send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Hospital Admin':
            # hospitals = Hospital.objects.all()
            # for hospital in hospitals:
            for user in Users.objects.filter(is_hospital_admin=True):
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Doctors':
            # hospitals = Hospital.objects.all()
            # for hospital in hospitals:
            for user in Users.objects.filter(is_doctor=True):
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        if user_type == 'Normal Users':
            # hospitals = Hospital.objects.all()
            # for hospital in hospitals:
            for user in Users.objects.filter(is_doctor=False,is_hospital_admin=False,is_company_admin=False,is_society_admin=False,is_school_admin=False,is_admin=False):
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[user.user.email], fail_silently=False)
        return 'Sent Notifications'

@shared_task
def send_notifications_excel(notification_id,file):
    notification = Notifications.objects.get(id=notification_id)
    # print(file)
    if notification.notification_type == 'Email':
        xl_file = base64.b64decode(file)
        try:
            excel_data = pd.read_excel(xl_file)
            emails = excel_data['Email'].to_list()
            for email in emails:
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[email], fail_silently=False)
        except Exception as e:
            excel_data = pd.read_excel(xl_file,engine='pyxlsb')
            emails = excel_data['Email'].to_list()
            for email in emails:
                send_mail(notification.title, notification.message, settings.FROM_EMAIL,[email], fail_silently=False)
    return 'Sent Notifications'


