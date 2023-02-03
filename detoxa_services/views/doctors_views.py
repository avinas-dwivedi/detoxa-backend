from re import X
import boto3
import random
import string
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, status
from detoxa_services.models.blogs import Blog, BlogCategory
from detoxa_services.models.kits_models import Kit, KitCategory
from detoxa_services.models.promocode_models import Promocode
from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..serializers.doctors_serializer import DoctorsSerializer, DoctorSpecializtionSerializer, ImageUploadSerializer
from ..models.doctors_models import Doctor, Speciality
from ..models.users import Users
from rest_framework.parsers import MultiPartParser, FormParser
from ..models.user_child_relation import UserChildRelation

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def randomword():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))


class GetDoctorsView(ListAPIView):
    serializer_class = DoctorsSerializer
    models = Doctor
    authentication_classes = []
    pagination_class = StandardResultsSetPagination

    name = openapi.Parameter('name', openapi.IN_QUERY,  required=False, type=openapi.TYPE_STRING)
    speciality = openapi.Parameter('speciality', openapi.IN_QUERY,required=False, type=openapi.TYPE_STRING)
    experience = openapi.Parameter('experience', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[name,speciality,experience])

    def get(self, request, *args, **kwargs):
        total_count = Doctor.objects.filter(is_active=True).count()
        if self.request.query_params.get('name'):
            data = self.models.objects.filter(
                name__icontains=self.request.query_params.get('name'))
            page = self.paginate_queryset(data)
            doctors = DoctorsSerializer(page, many=True)
            return Response({'data':doctors.data,'count':total_count}, status=status.HTTP_200_OK)
        if self.request.query_params.get('speciality'):
            data = self.models.objects.filter(
                speciality__icontains=self.request.query_params.get('speciality'))
            page = self.paginate_queryset(data)
            doctors = DoctorsSerializer(page, many=True)
            return Response({'data':doctors.data,'count':total_count}, status=status.HTTP_200_OK)
        if self.request.query_params.get('experience'):
            data = self.models.objects.filter(
                experience=self.request.query_params.get('experience'))
            page = self.paginate_queryset(data)
            doctors = DoctorsSerializer(page, many=True)
            return Response({'data':doctors.data,'count':total_count}, status=status.HTTP_200_OK)
        data = Doctor.objects.filter(is_active=True)
        page = self.paginate_queryset(data)
        doctors = DoctorsSerializer(page, many=True)
        return Response({'data':doctors.data,'count':len(data)}, status=status.HTTP_200_OK)


class CreateDoctorsView(CreateAPIView):
    serializer_class = DoctorsSerializer
    models = Doctor
    authentication_classes = []
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            serializer = DoctorsSerializer(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                speciality = serializer.validated_data.get('speciality')
                degree = serializer.validated_data.get('degree')
                image = serializer.validated_data.get('image')
                experience = serializer.validated_data.get('experience')
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('phone')
                time_slots = serializer.validated_data.get('time_slots')
                fees = serializer.validated_data.get('fees')
                is_active = serializer.validated_data.get('is_active')
                user = Users.objects.create(
                    full_name=name, email=email, mobile=phone, is_doctor=True)
                password = randomword()
                user.password = make_password(password)
                user.save()
                doctor_obj = Doctor.objects.create(user=user, name=name, speciality=speciality, degree=degree, experience=experience,
                                                   email=email, phone=phone, time_slots=time_slots, fees=fees, is_active=is_active)
                if image:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=image.name, Body=image, ACL='public-read',
                                                       ContentType=image.content_type, ContentDisposition='inline')

                        # s3_client = boto3.client('s3',
                        #                     region_name='us-east-2',
                        #                     aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                        #                     aws_secret_access_key='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')
                        # s3_client.upload_file(image.name, 'detoxa', image)
                        # S3_url = s3_client.generate_presigned_url(
                        # ClientMethod='get_object',
                        # Params={
                        #     'Bucket': 'detoxa',
                        #     'Key': f'{image.name}'
                        #     }
                        # )
                        # print(S3_url)

                        doctor_obj.image = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                        doctor_obj.save()
                    except Exception as e:
                        print(e)
                doctor_obj_dict = {'id': doctor_obj.id}
                doctor_obj_dict.update(serializer.data)
                doctor_obj_dict.update({'image': doctor_obj.image})
                return Response(doctor_obj_dict, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


class DoctorSpecializationView(ListAPIView):
    serializer_class = DoctorSpecializtionSerializer
    models = Doctor
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        data = Speciality.objects.all()
        doctors = DoctorSpecializtionSerializer(data, many=True)
        return Response(doctors.data, status=status.HTTP_200_OK)


##### Testing S3 uploads #####

class S3UploadView(GenericAPIView):
    authentication_classes = []
    parser_classes = (MultiPartParser,)
    serializer_class = ImageUploadSerializer



    def post(self, request, *args, **kwargs):
        try:
            image = request.data.get('image')
            ##### Code to upload image to S3 #####
            s3 = boto3.resource('s3', region_name='us-east-2',
                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                aws_secret_access_key='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')
            s3.Bucket('detoxa').put_object(Key=image.name, Body=image, ACL='public-read',
                                                       ContentType=image.content_type, ContentDisposition='inline')


            ### Code to download image from S3 ###
            # url = s3.generate_presigned_url(
            # ClientMethod='get_object',
            # Params={
            #     'Bucket': 'detoxa',
            #     'Key': f'{image.name}'
            #     }
            # )
            ###  Code to view the image in browser ###
            # https://detoxa.s3.us-east-2.amazonaws.com/goku-clipart.png
            # https://detoxa.s3.us-east-2.amazonaws.com/drf.png
            url = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
            return Response({'message': 'image uploaded successfully', 'url': url}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'image not uploaded'}, status=status.HTTP_400_BAD_REQUEST)


