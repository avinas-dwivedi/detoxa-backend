from email.policy import default
from rest_framework.fields import ChoiceField
from detoxa_services import models
from detoxa_services.models.hand_eye_tracker import HandEyeTracker
from ..models.reports_models import UserGrowthReport, UserHandEyeCoordinationReport, UserLearnabilityReport, UserEyeSightReport, UserMedicalReport
from rest_framework import serializers

REPORT_TYPE_CHOICES = (
    ('Growth', 'Growth'),
    ('Learnability', 'Learnability'),
    ('Eyesight', 'Eyesight'),
    ('Vaccination', 'Vaccination'),
    ('Food & Nutrition', 'Food & Nutrition'),
    ('Hand & Eye Coordination', 'Hand & Eye Coordination'),
    ('Analytical', 'Analytical'),
    ('Skin', 'Skin'),
    ('Hair', 'Hair'),
)


class CreateReportSerializer(serializers.Serializer):
    child_user = serializers.IntegerField()
    report_id = serializers.IntegerField()
    interpretations = serializers.CharField(max_length=800)
    note_1 = serializers.CharField(max_length=200, required=False)
    note_2 = serializers.CharField(max_length=200, required=False)


class CreateEyeSightReportSerializer(serializers.Serializer):
    child_user = serializers.IntegerField()
    report_id = serializers.ListField()
    interpretations = serializers.CharField(max_length=800)
    note_1 = serializers.CharField(max_length=200, required=False)
    note_2 = serializers.CharField(max_length=200, required=False)
    # id = serializers.IntegerField()
    # class Meta:
    #     model = Reports
    #     fields = ['id']


class CreateCoordinatioReportSerializer(serializers.Serializer):
    child_user = serializers.IntegerField()
    report_id = serializers.ListField()
    interpretations = serializers.CharField(max_length=800)
    note_1 = serializers.CharField(max_length=200, required=False)
    note_2 = serializers.CharField(max_length=200, required=False)


class CreateHairTrackerReportSerializer(serializers.Serializer):
    child_user = serializers.IntegerField()
    report_id = serializers.ListField()
    interpretations = serializers.CharField(max_length=800)
    note_1 = serializers.CharField(max_length=200, required=False)
    note_2 = serializers.CharField(max_length=200, required=False)



class ReportSerializer(serializers.ModelSerializer):
    report_date = serializers.SerializerMethodField()
    report_time = serializers.SerializerMethodField()

    class Meta:
        model = UserLearnabilityReport
        fields = ['id', 'report_date', 'report_time', 'report_name', 'report_image_url',
                  'report', 'report_type', 'child_user', 'parent_user']
        depth = 1
        read_only_fields = fields

    def get_report_date(self, obj):
        return obj.report_date.date()   

    def get_report_time(self, obj):
        return obj.report_date.time()


class GrowthReportSerializer(serializers.ModelSerializer):
    report_date = serializers.SerializerMethodField()
    report_time = serializers.SerializerMethodField()

    class Meta:
        model = UserGrowthReport
        fields = ['id','report_date','report_time','report_name','report_image_url','report','report_type','child_user','parent_user']
        depth = 1
        read_only_fields = fields

    def get_report_date(self, obj):
        return obj.report_date.date()   

    def get_report_time(self, obj):
        return obj.report_date.time()


class EyeSightReportSerializer(serializers.ModelSerializer):
    report_date = serializers.SerializerMethodField()
    report_time = serializers.SerializerMethodField()

    class Meta:
        model = UserEyeSightReport
        fields = ['id', 'report_date','report_time', 'report_name', 'report_image_url', 'report', 'report_id', 'child_user', 'parent_user']
        depth = 1
        read_only_fields = fields
    
    def get_report_date(self, obj):
        return obj.report_date.date()   

    def get_report_time(self, obj):
        return obj.report_date.time()


class HandEyeTrackerReportSerializer(serializers.ModelSerializer):
    report_date = serializers.SerializerMethodField()
    report_time = serializers.SerializerMethodField()

    class Meta:
        model = UserHandEyeCoordinationReport
        fields = ['id', 'report_conducted_date','report_time', 'report_name', 'report_image_url', 'report', 'report_type', 'child_user', 'parent_user']
        depth = 1
        read_only_fields = fields

    def get_report_date(self, obj):
        return obj.report_date.date()   

    def get_report_time(self, obj):
        return obj.report_date.time()


class GetReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=REPORT_TYPE_CHOICES)


class GenerateOTPforReportSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)
    report_id = serializers.IntegerField(default=0)


class VerifyOTPforReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=REPORT_TYPE_CHOICES)
    phone_number = serializers.CharField(max_length=12)
    session_id = serializers.CharField(max_length=100)
    otp = serializers.CharField(max_length=6)
    report_id = serializers.IntegerField()


class GenerateMedicalReportCardSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    user_class = serializers.CharField(max_length=100)
    user_section = serializers.CharField(max_length=100)
    quarter = serializers.IntegerField(default=1)
    year = serializers.IntegerField(default=1)


class GetMedicalReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedicalReport
        fields = '__all__'
        depth = 2
        read_only_fields = (fields,)


class SendMedicalReportOnEmailSerializer(serializers.Serializer):
    user_class = serializers.CharField(required=False)
    user_section = serializers.CharField(required=False)
    report_id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)