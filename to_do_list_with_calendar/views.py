import os

import jwt
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from .utils import Util


class IsAdmin(permissions.BasePermission):
    """
    Custom permission for administrators.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class HealthCheckView(generics.ListAPIView):
    """
    Checks the API's health.
    """

    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'})


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Details of a task.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAdmin | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        elif User.objects.filter(username=self.request.user.username).exists():
            return Task.objects.filter(User=self.request.user)
        else:
            Task.objects.none()


class TaskList(generics.ListCreateAPIView):
    """
    Listing and creation of tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAdmin | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        elif User.objects.filter(username=self.request.user.username).exists():
            return Task.objects.filter(User=self.request.user)
        else:
            Task.objects.none()

    def perform_create(self, serializer):
        if self.request.data.get('User') == None:
            serializer.save(User=self.request.user)
        elif self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(User=self.request.user)


class BaseUserCreate(generics.CreateAPIView):
    """
    A base class for user creation.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer, is_superuser):
        user_data = serializer.validated_data
        email = user_data.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'An user with this email already exists.'
            )

        user = serializer.save(is_superuser=is_superuser)

        user_model = get_user_model()
        refresh = RefreshToken.for_user(user_model.objects.get(email=email))
        token = str(refresh.access_token)

        current_site = get_current_site(self.request).domain
        relative_link = reverse('VerifyEmailToken')
        absurl = 'https://' + current_site + relative_link + '?token=' + token
        email_body = (
            'Hi, '
            + user.username
            + ' click in the link below to verify your account.\n'
            + absurl
        )
        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
            'to_email': user.email,
        }
        Util.send_email(data)

        return user


class UserCreate(BaseUserCreate):
    """
    Creating a new user.
    """

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class UserAdminCreate(BaseUserCreate):
    """
    Creating a new administrator user.
    """

    def perform_create(self, serializer):
        return super().perform_create(serializer, is_superuser=True)


class UserList(generics.ListAPIView):
    """
    User listing (for admins only).
    """

    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()


class UserDetailAdmin(generics.RetrieveUpdateDestroyAPIView):
    """
    User drillthrough for administrators.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()


class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Breakdown of user's himself.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class VerifyEmailToken(APIView):
    """
    Verifying the email token for new users.
    """

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        secret_key = os.environ.get('SECRET_KEY')
        algorithms = ['HS256']
        try:
            payload = jwt.decode(token, secret_key, algorithms=algorithms)
            user = User.objects.get(id=payload['user_id'])
            if not user.validated:
                user.validated = True
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
