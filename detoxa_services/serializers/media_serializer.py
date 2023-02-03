from rest_framework import serializers
from ..models.media import Media, MediaCategory
from ..constants import constants
from rest_framework import exceptions


class MediaSerializer(serializers.ModelSerializer):
    media_file = serializers.FileField(write_only=True, required=False, allow_null=True)

    def validate(self, data):
        media_file_obj = data.get('media_file')
        if media_file_obj:
            media_file_size = data.get('media_file').size

            if media_file_size > constants.MEDIA_FILE_SIZE_IMAGE:
                raise exceptions.ValidationError("The maximum file size that can be uploaded is 10 MB")
            else:
                return data
        else:
            return data

    class Meta:
        model = Media
        fields = ['title','media_type', 'category', 'is_active', 'media_file']
        extra_kwargs = {'title': {'required': True}, 'media_type': {'required': True},
                        'category': {'required': False},
                        'media_file': {'required': True}
                        }


class GetAllMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'media_type', 'is_active']


class GetMediaByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'media_type', 'is_active']


class AddMediaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = ['name']
        extra_kwargs = {'name': {'required': True}}


class GetAllMediaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = ['id', 'name']


class RemoveMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id']