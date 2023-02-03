from asyncio.log import logger
import io
import boto3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from reportlab.platypus import Paragraph
from detoxa_services.models.child_tracker import ChildTracker
from detoxa_services.models.learnability_tracker import LearnabilityTracker, LearnalityTrackerSectionAnswers
from detoxa_services.models.motor_skills import MotorSkillTracker
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser
from detoxa_services.models.eyesight_tracker import EyeSightTracker
from detoxa_services.models.hand_eye_tracker import HandEyeTracker
from detoxa_services.models.organizations_models import Organizations
from detoxa_services.models.users import Users
from detoxa_services.models.analytical_tracker import AnalyticalTracker
from detoxa_services.tasks.medicalreportgeneration import generatemedicalreport
from detoxa_services.tasks.send_report import send_report
from detoxa_services.utils.generate_otp import generateMobileOTP, verifyMobileOTP
from ..models.reports_models import UserGrowthReport, UserLearnabilityReport, UserEyeSightReport, \
    UserHandEyeCoordinationReport, UserMedicalReport, UserMotorSkillsReport, UserAnalyticalReport, UserHairReport, UserSkinReport
from reportlab.lib.styles import getSampleStyleSheet

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus.tables import Table, TableStyle

from reportlab.lib.colors import Whiter, black, green, purple, red, blue, yellow
from detoxa_services.serializers.report_serializer import CreateEyeSightReportSerializer, CreateReportSerializer, \
    GenerateMedicalReportCardSerializer, GenerateOTPforReportSerializer, GetMedicalReportListSerializer, GetReportSerializer, \
    GrowthReportSerializer, HandEyeTrackerReportSerializer, ReportSerializer, EyeSightReportSerializer, SendMedicalReportOnEmailSerializer, \
    VerifyOTPforReportSerializer, CreateCoordinatioReportSerializer,CreateHairTrackerReportSerializer
from ..utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination

from detoxa_services.models.skin_tracker import SkinTracker, SkinTrackerSectionAnswers
from detoxa_services.models.hair_tracker import HairTracker, HairTrackerSectionAnswers
from django.core.mail import send_mail
from detoxa_backend import settings


