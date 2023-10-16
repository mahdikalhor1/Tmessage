from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name='user'

router=DefaultRouter()
router.register('users', viewset=views.CreateUserView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
