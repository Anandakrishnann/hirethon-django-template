from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hirethon_template.users.api.views import UserViewSet
from hirethon_template.organization.api.views import OrganizationViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("organizations", OrganizationViewSet)


app_name = "api"
urlpatterns = router.urls
