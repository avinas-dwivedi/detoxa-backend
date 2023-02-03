from ..models.hand_eye_tracker import HandEyeTracker
from ..serializers.hand_eye_tracker_serializer import HandEyeTrackerSerializer, GetHandEyeTrackerByIdSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
from rest_framework import exceptions
from ..utils.helper_functions import mandatory_params, mandatory_key_exist, check_length_of_params


class HandEyeTrackerView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = HandEyeTrackerSerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        hand_eye_serializer = HandEyeTrackerSerializer(data=request.data)
        if hand_eye_serializer.is_valid():
            try:
                test_name = hand_eye_serializer.validated_data.get('test_name')
                test_question_answer = hand_eye_serializer.validated_data.get('test_question_answer')
                gender = hand_eye_serializer.validated_data.get('gender')
                child = hand_eye_serializer.validated_data.get('child')

                # mandatory_key_exist(request.data, test_name, test_question_answer)
                # mandatory_params(child=child,
                #                  gender=gender)

                # if test_name == 'hand_and_eye_test_1':
                #     check_length_of_params(test_question_answer, test_name)

                # elif test_name == 'hand_and_eye_test_2':
                #     check_length_of_params(test_question_answer, test_name)

                # else:
                #     raise exceptions.ValidationError("Invalid test")

                hand_eye_obj = HandEyeTracker.objects.create(user=user, test_name=test_name,
                                                             test_question_answer=test_question_answer,
                                                             child=child,
                                                             gender=gender
                                                             )
                # sum_of_light_on_time = []
                # sum_of_reaction_time = []
                # for light_on_time in test_question_answer['light_on_time']:
                #     sum_of_light_on_time.append(light_on_time)
                # for reaction_time in test_question_answer['reaction_time']:
                #     sum_of_reaction_time.append(reaction_time)
                # average_of_test = (sum(sum_of_light_on_time) - sum(sum_of_reaction_time)) / 5
                # hand_eye_obj.average = average_of_test
                # hand_eye_obj.save()
                data = {
                    "success": True,
                    "hand_eye_tracker_data": GetHandEyeTrackerByIdSerializer(hand_eye_obj).data
                }
                return Response(data, status=status.HTTP_201_CREATED)

            except Exception as e:
                raise e
        else:
            return Response(hand_eye_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetHandEyeTrackerView(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetHandEyeTrackerByIdSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        hand_eye_obj = HandEyeTracker.objects.filter(user=user)
        if hand_eye_obj:
            data = {
                "success": True,
                "hand_eye_tracker_data": GetHandEyeTrackerByIdSerializer(hand_eye_obj,many=True).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            raise exceptions.NotFound('No data found')


