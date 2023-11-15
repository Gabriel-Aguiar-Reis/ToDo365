from django.contrib import admin

# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from to_do_list_with_calendar.urls import urlpatterns as to_do_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(to_do_urls)),
    path('api-auth/', include('rest_framework.urls')),
    re_path(
        r'^docs/(?P<path>,*)$',
        TemplateView.as_view,
        template_name='docs/index.html',
    ),
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
