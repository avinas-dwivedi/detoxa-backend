from rest_framework import serializers
from ..models.hand_eye_tracker import HandEyeTracker


class HandEyeTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandEyeTracker
        fields = ['test_name', 'test_question_answer', 'child', 'gender']
        extra_kwargs = {
            'test_name': {'required': True}, 'test_question_answer': {'required': True},
            'child': {'required': True},
            'gender': {'required': True}
        }


class GetHandEyeTrackerByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandEyeTracker
        fields = ['id', 'user','child', 'test_name', 'test_question_answer', 'gender', 'average']
        depth = 4