class CreateLearnabilityReportPDFView(CreateAPIView):
    serializer_class = CreateReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Learnability Report PDF
        '''

        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserLearnabilityReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),
                report_type=LearnabilityTracker.objects.get(
                    id=serializer.validated_data.get('report_id')),
                report_name='Learnability Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                learnablity_tracker=LearnabilityTracker.objects.get(id=serializer.validated_data.get('report_id')))
            reading = 0
            spelling_writing = 0
            math_logic = 0
            emotion_self_control = 0
            listening = 0
            attention = 0
            for i in learnability_obj:
                if i.section_name == 'Reading':
                    reading = i.answer
                elif i.section_name == 'Spelling & Writing':
                    spelling_writing = i.answer
                elif i.section_name == 'Math & Logic':
                    math_logic = i.answer
                elif i.section_name == 'Emotion & Self-Control':
                    emotion_self_control = i.answer
                elif i.section_name == 'Listening':
                    listening = i.answer
                elif i.section_name == 'Attention':
                    attention = i.answer

            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')

            c.setFillColor('#800000')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, 'Child Trackers - Child Kits - Consultation - Therapy')

            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')

            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 730, 'www.detoxa.in')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 918448669501')

            c.setFillColor('#800000')
            c.setFont('Helvetica-Bold', 10)
            # c.setFont('Times-Roman', 10)
            c.drawString(
                # 45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
                45, 680, f'Test Conducted At : {report_obj.report_date.strftime("%Y-%m-%d")}')

            # c.setFont('Times-Roman', 10)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')

            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age} Years')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 575, '120cm')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 510, 'Learnability Tracker Report')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 480, 'PARAMETER')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 480, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(230, 480, 'YOUR AVG. SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(430, 480, 'MAXIMUM AVG. SCORE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # para = Paragraph(serializer.validated_data.get(
            #     'interpretations'), style=normalStyle)
            # if len(serializer.validated_data.get('interpretations')) < 250:
            #     para.wrap(580, 280)
            #     para.drawOn(c, 15, 280)
            # elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
            #     para.wrap(580, 240)
            #     para.drawOn(c, 15, 240)
            # else:
            #     para.wrap(580, 210)
            #     para.drawOn(c, 15, 210)
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 285, "Your child has successfully performed Learnability test using Detoxa's "
                                  "Learnability Tracker. If your avg. score is ")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 265, "below 5, then there is considerable scope to improve learnability "
                                  "of the child. This can be improved by practicing ")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 245, "specially designed activities using Detoxa's child kits. You can select Learnability option under "
                                  "Child Tracker section ")
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 12)
            # c.drawString(15, 220, " ")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 225, "from the navigation bar. In case of any concerns or if you feel to discuss about your child, you may consult ")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 205, "Detoxa experts or any trusted doctors available on Detoxa portal. For booking interaction session or doctor "
                                  "appointment, ")

            # c.setFillColor(blue)
            # c.setFont('Times-Roman', 12)
            # c.drawString(15, 185, "")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 185, "you can login on www.detoxa.in or can call at 8448669501.")
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            c.setFont('Times-Roman', 12, )
            c.drawString(15, 25, 'Disclaimer :- ')
            c.setFont('Times-Roman', 10)
            c.drawString(
                80, 25, 'If you think you have a medical emergency, '
                        'call your doctor or 102 immediately. Do not rely on electronic communications')
            c.drawString(
                15, 15, 'or communication through this website for immediate, urgent medical needs. '
                        'This website is not designed to facilitate medical emergencies.')
            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             460, 50, width=50, height=50, mask='auto')
            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             540, 50, width=50, height=50, mask='auto')
            # c.setFont('Times-Roman', 10)
            # c.drawString(455, 45, 'Download iOS')
            # c.drawString(530, 45, 'Download android')
            # c.setFont('Times-Roman', 12)
            # c.drawString(
            #     150, 30, 'Disclaimer :- This a dummy disclaimer for reports generated on detoxa platform.')
            # c.drawString(250, 15, 'https://detoxa.netlify.app')
            data = [
                ['Reading', f'{reading}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 455)

            data = [
                ['Spelling and Writing', f'{spelling_writing}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 435)
            data = [
                ['Math & Logic', f'{math_logic}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 415)
            data = [
                ['Emotion & Self-Control', f'{emotion_self_control}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 395)
            data = [
                ['Listening', f'{listening}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 375)
            data = [
                ['Attention', f'{attention}', '5'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 355)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')),
                                               ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class CreateMotorSkillReportPDFView(CreateAPIView):
    serializer_class = CreateReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Skill Report PDF
        '''
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserMotorSkillsReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),
                report_type=MotorSkillTracker.objects.get(
                    id=serializer.validated_data.get('report_id')),
                report_name='Motor Skill Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, '931 Maidan Gari, North Delhi INDIA-181004')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(
                # 45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
                45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d")}')
            c.setFont('Times-Roman', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 575, '120cm')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 465, 'TEST NAME')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 465, 'MEASURED VALUE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(260, 465, 'MEASURED VALUE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            para = Paragraph(serializer.validated_data.get(
                'interpretations'), style=normalStyle)
            if len(serializer.validated_data.get('interpretations')) < 250:
                para.wrap(580, 280)
                para.drawOn(c, 15, 280)
            elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
                para.wrap(580, 240)
                para.drawOn(c, 15, 240)
            else:
                para.wrap(580, 210)
                para.drawOn(c, 15, 210)
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        460, 50, width=50, height=50, mask='auto')
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        540, 50, width=50, height=50, mask='auto')
            c.setFont('Times-Roman', 10)
            c.drawString(455, 45, 'Download iOS')
            c.drawString(530, 45, 'Download android')
            c.setFont('Times-Roman', 12)
            c.drawString(
                150, 30, 'Disclaimer :- This a dummy disclaimer for reports generated on detoxa platform.')
            c.drawString(250, 15, 'https://detoxa.netlify.app')
            data = [
                ['Reading Skills', '17'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 440)

            data = [
                ['Spelling Skills', '17'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 420)
            data = [
                ['Writing Skills', '17'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 400)
            data = [
                ['Math & Logic Skills ', '17'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 380)
            data = [
                ['Listening & Attention Skills', '17'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 360)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(
                    open(pdf_file_name, 'rb')), ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class CreateGrowthReportPDFView(CreateAPIView):
    serializer_class = CreateReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Growth Report PDF
        '''
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateReportSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.validated_data)
            # report_obj = UserGrowthReport.objects.get(id=serializer.validated_data.get('id'))
            report_obj = UserGrowthReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(id=serializer.validated_data.get('child_user')),
                report_type=ChildTracker.objects.get(id=serializer.validated_data.get('report_id')),
                report_name='Growth Tracker',
                report_image_url='https://detoxa.netlify.app/static/media/growth-tracker.be5f2374.png',
            )
            child_tracker_obj = ChildTracker.objects.get(
                id=serializer.validated_data.get('report_id'))
            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor('#800000')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, 'Child Trackers - Child Kits - Consultation - Therapy')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')
            # c.setFont('Times-Roman', 10)
            # c.drawString(420, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')

            c.setFont('Times-Roman', 10)
            c.drawString(420, 730, 'www.detoxa.in')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor('#800000')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(
                # 45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
                45, 680, f'Test Conducted At : {report_obj.report_date.strftime("%Y-%m-%d")}')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age} Years')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 600, f'{child_tracker_obj.weight}Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 575, f'{child_tracker_obj.height}cm')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 510, 'Growth Tracker Report')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 465, 'PARAMETER')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(230, 465, 'ENTERED VALUE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(430, 465, 'CALCULATED VALUE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # para = Paragraph(serializer.validated_data.get('interpretations'), style=normalStyle)
            # para = Paragraph('Refer standard growth chart as reference, which is available in Growth Tracker '
            #                  'Section on Detoxa portal, click here to open. In case of any deviation from '
            #                  'standard growth pattern, you may consult Detoxa experts or any trusted doctors '
            #                  'available on Detoxa portal. For booking appointment, you can login on www.detoxa.in or '
            #                  'can call at 8448669501.', style=normalStyle)
            # if len(serializer.validated_data.get('interpretations')) < 250:
            #     para.wrap(580, 280)
            #     para.drawOn(c, 15, 280)
            # elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
            #     para.wrap(580, 240)
            #     para.drawOn(c, 15, 240)
            # else:
            # para.wrap(580, 255)
            # para.drawOn(c, 15, 255)
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 285, 'Refer standard growth chart as reference, which is available in Growth Tracker '
                             'Section on Detoxa portal, You can select Growth option under Child Tracker section from the navigation bar.')

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 265, 'In case of any deviation from standard growth pattern, you may consult '
                                  'Detoxa experts or any trusted doctors')
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 245, 'available on Detoxa portal. For booking appointment, you can login on')

            c.setFillColor(blue)
            c.setFont('Times-Roman', 12)
            c.drawString(360, 245, 'www.detoxa.in')

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(435, 245, 'or can call at 8448669501.')
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             460, 50, width=50, height=50, mask='auto')
            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             540, 50, width=50, height=50, mask='auto')
            # c.setFont('Times-Roman', 10)
            # c.drawString(455, 45, 'Download iOS')
            # c.drawString(530, 45, 'Download android')
            c.setFont('Times-Roman', 12, )
            c.drawString(15, 25, 'Disclaimer :- ')
            c.setFont('Times-Roman', 10)
            c.drawString(
                80, 25, 'If you think you have a medical emergency, '
                        'call your doctor or 102 immediately. Do not rely on electronic communications')
            c.drawString(
                15, 15, 'or communication through this website for immediate, urgent medical needs. '
                        'This website is not designed to facilitate medical emergencies.')
            data = [
                ['Height Analysis', f'{child_tracker_obj.height}cm', '-'],
            ]
            t = Table(data, 2 * [2.68 * inch], 1 * [0.2 * inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            # c.drawString(250, 10, 'https://detoxa.netlify.app')

            t.wrap(0, 0)
            t.drawOn(c, 15, 440)

            data = [
                ['Weight Analysis', f'{child_tracker_obj.weight}Kg', '-'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 420)
            data = [
                ['BMI Analysis', '-', f'{child_tracker_obj.result}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 400)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()

            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(
                    open(pdf_file_name, 'rb')), ACL='public-read', ContentDisposition='inline')
                # s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')))

                # s3_client = boto3.client('s3',
                #                         region_name='us-east-2',
                #                         aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                #                         aws_secret_access_key='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')
                # S3_url = s3_client.generate_presigned_url(
                # ClientMethod='get_object',
                # Params={
                #     'Bucket': 'detoxa',
                #     'Key': f'{pdf_file_name}'
                #     }
                # )
                # print(S3_url)
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateEyeSightReportPDFView(CreateAPIView):
    serializer_class = CreateEyeSightReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Learnability Report PDF
        '''
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateEyeSightReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserEyeSightReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),
                report_id=EyeSightTracker.objects.get(
                    id=serializer.validated_data.get('report_id')[0]),
                report_name='Eye Sight Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            color_blindness_test_final_value = 0
            left_eye_visual_acquity_test_final_value = 0
            right_eye_visual_acquity_test_final_value = 0
            left_eye_astigmatism_test_final_value = 'No'
            right_eye_astigmatism_test_final_value = 'No'
            left_eye_corneal_curvature_test_final_value = 'No'
            right_eye_corneal_curvature_test_final_value = 'No'
            dry_eye_test_final_value = 0

            for i in serializer.validated_data.get('report_id'):
                eyesight_tracker_obj = EyeSightTracker.objects.get(id=i)

                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'color_blindness_test')
                    for i in test_values.values():
                        if i == 'True':
                            color_blindness_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)

                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get('visual_acquity_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         visual_acquity_test_final_value += 1
                    left_eye_visual_acquity_test_final_value = test_values.get('left_eye').get('line_no')
                    right_eye_visual_acquity_test_final_value = test_values.get('right_eye').get('line_no')
                except Exception as e:
                    print('Exception from visual_acquity_test-> ', e)

                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get('astigmatism_test')
                    print(test_values, '==================+++++++++++++++=====')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         astigmatism_test_final_value += 1
                    left_eye_astigmatism_test_final_value = test_values.get('left_eye').get('ans').title()
                    right_eye_astigmatism_test_final_value = test_values.get('right_eye').get('ans').title()

                except Exception as e:
                    print('Exception-> ', e)

                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'corneal_curvature_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         corneal_curvature_test_final_value += 1
                    left_eye_corneal_curvature_test_final_value = test_values.get(
                        'left_eye').get('ans').title()
                    right_eye_corneal_curvature_test_final_value = test_values.get(
                        'right_eye').get('ans').title()
                except Exception as e:
                    print('Exception-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'dry_eye_test')
                    for i in test_values.values():
                        if i == 'True':
                            dry_eye_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor('#800000')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, 'Child Trackers - Child Kits - Consultation - Therapy')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')

            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 730, 'www.detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor('#800000')

            c.setFont('Helvetica-Bold', 10)
            c.drawString(
                # 45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
                45, 680, f'Test Conducted At : {report_obj.report_date.strftime("%Y-%m-%d")}')

            c.setFont('Helvetica-Bold', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age} Years')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 575, '120cm')
            c.setFillColor('#9f0a10')

            c.setFont('Times-Roman', 16)
            c.drawString(10, 505, 'Eyesight Tracker Report')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(50, 465, 'TEST NAME')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 465, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(250, 465, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(450, 465, 'IDEAL SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 330, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # para = Paragraph(serializer.validated_data.get(
            #     'interpretations'), style=normalStyle)
            # if len(serializer.validated_data.get('interpretations')) < 250:
            #     para.wrap(580, 280)
            #     para.drawOn(c, 15, 280)
            # elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
            #     para.wrap(580, 240)
            #     para.drawOn(c, 15, 240)
            # else:
            #     para.wrap(580, 210)
            #     para.drawOn(c, 15, 210)

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 285, "Your child has successfully performed Eyesight Tests using Detoxa's Eyesight "
                                  "Tracker. If the your child's score is less")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 265, "than the ideal score, then there is considerable scope to improve eyesight of the "
                                  "child. These can be improved by")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 245, "practicing specially designed activities using Detoxa's child kits. You can select Eyesight option under Child Tracker")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 225, "section from the navigation bar. In case of any concerns or if you feel to discuss about your child, you may consult")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 205, "Detoxa experts or any trusted doctors available on Detoxa portal. For booking interaction session or doctor appointment, ")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 185, "you can login on www.detoxa.in or can call at 8448669501.")

            # c.setFillColor(blue)
            # c.setFont('Times-Roman', 12)
            # c.drawString(15, 170, "")

            # c.setFillColor(black)
            # c.setFont('Times-Roman', 12)
            # c.drawString(15, 180, "")
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)

            c.setFont('Times-Roman', 12, )
            c.drawString(15, 25, 'Disclaimer :- ')
            c.setFont('Times-Roman', 10)
            c.drawString(
                80, 25, 'If you think you have a medical emergency, '
                        'call your doctor or 102 immediately. Do not rely on electronic communications or')
            c.drawString(
                15, 15, 'communication through this website for immediate, urgent medical needs. '
                        'This website is not designed to facilitate medical emergencies.')
            data = [
                ['Color Blindness Test',
                    f'{color_blindness_test_final_value}', '20'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 440)

            data = [
                ['Visual Acquity Test', f'Left - {left_eye_visual_acquity_test_final_value} '
                    f' Right - {right_eye_visual_acquity_test_final_value}', 'NA'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 420)
            data = [
                ['Astigmatism Test', f'Left - {left_eye_astigmatism_test_final_value} '
                    f' Right - {right_eye_astigmatism_test_final_value}', 'NA'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 400)
            data = [
                ['Corneal Curvature Test ', f'Left - {left_eye_corneal_curvature_test_final_value} '
                    f' Right - {right_eye_corneal_curvature_test_final_value}', 'NA'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 380)
            data = [
                ['Dry Eye Test', f'{dry_eye_test_final_value}', '12'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 360)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(
                    open(pdf_file_name, 'rb')), ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class CreateCoordinationReportPDFView(CreateAPIView):
    serializer_class = CreateCoordinatioReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Learnability Report PDF
        '''
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateCoordinatioReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserHandEyeCoordinationReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),
                report_type=HandEyeTracker.objects.get(
                    id=serializer.validated_data.get('report_id')[0]),
                report_name='Hand Eye Coordination Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            average_score = report_obj.report_type.test_question_answer['hand_eye_test_1']['avg']
            # test2_average_score = report_obj.report_type.test_question_answer['hand_eye_test_2']['avg']
            test2_average_score = ''

            # for i in serializer.validated_data.get('report_id'):
            #     eyesight_tracker_obj = HandEyeTracker.objects.get(id=i)
            #
            #     try:
            #         test_values = eyesight_tracker_obj.test_question_answer.get('hand_and_eye_test_2')
            #         print(test_values)
            #         for i in test_values.values():
            #             print(i)
            #             # if i == 'True':
            #             #     test2_average_score += 1
            #     except Exception as e:
            #         print('Exception-> ', e)


            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor('#800000')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, 'Child Trackers - Child Kits - Consultation - Therapy')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')

            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 730, 'www.detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor('#9f0a10')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(
                # 45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
                45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d")}')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age} Years')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 575, '120cm')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 505, 'Hand & Eye Coordination Tracker Report')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 465, 'TEST NAME')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 465, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(230, 465, 'YOUR AVG. RESPONSE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(430, 465, 'IDEAL AVG. RESPONSE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(20, 320, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # para = Paragraph(serializer.validated_data.get(
            #     'interpretations'), style=normalStyle)
            # if len(serializer.validated_data.get('interpretations')) < 250:
            #     para.wrap(580, 280)
            #     para.drawOn(c, 15, 280)
            # elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
            #     para.wrap(580, 240)
            #     para.drawOn(c, 15, 240)
            # else:
            #     para.wrap(580, 210)
            #     para.drawOn(c, 15, 210)

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 290, "Your child has successfully performed Traffic Light test and Light Matrix test "
                                  "using Detoxa's Hand & Eye Coordination")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 275, "Tracker. If the your child's average response time is more than 1 second, then "
                                  "there is considerable scope to improve ")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 260, "hand & eye coordination of the child. These can be improved by practicing specially "
                                  "designed activities using Detoxa's")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 245, "child kits. You can select Hand & Eye Coordination option under Child Tracker section from the navigation bar. In case")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 230, " of any concerns or if you feel to discuss about your child, you may consult Detoxa experts or any trusted doctors")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 215, " available on Detoxa portal. on Detoxa portal. For booking interaction session or doctor appointment, you can login on ")

            c.setFillColor(blue)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 200, "www.detoxa.in")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(100, 200, "or can call at 8448669501.")

            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)

            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             460, 50, width=50, height=50, mask='auto')
            # c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
            #             540, 50, width=50, height=50, mask='auto')
            # c.setFont('Times-Roman', 10)
            # c.drawString(455, 45, 'Download iOS')
            # c.drawString(530, 45, 'Download android')
            # c.setFont('Times-Roman', 12)
            # c.drawString(
            #     150, 30, 'Disclaimer :- This a dummy disclaimer for reports generated on detoxa platform.')
            # c.drawString(250, 15, 'https://detoxa.netlify.app')
            c.setFont('Times-Roman', 12, )
            c.drawString(15, 25, 'Disclaimer :- ')
            c.setFont('Times-Roman', 10)
            c.drawString(
                80, 25, 'If you think you have a medical emergency, '
                        'call your doctor or 102 immediately. Do not rely on electronic communications')
            c.drawString(
                15, 15, 'or communication through this website for immediate, urgent medical needs. '
                        'This website is not designed to facilitate medical emergencies.')
            data = [
                ['Traffic Light Test', f'{average_score}', '<1'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 440)

            data = [
                ['Light Matrix Test', '17', '<1'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 420)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(
                    open(pdf_file_name, 'rb')), ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report,
                'report_id': report_obj.id,
                'report_type_id': report_obj.report_type_id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class CreateAnalyticalReportPDFView(CreateAPIView):
    serializer_class = CreateEyeSightReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Analytical Report PDF
        '''
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateEyeSightReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserAnalyticalReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),
                report_id=AnalyticalTracker.objects.get(
                    id=serializer.validated_data.get('report_id')[0]),
                report_name='Analytical Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            analytical_test_final_value = 0

            for i in serializer.validated_data.get('report_id'):
                analytical_tracker_obj = AnalyticalTracker.objects.get(id=i)
                try:
                    test_values = analytical_tracker_obj.test_answer.get(
                        'analytical_test')
                    for i in test_values.values():
                        if i == 'True':
                            analytical_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)

            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg', 0, 0, width=610,
                        height=800, mask='auto')
            c.setFillColor('#800000')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, 'Child Trackers - Child Kits - Consultation - Therapy')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')

            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 730, 'www.detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor('#9f0a10')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(
                45, 680, f'Test Conducted At : {report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
            c.setFont('Helvetica-Bold', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(325, 550, 'Age -')
            # c.setFillColor(black)
            # c.setFont('Times-Roman', 14)
            # c.drawString(365, 550, f'{report_obj.child_user.age} Years')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            # c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            # c.drawString(555, 575, '120cm')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 510, 'Analytical Tracker Report')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 465, 'PARAMETER')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(230, 465, 'YOUR SCORE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(430, 465, 'MAXIMUM SCORE')

            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # para = Paragraph(serializer.validated_data.get(
            #     'interpretations'), style=normalStyle)
            # if len(serializer.validated_data.get('interpretations')) < 250:
            #     para.wrap(580, 280)
            #     para.drawOn(c, 15, 280)
            # elif len(serializer.validated_data.get('interpretations')) > 250 and len(
            #         serializer.validated_data.get('interpretations')) < 450:
            #     para.wrap(580, 240)
            #     para.drawOn(c, 15, 240)
            # else:
            #     para.wrap(580, 210)
            #     para.drawOn(c, 15, 210)

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 285, "Your child has successfully performed Analytical Ability test using Detoxa's "
                                  "Analytical Tracker. If the score is below")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 265, "15, then there is considerable scope to improve analytical "
                                  "ability of the child. This can be improved by practicing ")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 245, "specially designed activities using Detoxa's "
                                  "child kits. You can select Analytical option under Child Tracker section " )

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 225, "from the navigation bar. In case of any concerns or if you feel to discuss about your child, you may consult Detoxa ")
            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 205, "experts or any trusted doctors available on Detoxa portal. For booking interaction session or doctor appointment,")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(15, 185, " you can login on")

            c.setFillColor(blue)
            c.setFont('Times-Roman', 12)
            c.drawString(105, 185, "www.detoxa.in")

            c.setFillColor(black)
            c.setFont('Times-Roman', 12)
            c.drawString(180, 185, "or can call at 8448669501.")

            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1." + serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2." + serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            # c.drawImage(
            #     'https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png', 460,
            #     50, width=50, height=50, mask='auto')
            # c.drawImage(
            #     'https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png', 540,
            #     50, width=50, height=50, mask='auto')
            # c.setFont('Times-Roman', 10)
            # c.drawString(455, 45, 'Download iOS')
            # c.drawString(530, 45, 'Download android')
            c.setFont('Times-Roman', 12, )
            c.drawString(15, 25, 'Disclaimer :- ')
            c.setFont('Times-Roman', 10)
            c.drawString(
                80, 25, 'If you think you have a medical emergency, '
                        'call your doctor or 102 immediately. Do not rely on electronic communications')
            c.drawString(
                15, 15, 'or communication through this website for immediate, urgent medical needs. '
                        'This website is not designed to facilitate medical emergencies.')

            # c.drawString(250, 10, 'https://detoxa.netlify.app')
            # c.drawString(250, 15, 'https://detoxa.netlify.app')
            data = [
                ['Analytical Ability', f'{analytical_test_final_value}', '20'],
            ]
            t = Table(data, 3 * [2.68 * inch], 1 * [0.2 * inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, -1), (0, -1), 'LEFT'),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 440)

            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')

                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')), ACL='public-read',
                                               ContentDisposition='inline')

                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class ReportListView(ListAPIView):
    serializer_class = ReportSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        if self.request.GET.get('report_type') and not (self.request.GET.get('child_user') or (self.request.GET.get('from_date') and self.request.GET.get('to_date'))):
            if self.request.GET.get('report_type') == 'Learnability Tracker':
                queryset = UserLearnabilityReport.objects.filter(
                    parent_user=user)
                # serializer = ReportSerializer(queryset, many=True)
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)
            elif self.request.GET.get('report_type') == 'Growth Tracker' and not (self.request.GET.get('child_user') or (self.request.GET.get('from_date') and self.request.GET.get('to_date'))):
                queryset = UserGrowthReport.objects.filter(parent_user=user)

            elif self.request.GET.get('report_type') == 'Hand Eye Coordination Report' \
                    and not (self.request.GET.get('child_user')
                             or (self.request.GET.get('from_date')
                                 and self.request.GET.get('to_date'))):
                queryset = UserHandEyeCoordinationReport.objects.filter(
                    parent_user=user)
                # serializer = GrowthReportSerializer(queryset, many=True)
                return Response(queryset.values('id', 'report_type', 'report_name',
                                                'report_image_url', 'description',
                                                'report_date__date', 'report_date__time', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Eye Sight Report' \
                    and not (self.request.GET.get('child_user')
                             or (self.request.GET.get('from_date')
                                 and self.request.GET.get('to_date'))):
                queryset = UserEyeSightReport.objects.filter(parent_user=user)
                return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description',
                                                'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        if self.request.GET.get('child_user') and self.request.GET.get('report_type') == 'Learnability Tracker':
            queryset = UserLearnabilityReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user'))
            # serializer = ReportSerializer(queryset, many=True)
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)
        if self.request.GET.get('from_date') and self.request.GET.get('to_date') and self.request.GET.get('report_type') == 'Learnability Tracker':
            queryset = UserLearnabilityReport.objects.filter(parent_user=user, report_date__range=[
                                                             self.request.GET.get('from_date'), self.request.GET.get('to_date')])
            # serializer = ReportSerializer(queryset, many=True)
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        if self.request.GET.get('child_user') and self.request.GET.get('report_type') == 'Growth Tracker':
            queryset = UserGrowthReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user'))
            # serializer = GrowthReportSerializer(queryset, many=True)
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)
        if self.request.GET.get('from_date') and self.request.GET.get('to_date') and self.request.GET.get('report_type') == 'Growth Tracker':
            queryset = UserGrowthReport.objects.filter(parent_user=user, report_date__range=[
                                                       self.request.GET.get('from_date'), self.request.GET.get('to_date')])
            # serializer = GrowthReportSerializer(queryset, many=True)
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        if self.request.GET.get('child_user') and self.request.GET.get('report_type') == 'Hand Eye Coordination Report':
            queryset = UserHandEyeCoordinationReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user'))
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)
        if self.request.GET.get('from_date') and self.request.GET.get('to_date') and self.request.GET.get('report_type') == 'Hand Eye Coordination Report':
            queryset = UserHandEyeCoordinationReport.objects.filter(parent_user=user, report_date__range=[
                                                                    self.request.GET.get('from_date'), self.request.GET.get('to_date')])
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        if self.request.GET.get('child_user') and self.request.GET.get('report_type') == 'Eye Sight Report':
            queryset = UserEyeSightReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user'))
            return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)
        if self.request.GET.get('from_date') and self.request.GET.get('to_date') and self.request.GET.get('report_type') == 'Eye Sight Report':
            queryset = UserEyeSightReport.objects.filter(parent_user=user, report_date__range=[
                                                         self.request.GET.get('from_date'), self.request.GET.get('to_date')])
            return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description', 'report_date', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        if self.request.GET.get('child_user') and not ((self.request.GET.get('from_date') and self.request.GET.get('to_date')) or self.request.GET.get('report_type')):
            learnability_queryset = UserLearnabilityReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user')).select_related()
            growth_queryset = UserGrowthReport.objects.filter(
                parent_user=user, child_user__id=self.request.GET.get('child_user')).select_related()
            # serializer = GrowthReportSerializer(queryset, many=True)
            data = {'learnability_reports': learnability_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob',
                                                                         'child_user__age'), 'growth_reports': growth_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age')}
            return Response(data, status=status.HTTP_200_OK)

        if (self.request.GET.get('from_date') and self.request.GET.get('to_date')) and not (self.request.GET.get('child_user') or self.request.GET.get('report_type')):
            learnability_queryset = UserLearnabilityReport.objects.filter(parent_user=user, report_date__range=[
                                                                          self.request.GET.get('from_date'), self.request.GET.get('to_date')]).select_related()
            growth_queryset = UserGrowthReport.objects.filter(parent_user=user, report_date__range=[
                                                              self.request.GET.get('from_date'), self.request.GET.get('to_date')]).select_related()
            # serializer = GrowthReportSerializer(queryset, many=True)
            data = {'learnability_reports': learnability_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob',
                                                                         'child_user__age'), 'growth_reports': growth_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age')}
            return Response(data, status=status.HTTP_200_OK)

        if self.request.GET.get('from_date') and self.request.GET.get('to_date') and self.request.GET.get('report_type') == 'Growth Tracker':
            queryset = UserGrowthReport.objects.filter(parent_user=user, report_date__range=[
                                                       self.request.GET.get('from_date'), self.request.GET.get('to_date')])
            # serializer = GrowthReportSerializer(queryset, many=True)
            return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

        # if not self.request.GET.get('report_type') or (self.request.GET.get('from_date') and self.request.GET.get('to_date')) or self.request.GET.get('child_user'):

        learnability_queryset = UserLearnabilityReport.objects.filter(
            parent_user=user).select_related()
        growth_queryset = UserGrowthReport.objects.filter(
            parent_user=user).select_related()
        hand_eye_queryset = UserHandEyeCoordinationReport.objects.filter(
            parent_user=user).select_related()
        eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user).select_related()
        # learnability_serializer = ReportSerializer(learnability_queryset, many=True)
        # growth_serializer = GrowthReportSerializer(growth_queryset, many=True)
        # data = {'learnability_reports':learnability_serializer.data,'growth_reports':growth_serializer.data}
        data = {'learnability_reports': learnability_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'),
                'growth_reports': growth_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'),
                'hand_eye_reports': hand_eye_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'),
                'eye_sight_reports': eye_sight_queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description', 'report_date__date', 'report_date__time', 'report', 'parent_user_id', 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address', 'parent_user__dob', 'parent_user__age', 'child_user_id', 'child_user__full_name', 'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url', 'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age')}
        return Response(data, status=status.HTTP_200_OK)


