import io
import os
import boto3
from celery import shared_task
from detoxa_services.models.eyesight_tracker import EyeSightTracker
from detoxa_services.models.learnability_tracker import LearnabilityTracker, LearnalityTrackerSectionAnswers
from detoxa_services.models.organizations_models import Organizations,OrganizationUser
from detoxa_services.models.users import Users
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch,A4,landscape
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Whiter, black, green, purple, red, blue, yellow
from detoxa_services.models.reports_models import (UserLearnabilityReport, UserMedicalReport,
                                                    UserMotorSkillsReport,
                                                    UserGrowthReport,
                                                    UserEyeSightReport,
                                                    UserHairReport,
                                                    UserHandEyeCoordinationReport,
                                                    UserAnalyticalReport,
                                                    UserSkinReport,
                                                    UserHairReport)

def generatepdf(organization,quarter,user_section,user,user_class,year):
    print('QUARTER:',quarter,user.user)
    print('FROM generatepdf')
    report_obj = UserMedicalReport.objects.create(
        organization=organization,
        user=user.user,
        user_class=user_class,
        user_section=user_section.capitalize(),
        year=year
    )
    file_name = f'{(report_obj.user.full_name).lower()}_{report_obj.id}_report.pdf'
    buf = io.BytesIO()
    c = canvas.Canvas(buf, landscape(pagesize=A4))

    c.drawImage('https://detoxa.s3.us-east-2.amazonaws.com/Detoxa_Report_Card.jpg',
                0, 0, width=845, height=600, mask='auto')
    c.drawImage(f'{organization.image}',30, 500, width=90, height=90, mask='auto')
    c.setFillColor(black)
    c.setFont('Times-Roman', 12)
    c.drawString(20, 490, f'{organization.address}')
    user_profile_pic = user.user.profile_pic_url if user.user.profile_pic_url is not None else 'https://detoxa.netlify.app/static/media/subscription-school.dce14b00.png'
    c.drawImage(f'{user_profile_pic}',10, 365, width=100, height=100, mask='auto')
    c.setFillColor(black)
    c.setFont('Times-Roman', 12)
    c.drawString(55, 335, f'{report_obj.user.full_name}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(50, 310, f'{report_obj.user.age}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(65, 285, f'{report_obj.user.gender}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(55, 265, f'{user.user_class}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(68, 243, f'{user.user_section}'.title())
    c.setFont('Times-Roman', 14)
    c.drawString(65, 218, f'{user.admission_number}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(75, 195, f'{user.admission_number}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 14)
    c.drawString(70, 168, f'{user.father_name}'.title())
    c.setFont('Times-Roman', 14)
    c.drawString(75, 145, f'{user.mother_name}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 13)
    c.drawString(70, 120, f'{user.father_phone}')
    c.setFillColor(black)
    c.setFont('Times-Roman', 13)
    c.drawString(75, 97, f'{user.mother_phone}'.title())
    for i in quarter:
        if i == 1:
            # print(growth_tracker_report,eyesight_tracker_report,user)
            learnability_tracker_report = UserLearnabilityReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            growth_tracker_report = UserGrowthReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            hair_tracker_report = UserHairReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            coordination_tracker_report = UserHandEyeCoordinationReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            analytical_tracker_report = UserAnalyticalReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            skin_tracker_report = UserSkinReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            eyesight_tracker_report = UserEyeSightReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            motor_tracker_report = UserMotorSkillsReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=4)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=5)|
                                                                                        Q(parent_user=user.user,report_date__year=year,report_date__month=6)).last()
            if growth_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 435, 'Height:'+growth_tracker_report.height)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(380, 435, 'Weight:'+growth_tracker_report.weight)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 425, 'Bmi:'+growth_tracker_report.bmi)
            if learnability_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 290, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(390, 290, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 280, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(395, 280, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(420, 270, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 270,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if eyesight_tracker_report is not None:
                color_blindness_test_final_value = 0
                left_eye_visual_acquity_test_final_value = 0
                right_eye_visual_acquity_test_final_value = 0
                left_eye_astigmatism_test_final_value = 'No'
                right_eye_astigmatism_test_final_value = 'No'
                left_eye_corneal_curvature_test_final_value = 'No'
                right_eye_corneal_curvature_test_final_value = 'No'
                dry_eye_test_final_value = 0
                eyesight_tracker_obj = UserEyeSightReport.objects.get(id=eyesight_tracker_report.id)
                print('Eye sight report',eyesight_tracker_obj,eyesight_tracker_report)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'color_blindness_test')
                    for i in test_values.values():
                        if i == 'True':
                            color_blindness_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'visual_acquity_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         visual_acquity_test_final_value += 1
                    left_eye_visual_acquity_test_final_value = test_values.get(
                        'left_eye').get('line_no')
                    right_eye_visual_acquity_test_final_value = test_values.get(
                        'right_eye').get('line_no')
                except Exception as e:
                    print('Exception from visual_acquity_test-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'astigmatism_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         astigmatism_test_final_value += 1
                    left_eye_astigmatism_test_final_value = test_values.get(
                        'left_eye').get('ans').title()
                    right_eye_astigmatism_test_final_value = test_values.get(
                        'right_eye').get('ans').title()

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
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(340, 405, 'L.E Visual Acquity:'+str(left_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(400, 405, 'R.E Visual Acquity:'+str(right_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(340, 395, 'L.E Astigmatism:'+str(left_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(395, 395, 'R.E Astigmatism:'+str(right_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(400, 385, 'R.E Corneal Curvature:'+str(right_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(340, 385,'L.E Corneal Curvature:'+str(left_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(410, 375,'Dry Eye Test:'+str(dry_eye_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(340, 375, 'Color Blindness:'+str(color_blindness_test_final_value))
            if coordination_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 345, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(390, 345, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 335, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(395, 335, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(420, 325, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 325,'Emotion & Self-Ctrl:'+str(emotion_self_control)) 
            if motor_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 260, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(390, 260, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 250, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(395, 250, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(420, 240, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 240,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if analytical_tracker_report is not None:
                print(analytical_tracker_report)
                analytical_test_final_value = 0
                analytical_tracker_obj = analytical_tracker_report
                try:
                    test_values = analytical_tracker_obj.test_answer.get(
                        'analytical_test')
                    for i in test_values.values():
                        if i == 'True':
                            analytical_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(340, 175, 'Analytical Test Result:'+str(analytical_test_final_value))
        if i == 2:
            learnability_tracker_report = UserLearnabilityReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            growth_tracker_report = UserGrowthReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            hair_tracker_report = UserHairReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            coordination_tracker_report = UserHandEyeCoordinationReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            analytical_tracker_report = UserAnalyticalReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            skin_tracker_report = UserSkinReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            eyesight_tracker_report = UserEyeSightReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()
            motor_tracker_report = UserMotorSkillsReport.objects.filter(Q(parent_user=user.user,report_date__year=year,report_date__month=7)|
                                                                                        Q(parent_user=user.user,report_date__year=year,report_date__month=8)|
                                                                                        Q(parent_user=user.user,report_date__year=year,report_date__month=9)).last()

            
            print(growth_tracker_report,eyesight_tracker_report,user)
            if growth_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 435, 'Height:'+growth_tracker_report.height)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(510, 435, 'Weight:'+growth_tracker_report.weight)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 425, 'Bmi:'+growth_tracker_report.bmi)
            if learnability_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 290, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(520, 290, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 280, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(525, 280, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(550, 270, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 270,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if eyesight_tracker_report is not None:
                color_blindness_test_final_value = 0
                left_eye_visual_acquity_test_final_value = 0
                right_eye_visual_acquity_test_final_value = 0
                left_eye_astigmatism_test_final_value = 'No'
                right_eye_astigmatism_test_final_value = 'No'
                left_eye_corneal_curvature_test_final_value = 'No'
                right_eye_corneal_curvature_test_final_value = 'No'
                dry_eye_test_final_value = 0
                eyesight_tracker_obj = UserEyeSightReport.objects.get(id=eyesight_tracker_report.id)
                print('Eye sight report',eyesight_tracker_obj,eyesight_tracker_report)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'color_blindness_test')
                    for i in test_values.values():
                        if i == 'True':
                            color_blindness_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'visual_acquity_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         visual_acquity_test_final_value += 1
                    left_eye_visual_acquity_test_final_value = test_values.get(
                        'left_eye').get('line_no')
                    right_eye_visual_acquity_test_final_value = test_values.get(
                        'right_eye').get('line_no')
                except Exception as e:
                    print('Exception from visual_acquity_test-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'astigmatism_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         astigmatism_test_final_value += 1
                    left_eye_astigmatism_test_final_value = test_values.get(
                        'left_eye').get('ans').title()
                    right_eye_astigmatism_test_final_value = test_values.get(
                        'right_eye').get('ans').title()

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
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(470, 405, 'L.E Visual Acquity:'+str(left_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(530, 405, 'R.E Visual Acquity:'+str(right_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(470, 395, 'L.E Astigmatism:'+str(left_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(535, 395, 'R.E Astigmatism:'+str(right_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(530, 385, 'R.E Corneal Curvature:'+str(right_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(470, 385,'L.E Corneal Curvature:'+str(left_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(550, 375,'Dry Eye Test:'+str(dry_eye_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(470, 375, 'Color Blindness:'+str(color_blindness_test_final_value))
            if coordination_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 345, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(520, 345, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 335, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(525, 335, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(550, 325, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 325,'Emotion & Self-Ctrl:'+str(emotion_self_control))     
            if motor_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 260, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(520, 260, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 250, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(525, 250, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(540, 240, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 240,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if analytical_tracker_report is not None:
                print(analytical_tracker_report)
                analytical_test_final_value = 0
                analytical_tracker_obj = analytical_tracker_report
                try:
                    test_values = analytical_tracker_obj.test_answer.get(
                        'analytical_test')
                    for i in test_values.values():
                        if i == 'True':
                            analytical_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(470, 175, 'Analytical Test Result:'+str(analytical_test_final_value))
        if i == 3:
            learnability_tracker_report = UserLearnabilityReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            growth_tracker_report = UserGrowthReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            hair_tracker_report = UserHairReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            coordination_tracker_report = UserHandEyeCoordinationReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            analytical_tracker_report = UserAnalyticalReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            skin_tracker_report = UserSkinReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            eyesight_tracker_report = UserEyeSightReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            motor_tracker_report = UserMotorSkillsReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=10)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=11)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=12)).last()
            
            print(growth_tracker_report,eyesight_tracker_report,user)
            if growth_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 435, 'Height:'+growth_tracker_report.height)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(640, 435, 'Weight:'+growth_tracker_report.weight)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 425, 'Bmi:'+growth_tracker_report.bmi)
            if learnability_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 290, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(650, 290, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 280, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(655, 280, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(680, 270, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 270,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if eyesight_tracker_report is not None:
                color_blindness_test_final_value = 0
                left_eye_visual_acquity_test_final_value = 0
                right_eye_visual_acquity_test_final_value = 0
                left_eye_astigmatism_test_final_value = 'No'
                right_eye_astigmatism_test_final_value = 'No'
                left_eye_corneal_curvature_test_final_value = 'No'
                right_eye_corneal_curvature_test_final_value = 'No'
                dry_eye_test_final_value = 0
                eyesight_tracker_obj = UserEyeSightReport.objects.get(id=eyesight_tracker_report.id)
                print('Eye sight report',eyesight_tracker_obj,eyesight_tracker_report)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'color_blindness_test')
                    for i in test_values.values():
                        if i == 'True':
                            color_blindness_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'visual_acquity_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         visual_acquity_test_final_value += 1
                    left_eye_visual_acquity_test_final_value = test_values.get(
                        'left_eye').get('line_no')
                    right_eye_visual_acquity_test_final_value = test_values.get(
                        'right_eye').get('line_no')
                except Exception as e:
                    print('Exception from visual_acquity_test-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'astigmatism_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         astigmatism_test_final_value += 1
                    left_eye_astigmatism_test_final_value = test_values.get(
                        'left_eye').get('ans').title()
                    right_eye_astigmatism_test_final_value = test_values.get(
                        'right_eye').get('ans').title()

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
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(600, 405, 'L.E Visual Acquity:'+str(left_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(660, 405, 'R.E Visual Acquity:'+str(right_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(600, 395, 'L.E Astigmatism:'+str(left_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(665, 395, 'R.E Astigmatism:'+str(right_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(660, 385, 'R.E Corneal Curvature:'+str(right_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(600, 385,'L.E Corneal Curvature:'+str(left_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(680, 375,'Dry Eye Test:'+str(dry_eye_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(600, 375, 'Color Blindness:'+str(color_blindness_test_final_value))
            if coordination_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 345, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(650, 345, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 335, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(655, 335, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(680, 325, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 325,'Emotion & Self-Ctrl:'+str(emotion_self_control))     
            if analytical_tracker_report is not None:
                print(analytical_tracker_report)
                analytical_test_final_value = 0
                analytical_tracker_obj = analytical_tracker_report
                try:
                    test_values = analytical_tracker_obj.test_answer.get(
                        'analytical_test')
                    for i in test_values.values():
                        if i == 'True':
                            analytical_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(600, 175, 'Analytical Test Result:'+str(analytical_test_final_value))
        if i == 4:
            learnability_tracker_report = UserLearnabilityReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            growth_tracker_report = UserGrowthReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            hair_tracker_report = UserHairReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            coordination_tracker_report = UserHandEyeCoordinationReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            analytical_tracker_report = UserAnalyticalReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            skin_tracker_report = UserSkinReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            eyesight_tracker_report = UserEyeSightReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            motor_tracker_report = UserMotorSkillsReport.objects.filter(Q(parent_user=user,report_date__year=year,report_date__month=1)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=2)|
                                                                                Q(parent_user=user,report_date__year=year,report_date__month=3)).last()
            
            print(growth_tracker_report,eyesight_tracker_report,user)
            if growth_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 435, 'Height:'+growth_tracker_report.height)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(770, 435, 'Weight:'+growth_tracker_report.weight)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 425, 'Bmi:'+growth_tracker_report.bmi)
            if learnability_tracker_report is not None:
                print(learnability_tracker_report,learnability_tracker_report.report_type)
                learnability_obj = LearnalityTrackerSectionAnswers.objects.filter(
                    learnablity_tracker__id=learnability_tracker_report.id)
                print(learnability_obj)
                reading = 0
                spelling_writing = 0
                math_logic = 0
                emotion_self_control = 0
                listening = 0
                attention = 0
                for i in learnability_obj:
                    print(i.section_name, i.answer)
                    if i.section_name == 'Reading':
                        reading = i.answer
                    elif i.section_name == 'Spelling & Writing':
                        spelling_writing = i.answer
                    elif i.section_name == 'Math & Logic':
                        math_logic = i.answer
                    elif i.section_name == 'Emotion & Self-Ctrl':
                        emotion_self_control = i.answer
                    elif i.section_name == 'Listening':
                        listening = i.answer
                    elif i.section_name == 'Attention':
                        attention = i.answer
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 29, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(780, 29, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 28, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(785, 28, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(810, 27, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 27,'Emotion & Self-Ctrl:'+str(emotion_self_control))
            if eyesight_tracker_report is not None:
                color_blindness_test_final_value = 0
                left_eye_visual_acquity_test_final_value = 0
                right_eye_visual_acquity_test_final_value = 0
                left_eye_astigmatism_test_final_value = 'No'
                right_eye_astigmatism_test_final_value = 'No'
                left_eye_corneal_curvature_test_final_value = 'No'
                right_eye_corneal_curvature_test_final_value = 'No'
                dry_eye_test_final_value = 0
                eyesight_tracker_obj = UserEyeSightReport.objects.get(id=eyesight_tracker_report.id)
                print('Eye sight report',eyesight_tracker_obj,eyesight_tracker_report)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'color_blindness_test')
                    for i in test_values.values():
                        if i == 'True':
                            color_blindness_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'visual_acquity_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         visual_acquity_test_final_value += 1
                    left_eye_visual_acquity_test_final_value = test_values.get(
                        'left_eye').get('line_no')
                    right_eye_visual_acquity_test_final_value = test_values.get(
                        'right_eye').get('line_no')
                except Exception as e:
                    print('Exception from visual_acquity_test-> ', e)
                try:
                    test_values = eyesight_tracker_obj.test_name_answer.get(
                        'astigmatism_test')
                    # for i in test_values.values():
                    #     if i == 'True':
                    #         astigmatism_test_final_value += 1
                    left_eye_astigmatism_test_final_value = test_values.get(
                        'left_eye').get('ans').title()
                    right_eye_astigmatism_test_final_value = test_values.get(
                        'right_eye').get('ans').title()

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
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(730, 405, 'L.E Visual Acquity:'+str(left_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(790, 405, 'R.E Visual Acquity:'+str(right_eye_visual_acquity_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(730, 395, 'L.E Astigmatism:'+str(left_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(795, 395, 'R.E Astigmatism:'+str(right_eye_astigmatism_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(790, 385, 'R.E Corneal Curvature:'+str(right_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 5)
                c.drawString(730, 385,'L.E Corneal Curvature:'+str(left_eye_corneal_curvature_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(810, 375,'Dry Eye Test:'+str(dry_eye_test_final_value))
                c.setFillColor(black)
                c.setFont('Times-Roman', 6)
                c.drawString(730, 375, 'Color Blindness:'+str(color_blindness_test_final_value))
            if coordination_tracker_report is not None:
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 345, 'Reading:'+str(reading))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(780, 345, 'Spelling & Writing:'+str(spelling_writing))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 335, 'Math & Logic:'+str(math_logic))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(785, 335, 'Attention:'+str(attention))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(810, 325, 'Listening:'+str(listening))
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 325,'Emotion & Self-Ctrl:'+str(emotion_self_control))     
            if analytical_tracker_report is not None:
                print(analytical_tracker_report)
                analytical_test_final_value = 0
                analytical_tracker_obj = analytical_tracker_report
                try:
                    test_values = analytical_tracker_obj.test_answer.get(
                        'analytical_test')
                    for i in test_values.values():
                        if i == 'True':
                            analytical_test_final_value += 1
                except Exception as e:
                    print('Exception-> ', e)
                c.setFillColor(black)
                c.setFont('Times-Roman', 8)
                c.drawString(730, 175, 'Analytical Test Result:'+str(analytical_test_final_value))
    c.showPage()
    c.save()
    buf.seek(0)
    pdf_file_name = file_name
    with open(pdf_file_name, 'wb') as f:
        f.write(buf.getvalue())
        buf.close()
        s3 = boto3.resource('s3', region_name='us-east-2',
                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                            aws_secret_access_key='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')
        s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(open(pdf_file_name, 'rb')),
                                        ACL='public-read', ContentDisposition='inline')
        report_obj.report_url = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
        report_obj.save()
    if pdf_file_name:
        os.remove(pdf_file_name)
    return report_obj.report_url


@shared_task
def generatemedicalreport(organization_id,user_class,user_section,quarter,year):
    print('from generatemedicalreport')
    organization = Organizations.objects.get(id=organization_id)
    for user in OrganizationUser.objects.filter(organization=organization,user_class=user_class):
        if quarter == 1:
            x = generatepdf(organization,[1],user,user_section,user_class,year)
            print(x)
        if quarter == 2:
            x = generatepdf(organization,[1,2],user_section,user,user_class,year)
            print(x)

        if quarter == 3:
            x = generatepdf(organization,[1,2,3],user_section,user,user_class,year)
            print(x)

        if quarter == 4:
            x = generatepdf(organization,[1,2,3,4],user_section,user,user_class,year)
            print(x)
    return "generating medical report"