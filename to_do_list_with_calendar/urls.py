from django.urls import path

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
