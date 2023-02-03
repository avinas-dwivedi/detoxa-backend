import json
from ..models.skin_tracker import *
from ..serializers.skin_tracker_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
from ..constants.constants import *
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SkinTrackerView(generics.GenericAPIView):
    serializer_class = SkinTrackerSerializer
    authentication_class = []

    def post(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        serializer = SkinTrackerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_id = serializer.validated_data.get('user_id')
                child_id = serializer.validated_data.get('child_id')
                section_names = serializer.validated_data.get('section_name')
                answers = serializer.validated_data.get('answers')
                answer_arr = json.loads(json.dumps(answers))

                if section_names == 'Reading':
                    tracker_id = SkinTracker.objects.create(user_id=user_id, child_user_id=child_id)
                else:
                    tracker_id = SkinTracker.objects.filter(user_id=user_id, child_user_id=child_id).order_by('-id')[0]

                for obj in answer_arr:
                    SkinTrackerSectionAnswers.objects.create(section_name=section_names,
                                                             answer=obj, skin_tracker_id=tracker_id.id)
                data = {
                    "success": True,
                    "child_user_id": child_id,
                    "skin_tracker_id": tracker_id.id
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSkinTracker(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetSkinTrackerSerializer
    org_tracker_param = openapi.Parameter('tracker_id', openapi.IN_QUERY, description="tracker id  should be passed to get the data of skin tracker.", required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[org_tracker_param])
    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        user_id = request.GET.get('user_id')
        tracker_id = request.GET.get('tracker_id')
        data_list = list()
        tracker_list = list()
        tracker_obj = SkinTracker.objects.filter(id=int(tracker_id)).order_by('-id')[0]
        for section in learnability_section_array:
            answer_sum = SkinTrackerSectionAnswers.objects.filter(section_name=section,
                                                                  skin_tracker_id=int(tracker_id)).aggregate(Sum('answer'))

            avg = int(answer_sum['answer__sum']) / 5 if answer_sum['answer__sum'] else 0
            if 1 <= avg <= 2:
                result = "LOW"
            elif 2.1 <= avg <= 4:
                result = "MEDIUM"
            elif 4.1 <= avg <= 6:
                result = "HIGH"
            else:
                result = None
            json_output = {"section_name": section, "answers_avg": avg, "result": result}
            tracker_list.append(json_output)

        user_details = {"id": tracker_obj.child_user.id, "full_name": tracker_obj.child_user.full_name, "gender": tracker_obj.child_user.gender,
                        'age': tracker_obj.child_user.age}
        json_output = {"success": True, 'data': tracker_list, 'user_details': user_details}
        data_list.append(json_output)
        return Response(data_list, status=status.HTTP_200_OK)
