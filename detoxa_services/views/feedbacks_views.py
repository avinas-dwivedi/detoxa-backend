import csv
from django.conf import settings
from detoxa_services.models.feedback_models import Feedback
from detoxa_services.serializers.feedback_serializers import FeedbackSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail.message import EmailMessage



class CreateFeedbackView(CreateAPIView):
    """
    Create a new feedback
    """
    serializer_class = FeedbackSerializer
    model = Feedback
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback_obj = Feedback.objects.create(
                rating=serializer.validated_data['rating'],
                comment=serializer.validated_data['comment'],
                email=serializer.validated_data.get('email'),
            )
            try:
                with open('feedback.csv', 'w') as csvfile:
                    fieldnames = ['rating', 'comment', 'email']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'Rating':feedback_obj.rating , 'comment': feedback_obj.comment, 'email': feedback_obj.email})
   
                mail = EmailMessage('New Feedback Report', 'Please find the attached new registration report.',settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                mail.attach_file('feedback.csv','text/csv')
                mail.send()
            except Exception as e:
                pass
            return Response({'message': 'Feedback saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)