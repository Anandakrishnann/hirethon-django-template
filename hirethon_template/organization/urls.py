from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    # Organization URLs
    path('', views.OrganizationListView.as_view(), name='list'),
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='detail'),
    path('create/', views.OrganizationCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.OrganizationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='delete'),
    
    # Membership URLs
    path('memberships/', views.MembershipListView.as_view(), name='membership_list'),
    path('memberships/<int:pk>/', views.MembershipDetailView.as_view(), name='membership_detail'),
    path('memberships/create/', views.MembershipCreateView.as_view(), name='membership_create'),
    path('memberships/<int:pk>/update/', views.MembershipUpdateView.as_view(), name='membership_update'),
    path('memberships/<int:pk>/delete/', views.MembershipDeleteView.as_view(), name='membership_delete'),
    
    # Invite URLs
    path('invites/', views.InviteListView.as_view(), name='invite_list'),
    path('invites/<int:pk>/', views.InviteDetailView.as_view(), name='invite_detail'),
    path('invites/create/', views.InviteCreateView.as_view(), name='invite_create'),
    path('invites/<int:pk>/update/', views.InviteUpdateView.as_view(), name='invite_update'),
    path('invites/<int:pk>/delete/', views.InviteDeleteView.as_view(), name='invite_delete'),
    path('invites/accept/<uuid:token>/', views.InviteAcceptView.as_view(), name='invite_accept'),
]
