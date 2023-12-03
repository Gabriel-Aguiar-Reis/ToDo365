from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    HealthCheckView,
    TaskDetail,
    TaskList,
    UserAdminCreate,
    UserCreate,
    UserDetail,
    UserDetailAdmin,
    UserList,
    VerifyEmailToken,
)

schema_view = get_schema_view(
   openapi.Info(
      title="ToDo365 API",
      default_version='v1',
      description="This is a ToDo365 API swagger.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="lugafeagre@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('healthcheck/', HealthCheckView.as_view(), name='HealthCheckView'),
    path('new_user/', UserCreate.as_view(), name='UserCreate'),
    path(
        'new_user_admin/',
        UserAdminCreate.as_view(),
        name='UserAdminCreate',
    ),
    path('tasks/', TaskList.as_view(), name='TaskList'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='TaskDetail'),
    path('user/', UserDetail.as_view(), name='UserDetail'),
    path(
        'user/<int:pk>/',
        UserDetailAdmin.as_view(),
        name='UserDetailAdmin',
    ),
    path('users/', UserList.as_view(), name='UserList'),
    path('verify_email/', VerifyEmailToken.as_view(), name='VerifyEmailToken'),
]

urlpatterns += [
   path('<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]