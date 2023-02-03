from gzip import READ
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..models.blogs import Blog, BlogCategory, Author
from ..serializers.blog_serializer import BlogSerializer, GetAllBlogSerializer, GetAllBlogByIdSerializer, AddBlogCategorySerializer, \
                                    GetAllBlogCategorySerializer, GetAllAuthorSerializer, RemoveBlogSerializer, UpdateBlogSerializer
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser
from detoxa_backend import settings
from botocore.exceptions import ClientError
from ..utils.helper_functions import unique_s3_key
from ..utils.user_authentication import UserAuthentication
from django.db.models import Count
import logging
import boto3
import django_filters

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateBlog(generics.GenericAPIView):
    authentication_class = []
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        print(request.data)
        blog_serializer = BlogSerializer(data=request.data)
        if blog_serializer.is_valid():
            try:
                title = blog_serializer.validated_data.get('title')
                blog_category = blog_serializer.validated_data.get('blog_category')
                media_url = blog_serializer.validated_data.get('media_url')
                author = blog_serializer.validated_data.get('author')
                para1 = blog_serializer.validated_data.get('para1')
                para2 = blog_serializer.validated_data.get('para2')
                para3 = blog_serializer.validated_data.get('para3')
                para4 = blog_serializer.validated_data.get('para4')

                exist_author_obj = Author.objects.filter(name=author).first()
                if exist_author_obj:
                    pass
                else:
                    author_created_obj = Author.objects.create(name=author)
                author = exist_author_obj.id if exist_author_obj else author_created_obj.id
                url = ''
                if media_url:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=media_url.name, Body=media_url, ACL='public-read',
                                                       ContentType=media_url.content_type, ContentDisposition='inline')

                    url = f"https://detoxa.s3.us-east-2.amazonaws.com/{media_url.name}"
                blog_obj = Blog.objects.create(title=title, blog_category=blog_category, author=author,
                                               para1=para1, para2=para2, para3=para3, para4=para4, media_url=url)
                data = {
                    "success": True,
                    'blog': GetAllBlogSerializer(blog_obj).data
                }
                data['blog']['blog_category'] = blog_obj.blog_category.name
                data['blog']['author'] = blog_obj.author
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateBlogDetails(generics.GenericAPIView):
    serializer_class = UpdateBlogSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request,*args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        blog_serializer = UpdateBlogSerializer(data=request.data)
        if blog_serializer.is_valid():
            try:
                title = blog_serializer.validated_data.get('title')
                blog_category = blog_serializer.validated_data.get('blog_category')
                media_url = blog_serializer.validated_data.get('media_url')
                author = blog_serializer.validated_data.get('author')
                para1 = blog_serializer.validated_data.get('para1')
                para2 = blog_serializer.validated_data.get('para2')
                para3 = blog_serializer.validated_data.get('para3')
                para4 = blog_serializer.validated_data.get('para4')

                exist_author_obj = Author.objects.filter(name=author).first()
                if exist_author_obj:
                    pass
                else:
                    author_created_obj = Author.objects.create(name=author)

                author = exist_author_obj.id if exist_author_obj else author_created_obj.id
                image_url = None
                if media_url:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=media_url.name, Body=media_url, ACL='public-read',
                                                            ContentType=media_url.content_type, ContentDisposition='inline')
                        image_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{media_url.name}"
                    except Exception as e:
                        print(e)
                blog_category_obj = BlogCategory.objects.filter(id=blog_category).first()
                blog_obj = Blog.objects.get(id=kwargs['pk'])
                blog_obj.title=title
                # blog_obj.blog_category=blog_category_obj, 
                blog_obj.author=author
                blog_obj.para1=para1
                blog_obj.para2=para2 
                blog_obj.para3=para3 
                blog_obj.para4=para4 
                blog_obj.media_url=image_url
                blog_obj.blog_category = blog_category_obj
                blog_obj.save()
                # data = {
                #     "success": True,
                #     'blog': GetAllBlogSerializer(blog_obj).data
                # }
                # data['blog']['blog_category'] = blog_obj.blog_category.name
                # data['blog']['author'] = blog_obj.author.name
                return Response({'msg':'Blog updated successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllBlogFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method='filter_by_status')
    author = django_filters.CharFilter(method='filter_by_author')
    category = django_filters.CharFilter(method='filter_by_category')
    title = django_filters.CharFilter(method='filter_by_title')

    class Meta:
        model = Blog
        fields = []

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(is_active=value)

    def filter_by_author(self, queryset, name, value):
        return queryset.filter(author__contains=value)

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(blog_category__exact=value)

    def filter_by_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)


class GetAllBlogs(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllBlogSerializer
    pagination_class = StandardResultsSetPagination

    # filterset_class = GetAllBlogFilter
    org_status_param = openapi.Parameter('status', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    org_category_param = openapi.Parameter('category', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    org_author_param = openapi.Parameter('author', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    org_title_param = openapi.Parameter('title', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[org_status_param,org_category_param,org_author_param,org_title_param])
    def get(self, request, *args, **kwargs):
        # blog_obj = Blog.objects
        # blog_obj = GetAllBlogFilter(request.GET, queryset=blog_obj).qs.distinct()
        # data_list = list()
        # for s3_key in blog_obj:
        #     data = GetAllBlogSerializer(s3_key).data
        #     data['category_name'] = s3_key.blog_category.name
        #     author = Author.objects.filter(id=int(s3_key.author)).values("name")
        #     data['author'] = author[0]["name"]
        #     data_list.append(data)
       
        blog_status = request.query_params.get('status')
        category = request.query_params.get('category')
        author = request.query_params.get('author')
        title = request.query_params.get('title')
        if blog_status:
            total_count = Blog.objects.filter(is_active=True).count()
            blogs_list = Blog.objects.filter(is_active=blog_status.title()).order_by('-id')
            page = self.paginate_queryset(blogs_list)
            serializer = GetAllBlogSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
        if category:
            total_count = Blog.objects.filter(is_active=True).count()
            blogs_list = Blog.objects.filter(blog_category__name__icontains=category,
                                             is_active=True).order_by('-id')
            page = self.paginate_queryset(blogs_list)
            serializer = GetAllBlogSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
        if author:
            total_count = Blog.objects.filter(is_active=True).count()
            blog_category = Author.objects.filter(name=author)
            for i in blog_category:
                blogs_list = Blog.objects.filter(author__icontains=i.id, is_active=True).order_by('-id')
                page = self.paginate_queryset(blogs_list)
                serializer = GetAllBlogSerializer(page, many=True)
                return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
        if title:
            total_count = Blog.objects.filter(is_active=True).count()
            blogs_list = Blog.objects.filter(title__icontains=title, is_active=True).order_by('-id')
            page = self.paginate_queryset(blogs_list)
            serializer = GetAllBlogSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
        total_count = Blog.objects.filter(is_active=True).count()
        blogs_list = Blog.objects.filter(is_active=True).order_by('-id')
        page = self.paginate_queryset(blogs_list)
        serializer = GetAllBlogSerializer(page, many=True)
        return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)


class GetBlogById(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllBlogByIdSerializer

    def get(self, request, *args, **kwargs):
        try:
            blog_obj = Blog.objects.get(id=kwargs['pk'])
            data = GetAllBlogByIdSerializer(blog_obj).data
        #         data['category_name'] = blog_obj.blog_category.name
        #         author = Author.objects.filter(id=int(data['author'])).values("name")
                # data['author'] = author[0]["name"]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            raise exceptions.NotFound('Blog Not found')


class AddBlogCategory(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = AddBlogCategorySerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        blog_category_serializer = AddBlogCategorySerializer(data=request.data)
        if blog_category_serializer.is_valid():
            try:
                name = blog_category_serializer.validated_data.get('name')
                media_url = blog_category_serializer.validated_data.get('media_url')
                blog_category_exist = BlogCategory.objects.filter(name=name).first()
                if blog_category_exist:
                    raise exceptions.ValidationError('Category Already exist')
                url = ''
                if media_url:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=media_url.name, Body=media_url, ACL='public-read',
                                                       ContentType=media_url.content_type, ContentDisposition='inline')

                    url = f"https://detoxa.s3.us-east-2.amazonaws.com/{media_url.name}"
                blog_category_obj = BlogCategory.objects.create(name=name, media_url=url)
                if blog_category_obj:
                    data = {
                        "success":  True,
                        'id': blog_category_obj.id,
                        "name": blog_category_obj.name,
                        "media_url": blog_category_obj.media_url
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError('Error in creating category')
            except Exception as e:
                raise e
        else:
            return Response(blog_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllBlogCategory(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllBlogCategorySerializer
    queryset = BlogCategory.objects.all()


class GetAllAuthors(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllAuthorSerializer
    queryset = Author.objects.all()


class RemoveBlog(generics.DestroyAPIView):
    authentication_classes = []
    serializer_class = RemoveBlogSerializer

    def delete(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        s3_client = boto3.client('s3')
        blog_obj = Blog.objects.filter(id=kwargs['pk']).first()
        if blog_obj:
        #     key = blog_obj.key
        #     if key:
        #         try:
        #             s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        #         except ClientError as e:
        #             logging.error(e)
        #             raise e
            blog_obj.is_active = False
            blog_obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Blog not found')

class DeleteBlogCategory(generics.GenericAPIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        if user.is_admin:
            try:
                blog_category_obj = BlogCategory.objects.get(id=kwargs['pk'])
                if blog_category_obj:
                    blog_category_obj.delete()
                    return Response({"success":True,"message":"Blog category deleted successfully"},status=status.HTTP_200_OK)
                else:
                    raise exceptions.NotFound('Blog category not found')
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exceptions.PermissionDenied('You are not authorized to perform this action')


class BlogByCategory(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllBlogSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        blog_category = BlogCategory.objects.filter(name=kwargs['category']).first()
        if blog_category:
            blog_obj = Blog.objects.filter(blog_category=blog_category).order_by('-id')
            serializer = GetAllBlogSerializer(blog_obj,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Category does not exist')


class MostViewedBlogs(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllBlogSerializer

    def get(self, request, *args, **kwargs):
        # user = UserAuthentication.authenticate(self, request)[0]
        # s3_client = boto3.client('s3')
        blog_obj = Blog.objects.filter(is_active=True).annotate(viewed_count=Count('viewed')).order_by('-viewed')[:4]
        if blog_obj:
            data_list = list()
            for s3_key in blog_obj:
                # key = s3_key.key
                # if key:
                #     url = s3_client.generate_presigned_url('get_object',
                #                                             Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                #                                             'Key': key}, ExpiresIn=604800)
                    data = GetAllBlogSerializer(s3_key).data
                    data['media_url'] = s3_key.media_url
                    data['category'] = s3_key.blog_category.name
                    data_list.append(data)
                    # s3_key.media_url = url
            return Response(data_list, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('No Blog found')