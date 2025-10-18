from django.contrib import admin
from .models import Organization, Membership, Invite


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'joined_at']
    list_filter = ['role', 'joined_at', 'organization']
    search_fields = ['user__email', 'organization__name']
    readonly_fields = ['joined_at']


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'role', 'invited_by', 'created_at', 'accepted']
    list_filter = ['role', 'accepted', 'created_at', 'organization']
    search_fields = ['email', 'organization__name']
    readonly_fields = ['token', 'created_at']
