from rest_framework import serializers
from ..models.skin_tracker import SkinTracker


class SkinTrackerSerializer(serializers.Serializer):
    class SectionName:
        choices = (('Reading', 'Reading'), ('Spelling and Writing', 'Spelling and Writing'),
                   ('Math & Logic', 'Math & Logic'), ('Emotion & Self-Control', 'Emotion & Self-Control'),
                   ('Listening', 'Listening'), ('Attention', 'Attention'))

    user_id = serializers.IntegerField()
    child_id = serializers.IntegerField()
    section_name = serializers.ChoiceField(choices=SectionName.choices)
    answers = serializers.ListField(child=serializers.CharField(min_length=0, max_length=50, required=True))

    class Meta:
        fields = ['user_id', 'child_id', 'section_name', 'answers']
        extra_kwargs = {
            'section_name': {'required': True}, 'answers': {'required': True},
        }


class GetSkinTrackerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tracker_id = serializers.IntegerField()

    class Meta:
        model = SkinTracker
        fields = ['user_id', 'tracker_id']
