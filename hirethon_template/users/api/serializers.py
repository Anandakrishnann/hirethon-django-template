from django.contrib.auth import get_user_model
from rest_framework import serializers
from hirethon_template.organization.models import Membership

from hirethon_template.users.models import User as UserType


User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    organizations = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "id", "email", "name", "is_active", "is_staff", 
            "date_joined", "url", "organizations", "roles"
        ]
        read_only_fields = ["id", "email", "date_joined", "is_staff"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
    
    def get_organizations(self, obj):
        """Get organizations where user is a member"""
        memberships = Membership.objects.filter(user=obj).select_related('organization')
        return [
            {
                "id": membership.organization.id,
                "name": membership.organization.name,
                "role": membership.role,
                "joined_at": membership.joined_at
            }
            for membership in memberships
        ]
    
    def get_roles(self, obj):
        """Get all roles for the user across organizations"""
        memberships = Membership.objects.filter(user=obj)
        return [membership.role for membership in memberships]



class LoginResponseSerializer(serializers.Serializer):
    """Serializer for login response with user details and tokens"""
    user = UserSerializer()
    access = serializers.CharField()
    refresh = serializers.CharField()
    message = serializers.CharField(default="Login successful")
