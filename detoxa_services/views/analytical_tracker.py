from ..models.analytical_tracker import AnalyticalTracker
from ..serializers.analytical_tracker_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
import django_filters


class AnalyticalTrackerView(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AnalyticalTrackerSerializer
    # parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        analytical_serializer = AnalyticalTrackerSerializer(data=request.data)
        if analytical_serializer.is_valid():
            try:
                user_id = analytical_serializer.validated_data.get('user_id')
                child = analytical_serializer.validated_data.get('child')
                test_answer = analytical_serializer.validated_data.get('test_answer')
                test_type = analytical_serializer.validated_data.get('test_type')

                analytical_obj = AnalyticalTracker.objects.create(user_id=user_id, child=child,
                                                                  test_answer=test_answer,
                                                                  test_type=test_type)
                data = {
                    "success": True,
                    "message": "SUCCESS",
                    "data": AnalyticalTrackerSerializer(analytical_obj).data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(AnalyticalTracker.errors, status=status.HTTP_400_BAD_REQUEST)
