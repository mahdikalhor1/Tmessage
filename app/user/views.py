from django.shortcuts import render
from rest_framework import mixins
from .serializers import UserCreateSerializer
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
class CreateUserView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet,
                      ):
    serializer_class=UserCreateSerializer
    authentication_classes=[JWTAuthentication,]
    permission_classes=[IsAuthenticated,]
    queryset=get_user_model().objects.all()

    def get_permissions(self):
        """it returns no permission in case of creating new user (signing up)"""
        if self.action=='create':
            return []
        return [permission() for permission in self.permission_classes]
    