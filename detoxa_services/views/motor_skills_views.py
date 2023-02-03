from audioop import avg
import json
from ..models.motor_skills import *
from ..serializers.motor_skill_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
from ..constants.constants import *
from django.db.models import Sum
from ..models.users import Users
from rest_framework.parsers import MultiPartParser

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



class MotorSkillTrackerView(generics.GenericAPIView):
    serializer_class = MotorSkillTrackerSerializer
    authentication_class = []
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        serializer = MotorSkillTrackerSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            try:
                user_id = serializer.validated_data.get('user_id')
                child_id = serializer.validated_data.get('child_id')
                age_group = serializer.validated_data.get('age_group')
                answers = serializer.validated_data.get('answers')
                # answer_arr = json.loads(json.dumps(answers))

                # if section_names == 'Reading':
                tracker_id = MotorSkillTracker.objects.create(user_id=user_id, child_user_id=child_id)
                # else:
                #     tracker_id = \
                #         MotorSkillTracker.objects.filter(user_id=user_id, child_user_id=child_id).order_by('-id')[0]

                # for obj in answer_arr:
                MotorSkillTrackerSectionAnswers.objects.create(age_group=age_group, answers=answers,
                                                               motor_skill_tracker=tracker_id)
                data = {
                    "success": True,
                    "child_user_id": child_id,
                    "motor_skill_id": tracker_id.id
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMotorSkillTracker(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetMotorSkillTrackerSerializer
    tracker_param = openapi.Parameter('tracker_id', openapi.IN_QUERY, description="Tracker id should be passed to get the data based on their type. If no report type is passed then the repsonse will be an empty queryset",
                                      required=True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[tracker_param])
    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        # user_id = request.GET.get('user_id')
        tracker_id = request.GET.get('tracker_id')
        data_list = list()
        tracker_list = list()
        tracker_obj = MotorSkillTracker.objects.get(id=int(tracker_id))
        # for section in learnability_section_array:
        answer_sum = MotorSkillTrackerSectionAnswers.objects.get(motor_skill_tracker=int(tracker_id))

        # avg = int(answer_sum['answer__sum']) / 5 if answer_sum['answer__sum'] else 0
        correct_answers = 0
        for i in answer_sum.answers:
            if answer_sum.answers[i] == 'True':
                correct_answers += 1
        avg = int(correct_answers) / 5 if correct_answers else 0
        if 1 <= avg <= 2:
            result = "LOW"
        elif 2.1 <= avg <= 4:
            result = "MEDIUM"
        elif 4.1 <= avg <= 6:
            result = "HIGH"
        else:
            result = None
        json_output = {"answers": answer_sum.answers, "answers_avg": avg, "result": result}
        tracker_list.append(json_output)

        user_details = {"id": tracker_obj.child_user.id, "full_name": tracker_obj.child_user.full_name, "gender": tracker_obj.child_user.gender,
                        'age': tracker_obj.child_user.age}
        json_output = {"success": True, 'data': tracker_list, 'user_details': user_details}
        data_list.append(json_output)
        return Response(data_list, status=status.HTTP_200_OK)
