from detoxa_services.models.users import Users,Address
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST

from detoxa_services.serializers.address_serializer import AddAddressSerializer
from detoxa_services.utils.user_authentication import UserAuthentication


class AddressListView(ListAPIView):
    serializer_class = AddAddressSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        queryset = Address.objects.filter(user=logged_in_user)
        serializer = AddAddressSerializer(queryset,many=True)
        return Response(serializer.data,status=HTTP_200_OK)
        
class AddAddressView(CreateAPIView):
    serializer_class = AddAddressSerializer

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = AddAddressSerializer(data=request.data)
        if serializer.is_valid():
            Address.objects.create(user=logged_in_user, **serializer.validated_data)
            return Response({'data': serializer.data, 'msg': 'Address created successfully'}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class GetAddressById(RetrieveAPIView):
    serializer_class = AddAddressSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Address.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            serializer = AddAddressSerializer(queryset,many=False)
            return Response(serializer.data,status=HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'msg':'Address does not exists'},status=HTTP_400_BAD_REQUEST)


class UpdateAddressView(UpdateAPIView):
    serializer_class = AddAddressSerializer

    def put(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            address_obj = Address.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            serializer = AddAddressSerializer(address_obj,data=request.data,many=False)
            if serializer.is_valid():
                address_obj.street = serializer.validated_data.get('street')
                address_obj.city = serializer.validated_data.get('city')
                address_obj.state = serializer.validated_data.get('state')
                address_obj.country = serializer.validated_data.get('country')
                address_obj.pincode = serializer.validated_data.get('pincode')
                address_obj.save()
                return Response({'msg':'Address updated successfully'},status=HTTP_200_OK)
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({'msg':'Address does not exists'},status=HTTP_400_BAD_REQUEST)

class DeleteAddressView(DestroyAPIView):
    serializer_class = AddAddressSerializer

    def delete(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Address.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            queryset.delete()
            return Response({'msg':'Address deleted successfully'},status=HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'msg':'Address does not exists'},status=HTTP_400_BAD_REQUEST)

