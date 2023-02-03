import boto3
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveAPIView,CreateAPIView
from detoxa_services.serializers.meals_serializer import RecommendedMealsCreateSerializer, RecommendedMealsSerializer
from detoxa_services.models.meals_models import RecommendedMeals
from detoxa_services.views.doctors_views import CreateDoctorsView
from rest_framework.parsers import MultiPartParser


class RecommendedMealsView(ListAPIView):
    serializer_class = RecommendedMealsSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            meals = RecommendedMeals.objects.filter(is_active=True)
            serializer = RecommendedMealsSerializer(meals, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class RecommendedMealsDetailsView(RetrieveAPIView):
    serializer_class = RecommendedMealsSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            meals = RecommendedMeals.objects.get(is_active=True, id=kwargs.get('pk'))
            serializer = RecommendedMealsSerializer(meals, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class AddMealsView(CreateAPIView):
    serializer_class = RecommendedMealsCreateSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            serializer = RecommendedMealsCreateSerializer(data=request.data)
            if serializer.is_valid():
                image_url= None
                if serializer.validated_data.get('image'):
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image').name, Body=serializer.validated_data.get('image'), ACL='public-read',
                                                       ContentType=serializer.validated_data.get('image').content_type, ContentDisposition='inline')
                        image_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image').name}"
                    except Exception as e:
                        print(e)
                meal = RecommendedMeals.objects.create(
                    title=serializer.data.get('title'),
                    description=serializer.data.get('description'),
                    image_url=image_url,
                    para_1=serializer.data.get('para_1'),
                    para_2=serializer.data.get('para_2'),
                    para_3=serializer.data.get('para_3'),
                    para_4=serializer.data.get('para_4')
                )
                return Response({"msg":"Meal added succssfully"}, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)