####### UTILITY FUNCTIONS FOR BULK DATA ENTRY #########

class EnterInitialData(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            speciality_list = ['Cardiology', 'Dermatology', 'Gastroenterology', 'Gynaecology',
                               'Neurology', 'Oncology', 'Orthopaedics', 'Paediatrics', 'Psychiatry', 'Radiology', 'Urology']
            time_slots = ['10:00-12:00', '12:00-14:00', '14:00-16:00',
                          '16:00-18:00', '18:00-20:00', '20:00-22:00', '22:00-24:00']
            blog_category = ['Child Care','Mental Health','Emotional Health','Physical Health','Development','Medical']
            Speciality.objects.bulk_create(
                [Speciality(name=name) for name in speciality_list])
            try:
                # user_obj = Users.objects.create(
                #     full_name='admin', email='admin@admin.com', is_admin=True)
                # user_obj.password = make_password('123456')
                # user_obj.save()
                for i in range(2,10):
                    user_obj = Users.objects.create(
                    full_name=f'admin{i}', email=f'admin{i}@gmail.com', is_admin=True)
                user_obj.password = make_password('123456')
                user_obj.save()
            except Exception as e:
                print(e)
            try:
                for i in range(10):
                    user_obj = Users.objects.create(
                        full_name=f'user{i}', email=f'user{i}@email.com')
                    user_obj.password = make_password('123456')
                    user_obj.save()
            except Exception as e:
                print(e)
            try:
                for i in range(5):
                    doctor_obj = Doctor.objects.create(
                        name=f'Dr.Doctor{i}',
                        speciality=Speciality.objects.get(id=i+1),
                        degree=f'MBBS',
                        email=f'doctor{i}@email.com',
                        phone=f'+91767868935{i}',
                        time_slots=time_slots[i],
                        fees=500+i*100,
                        experience=i+5
                    )
            except Exception as e:
                pass
            try:
                for i in range(10):
                    Promocode.objects.create(
                    code='PROMO'+str(i),
                    discount=i*10,
                    description=f'Promo code for {10*i}% discount',

                    )
            except Exception as e:
                pass
            try:
                for i in range(len(blog_category)):
                    BlogCategory.objects.create(
                    name=blog_category[i],
                    media_url='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png'
                    )
            except Exception as e:
                pass
            for j in range(1,6):
                for i in range(1,6):
                    Blog.objects.create(
                        title=f'Blog on {blog_category[i]}',
                        blog_category=BlogCategory.objects.get(id=i),
                        media_url='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png',
                        author='Admin',
                        para1="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                        para2="It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
                        para3="There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
                        para4="Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of 'de Finibus Bonorum et Malorum' (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, 'Lorem ipsum dolor sit amet..', comes from a line in section 1.10.32.",
                    )
            for i in range(1,7):
                for j in range(7):
                    try:
                        Kit.objects.create(
                            name = f'Kit{i}',
                            description = f'Test description for Kit{i}. It contains dummy data as a description of this kit.',
                            price = i*100,
                            category=KitCategory.objects.get(id=i),
                            stock=i*10,
                            image_1='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png',
                            image_2='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png',
                            image_3='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png',
                            image_4='https://detoxa.s3.us-east-2.amazonaws.com/4620961.png',
                        )
                    except Exception as e:
                        continue
            try:
                for i in range(1,10):
                    Doctor.objects.create(
                        name=f'Dr.Doctor{i}',
                        speciality=Speciality.objects.get(id=1),
                        degree=f'MBBS',
                        user=Users.objects.get(id=i+10),
                        experience=i+5,
                        fees=500+i*100
                    )
            except Exception as e:
                pass
            return Response({'message': 'Initial data entered successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
