from ..models import Banner
from ..serializers.banners_serializer import AddBannerSerializer, GetAllBannersSerializer, GetBannerByIdSerializer, \
                            RemoveBannerByIdSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser
from detoxa_backend import settings
from botocore.exceptions import ClientError
from ..utils.user_authentication import UserAuthentication
from ..utils.helper_functions import unique_s3_key
import logging
import boto3
import django_filters


class AddBanner(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AddBannerSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        banner_serializer = AddBannerSerializer(data=request.data)
        if banner_serializer.is_valid():
            try:
                title = banner_serializer.validated_data.get('title')
                picture_url = banner_serializer.validated_data.get('picture_url')
                device_type = banner_serializer.validated_data.get('device_type')
                sequence_number = banner_serializer.validated_data.get('sequence_number')
                page_link = banner_serializer.validated_data.get('page_link')
                start_date = banner_serializer.validated_data.get('start_date')
                end_date = banner_serializer.validated_data.get('end_date')

                s3_client = boto3.client('s3')
                key = unique_s3_key()
                try:
                    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                         ACL='bucket-owner-full-control', Key=key,
                                         Body=picture_url)
                except ClientError as e:
                    logging.error(e)
                    raise e

                banner_obj = Banner.objects.create(title=title, device_type=device_type, sequence_number=sequence_number,
                                                        page_link=page_link, start_date=start_date, end_date=end_date, key=key
                                                        )

                if banner_obj is not None:
                    try:
                        url = s3_client.generate_presigned_url('get_object',
                                                               Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                       'Key': banner_obj.key}, ExpiresIn=604800)
                    except ClientError as e:
                        logging.error(e)
                        raise e

                    banner_obj.picture_url = url
                    banner_obj.save()

                data = {
                    "success": True,
                    'banner': {
                        'id': banner_obj.id,
                        'image_url': banner_obj.picture_url,
                        'title': banner_obj.title,
                        'device_type': banner_obj.device_type,
                        'key': banner_obj.key,
                        'start_date': banner_obj.start_date,
                        'end_date': banner_obj.end_date,
                        'is_active': banner_obj.is_active
                    }
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllBannerFilter(django_filters.FilterSet):
    active = django_filters.CharFilter(method='filter_by_status')
    device_type = django_filters.CharFilter(method='filter_by_device_type')
    title = django_filters.CharFilter(method='filter_by_title')

    class Meta:
        model = Banner
        fields = []

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(is_active=value)

    def filter_by_device_type(self, queryset, name, value):
        return queryset.filter(device_type__exact=value)

    def filter_by_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)


class GetAllBanners(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetAllBannersSerializer
    filterset_class = GetAllBannerFilter

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        banner_obj = Banner.objects
        banner_obj = GetAllBannerFilter(request.GET, queryset=banner_obj).qs.distinct()
        data_list = list()
        for s3_key in banner_obj:
            key = s3_key.key
            if key:
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                               'Key': key}, ExpiresIn=604800)
                data = GetAllBannersSerializer(s3_key).data
                data['picture_url'] = url
                data_list.append(data)
                s3_key.picture_url = url
        return Response(data_list, status=status.HTTP_200_OK)


class GetBannerById(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetBannerByIdSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        banner_obj = Banner.objects.filter(id=kwargs['pk']).first()
        data = {}
        if banner_obj:
            key = banner_obj.key
            if key:
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                               'Key': key}, ExpiresIn=604800)
                data = GetBannerByIdSerializer(banner_obj).data
                data['picture_url'] = url
                banner_obj.picture_url = url
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Banner not found')


class RemoveBanner(generics.DestroyAPIView):
    authentication_class = []
    serializer_class = RemoveBannerByIdSerializer

    def delete(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        banner_obj = Banner.objects.filter(id=kwargs['pk']).first()
        if banner_obj:
            key = banner_obj.key
            if key:
                try:
                    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
                except ClientError as e:
                    logging.error(e)
                    raise e
                banner_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Banner not found')



