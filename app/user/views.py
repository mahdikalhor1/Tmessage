from django.shortcuts import render
from rest_framework import mixins
from .serializers import UserCreateSerializer
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
class CreateUserView(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                      GenericViewSet,
                      ):
    serializer_class=UserCreateSerializer
    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    queryset=get_user_model().objects.all()

    def get_permissions(self):
        """It returns no permission in case of creating new user (signing up)"""
        if self.action=='create':
            return []
        return [permission() for permission in self.permission_classes]

    
    @action(detail=True, url_name='myprofile', methods=['GET'])
    def myprofile(self, request):
        """return authenticated users profile"""
        instance=self.get_object()
        serializer=self.get_serializer(instance)

        return Response(serializer.data)
    
    
    
    # @action(detail=False, url_name='userprofile', methods=['GET'])
    # def userprofile(self, username):
    #     """return specified users profile."""
    #     instance=get_user_model().objects.get(username=username)
    #     serializer=self.get_serializer(instance)
        
    #     return Response(serializer.data)
    
class UserProfileManagerView(
    UpdateAPIView
    ):
    
    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    serializer_class=UserCreateSerializer
    
    def get_object(self):
        return self.request.user
    