from rest_framework import serializers
from detoxa_services.models.users import Users
from ..models.analytical_tracker import AnalyticalTracker


class AnalyticalTrackerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    child = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    analytical_test = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnalyticalTracker
        fields = ['id', 'user_id', 'child', 'test_answer', 'test_type', 'analytical_test']
        extra_kwargs = {
            'test_answer': {'required': True},
            'test_type': {'required': True},
            'child': {'required': True},
        }
        depth = 4

    def get_analytical_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_answer.get('analytical_test')
            for i in test_values.values():
                if i == 'True':
                    final_value += 1
        except Exception as e:
            print('Exception-> ', e)
        return final_value

