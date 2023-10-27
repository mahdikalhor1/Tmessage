from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name='user'

router=DefaultRouter()
router.register('users', viewset=views.CreateUserView, basename='user')
router.register('userprofile', viewset=views.UserProfileView, basename='userprofile')
router.register('profileimage', viewset=views.MyProfileImageManagerView, basename='profileimage')

urlpatterns = [
    path('', include(router.urls)),
    path('my-profile/',
        view=views.MyProfileManagerView.as_view(), name='my-profile'
        ),
]
