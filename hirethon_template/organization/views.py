from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Organization, Membership, Invite


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organization/organization_form.html'
    fields = ['name']
    success_url = reverse_lazy('organization:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'organization/organization_form.html'
    fields = ['name']
    success_url = reverse_lazy('organization:list')


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'organization/organization_confirm_delete.html'
    success_url = reverse_lazy('organization:list')


class MembershipListView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'organization/membership_list.html'
    context_object_name = 'memberships'
    paginate_by = 10


class MembershipDetailView(LoginRequiredMixin, DetailView):
    model = Membership
    template_name = 'organization/membership_detail.html'
    context_object_name = 'membership'


class MembershipCreateView(LoginRequiredMixin, CreateView):
    model = Membership
    template_name = 'organization/membership_form.html'
    fields = ['user', 'organization', 'role']
    success_url = reverse_lazy('organization:membership_list')


class MembershipUpdateView(LoginRequiredMixin, UpdateView):
    model = Membership
    template_name = 'organization/membership_form.html'
    fields = ['role']
    success_url = reverse_lazy('organization:membership_list')


class MembershipDeleteView(LoginRequiredMixin, DeleteView):
    model = Membership
    template_name = 'organization/membership_confirm_delete.html'
    success_url = reverse_lazy('organization:membership_list')

    def get(self, request, *args, **kwargs):
        membership = self.get_object()
        if membership.user != self.request.user:
            return redirect(reverse_lazy('organization:membership_list'))
        return super().get(request, *args, **kwargs)



class InviteCreateView(LoginRequiredMixin, CreateView):
    model = Invite
    template_name = 'organization/invite_form.html'
    fields = ['email', 'organization', 'role']
    success_url = reverse_lazy('organization:invite_list')
    
    def form_valid(self, form):
        form.instance.invited_by = self.request.user
        return super().form_valid(form)


class InviteUpdateView(LoginRequiredMixin, UpdateView):
    model = Invite
    template_name = 'organization/invite_form.html'
    fields = ['role']
    success_url = reverse_lazy('organization:invite_list')

class InviteDeleteView(LoginRequiredMixin, DeleteView):
    model = Invite
    template_name = 'organization/invite_confirm_delete.html'
    success_url = reverse_lazy('organization:invite_list')

class InviteListView(LoginRequiredMixin, ListView):
    model = Invite
    template_name = 'organization/invite_list.html'
    context_object_name = 'invites'
    paginate_by = 10

class InviteDetailView(LoginRequiredMixin, DetailView):
    model = Invite
    template_name = 'organization/invite_detail.html'
    context_object_name = 'invite'

class InviteAcceptView(LoginRequiredMixin, View):
    template_name = 'organization/invite_accept.html'
    success_url = reverse_lazy('organization:list')

    def get_object(self):
        token = self.kwargs.get('token')
        return Invite.objects.get(token=token)

    def get(self, request, *args, **kwargs):
        invite = self.get_object()
        if invite.is_expired():
            return redirect(reverse_lazy('organization:list'))
        return render(request, self.template_name, {'invite': invite})

    def post(self, request, *args, **kwargs):
        invite = self.get_object()
        if invite.is_expired():
            return redirect(reverse_lazy('organization:list'))
        
        # Create membership when invite is accepted
        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role
        )
        invite.accepted = True
        invite.save()
        return redirect(self.success_url)
