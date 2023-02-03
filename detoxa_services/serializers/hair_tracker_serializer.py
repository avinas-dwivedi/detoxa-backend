from rest_framework import serializers
from ..models.hair_tracker import HairTracker
from ..constants import constants
from rest_framework import exceptions


class HairTrackerSerializer(serializers.Serializer):

    class SectionName:
        choices = (('Hair-Tracker', 'Hair-Tracker'))

    user_id = serializers.IntegerField()
    child_id = serializers.IntegerField()
    section_name = serializers.ChoiceField(choices=SectionName.choices)
    answers = serializers.ListField(child=serializers.CharField(min_length=0, max_length=50, required=True))

    class Meta:
        fields = ['user_id', 'child_id', 'section_name', 'answers']
        extra_kwargs = {
            'section_name': {'required': True}, 'answers': {'required': True},
        }


class GetHairTrackerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tracker_id = serializers.IntegerField()

    class Meta:
        model = HairTracker
        fields = ['user_id', 'tracker_id']
