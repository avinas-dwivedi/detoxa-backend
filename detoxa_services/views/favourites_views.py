from detoxa_services.models.doctors import Doctors
from detoxa_services.models.favourites import Favourites
from detoxa_services.models.therapist import Therapist
from detoxa_services.serializers.favourite_serializer import FavouritesSerializer,CreateFavouritesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveAPIView,CreateAPIView
from rest_framework.parsers import MultiPartParser

from detoxa_services.utils.user_authentication import UserAuthentication


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class AddFavouritesView(CreateAPIView):
    serializer_class = CreateFavouritesSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = []

    favourite = openapi.Parameter('favourite', openapi.IN_QUERY, description="Doctor or therapist  should be passed to mark them as favourite or unmark as favourite",required=True, type=openapi.TYPE_STRING, enum=['Doctor','Therapist'])
    @swagger_auto_schema(manual_parameters=[favourite])
    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            serializer = CreateFavouritesSerializer(data=request.data)
            if serializer.is_valid():
                if request.query_params.get('favourite') == 'Doctor':
                    try:
                        fav_obj = Favourites.objects.get(user=logged_in_user, doctor=serializer.validated_data['doctor'])
                        fav_obj.delete()
                        return Response({"message": "Doctor removed from favourites"}, status=status.HTTP_200_OK)
                    except Favourites.DoesNotExist:
                        Favourites.objects.create(
                            user=logged_in_user,
                            doctor=Doctors.objects.get(id=serializer.data.get('doctor'))
                        )
                    return Response({"msg":'Doctor added as favourites successfully'}, status=status.HTTP_201_CREATED)
                elif request.query_params.get('favourite') == 'Therapist':
                    try:
                        fav_obj = Favourites.objects.get(user=logged_in_user, therapist=serializer.validated_data['therapist'])
                        fav_obj.delete()
                        return Response({"message": "Therapist removed from favourites"}, status=status.HTTP_200_OK)
                    except Favourites.DoesNotExist:
                        Favourites.objects.create(
                            user=logged_in_user,
                            therapist=Therapist.objects.get(id=serializer.data.get('therapist'))
                        )
                    return Response({"msg":'Therapist added as favourites successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavouritesListView(ListAPIView):
    serializer_class = FavouritesSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            favourites = Favourites.objects.filter(user=logged_in_user)
            serializer = FavouritesSerializer(favourites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RemoveFavourite(GenericAPIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            Favourites.objects.get(id=kwargs['pk'],user=logged_in_user).delete()
            return Response({"message": "Doctor removed from favourites"}, status=status.HTTP_200_OK)
        except Favourites.DoesNotExist:
            return Response({"message": "Doctor not found in favourites"}, status=status.HTTP_200_OK)