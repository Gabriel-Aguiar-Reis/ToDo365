from django.contrib import admin

# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import include, path

from to_do_list_with_calendar.urls import urlpatterns as to_do_urls
from to_do_list_with_calendar.views import DocumentationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(to_do_urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('documentation/', Documentation.as_view(), name='documentation')
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
