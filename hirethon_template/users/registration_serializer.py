from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    """Custom registration serializer that handles the name field"""
    name = serializers.CharField(max_length=255, required=True)
    
    def custom_signup(self, request, user):
        """Override custom_signup to save the name field"""
        user.name = self.validated_data.get('name', '')
        user.save()
        return user
