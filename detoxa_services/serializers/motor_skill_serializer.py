from rest_framework import serializers
from ..models.motor_skills import MotorSkillTracker, MotorSkillTrackerSectionAnswers


class MotorSkillTrackerSerializer(serializers.Serializer):
    class AgeGroups:
        choices = (('2-3 Months', '2-3 Months'), ('3 Months to 1 Yr', '3 Months to 1 Yr'),
                   ('1 Yr to 3 Yr', '1 Yr to 3 Yr'), ('3 Yr to 10 Yr', '3 Yr to 10 Yr'))

    user_id = serializers.IntegerField()
    child_id = serializers.IntegerField()
    age_group = serializers.ChoiceField(choices=AgeGroups.choices)
    answers = serializers.JSONField()

    class Meta:
        fields = ['user_id', 'child_id', 'section_name', 'answers']
        extra_kwargs = {
            'section_name': {'required': True}, 'answers': {'required': True},
        }


class GetMotorSkillTrackerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tracker_id = serializers.IntegerField()

    class Meta:
        model = MotorSkillTracker
        fields = ['user_id', 'tracker_id']
