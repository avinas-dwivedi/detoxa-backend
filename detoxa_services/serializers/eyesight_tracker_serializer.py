from rest_framework import serializers
from detoxa_services.models.users import Users
from ..models.eyesight_tracker import EyeSightTracker
from ..constants import constants
from rest_framework import exceptions


class EyeSight_Tracker_Serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    child = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    color_blindness_test = serializers.SerializerMethodField(read_only=True)
    visual_acquity_test = serializers.SerializerMethodField(read_only=True)
    astigmatism_test = serializers.SerializerMethodField(read_only=True)
    corneal_curvature_test = serializers.SerializerMethodField(read_only=True)
    dry_eye_test = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EyeSightTracker
        fields = ['id', 'user_id', 'child', 'test_name_answer', 'test_type', 'color_blindness_test',
                  'visual_acquity_test', 'astigmatism_test', 'corneal_curvature_test', 'dry_eye_test']
        extra_kwargs = {
            'test_name_answer': {'required': True},
            'test_type': {'required': True},
            'child': {'required': True},
        }
        depth = 4

    def get_color_blindness_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_name_answer.get('color_blindness_test')
            for i in test_values.values():
                if i == 'True':
                    final_value += 1
        except Exception as e:
            print('Exception-> ', e)
            
        return final_value

    def get_visual_acquity_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_name_answer.get('visual_acquity_test')
            for i in test_values.values():
                print('i-> ', i)
        except Exception as e:
            pass
        return final_value

    def get_astigmatism_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_name_answer.get('astigmatism_test')
            for i in test_values.values():
                if i == 'True':
                    final_value += 1
                print(i)
            
        except Exception as e:
            pass
        return final_value

    def get_corneal_curvature_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_name_answer.get('corneal_curvature_test')
            for i in test_values.values():
                if i == 'True':
                    final_value += 1
                print(i)
            
        except Exception as e:
            pass
        return final_value
    
    def get_dry_eye_test(self, obj):
        final_value = 0
        try:
            test_values = obj.test_name_answer.get('dry_eye_test')
            for i in test_values.values():
                if i == 'True':
                    final_value += 1
                print(i)
            
        except Exception as e:
            pass
        return final_value
