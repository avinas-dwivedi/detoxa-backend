import boto3

from detoxa_services.models.country import CountryStates, Animals, Country, Vehicle, SolorSystem, Profession
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import generics, status

import os
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from django.core.files.storage import FileSystemStorage
from detoxa_services.serializers.country_serializer import GetCountryStatesSerializer, GetStatesSerializer, \
    GetAnimalsbyIDSerializer, GetCountryIDSerializer, GetVehicleSerializer, GetSolarSerializer, GetProfessionSerializer


class CountryStatesView(ListAPIView):
    serializer_class = GetCountryStatesSerializer

    def get(self, request, *args, **kwargs):
        try:
            code = kwargs['code']
            data = CountryStates.objects.get(state_code=code)
            serializer = GetCountryStatesSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)


class GetAnimalsView(ListAPIView):
    serializer_class = GetAnimalsbyIDSerializer

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs['name'].lower()
            data = Animals.objects.get(animal_name=name)
            serializer = GetAnimalsbyIDSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=HTTP_400_BAD_REQUEST)


class GetVehiclesView(ListAPIView):
    serializer_class = GetVehicleSerializer

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs['name'].lower()
            data = Vehicle.objects.get(vehicle_name=name)
            serializer = GetVehicleSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)


class CountryView(ListAPIView):
    serializer_class = GetCountryIDSerializer

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs['name'].lower()
            data = Country.objects.get(country_name=name)
            serializer = GetCountryIDSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)


class GetSolarView(ListAPIView):
    serializer_class = GetSolarSerializer

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs['name'].lower()
            data = SolorSystem.objects.get(solor_name=name)
            serializer = GetSolarSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)


class GetProfessionView(ListAPIView):
    serializer_class = GetProfessionSerializer

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs['name'].lower()
            data = Profession.objects.get(profession_name=name)
            serializer = GetProfessionSerializer(data)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)


class UploadVoiceView(CreateAPIView):
    serializer_class = GetStatesSerializer

    def post(self, request, *args, **kwargs):

        serializer = GetStatesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                state_id = serializer.validated_data.get('id')
                audio_file1 = serializer.validated_data.get('audio_file')

                fs = FileSystemStorage(location=settings.UPLOAD_PATH)
                temp_audio_file_location = os.path.join(settings.UPLOAD_PATH, audio_file1._name)

                if os.path.exists(temp_audio_file_location):
                    print("File Exists")
                    filename =audio_file1._name
                    filepath = temp_audio_file_location

                else:
                    filename = fs.save(audio_file1._name, audio_file1.file)
                    filepath = settings.UPLOAD_PATH + '/'+ filename

                # import ipdb
                # ipdb.set_trace()
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=filepath, Body=(
                    open(filepath, 'rb')), ACL='public-read', ContentDisposition='inline')
                # pdf_url = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'

                # session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                #                             aws_secret_access_key=settings.AWS_SECRET_KEY,
                #                             region_name='us-east-2')
                # s3_client = session.resource('s3')
                # s3_client.Bucket(settings.AWS_STORAGE_BUCKET_NAME).upload_file(filepath, filename)4

                audio_url = f'https://detoxa.s3.us-east-2.amazonaws.com/{audio_file1}'

                if CountryStates.objects.filter(id = state_id).exists():
                    CountryStates.objects.filter(id=state_id).update(
                        audio_1_url = audio_url
                    )
                    return Response({"msg":"Audio file has been uploaded"},status=status.HTTP_200_OK)
                else:
                    return Response({"msg":'Please create the state entry first'}, status = status.HTTP_404_NOT_FOUND)


            except Exception as e:
                return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
