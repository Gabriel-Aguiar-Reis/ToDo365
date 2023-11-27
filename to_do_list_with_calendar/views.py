import os
from datetime import datetime

import jwt
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tarefa, Usuario
from .serializers import TarefaSerializer, UsuarioSerializer
from .utils import Util


class IsAdmin(permissions.BasePermission):
    """
    Permissão personalizada para administradores.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


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


class BaseUsuarioCreate(generics.CreateAPIView):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def perform_create(self, serializer):
        user_data = serializer.validated_data
        email = user_data.get('email')

        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'An user with this email already exists.'
            )

        usuario = serializer.save()

        user_model = get_user_model()
        refresh = RefreshToken.for_user(user_model.objects.get(email=email))
        token = str(refresh.access_token)

        current_site = get_current_site(self.request).domain
        relative_link = reverse('VerifyEmail')
        absurl = 'http://' + current_site + relative_link + '?token=' + token
        email_body = (
            'Hi, '
            + usuario.username
            + ' click in the link below to verify your account.\n'
            + absurl
        )
        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
            'to_email': usuario.email,
        }
        Util.send_email(data)

        return usuario


class UsuarioCreate(BaseUsuarioCreate):
    """
    Criação de um novo usuário.
    """

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class UsuarioAdminCreate(BaseUsuarioCreate):
    """
    Criação de um novo usuário administrador.
    """

    def perform_create(self, serializer):
        return super().perform_create(serializer, is_superuser=True)


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


class VerifyEmail(APIView):
    """
    Verifying email for users to validate.
    """

    serializer_class = UsuarioSerializer

    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        secret_key = os.environ.get('SECRET_KEY')
        algorithms = ['HS256']
        try:
            payload = jwt.decode(token, secret_key, algorithms=algorithms)
            user = Usuario.objects.get(id=payload['user_id'])
            if not user.validado:
                user.validado = True
                user.save()
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'error': 'Activation Expired'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError as identifier:
            print('Error Decoding Token:', identifier)
            return Response(
                {'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST
            )
