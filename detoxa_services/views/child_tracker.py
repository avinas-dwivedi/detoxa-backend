from detoxa_services.models.users import Users
from ..models.child_tracker import ChildTracker
from ..serializers.child_tracker_serializer import ChildTrackerSerializer, GetAllChildTrackerSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
import django_filters
from rest_framework import exceptions


class ChildTrackerView(generics.CreateAPIView):
    serializer_class = ChildTrackerSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        track_serializer = ChildTrackerSerializer(data=request.data)
        if track_serializer.is_valid():
            try:
                # first_name = track_serializer.validated_data.get('first_name')
                # last_name = track_serializer.validated_data.get('last_name')
                child = track_serializer.validated_data.get('child')
                age = track_serializer.validated_data.get('age')
                height = track_serializer.validated_data.get('height')
                weight = track_serializer.validated_data.get('weight')
                gender = track_serializer.validated_data.get('gender')

                cm_to_m = height / 100
                bmi = weight/(cm_to_m ** 2)
                bmi = round(bmi, 2)

                bmi_result = ''
                if bmi < 18.5:
                    bmi_result = 'Underweight'
                elif 18.5 <= bmi <= 24.9:
                    bmi_result = 'Normal'
                elif 24.9 <= bmi <= 29.9:
                    bmi_result = 'Overweight'
                else:
                    bmi_result = 'Obese'

                track_obj = ChildTracker.objects.create(child=child, age=age,
                                                        height=height, weight=weight, parent=user, gender=gender,
                                                        result=bmi)
                data = {
                    "success": True,
                    'data' : {
                        'id': track_obj.id,
                        'name' : track_obj.child.full_name,
                        'age' : track_obj.age,
                        'height': track_obj.height,
                        'weight': track_obj.weight,
                        'gender': track_obj.gender,
                        'parent': track_obj.parent_id,
                        'bmi': track_obj.result,
                        'bmi_result': bmi_result,
                        'child_id': track_obj.child_id
                    }
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(track_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetAllChildTracker(generics.ListAPIView):
#     authentication_class = []
#     serializer_class = GetAllChildTrackerSerializer
#     queryset = ChildTracker.objects.all()


class GetAllChildTrackerById(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllChildTrackerSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        child_tracker_obj = ChildTracker.objects.filter(parent=user.id)
        if child_tracker_obj:
            data = GetAllChildTrackerSerializer(child_tracker_obj,many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Child details not found')