class GetReportsDetails(RetrieveAPIView):
    serializer_class = GetReportSerializer
    report_param = openapi.Parameter('report_type', openapi.IN_QUERY, description="Report type should be passed to get the data based on their type. If no report type is passed then the repsonse will be an empty queryset",
                                     required=True, type=openapi.TYPE_STRING, enum=['Learnability', 'Growth', 'Eyesight', 'Vaccination', 'Food & Nutrition', 'Hand & Eye Coordination'])

    @swagger_auto_schema(manual_parameters=[report_param])
    def get(self, request, *args, **kwargs):
        report_id = self.kwargs['pk']
        report_type = request.query_params.get('report_type')
        print(report_type)
        if report_type == 'Learnability':
            if UserLearnabilityReport.objects.filter(report_type=report_id).exists():
                report = UserLearnabilityReport.objects.get(
                    report_type=report_id)
                serializer = ReportSerializer(report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No report found'}, status=status.HTTP_400_BAD_REQUEST)
        elif report_type == 'Growth':
            if UserGrowthReport.objects.filter(report_type=report_id).exists():
                report = UserGrowthReport.objects.get(report_type=report_id)
                serializer = GrowthReportSerializer(report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No report found'}, status=status.HTTP_400_BAD_REQUEST)

        elif report_type == 'Eyesight':
            if UserEyeSightReport.objects.filter(report_id=report_id).exists():
                report = UserEyeSightReport.objects.get(report_id=report_id)
                serializer = EyeSightReportSerializer(report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No report found'}, status=status.HTTP_400_BAD_REQUEST)

        elif report_type == 'Hand & Eye Coordination':
            if UserHandEyeCoordinationReport.objects.filter(report_type=report_id).exists():
                report = UserHandEyeCoordinationReport.objects.get(
                    report_type=report_id)
                serializer = HandEyeTrackerReportSerializer(report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No report found'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response([], status=status.HTTP_200_OK)
# from reportlab.pdfgen import canvas

# def create_multiple_pdfs():
#     pdf_file = 'multipage.pdf'

#     can = canvas.Canvas(pdf_file)

#     can.drawString(20, 800, "First Page")
#     can.showPage()

#     can.drawString(20, 800, "Second Page")
#     can.showPage()

#     can.drawString(20, 700, "Third Page")
#     can.showPage()

#     can.save()

# create_multiple_pdfs()


class GetLatestReportListView(ListAPIView):
    serializer_class = ReportSerializer

    report_param = openapi.Parameter('report_type', openapi.IN_QUERY, description="Report type should be passed to get the data based on their type. If no report type is passed then the repsonse will be an empty queryset",
                                     required=False, type=openapi.TYPE_STRING, enum=['Learnability', 'Growth', 'Eyesight', 'Vaccination', 'Food & Nutrition', 'Hand & Eye Coordination', 'Analytical', 'Skin', 'Hair'])
    child_id = openapi.Parameter('child_id', openapi.IN_QUERY,
                                 description="Child id should be passed to get the data based on their type. If no report type is passed then the repsonse will be an empty queryset", required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[report_param, child_id])
    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        if self.request.GET.get('report_type') and self.request.GET.get('child_id'):
            if self.request.GET.get('report_type') == 'Learnability Tracker':
                queryset = UserLearnabilityReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                'description', 'report_date', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                                                'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address',
                                                'parent_user__dob', 'parent_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Growth Tracker':
                queryset = UserGrowthReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                'description', 'report_date', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                                                'parent_user__profile_pic_url', 'parent_user__gender',
                                                'parent_user__address',
                                                'parent_user__dob', 'parent_user__age', 'child_user_id',
                                                'child_user__full_name',
                                                'child_user__email', 'child_user__mobile',
                                                'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob',
                                                'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Hand Eye Coordination Report':
                queryset = UserHandEyeCoordinationReport.objects.filter(
                    parent_user=user, child_user=Users.objects.get(id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_type__test_question_answer', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob',
                                                'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Eye Sight Report':
                queryset = UserEyeSightReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Analytical Report':
                queryset = UserAnalyticalReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Skin Tracker':
                print("in condition")
                queryset = UserSkinReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                return Response(queryset.values(
                    'id', 'report_type', 'report_name', 'report_image_url',
                    'description', 'report_date', 'report', 'parent_user_id',
                    'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                    'parent_user__profile_pic_url', 'parent_user__gender',
                    'parent_user__address', 'parent_user__dob', 'parent_user__age'),
                    status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Hair Tracker':
                queryset = UserHairReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                    id=self.request.GET.get('child_id'))).order_by('-id')[:1]
                child_score = HairTrackerSectionAnswers.objects.filter(hair_tracker=queryset.values('report_type__id'))
                return Response(queryset.values(
                    'id', 'report_type', 'report_name', 'report_image_url',
                    'description', 'report_date', 'report', 'parent_user_id',
                    'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                    'parent_user__profile_pic_url', 'parent_user__gender',
                    'parent_user__address', 'parent_user__dob', 'parent_user__age'),
                    status=status.HTTP_200_OK)

            learnability_queryset = UserLearnabilityReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            growth_queryset = UserGrowthReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            hand_eye_queryset = UserHandEyeCoordinationReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            hand_eye_test_1_queryset = UserHandEyeCoordinationReport.objects.filter(
            parent_user=user,child_user=Users.objects.get(
                id=self.request.GET.get('child_id')),report_type__test_name='hand_and_eye_test_1').select_related().order_by('-id')[:1]
            hand_eye_test_2_queryset = UserHandEyeCoordinationReport.objects.filter(
            parent_user=user,child_user=Users.objects.get(
                id=self.request.GET.get('child_id')),report_type__test_name='hand_and_eye_test_2').select_related().order_by('-id')[:1]
            dry_eye_sight_queryset = UserEyeSightReport.objects.filter(parent_user=user, report_id__test_type='dry_eyesight_test', child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            colorblindness_eye_sight_queryset = UserEyeSightReport.objects.filter(parent_user=user, report_id__test_type='color_blindness_test', child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            astigmatism_eye_sight_queryset = UserEyeSightReport.objects.filter(parent_user=user, report_id__test_type='astigmatism_test', child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            corneal_curvature_eye_sight_queryset = UserEyeSightReport.objects.filter(
                parent_user=user, report_id__test_type='corneal_curvature_test', child_user=Users.objects.get(id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            visual_acquity_eye_sight_queryset = UserEyeSightReport.objects.filter(parent_user=user, report_id__test_type='visual_acquity_test', child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            analytical_queryset = UserAnalyticalReport.objects.filter(parent_user=user,
                                                                      report_id__test_type='analytical_test',
                                                                      child_user=Users.objects.get(id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]

            skin_queryset = UserSkinReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            hair_queryset = UserHairReport.objects.filter(parent_user=user, child_user=Users.objects.get(
                id=self.request.GET.get('child_id'))).select_related().order_by('-id')[:1]
            child_score = HairTrackerSectionAnswers.objects.filter(hair_tracker=hair_queryset.values('report_type__id'))
            answer_array = []
            for i in child_score:
                answer_array.append(i)
            data = {
                'learnability_reports': learnability_queryset.values('id', 'report_type', 'report_name',
                                                                     'report_image_url', 'description', 'report_date__date',
                                                                     'report_date__time__hour', 'report_date__time__minute', 'report',
                                                                     'parent_user_id', 'parent_user__full_name',
                                                                     'parent_user__email', 'parent_user__mobile',
                                                                     ),

                'growth_reports': growth_queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                         'description',  'report_date__date', 'report_date__time__hour',
                                                         'report_date__time__minute', 'report', 'parent_user_id',
                                                         'parent_user__full_name', 'parent_user__email',
                                                         'parent_user__mobile'),
                'hand_eye_reports': {'hand_and_eye_test_1': hand_eye_test_1_queryset.values('id', 'report_type',
                                                                                            'report_type__test_question_answer',
                                                                                            'report_name', 'report_image_url',
                                                                                            'description', 'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                            'parent_user__full_name', 'parent_user__email',
                                                                                            'parent_user__mobile'),
                                'hand_and_eye_test_2':hand_eye_test_2_queryset.values('id', 'report_type', 'report_type__test_question_answer',
                                                         'report_name', 'report_image_url',
                                                         'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                         'parent_user__full_name', 'parent_user__email',
                                                         'parent_user__mobile')
                                },
                'analytical_reports': analytical_queryset.values('id', 'report_id', 'report_id__test_answer',
                                                                 'report_name', 'report_image_url',  'description', 'report_date__date',
                                                                 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                 'parent_user__full_name', 'parent_user__email', 'parent_user__mobile'),

                'eye_sight_reports': {
                    'color_blindness_test': colorblindness_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                     'report_id__test_name_answer', 'report_name',
                                                                                     'report_image_url', 'description', 'report_date__date',
                                                                                     'report_date__time__hour', 'report_date__time__minute', 'report',
                                                                                     'parent_user_id', 'parent_user__full_name', 'parent_user__email',
                                                                                     'parent_user__mobile'),
                    'dry_eye_test': dry_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                  'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                  'description',  'report_date__date', 'report_date__time__hour',
                                                                  'report_date__time__minute', 'report', 'parent_user_id',
                                                                  'parent_user__full_name', 'parent_user__email',
                                                                  'parent_user__mobile'),
                    'astigmatism_eye_test': astigmatism_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                  'report_id__test_name_answer', 'report_name',
                                                                                  'report_image_url', 'description',  'report_date__date',
                                                                                  'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                  'parent_user__full_name', 'parent_user__email',
                                                                                  'parent_user__mobile'),
                    'corneal_curvature_eye_test': corneal_curvature_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                              'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                              'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                              'parent_user__full_name', 'parent_user__email',
                                                                                              'parent_user__mobile'),
                    'visual_acquity_eye_test': visual_acquity_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                        'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                        'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                        'parent_user__full_name', 'parent_user__email',
                                                                                        'parent_user__mobile')},

                'skin_reports': skin_queryset.values('id', 'report_type', 'report_name', 'report_image_url', 'description',
                                                     'report_date__date', 'report_date__time__hour',
                                                     'report_date__time__minute', 'report', 'parent_user_id',
                                                     'parent_user__full_name', 'parent_user__email', 'parent_user__mobile'),
                'hair_reports': child_score.values('id', 'hair_tracker_id','hair_tracker__user__id','hair_tracker__user__full_name', 'hair_tracker__user__email', 'hair_tracker__user__mobile'),

            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            if self.request.GET.get('report_type') == 'Learnability Tracker':
                queryset = UserLearnabilityReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                'description', 'report_date', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                                                'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address',
                                                'parent_user__dob', 'parent_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Growth Tracker':
                queryset = UserGrowthReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                'description', 'report_date', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                                                'parent_user__profile_pic_url', 'parent_user__gender',
                                                'parent_user__address',
                                                'parent_user__dob', 'parent_user__age', 'child_user_id',
                                                'child_user__full_name',
                                                'child_user__email', 'child_user__mobile',
                                                'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob',
                                                'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Hand Eye Coordination Report':
                queryset = UserHandEyeCoordinationReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_type__test_question_answer', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob',
                                                'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Eye Sight Report':
                queryset = UserEyeSightReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Analytical Report':
                queryset = UserAnalyticalReport.objects.filter(parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_id', 'report_name', 'report_image_url', 'description',
                                                'report_date', 'report', 'parent_user_id', 'parent_user__full_name',
                                                'parent_user__email', 'parent_user__mobile', 'parent_user__profile_pic_url',
                                                'parent_user__gender', 'parent_user__address', 'parent_user__dob',
                                                'parent_user__age', 'child_user_id', 'child_user__full_name',
                                                'child_user__email', 'child_user__mobile', 'child_user__profile_pic_url',
                                                'child_user__gender', 'child_user__address', 'child_user__dob', 'child_user__age'), status=status.HTTP_200_OK)

            elif self.request.GET.get('report_type') == 'Skin Tracker':
                queryset = UserSkinReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                'description', 'report_date', 'report', 'parent_user_id',
                                                'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                                                'parent_user__profile_pic_url', 'parent_user__gender', 'parent_user__address',
                                                'parent_user__dob', 'parent_user__age'), status=status.HTTP_200_OK)
            elif self.request.GET.get('report_type') == 'Hair Tracker':
                queryset = UserHairReport.objects.filter(
                    parent_user=user).order_by('-id')[:1]
                return Response(queryset.values(
                    'id', 'report_type', 'report_name', 'report_image_url',
                    'description', 'report_date', 'report', 'parent_user_id','report_type_id',
                    'parent_user__full_name', 'parent_user__email', 'parent_user__mobile',
                    'parent_user__profile_pic_url', 'parent_user__gender',
                    'parent_user__address', 'parent_user__dob', 'parent_user__age'),
                    status=status.HTTP_200_OK)

        learnability_queryset = UserLearnabilityReport.objects.filter(
            parent_user=user).select_related().order_by('-id')[:1]
        growth_queryset = UserGrowthReport.objects.filter(
            parent_user=user).select_related().order_by('-id')[:1]
        hand_eye_test_1_queryset = UserHandEyeCoordinationReport.objects.filter(
            parent_user=user,report_type__test_name='hand_and_eye_test_1').select_related().order_by('-id')[:1]
        hand_eye_test_2_queryset = UserHandEyeCoordinationReport.objects.filter(
            parent_user=user,report_type__test_name='hand_and_eye_test_2').select_related().order_by('-id')[:1]
        dry_eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user, report_id__test_type='dry_eyesight_test').select_related().order_by('-id')[:1]
        colorblindness_eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user, report_id__test_type='color_blindness_test').select_related().order_by('-id')[:1]
        astigmatism_eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user, report_id__test_type='astigmatism_test').select_related().order_by('-id')[:1]
        corneal_curvature_eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user, report_id__test_type='corneal_curvature_test').select_related().order_by('-id')[:1]
        visual_acquity_eye_sight_queryset = UserEyeSightReport.objects.filter(
            parent_user=user, report_id__test_type='visual_acquity_test').select_related().order_by('-id')[:1]
        analytical_queryset = UserAnalyticalReport.objects.filter(
            parent_user=user, report_id__test_type='analytical_test').select_related().order_by('-id')[:1]
        skin_queryset = UserSkinReport.objects.filter(
            parent_user=user).select_related().order_by('-id')[:1]
        hair_queryset = UserHairReport.objects.filter(
            parent_user=user).select_related().order_by('-id')[:1]

        data = {
            'learnability_reports': learnability_queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                                 'description', 'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report',
                                                                 'parent_user_id', 'parent_user__full_name',
                                                                 'parent_user__email', 'parent_user__mobile',
                                                                 ),

            'growth_reports': growth_queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                     'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                     'parent_user__full_name', 'parent_user__email',
                                                     'parent_user__mobile'),

            'hand_eye_reports': {'hand_and_eye_test_1':hand_eye_test_1_queryset.values('id', 'report_type', 'report_type__test_question_answer',
                                                         'report_name', 'report_image_url',
                                                         'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                         'parent_user__full_name', 'parent_user__email',
                                                         'parent_user__mobile'),
                                'hand_and_eye_test_2':hand_eye_test_2_queryset.values('id', 'report_type', 'report_type__test_question_answer',
                                                         'report_name', 'report_image_url',
                                                         'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                         'parent_user__full_name', 'parent_user__email',
                                                         'parent_user__mobile')
                                },

            'analytical_reports': analytical_queryset.values('id', 'report_id', 'report_id__test_answer',
                                                             'report_name', 'report_image_url',
                                                             'description', 'report_date__date', 'report_date__time__hour',
                                                             'report_date__time__minute', 'report', 'parent_user_id',
                                                             'parent_user__full_name', 'parent_user__email', 'parent_user__mobile'),

            'eye_sight_reports': {'color_blindness_test': colorblindness_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                                   'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                                   'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                                   'parent_user__full_name', 'parent_user__email',
                                                                                                   'parent_user__mobile'),
                                  'dry_eye_test': dry_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                'parent_user__full_name', 'parent_user__email',
                                                                                'parent_user__mobile'),
                                  'astigmatism_eye_test': astigmatism_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                                'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                                'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                                'parent_user__full_name', 'parent_user__email',
                                                                                                'parent_user__mobile'),
                                  'corneal_curvature_eye_test': corneal_curvature_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                                            'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                                            'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                                            'parent_user__full_name', 'parent_user__email',
                                                                                                            'parent_user__mobile'),
                                  'visual_acquity_eye_test': visual_acquity_eye_sight_queryset.values('id', 'report_id', 'report_id__test_type',
                                                                                                      'report_id__test_name_answer', 'report_name', 'report_image_url',
                                                                                                      'description',  'report_date__date', 'report_date__time__hour', 'report_date__time__minute', 'report', 'parent_user_id',
                                                                                                      'parent_user__full_name', 'parent_user__email',
                                                                                                      'parent_user__mobile')},
            'skin_reports': skin_queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                 'description', 'report_date__date',
                                                 'report_date__time__hour', 'report_date__time__minute',
                                                 'report', 'parent_user_id', 'parent_user__full_name',
                                                 'parent_user__email', 'parent_user__mobile'),
            'hair_reports': hair_queryset.values('id', 'report_type', 'report_name', 'report_image_url',
                                                 'description', 'report_date__date', 'report_type_id',
                                                 'report_date__time__hour', 'report_date__time__minute',
                                                 'report', 'parent_user_id', 'parent_user__full_name',
                                                 'parent_user__email', 'parent_user__mobile',
                                                 ),

        }
        return Response(data, status=status.HTTP_200_OK)


