from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    """serializer class to create new user"""
    class Meta:
        model=get_user_model()
        fields=['username', 'password', 'email', 'name', 'bio']
        extra_kwargs={'password':
                        {
                            'write_only':True    
                        }
                      }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
