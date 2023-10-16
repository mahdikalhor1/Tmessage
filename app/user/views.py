from django.shortcuts import render
from rest_framework import mixins
from .serializers import UserCreateSerializer
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class=UserCreateSerializer
    queryset=get_user_model().objects.all()
