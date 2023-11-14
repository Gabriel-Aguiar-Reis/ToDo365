from django.urls import path

from .views import (HealthCheckView, TarefaDetail, TarefaList, 
                    UsuarioAdminCreate, UsuarioCreate, UsuarioDetail, 
                    UsuarioDetailAdmin, UsuarioList)

urlpatterns = [
    path(
        'healthcheck/',
        HealthCheckView.as_view(),
        name='HealthCheckView'
    ),
    path(
        'novo_usuario/',
        UsuarioCreate.as_view(),
        name='UsuarioCreate'
    ),
    path(
        'novo_usuario_admin/',
        UsuarioAdminCreate.as_view(),
        name='UsuarioAdminCreate'
    ),
    path(
        'tarefas/',
        TarefaList.as_view(),
        name='TarefaList'
    ),
    path(
        'tarefas/<int:pk>/',
        TarefaDetail.as_view(),
        name='TarefaDetail'
    ),
    path(
        'usuario/',
        UsuarioDetail.as_view(),
        name='UsuarioDetail'
    ),
    path(
        'usuario/<int:pk>/',
        UsuarioDetailAdmin.as_view(),
        name='UsuarioDetailAdmin',
    ),
    path(
        'usuarios/',
        UsuarioList.as_view(),
        name='UsuarioList'
    ),
]