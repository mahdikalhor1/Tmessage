from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name='user'

router=DefaultRouter()
router.register('users', viewset=views.CreateUserView, basename='user')

# print(router.urls)
urlpatterns = [
    path('', include(router.urls)),
    path('user-profile/',
        view=views.UserProfileManagerView.as_view(), name='user-profile'
        )
]
