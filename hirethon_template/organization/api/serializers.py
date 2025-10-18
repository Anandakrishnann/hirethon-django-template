from rest_framework import serializers
from hirethon_template.users.api.serializers import UserSerializer
from ..models import Organization, Membership, Invite


class OrganizationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    memberships = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'created_at', 'updated_at', 
            'created_by', 'memberships'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    organization_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Membership
        fields = [
            'id', 'user', 'organization', 'role', 'joined_at',
            'user_id', 'organization_id'
        ]
        read_only_fields = ['joined_at']


class InviteSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    invited_by = UserSerializer(read_only=True)
    organization_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Invite
        fields = [
            'id', 'organization', 'email', 'role', 'invited_by',
            'token', 'created_at', 'accepted', 'organization_id'
        ]
        read_only_fields = ['token', 'created_at', 'invited_by']
