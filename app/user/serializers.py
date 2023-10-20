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
    
    def update(self, instance, validated_data):
        
        password=validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user
    

class UserSerializer(serializers.ModelSerializer):
    """Serializer class to get otherusers profile."""
    
    class Meta:
        model=get_user_model()
        fields=['username', 'name', 'bio']
        read_only_fields=fields


