from ..models.eyesight_tracker import EyeSightTracker
from ..serializers.eyesight_tracker_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser
from botocore.exceptions import ClientError
from ..utils.helper_functions import unique_s3_key
from ..utils.user_authentication import UserAuthentication
import django_filters


class EyeSightTrackerView(generics.GenericAPIView):
    authentication_class = []
    serializer_class = EyeSight_Tracker_Serializer
    # parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        eyesight_serializer = EyeSight_Tracker_Serializer(data=request.data)
        # print(request.data)
        # print(eyesight_serializer)
        if eyesight_serializer.is_valid():
            print(eyesight_serializer.validated_data)
            # import ipdb
            # ipdb.set_trace()
            try:
                user_id = eyesight_serializer.validated_data.get('user_id')
                child = eyesight_serializer.validated_data.get('child')
                test_name_answer = eyesight_serializer.validated_data.get('test_name_answer')
                test_type = eyesight_serializer.validated_data.get('test_type')
                # answer = eyesight_serializer.validated_data.get('answer')

                learnability_obj = EyeSightTracker.objects.create(user_id=user_id,
                                                                  child=child,
                                                                  test_name_answer=test_name_answer,
                                                                  test_type=test_type)
                data = {
                    "success": True,
                    "message": "SUCCESS",
                    "data": EyeSight_Tracker_Serializer(learnability_obj).data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
                return Response(EyeSightTracker.errors, status=status.HTTP_400_BAD_REQUEST)


class EyeSightTrackerListView(generics.ListAPIView):
    authentication_class = []
    serializer_class = EyeSight_Tracker_Serializer

    def get_queryset(self):
        user = UserAuthentication.authenticate(self, self.request)[0]
        return EyeSightTracker.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        if user:
            queryset = self.get_queryset().order_by('-id')
            serializer = EyeSight_Tracker_Serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'message':'You are not authorized to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
