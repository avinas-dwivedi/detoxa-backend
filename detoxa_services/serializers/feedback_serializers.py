from detoxa_services.models.feedback_models import Feedback
from rest_framework import serializers

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('rating', 'comment', 'email')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': False},
            'comment': {'required': True}
        }