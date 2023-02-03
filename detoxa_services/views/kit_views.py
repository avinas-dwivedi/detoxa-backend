import boto3
from rest_framework.parsers import MultiPartParser,FileUploadParser
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from botocore import exceptions
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..serializers.kit_serializer import AddKitCategorySerializer, CreateKitSerializer, GetKitsSerializer, KitDetailSerializer, KitSerializer,KitCategorySerializer, UpdateKitSerializer
from ..models.kits_models import Kit, KitCategory, KitImages
from detoxa_services.utils.user_authentication import UserAuthentication
from rest_framework import generics, status
import django_filters


class GetKitList(ListAPIView):
    '''
    API to get kit list
    '''
    authentication_classes = []
    serializer_class = KitSerializer
    
    def get(self, request, *args, **kwargs):
        kits = Kit.objects.filter(category=kwargs.get('pk')).select_related().order_by('id')
        serializer = KitSerializer(kits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetKitCategoryList(ListAPIView):
    '''
    API to get kit category list
    '''
    authentication_classes = []
    serializer_class = KitCategorySerializer
    
    def get(self,request,*args,**kwargs):
        kits = KitCategory.objects.all()
        serializer = KitCategorySerializer(kits,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class DeleteKitCategroy(DestroyAPIView):
    '''
    API to delete kit category
    '''
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            kit_category = KitCategory.objects.get(id=kwargs.get('pk'))
            kit_category.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteKit(generics.DestroyAPIView):
    authentication_classes = []
    serializer_class = GetKitsSerializer

    def delete(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        print(kwargs.get('pk'))
        kit_obj = Kit.objects.filter(id=kwargs.get('pk')).first()
        if kit_obj:
            kit_obj.delete()
            data = {
                "success": True,
                "message": "Kit deleted successfully"
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Kit not found.')


class GetKitDetail(RetrieveAPIView):
    '''
    API to get kit detail
    '''
    authentication_classes = []
    serializer_class = KitDetailSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            kit = Kit.objects.get(id=kwargs.get('pk'))
            serializer = KitDetailSerializer(kit, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e), 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_200_OK)


class CreateKit(CreateAPIView):
    '''
    API to create kit
    '''
    authentication_classes = []
    serializer_class = CreateKitSerializer
    model = Kit
    parser_classes = [MultiPartParser]

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            serializer = CreateKitSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.validated_data)
                try:
                    kit_obj = Kit.objects.create(
                        name=serializer.validated_data.get('name'),
                        category=KitCategory.objects.get(id=serializer.validated_data.get('category')),
                        price=serializer.validated_data.get('price'),
                        description=serializer.validated_data.get('description'),
                        stock = serializer.validated_data.get('stock')
                    )
                    # images = request.data.getlist('image')

                    # if images:
                    for i in range(1,5):
                        s3 = boto3.resource('s3',region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                            # s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image_'+str(i)).name, Body=serializer.validated_data.get('image_'+str(i)), ACL='public-read',
                                                       ContentType=serializer.validated_data.get('image_'+str(i)).content_type, ContentDisposition='inline')


                            # s3_client = boto3.client('s3',
                            #                     region_name='us-east-2',
                            #                     aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                            #                     aws_secret_access_key='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')
                            # S3_url = s3_client.generate_presigned_url(
                            # ClientMethod='get_object',
                            # Params={
                            #     'Bucket': 'detoxa',
                            #     'Key': f'{image.name}'
                            #     }
                            # )
                            # print(S3_url)
                            # KitImages.objects.create(
                            #     kit=kit_obj,
                            #     image=f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                            # )
                    # print(serializer.validated_data['image_1'])
                    # print(serializer.validated_data['image_2'])
                    # print(serializer.validated_data['image_3'])
                    # print(serializer.validated_data.get('image_4'))
                    kit_obj.image_1 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_1').name}"
                    kit_obj.image_2 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_2').name}"
                    kit_obj.image_3 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_3').name}"
                    kit_obj.image_4 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_4').name}"
                    kit_obj.save()
                    kit_obj_dict = {'id':kit_obj.id}
                    kit_obj_dict.update(serializer.data)
                    # kit_obj_dict.update({'images':KitImages.objects.filter(kit=kit_obj).values('image')})
                    return Response(kit_obj_dict,status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error":str(e),'status':status.HTTP_400_BAD_REQUEST},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"You are not authorized to perform this action",'status':status.HTTP_401_UNAUTHORIZED},status=status.HTTP_200_OK)


class UpdateKit(UpdateAPIView):
    '''
    API to update kit
    '''
    authentication_classes = []
    serializer_class = UpdateKitSerializer
    queryset = Kit.objects.all()
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                kit_obj = Kit.objects.get(id=kwargs.get('pk'))
                serializer = UpdateKitSerializer(kit_obj,data=request.data)
                if serializer.is_valid():
                    print(serializer.validated_data)
                    if serializer.validated_data.get('name'):
                        kit_obj.name = serializer.validated_data.get('name')
                    if serializer.validated_data.get('category'):
                        kit_obj.category = serializer.validated_data.get('category')
                    if serializer.validated_data.get('price'):
                        kit_obj.price = serializer.validated_data.get('price')
                    if serializer.validated_data.get('description'):
                        kit_obj.description = serializer.validated_data.get('description')
                    if serializer.validated_data.get('stock'):
                        kit_obj.stock = serializer.validated_data.get('stock')
                    if serializer.validated_data.get('active') == True:
                        kit_obj.active = True
                        kit_obj.save()
                    if not serializer.validated_data.get('active'):
                        kit_obj.active = False
                        kit_obj.save()
                    # images = request.data.getlist('image')
                    if serializer.validated_data.get('image_1'):
                        s3 = boto3.resource('s3',region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                        # s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image_1').name, Body=serializer.validated_data.get('image_1'), ACL='public-read',
                                                    ContentType=serializer.validated_data.get('image_1').content_type, ContentDisposition='inline')
                        kit_obj.image_1 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_1').name}"
                    if serializer.validated_data.get('image_2'):
                        s3 = boto3.resource('s3',region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                        # s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image_2').name, Body=serializer.validated_data.get('image_2'), ACL='public-read',
                                                    ContentType=serializer.validated_data.get('image_2').content_type, ContentDisposition='inline')
                        kit_obj.image_2 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_2').name}"

                    if serializer.validated_data.get('image_3'):
                        s3 = boto3.resource('s3',region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                        # s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image_3').name, Body=serializer.validated_data.get('image_3'), ACL='public-read',
                                                    ContentType=serializer.validated_data.get('image_3').content_type, ContentDisposition='inline')
                        kit_obj.image_3 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_3').name}"

                    if serializer.validated_data.get('image_4'):
                        s3 = boto3.resource('s3',region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                        # s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image_4').name, Body=serializer.validated_data.get('image_4'), ACL='public-read',
                                                    ContentType=serializer.validated_data.get('image_4').content_type, ContentDisposition='inline')
                        kit_obj.image_4 = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image_4').name}"


                            # s3_client = boto3.client('s3',
                            #                     region_name='us-east-2',
                            #                     aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                            #                     aws_secret_access_key='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')
                            # S3_url = s3_client.generate_presigned_url(
                            # ClientMethod='get_object',
                            # Params={
                            #     'Bucket': 'detoxa',
                            #     'Key': f'{image.name}'
                            #     }
                            # )
                            # print(S3_url)
                            # KitImages.objects.create(
                            #     kit=kit_obj,
                            #     image=f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                            # )
                        # kit_obj.image = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                    kit_obj.save()
                    kit_obj_dict = {'id':kit_obj.id}
                    kit_obj_dict.update(serializer.data)
                    # kit_obj_dict.update({'images':KitImages.objects.filter(kit=kit_obj).values('image').distinct()})
                    return Response(kit_obj_dict,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e), 'status': status.HTTP_400_BAD_REQUEST},status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to perform this action", 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)


class GetAllKitFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method='filter_by_status')
    # service = django_filters.CharFilter(method='filter_by_service')
    # customer_name = django_filters.CharFilter(method='filter_by_customer_name')

    class Meta:
        model = Kit
        fields = []

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(active=value)

    # def filter_by_service(self, queryset, name, value):
    #     return queryset.filter(service__name__iexact=value)
    #
    # def filter_by_customer_name(self, queryset, name, value):
    #     return queryset.filter(customer_name__icontains=value)


class GetAllKits(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetKitsSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = GetAllKitFilter

    def get(self, request, *args, **kwargs):
        kit_obj = Kit.objects.filter().order_by("id")
        kit_obj = GetAllKitFilter(request.GET, queryset=kit_obj).qs.distinct()
        data_list = list()
        total_count = Kit.objects.filter().count()
        for kit in kit_obj:
            data = GetKitsSerializer(kit).data
            data_list.append(data)
        kit = self.paginate_queryset(data_list)
        return Response({'data': kit, 'count': total_count}, status=status.HTTP_200_OK)


# class GetAllKits(ListAPIView):
#     '''
#     API to get all kits
#     '''
#     authentication_classes = []
#     serializer_class = GetKitsSerializer
#     queryset = Kit.objects.all()
#     pagination_class = StandardResultsSetPagination
#
#     def get(self, request, *args, **kwargs):
#         logged_in_user = UserAuthentication.authenticate(self, request)[0]
#         if logged_in_user.is_admin:
#             kit_count = Kit.objects.filter(active=True).count()
#             if self.request.GET.get('status') == 'Active':
#                 kits = Kit.objects.filter(active=True).select_related('KitCategory').order_by('id')
#                 serializer = GetKitsSerializer(kits,many=True)
#                 return Response({'data': serializer.data, 'count':kit_count},status=status.HTTP_200_OK)
#             if self.request.GET.get('status') == 'In-active':
#                 kits = Kit.objects.filter(active=False).select_related('KitCategory').order_by('id')
#                 serializer = GetKitsSerializer(kits,many=True)
#                 return Response({'data': serializer.data, 'count': kit_count},status=status.HTTP_200_OK)
#             if self.request.GET.get('status') == 'All':
#                 kits = Kit.objects.all().select_related('KitCategory').order_by('id')
#                 serializer = GetKitsSerializer(kits, many=True)
#                 return Response({'data': serializer.data, 'count': kit_count}, status=status.HTTP_200_OK)
#             kits = Kit.objects.all().order_by('id')
#             page = self.paginate_queryset(kits)
#             serializer = GetKitsSerializer(page, many=True)
#             # data = serializer.data
#             # d.append({'kit_count': kit_count})
#             return Response({'data': serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "You are not authorized to perform this action", 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)


class AddKitCategory(CreateAPIView):
    '''
    API to add kit category
    '''
    authentication_classes = []
    serializer_class = AddKitCategorySerializer
    queryset = KitCategory.objects.all()
    parser_classes = (MultiPartParser,)
    
    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    image_url = None
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
                    kit_category_obj = KitCategory.objects.create(
                        name=serializer.validated_data.get('name'),
                        image=image_url
                    )
                    kit_category_obj_dict = {'id': kit_category_obj.id, 'name':kit_category_obj.name,'image':kit_category_obj.image}
                return Response({'msg': 'Kit Category added successfully','data':kit_category_obj_dict},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e), 'status': status.HTTP_400_BAD_REQUEST},status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to perform this action",'status':status.HTTP_401_UNAUTHORIZED},status=status.HTTP_200_OK)


            