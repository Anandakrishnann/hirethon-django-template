from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model

from .serializers import OrganizationSerializer, MembershipSerializer, InviteSerializer
from ..models import Organization, Membership, Invite

User = get_user_model()


class OrganizationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def invite_member(self, request, pk=None):
        organization = self.get_object()
        email = request.data.get('email')
        role = request.data.get('role', 'viewer')
        
        if not email:
            return Response(
                {'error': 'email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if invite already exists
        if Invite.objects.filter(organization=organization, email=email).exists():
            return Response(
                {'error': 'Invite already exists for this email'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invite = Invite.objects.create(
            organization=organization,
            email=email,
            role=role,
            invited_by=request.user
        )
        
        serializer = InviteSerializer(invite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MembershipViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()
    lookup_field = "pk"


class InviteViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        invite = self.get_object()
        
        if invite.accepted:
            return Response(
                {'error': 'Invite already accepted'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if invite.is_expired():
            return Response(
                {'error': 'Invite has expired'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        membership, created = Membership.objects.get_or_create(
            user=request.user,
            organization=invite.organization,
            defaults={'role': invite.role}
        )
        
        if not created:
            return Response(
                {'error': 'User is already a member of this organization'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark invite as accepted
        invite.accepted = True
        invite.save()
        
        membership_serializer = MembershipSerializer(membership)
        return Response(membership_serializer.data, status=status.HTTP_201_CREATED)
