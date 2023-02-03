from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from detoxa_services.utils.user_authentication import UserAuthentication
from ..serializers.promocode_serializer import PromocodeListSerializer, PromocodeSerializer, CreatePromoCodeSerializer
from ..models.promocode_models import Promocode
from rest_framework.parsers import MultiPartParser, FormParser


class CreatePromoCodeAPI(CreateAPIView):
    queryset = Promocode.objects.all()
    serializer_class = CreatePromoCodeSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    # promo_code_obj = Promocode.objects.get(code=serializer.validated_data['code'])
                    # data = {
                    #     'data': 'Promocode applied successfully',
                    #     'id': promo_code_obj.id,
                    #     'discount': promo_code_obj.discount,
                    #     'description': promo_code_obj.description,
                    #     'is_expired': promo_code_obj.is_expired,
                    # }
                    # if promo_code_obj.is_expired:
                    #     return Response({'data': 'Promocode is expired'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "You are not authorized to create promo code"}, status=status.HTTP_401_UNAUTHORIZED)


class ApplyPromocode(CreateAPIView):
    """
    This class is used to apply promo code
    """
    serializer_class = PromocodeSerializer
    model = Promocode

    def post(self, request, *args, **kwargs):
        """
        This method is used to apply promo code
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                promo_code_obj = Promocode.objects.get(code=serializer.validated_data['code'])
                data = {
                    'data': 'Promocode applied successfully',
                    'id': promo_code_obj.id,
                    'discount': promo_code_obj.discount,
                    'description': promo_code_obj.description,
                    'is_expired': promo_code_obj.is_expired,
                }
                if promo_code_obj.is_expired:
                    return Response({'data': 'Promo code is expired'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPromocodes(ListAPIView):
    """
    Lists all the promocodes
    """
    serializer_class = PromocodeListSerializer
    
    def get(self, request, *args, **kwargs):
        data = Promocode.objects.all()
        serializer = PromocodeListSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
