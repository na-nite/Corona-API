from django.conf.urls import url
from django.conf.urls.static import static

from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from app import settings

...

schema_view = get_schema_view(
    openapi.Info(
        title="Corona Watch API",
        default_version='v1.0',
        description="Corona Watch api_content",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  url('admin/', admin.site.urls),
                  url('api-content/', include('api_content.urls')),
                  url('api_account/', include('api_account.urls')),
                  url('api-map/', include('api_map.urls')),
                  url('api-report/', include('api_report.urls')),
                  url('api-robot/', include('api_robot.urls')),
                  url('api-diagnostic/', include('api_diagnostic.urls')),
                  url('doc/', schema_view.with_ui('swagger', cache_timeout=0)),
                  url(r'social/', include('rest_framework_social_oauth2.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
