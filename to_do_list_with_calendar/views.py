import requests
from bs4 import BeautifulSoup
from django.http import Http404, HttpResponse
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tarefa, Usuario
from .serializers import TarefaSerializer, UsuarioSerializer


class IsAdmin(permissions.BasePermission):
    """
    Permissão personalizada para administradores.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class DocumentationView(APIView):
    """
    Clona a documentação presente no Github Pages.
    """
    
    def extract_data():
        url = 'https://Gabriel-Aguiar-Reis.github.io/ToDo365'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('p', class_='conteudo').get_text()
            return content
        else:
            return None
    
    def get(self, request, format=None):
        data = extract_data()

        if data is not None:
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Falha ao obter dados do GitHub Pages'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheckView(generics.ListAPIView):
    """
    Checa a saúde da API.
    """

    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'})


class TarefaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes de uma tarefa.
    """

    serializer_class = TarefaSerializer
    permission_classes = [IsAdmin | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tarefa.objects.all()
        elif Usuario.objects.filter(
            username=self.request.user.username
        ).exists():
            return Tarefa.objects.filter(usuario=self.request.user)
        else:
            Tarefa.objects.none()


class TarefaList(generics.ListCreateAPIView):
    """
    Listagem e criação de tarefas.
    """

    serializer_class = TarefaSerializer
    permission_classes = [IsAdmin | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tarefa.objects.all()
        elif Usuario.objects.filter(
            username=self.request.user.username
        ).exists():
            return Tarefa.objects.filter(usuario=self.request.user)
        else:
            Tarefa.objects.none()

    def perform_create(self, serializer):
        if self.request.data.get('usuario') == None:
            serializer.save(usuario=self.request.user)
        elif self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(usuario=self.request.user)


class UsuarioCreate(generics.CreateAPIView):
    """
    Criação de um novo usuário.
    """

    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()


class UsuarioAdminCreate(generics.CreateAPIView):
    """
    Criação de um novo usuário administrador.
    """

    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def perform_create(self, serializer):
        return serializer.save(is_superuser=True)


class UsuarioList(generics.ListAPIView):
    """
    Listagem de usuários (apenas para administradores).
    """

    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]
    queryset = Usuario.objects.all()


class UsuarioDetailAdmin(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhamento de usuário para administradores.
    """

    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]
    queryset = Usuario.objects.all()


class UsuarioDetail(generics.RetrieveUpdateAPIView):
    """
    Detalhamento do próprio usuário.
    """

    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj
