from rest_framework import serializers
from ..models.banners import Banner
from ..constants import constants
from rest_framework import exceptions


class AddBannerSerializer(serializers.ModelSerializer):
    picture_url = serializers.FileField(write_only=True, required=False, allow_null=True)

    def validate(self, data):
        media_file_obj = data.get('picture_url')
        if media_file_obj:
            media_file_size = data.get('picture_url').size

            if media_file_size > constants.MEDIA_FILE_SIZE_IMAGE:
                raise exceptions.ValidationError("The maximum file size that can be uploaded is 10 MB")
            else:
                return data
        else:
            return data

    class Meta:
        model = Banner
        fields = ['title', 'device_type', 'picture_url', 'sequence_number', 'start_date', 'end_date', 'page_link']
        extra_kwargs = {'title': {'required': True}, 'device_type': {'required': True},
                        'sequence_number': {'required': True}, 'start_date': {'required': True}, 'end_date': {'required': True},
                        'picture_url': {'required': True}
                        }


class GetAllBannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'device_type', 'picture_url', 'sequence_number', 'start_date', 'end_date', 'page_link']


class GetBannerByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'device_type', 'picture_url', 'sequence_number', 'start_date', 'end_date', 'page_link']


class RemoveBannerByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id']
