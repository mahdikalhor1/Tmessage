from rest_framework import mixins
from .serializers import UserCreateSerializer, UserImageSerializer
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
class CreateUserView(mixins.CreateModelMixin,
                      GenericViewSet,
                      ):
    serializer_class=UserCreateSerializer
    queryset=get_user_model().objects.all()

    
    
    
class MyProfileManagerView(
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    ):
    
    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    serializer_class=UserCreateSerializer
    
    def get_object(self):
        return self.request.user

class MyProfileImageManagerView(
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    ):

    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    serializer_class=UserImageSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.request.user.image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    def get_object(self):
        return self.request.user

class UserProfileView(
    mixins.RetrieveModelMixin,
    GenericViewSet,
    ):
    
    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    serializer_class=UserSerializer
    queryset=get_user_model().objects.all()
    lookup_field='username'
    