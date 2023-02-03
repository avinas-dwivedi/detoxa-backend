from ..models.media import Media, MediaCategory
from ..serializers.media_serializer import MediaSerializer, GetAllMediaSerializer, GetMediaByIdSerializer, AddMediaCategorySerializer, \
                                GetAllMediaCategorySerializer, RemoveMediaSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser, FormParser
from detoxa_backend import settings
from botocore.exceptions import ClientError
from ..utils.helper_functions import unique_s3_key
from ..utils.user_authentication import UserAuthentication
import logging
import boto3
import django_filters


class MediaUpload(generics.GenericAPIView):
    authentication_class = []
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        media_serializer = MediaSerializer(data=request.data)
        if media_serializer.is_valid():
            try:
                title = media_serializer.validated_data.get('title')
                media_type = media_serializer.validated_data.get('media_type')
                category = media_serializer.validated_data.get('category')
                media_file = media_serializer.validated_data.get('media_file')

                s3_client = boto3.client('s3')
                key = unique_s3_key()
                try:
                    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                                    ACL='bucket-owner-full-control', Key=key,
                                                    Body=media_file)
                except ClientError as e:
                    logging.error(e)
                    raise e

                media_obj = Media.objects.create(title=title, media_type=media_type, category=category, key=key)

                if media_obj is not None:
                    try:
                        url = s3_client.generate_presigned_url('get_object',
                                                               Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                       'Key': media_obj.key}, ExpiresIn=604800)
                    except ClientError as e:
                        logging.error(e)
                        raise e

                    media_obj.media_url = url
                    media_obj.save()

                data = {
                    "success": True,
                    'media': {
                        'id': media_obj.id,
                        'image_url': media_obj.media_url,
                        'title': media_obj.title,
                        'media_type': media_obj.media_type,
                        'category': media_obj.category.name,
                        'key': media_obj.key
                    }
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(media_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllMediaFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method='filter_by_status')
    media_type = django_filters.CharFilter(method='filter_by_media_type')
    category = django_filters.CharFilter(method='filter_by_category')
    title = django_filters.CharFilter(method='filter_by_title')

    class Meta:
        model = Media
        fields = []

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(is_active=value)

    def filter_by_media_type(self, queryset, name, value):
        return queryset.filter(media_type__exact=value)

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(category__exact=value)

    def filter_by_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)


class GetAllMedia(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetAllMediaSerializer
    filterset_class = GetAllMediaFilter

    def get(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        media_obj = Media.objects
        media_obj = GetAllMediaFilter(request.GET, queryset=media_obj).qs.distinct()
        data_list = list()
        for s3_key in media_obj:
            key = s3_key.key
            if key:
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                               'Key': key}, ExpiresIn=604800)
                data = GetAllMediaSerializer(s3_key).data
                data['media_url'] = url
                data['category'] = s3_key.category.name
                data_list.append(data)
                s3_key.media_url = url
        return Response(data_list, status=status.HTTP_200_OK)


class GetMediaById(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetMediaByIdSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        media_obj = Media.objects.filter(id=kwargs['pk']).first()
        data = {}
        if media_obj:
            key = media_obj.key
            if key:
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                               'Key': key}, ExpiresIn=604800)
                data = GetMediaByIdSerializer(media_obj).data
                data['media_url'] = url
                data['category'] = media_obj.category.name
                media_obj.media_url = url
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Media not found')


class AddMediaCategory(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AddMediaCategorySerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        media_category_serializer = AddMediaCategorySerializer(data=request.data)
        if media_category_serializer.is_valid():
            name = media_category_serializer.validated_data.get('name')
            media_category_exist = MediaCategory.objects.filter(name=name).first()
            if media_category_exist:
                raise exceptions.ValidationError('Category Already exist')
            media_category_obj = MediaCategory.objects.create(name=name)
            if media_category_obj:
                data = {
                    "success":  True,
                    'id': media_category_obj.id,
                    "name": media_category_obj.name
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise exceptions.ValidationError('Category Not Created')
        else:
            return Response(media_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllMediaCategory(generics.ListAPIView):
    serializer_class = GetAllMediaCategorySerializer
    queryset = MediaCategory.objects.all()


class RemoveMedia(generics.DestroyAPIView):
    authentication_class = []
    serializer_class = RemoveMediaSerializer

    def delete(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        media_obj = Media.objects.filter(id=kwargs['pk']).first()
        if media_obj:
            key = media_obj.key
            if key:
                try:
                    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
                except ClientError as e:
                    logging.error(e)
                    raise e
                media_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Media not found')





