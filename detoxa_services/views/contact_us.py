import csv
from ..serializers.contact_us_serializer import ContactUsSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from ..models.contact_us import ContactUs
from django.core.mail import send_mail
from detoxa_backend import settings
from django.core.mail.message import EmailMessage


class ContactUsView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        new_query = ContactUsSerializer(data=request.data)
        if new_query.is_valid():
            try:
                full_name = new_query.validated_data.get('full_name')
                mobile = new_query.validated_data.get('mobile')
                email = new_query.validated_data.get('email')
                message = new_query.validated_data.get('message')
                user = ContactUs.objects.create(full_name=full_name, mobile=mobile, email=email, message=message)
                data = {
                    'name': full_name,
                    'mobile': mobile,
                    'email': email,
                    'message': message
                }
                try:
                    with open('contactus.csv', 'w') as csvfile:
                        fieldnames = ['rating', 'comment', 'email']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({'name':user.name , 'mobile': user.mobile, 'email': user.email,'message': user.message})
    
                    mail = EmailMessage('New Contactus', 'Please find the attached new contact us query.',settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                    mail.attach_file('contactus.csv','text/csv')
                    mail.send()
                except Exception as e:
                    pass
                # send_mail('Contact Us', str(data), settings.EMAIL_HOST_USER,
                #           ['approach.detoxa@gmail.com'], fail_silently=False)
                if user:
                    data = {
                        "success": True,
                        "message": "Thank you for Contacting us, we will revert you shortly."
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(new_query.errors, status=status.HTTP_400_BAD_REQUEST)
