from rest_framework import serializers
from ..models.child_tracker import ChildTracker


class ChildTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildTracker
        fields = ['child', 'age', 'height', 'weight', 'gender']


class GetAllChildTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildTracker
        fields = '__all__'
        depth = 4