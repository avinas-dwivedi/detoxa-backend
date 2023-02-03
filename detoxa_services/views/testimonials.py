from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..models import Testimonials, Services
from ..serializers.testimonials_serializer import AddServicesSerializer, GetAllServicesSerializer, RemoveServiceSerializer, \
                            AddTestimonialSerializer, GetAllTestimonialsSerializer, GetTestimonialsByIdSerializer, RemoveTestimonialSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from ..utils.user_authentication import UserAuthentication
import django_filters
import boto3
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AddService(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AddServicesSerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        service_serializer = AddServicesSerializer(data=request.data)
        if service_serializer.is_valid():
            try:
                name = service_serializer.validated_data.get('name', )
                service_exist = Services.objects.filter(name=name).first()
                if service_exist:
                    raise exceptions.ValidationError('Service Already exist')
                service_obj = Services.objects.create(name=name)
                if service_obj:
                    data = {
                        "success":  True,
                        'id': service_obj.id,
                        "name": service_obj.name
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError('Service Not Created')
            except Exception as e:
                raise e
        else:
            return Response(service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllServices(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetAllServicesSerializer
    queryset = Services.objects.all()


class RemoveService(generics.DestroyAPIView):
    authentication_class = []
    serializer_class = RemoveServiceSerializer

    def delete(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        service_obj = Services.objects.filter(id=kwargs['pk']).first()
        if service_obj:
            service_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Service not found')


class AddTestimonial(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = AddTestimonialSerializer
    parser_classes = [MultiPartParser]


    def post(self, request):
        testimonial_serializer = AddTestimonialSerializer(data=request.data)
        if testimonial_serializer.is_valid():
            try:
                customer_name = testimonial_serializer.validated_data.get('customer_name', )
                picture_url = testimonial_serializer.validated_data.get('picture_url', )
                service = testimonial_serializer.validated_data.get('service', )
                testimonial = testimonial_serializer.validated_data.get('testimonial', )
                url = ''
                if picture_url:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=picture_url.name, Body=picture_url, ACL='public-read',
                                                       ContentType=picture_url.content_type, ContentDisposition='inline')

                    url = f"https://detoxa.s3.us-east-2.amazonaws.com/{picture_url.name}"
                
                testimonial_obj = Testimonials.objects.create(customer_name=customer_name, testimonial=testimonial,
                                                              service=service, picture_url=url)

                data = {
                    "success": True,
                    'testimonial': {
                        'id': testimonial_obj.id,
                        'image_url': testimonial_obj.picture_url,
                        'customer_name': testimonial_obj.customer_name,
                        'service': testimonial_obj.service.name,
                        'is_active': testimonial_obj.is_active
                    }
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(testimonial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllTestimonialFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method='filter_by_status')
    service = django_filters.CharFilter(method='filter_by_service')
    customer_name = django_filters.CharFilter(method='filter_by_customer_name')

    class Meta:
        model = Testimonials
        fields = []

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(is_active=value)

    def filter_by_service(self, queryset, name, value):
        return queryset.filter(service__name__iexact=value)

    def filter_by_customer_name(self, queryset, name, value):
        return queryset.filter(customer_name__icontains=value)


class GetAllTestimonials(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllTestimonialsSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = GetAllTestimonialFilter

    def get(self, request, *args, **kwargs):
        testimonial_obj = Testimonials.objects.filter(is_active=True).order_by("-id")
        testimonial_obj = GetAllTestimonialFilter(request.GET, queryset=testimonial_obj).qs.distinct()
        data_list = list()
        total_count = Testimonials.objects.filter(is_active=True).count()
        for s3_key in testimonial_obj:
            data = GetAllTestimonialsSerializer(s3_key).data
            data['service_name'] = s3_key.service.name
            data_list.append(data)
        reports = self.paginate_queryset(data_list)
        return Response({'data': reports, 'count': total_count}, status=status.HTTP_200_OK)


# class GetAllTestimonials(generics.ListAPIView):
#     authentication_classes = []
#     serializer_class = GetAllTestimonialsSerializer
#     # filterset_class = GetAllTestimonialFilter
#     pagination_class = StandardResultsSetPagination
#
#     org_status_param = openapi.Parameter('active', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
#     org_category_param = openapi.Parameter('service', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
#     org_author_param = openapi.Parameter('customer_name', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
#
#     @swagger_auto_schema(manual_parameters=[org_status_param, org_category_param, org_author_param])
#     def get(self, request, *args, **kwargs):
#         # testimonial_obj = Testimonials.objects
#         # testimonial_obj = GetAllTestimonialFilter(request.GET, queryset=testimonial_obj).qs.distinct()
#         # data_list = list()
#         # for s3_key in testimonial_obj:
#         #     data = GetAllTestimonialsSerializer(s3_key).data
#         #     data['service_name'] = s3_key.service.name
#         #     data_list.append(data)
#         testimonial_status = request.GET.get('active')
#         category = request.GET.get('service')
#         customer_name = request.GET.get('customer_name')
#         if testimonial_status:
#             total_count = Testimonials.objects.filter(is_active=True).count()
#             blogs_list = Testimonials.objects.filter(is_active=testimonial_status.title()).order_by('-id')
#             page = self.paginate_queryset(blogs_list)
#             serializer = GetAllTestimonialsSerializer(page, many=True)
#             return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
#         elif category:
#             print(category)
#             total_count = Testimonials.objects.filter(is_active=True).count()
#             blogs_list = Testimonials.objects.filter(service__name__icontains=category, is_active=True).order_by('-id')
#             page = self.paginate_queryset(blogs_list)
#             serializer = GetAllTestimonialsSerializer(page, many=True)
#             return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
#         elif customer_name:
#             total_count = Testimonials.objects.filter(is_active=True).count()
#             blogs_list = Testimonials.objects.filter(customer_name__icontains=customer_name,is_active=True).order_by('-id')
#             page = self.paginate_queryset(blogs_list)
#             serializer = GetAllTestimonialsSerializer(page, many=True)
#             return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
#         else:
#             print('line 171')
#             total_count = Testimonials.objects.filter(is_active=True).count()
#             blogs_list = Testimonials.objects.filter(is_active=True).order_by('-id')
#             page = self.paginate_queryset(blogs_list)
#             serializer = GetAllTestimonialsSerializer(page, many=True)
#             return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)


class GetTestimonialById(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetTestimonialsByIdSerializer

    def get(self, request, *args, **kwargs):
        testimonial_obj = Testimonials.objects.filter(id=kwargs['pk']).first()
        if testimonial_obj:
                data = GetTestimonialsByIdSerializer(testimonial_obj).data
                data['service_name'] = testimonial_obj.service.name
                return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Testimonial not found')


class RemoveTestimonial(generics.DestroyAPIView):
    authentication_classes = []
    serializer_class = RemoveTestimonialSerializer

    def delete(self, request, *args, **kwargs):
        testimonial_obj = Testimonials.objects.filter(id=kwargs['pk']).first()
        if testimonial_obj:
            testimonial_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Testimonial not found')