class CreateSkinReportPDFView(CreateAPIView):
    serializer_class = CreateReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Skin Report PDF
        '''

        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserSkinReport.objects.create(parent_user=logged_in_user,
                                                       child_user=Users.objects.get(
                                                           id=serializer.validated_data.get('child_user')),
                                                       report_type=SkinTracker.objects.get(
                                                           id=serializer.validated_data.get('report_id')),
                                                       report_name='Skin Report',
                                                       report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
                                                       )
            skin_obj = SkinTrackerSectionAnswers.objects.filter(
                skin_tracker=SkinTracker.objects.get(id=serializer.validated_data.get('report_id')))
            reading = 0
            spelling_writing = 0
            math_logic = 0
            emotion_self_control = 0
            listening = 0
            attention = 0
            for i in skin_obj:
                print(i.section_name, i.answer)
                if i.section_name == 'Reading':
                    reading = i.answer
                elif i.section_name == 'Spelling & Writing':
                    spelling_writing = i.answer
                elif i.section_name == 'Math & Logic':
                    math_logic = i.answer
                elif i.section_name == 'Emotion & Self-Control':
                    emotion_self_control = i.answer
                elif i.section_name == 'Listening':
                    listening = i.answer
                elif i.section_name == 'Attention':
                    attention = i.answer

            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, '931 Maidan Gari, North Delhi INDIA-181004')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(
                45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
            c.setFont('Times-Roman', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 550, 'Age -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(365, 550, f'{report_obj.child_user.age}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 575, '120cm')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 480, 'TEST NAME')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 480, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(260, 480, 'MEASURED VALUE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            para = Paragraph(serializer.validated_data.get(
                'interpretations'), style=normalStyle)
            if len(serializer.validated_data.get('interpretations')) < 250:
                para.wrap(580, 280)
                para.drawOn(c, 15, 280)
            elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
                para.wrap(580, 240)
                para.drawOn(c, 15, 240)
            else:
                para.wrap(580, 210)
                para.drawOn(c, 15, 210)
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        460, 50, width=50, height=50, mask='auto')
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        540, 50, width=50, height=50, mask='auto')
            c.setFont('Times-Roman', 10)
            c.drawString(455, 45, 'Download iOS')
            c.drawString(530, 45, 'Download android')
            c.setFont('Times-Roman', 12)
            c.drawString(
                150, 30, 'Disclaimer :- This a dummy disclaimer for reports generated on detoxa platform.')
            c.drawString(250, 15, 'https://detoxa.netlify.app')
            data = [
                ['Reading Skills', f'{reading}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 455)

            data = [
                ['Spelling and Writing Skills', f'{spelling_writing}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 435)
            data = [
                ['Math & Logic Skills', f'{math_logic}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 415)
            data = [
                ['Emotion & Self-Control', f'{emotion_self_control}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 395)
            data = [
                ['Listening Skills ', f'{listening}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 375)
            data = [
                ['Attention Skills', f'{attention}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 355)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')),
                                               ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class CreateHairReportPDFView(CreateAPIView):
    serializer_class = CreateHairTrackerReportSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create Hair Report PDF
        '''

        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateHairTrackerReportSerializer(data=request.data)
        if serializer.is_valid():
            report_obj = UserHairReport.objects.create(
                parent_user=logged_in_user,
                child_user=Users.objects.get(
                    id=serializer.validated_data.get('child_user')),

                report_type=HairTracker.objects.get(
                    id=serializer.validated_data.get('report_id')[0]),

                # report_type=HairTracker.objects.get(
                #     id=serializer.validated_data.get('report_id')),
                report_name='Hair Report',
                report_image_url='https://detoxa.s3.us-east-2.amazonaws.com/learnability.png',
            )
            hair_obj = HairTrackerSectionAnswers.objects.filter(
                hair_tracker=HairTracker.objects.get(id=serializer.validated_data.get('report_id')[0]))
            reading = 0
            spelling_writing = 0
            math_logic = 0
            emotion_self_control = 0
            listening = 0
            attention = 0
            for i in hair_obj:
                print(i.section_name, i.answer)
                if i.section_name == 'Reading':
                    reading = i.answer
                elif i.section_name == 'Spelling & Writing':
                    spelling_writing = i.answer
                elif i.section_name == 'Math & Logic':
                    math_logic = i.answer
                elif i.section_name == 'Emotion & Self-Control':
                    emotion_self_control = i.answer
                elif i.section_name == 'Listening':
                    listening = i.answer
                elif i.section_name == 'Attention':
                    attention = i.answer

            file_name = f'{(report_obj.child_user.full_name).lower()}_{report_obj.id}_report.pdf'
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/PDF%20Report%20Format.jpg',
                        0, 0, width=610, height=800, mask='auto')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(320, 770, '931 Maidan Gari, North Delhi INDIA-181004')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(420, 750, '+91-8448669501')
            c.setFont('Times-Roman', 10)
            c.drawString(320, 730, 'support@detoxa.in')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(320, 665, 'Book Counselling Session - 8448669501')
            c.setFillColor(black)
            c.setFont('Times-Roman', 10)
            c.drawString(
                45, 680, f'Test Conducted At :{report_obj.report_date.strftime("%Y-%m-%d, %H:%M")}')
            c.setFont('Times-Roman', 10)
            c.drawString(45, 650, 'Test Mode : Online')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 600, 'User Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 600, f'{report_obj.parent_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 575, 'Child Name -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(95, 575, f'{report_obj.child_user.full_name}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(15, 550, 'User ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(80, 550, f'{report_obj.parent_user.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 600, 'Report ID -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(395, 600, f'{report_obj.id}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 575, 'Gender -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(385, 575, f'{report_obj.child_user.gender}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(325, 550, 'Age -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(365, 550, f'{report_obj.child_user.age}')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 600, 'Weight -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 600, '18Kg')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(500, 575, 'Height -')
            c.setFillColor(black)
            c.setFont('Times-Roman', 14)
            c.drawString(555, 575, '120cm')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(30, 480, 'TEST NAME')
            # c.setFillColor('#9f0a10')
            # c.setFont('Times-Roman', 14)
            # c.drawString(260, 480, 'YOUR SCORE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 14)
            c.drawString(260, 480, 'MEASURED VALUE')
            c.setFillColor('#9f0a10')
            c.setFont('Times-Roman', 16)
            c.drawString(10, 310, 'INTERPRETATIONS')
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            para = Paragraph(serializer.validated_data.get(
                'interpretations'), style=normalStyle)
            if len(serializer.validated_data.get('interpretations')) < 250:
                para.wrap(580, 280)
                para.drawOn(c, 15, 280)
            elif len(serializer.validated_data.get('interpretations')) > 250 and len(serializer.validated_data.get('interpretations')) < 450:
                para.wrap(580, 240)
                para.drawOn(c, 15, 240)
            else:
                para.wrap(580, 210)
                para.drawOn(c, 15, 210)
            c.setFillColor(black)
            c.setFont('Times-Roman', 16)
            c.drawString(10, 160, 'NOTES :-')
            if serializer.validated_data.get('note_1'):
                para = Paragraph(
                    "1."+serializer.validated_data.get('note_1'), style=normalStyle)
                para.wrap(530, 145)
                para.drawOn(c, 85, 145)
            if serializer.validated_data.get('note_2'):
                para = Paragraph(
                    "2."+serializer.validated_data.get('note_2'), style=normalStyle)
                para.wrap(530, 120)
                para.drawOn(c, 85, 120)
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        460, 50, width=50, height=50, mask='auto')
            c.drawImage('https://docs.microsoft.com/en-us/samples/xamarin/ios-samples/qrchestra/media/xamarin-barcode.png',
                        540, 50, width=50, height=50, mask='auto')
            c.setFont('Times-Roman', 10)
            c.drawString(455, 45, 'Download iOS')
            c.drawString(530, 45, 'Download android')
            c.setFont('Times-Roman', 12)
            c.drawString(
                150, 30, 'Disclaimer :- This a dummy disclaimer for reports generated on detoxa platform.')
            c.drawString(250, 15, 'https://detoxa.netlify.app')
            data = [
                ['Reading Skills', f'{reading}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 455)

            data = [
                ['Spelling and Writing Skills', f'{spelling_writing}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 435)
            data = [
                ['Math & Logic Skills', f'{math_logic}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 415)
            data = [
                ['Emotion & Self-Control', f'{emotion_self_control}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 395)
            data = [
                ['Listening Skills ', f'{listening}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 375)
            data = [
                ['Attention Skills', f'{attention}'],
            ]
            t = Table(data, 2*[2.68*inch], 1*[0.2*inch])
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                    ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), black),
                    ('BOX', (0, 0), (-1, -1), 0.25, black),
                ]
            ))
            t.wrap(0, 0)
            t.drawOn(c, 15, 355)
            c.showPage()

            c.save()
            buf.seek(0)
            pdf_file_name = file_name
            with open(pdf_file_name, 'wb') as f:
                f.write(buf.getvalue())
                buf.close()
            if not report_obj.is_downloaded:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')),
                                               ACL='public-read', ContentDisposition='inline')
                report_obj.report = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
                report_obj.is_downloaded = True
                report_obj.save()
            data = {
                "success": True,
                'data': 'Report downloaded successfully',
                'report_file': report_obj.report
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_200_OK)


class GenerateOTPforReport(GenericAPIView):
    serializer_class = GenerateOTPforReportSerializer

    def post(self, request, *args, **kwargs):
        serializer = GenerateOTPforReportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                report_obj = UserGrowthReport.objects.get(parent_user__mobile=serializer.validated_data['phone_number'],
                                                          id=serializer.validated_data['report_id'])
                # if report_obj.parent_user.mobile == serializer.validated_data['phone_number']:
                user_obj = Users.objects.get(mobile=report_obj.parent_user.mobile)
                if user_obj.is_active:
                    otp_generation = generateMobileOTP(serializer.validated_data['phone_number'])
                if request.META['HTTP_HOST'] == '127.0.0.1:8000':
                    if otp_generation['Status'] == 'Success':
                        data = {
                            "success": True,
                            'data': 'OTP sent successfully',
                            'otp': otp_generation
                        }
                        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
                    else:
                        logger.error("OTP not sent", otp_generation)
                        raise exceptions.ValidationError(otp_generation.json())
                else:
                    if otp_generation['Status'] == 'Success':
                        data = {
                            "success": True,
                            "otp": otp_generation,
                            "message": "OTP sent successfully"
                        }
                        logger.info("OTP sent successfully")
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        logger.error("OTP not sent", otp_generation)
                        raise exceptions.ValidationError(otp_generation.json())
                # else:
                #     data = {
                #         "success": False,
                #         'message': "This report id is not registered with this number."
                #     }
                #     return Response(data, status=status.HTTP_404_NOT_FOUND)
            except UserGrowthReport.DoesNotExist:
                data = {
                    "success": False,
                    'message': "Entered report Id does not belong to entered mobile number. Please enter registered "
                               "mobile number. "
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPforReport(GenericAPIView):
    serializer_class = VerifyOTPforReportSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPforReportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                report_obj = ''
                user_obj = Users.objects.get(
                    mobile=serializer.validated_data['phone_number'])
                report_type = serializer.validated_data['report_type']
                if user_obj.is_active:
                    otp_verification = verifyMobileOTP(
                        serializer.validated_data['session_id'], serializer.validated_data['otp'])
                    if serializer.validated_data['report_type'] == 'Growth':
                        try:
                            report_obj = UserGrowthReport.objects.get(id=serializer.validated_data['report_id'])
                        except Exception as e:
                            print(e)
                            data = {
                                "success": False,
                                "data": 'Report id does not exist.'
                            }
                            return Response(data, status=status.HTTP_404_NOT_FOUND)

                    if serializer.validated_data['report_type'] == 'Learnability':
                        report_obj = UserLearnabilityReport.objects.get(
                            id=serializer.validated_data['report_id'])
                    if serializer.validated_data['report_type'] == 'Eyesight':
                        report_obj = UserEyeSightReport.objects.get(id=serializer.validated_data['report_id'])
                    # if serializer.validated_data['report_type'] == 'Food & Nutrition':
                    #     report_obj = UserGrowthReport.objects.get(id=serializer.validated_data['report_id'])
                    if serializer.validated_data['report_type'] == 'Hand & Eye Coordination':
                        report_obj = UserHandEyeCoordinationReport.objects.get(
                            id=serializer.validated_data['report_id'])
                    if serializer.validated_data['report_type'] == 'Analytical':
                        report_obj = UserAnalyticalReport.objects.get(
                            id=serializer.validated_data['report_id'])
                    if serializer.validated_data['report_type'] == 'Skin':
                        report_obj = UserSkinReport.objects.get(
                            id=serializer.validated_data['report_id'])
                    if serializer.validated_data['report_type'] == 'Hair':
                        report_obj = UserHairReport.objects.get(
                            id=serializer.validated_data['report_id'])
                    if otp_verification == 200:
                        send_mail(f'Email for {report_type} report', f'{report_obj.report} ', settings.FROM_EMAIL, [
                                  user_obj.email], fail_silently=False)
                        data = {
                            "success": True,
                            'data': 'OTP verified successfully',
                            'report_url': report_obj.report
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        data = {
                            "success": False,
                            'data': 'OTP verification failed'
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                data = {
                    "success": False,
                    'data': str(e)
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "success": False,
                'data': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



class GenerateMedicalReportCard(GenericAPIView):
    serializer_class = GenerateMedicalReportCardSerializer

    def post(self,request,*args,**kwargs):
        serializer = GenerateMedicalReportCardSerializer(data=request.data)
        if serializer.is_valid():
            organization_obj = Organizations.objects.get(id=serializer.validated_data.get('organization_id'))
            generatemedicalreport.delay(organization_obj.id,
                                        serializer.validated_data.get('user_class'),
                                        serializer.validated_data.get('user_section'),
                                        serializer.validated_data.get('quarter'),
                                        serializer.validated_data.get('year'))
            # generatemedicalreport(organization_obj.id,serializer.validated_data.get('user_class'),serializer.validated_data.get('quarter'),serializer.validated_data.get('year'))
            return Response({"success":True,"data":"Report generated successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"success":False,"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class GetMedicalReportList(ListAPIView):
    serializer_class = GetMedicalReportListSerializer
    parser_classes = [MultiPartParser]
    pagination_class = StandardResultsSetPagination

    user_class = openapi.Parameter('user_class', openapi.IN_QUERY, description="User class should be passed to get the list of reports generated based on their class.",required=False, type=openapi.TYPE_STRING, enum=['prenursery','nursery','kg','1', '2', '3','4','5','6','7','8','9','10','11','12'])
    @swagger_auto_schema(manual_parameters=[user_class])
    def get(self,request,*args,**kwargs):
        if request.query_params.get('user_class'):
            user_class = request.query_params.get('user_class')
            logged_in_user = UserAuthentication.authenticate(self, request)[0]
            organization_obj = Organizations.objects.get(user=logged_in_user)
            data = UserMedicalReport.objects.filter(organization=organization_obj,user_class=user_class).order_by('-id')
            page = self.paginate_queryset(data)
            serializer = GetMedicalReportListSerializer(page,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        organization_obj = Organizations.objects.get(user=logged_in_user)
        data = UserMedicalReport.objects.filter(organization=organization_obj).order_by('-id')
        page = self.paginate_queryset(data)
        serializer = GetMedicalReportListSerializer(page,many=True)
        return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)


class SendMedicalReportOnEmail(GenericAPIView):
    serializer_class = SendMedicalReportOnEmailSerializer
    
    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = SendMedicalReportOnEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user_class = serializer.validated_data.get('user_class')
            user_section = serializer.validated_data.get('user_section')
            report_id = serializer.validated_data.get('report_id')
            print(email)
            send_report.delay(email,logged_in_user.id,user_class,user_section,report_id)
            return Response({"success":True,"data":"Report sent successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"success":False,"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
