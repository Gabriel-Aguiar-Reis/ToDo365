from django.contrib import admin
from django.urls import include, path

from to_do_list_with_calendar.urls import urlpatterns as to_do_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(to_do_urls)),
]
