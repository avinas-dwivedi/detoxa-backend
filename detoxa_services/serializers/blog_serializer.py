from dataclasses import fields
from rest_framework import serializers
from ..models.blogs import Blog, BlogCategory, Author
from ..constants import constants
from rest_framework import exceptions


class BlogSerializer(serializers.ModelSerializer):
    media_url = serializers.ImageField(required=False)
    #
    # def validate(self, data):
    #     media_file_obj = data.get('media_file')
    #     if media_file_obj:
    #         media_file_size = data.get('media_file').size
    #
    #         if media_file_size > constants.MEDIA_FILE_SIZE_IMAGE:
    #             raise exceptions.ValidationError("The maximum file size that can be uploaded is 10 MB")
    #         else:
    #             return data
    #     else:
    #         return data

    class Meta:
        model = Blog
        fields = ['id', 'title', 'blog_category', 'author', 'para1', 'para2', 'para3', 'para4', 'media_url']
        extra_kwargs = {'title': {'required': True}, 'blog_category': {'required': True},
                        'author': {'required': True}, 'para1': {'required': True}, 'para2': {'required': False},
                        'para3': {'required': False}, 'para4': {'required': False},
                        'media_url': {'required': True},
                        }
                        

class UpdateBlogSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    blog_category = serializers.IntegerField()
    author = serializers.CharField()
    para1 = serializers.CharField()
    para2 = serializers.CharField(required=False)
    para3 = serializers.CharField(required=False)
    para4 = serializers.CharField(required=False)
    media_url = serializers.ImageField(required=False)

class GetAllBlogSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'para1', 'para2', 'para3', 'para4', 'author', 'media_url', 'blog_category', 'viewed', 'is_active', 'published_on']
        depth = 4

    def get_author(self, obj):
        try:
            author_obj = Author.objects.get(id=obj.author)
            return author_obj.name
        except:
            pass

class GetAllBlogByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        depth = 4
        # fields = ['id', 'title', 'para1', 'para2', 'para3', 'para4', 'author', 'media_url', 'blog_category', 'viewed', 'is_active', 'published_on']


class AddBlogCategorySerializer(serializers.ModelSerializer):
    media_url = serializers.ImageField()
    class Meta:
        model = BlogCategory
        fields = ['name', 'media_url']
        extra_kwargs = {'name': {'required': True}, 'media_url': {'required': False}}


class GetAllBlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'media_url']


class GetAllAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class RemoveBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id']